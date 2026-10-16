import hashlib
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

load_dotenv()
app = Flask(__name__)

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
DATA_FILE = DATA_DIR / "items.json"
MONGO_URI = os.getenv("MONGO_URI", "").strip()
MONGO_DB = os.getenv("MONGO_DB", "git_github_assignment")
_mongo_collection = None


def get_mongo_collection():
    """Return a MongoDB collection when configured, otherwise None."""
    global _mongo_collection
    if not MONGO_URI:
        return None
    if _mongo_collection is None:
        try:
            from pymongo import MongoClient
            client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2500)
            client.admin.command("ping")
            _mongo_collection = client[MONGO_DB]["todo_items"]
        except Exception as exc:
            app.logger.warning("MongoDB unavailable; using JSON storage: %s", exc)
            return None
    return _mongo_collection


def read_items():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf-8")
    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_item(item):
    collection = get_mongo_collection()
    if collection is not None:
        collection.insert_one(item.copy())
        return "mongodb"
    items = read_items()
    items.append(item)
    DATA_FILE.write_text(json.dumps(items, indent=2), encoding="utf-8")
    return "json"


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/api")
def api_info():
    # Task 2 practises editing the JSON configuration consumed by this route.
    config_path = ROOT / "api_config.json"
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
        if not isinstance(config, dict):
            raise ValueError("API config must be a JSON object")
    except (OSError, json.JSONDecodeError, ValueError):
        config = {
            "name": "To-Do API",
            "version": "1.0",
            "routes": ["/api", "/submittodoitem", "/items"],
            "owner": "local"
        }
    config["method"] = "POST"
    config["storage"] = "MongoDB when configured; local JSON fallback otherwise"
    return jsonify(config)


@app.post("/submittodoitem")
def submit_todo_item():
    payload = request.get_json(silent=True)
    if payload is None:
        payload = request.form.to_dict()

    item_name = str(payload.get("itemName", "")).strip()
    item_description = str(payload.get("itemDescription", "")).strip()
    if not item_name or not item_description:
        return jsonify({
            "success": False,
            "error": "Both itemName and itemDescription are required."
        }), 400

    item_id = max([int(i.get("itemId", 0)) for i in read_items()] or [0]) + 1
    item_uuid = str(uuid.uuid4())
    canonical = f"{item_id}|{item_uuid}|{item_name}|{item_description}"
    item_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    item = {
        "itemId": item_id,
        "itemUUID": item_uuid,
        "itemHash": item_hash,
        "itemName": item_name,
        "itemDescription": item_description,
        "createdAt": datetime.now(timezone.utc).isoformat()
    }
    storage = save_item(item)
    return jsonify({"success": True, "storage": storage, "item": item}), 201


@app.get("/items")
def list_items():
    collection = get_mongo_collection()
    if collection is not None:
        try:
            items = list(collection.find({}, {"_id": 0}).sort("itemId", 1))
            return jsonify({"items": items, "storage": "mongodb"})
        except Exception as exc:
            app.logger.warning("MongoDB read failed; using JSON storage: %s", exc)
    return jsonify({"items": read_items(), "storage": "json"})


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
