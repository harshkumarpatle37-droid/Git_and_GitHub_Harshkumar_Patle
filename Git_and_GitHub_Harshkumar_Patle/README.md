# Git & GitHub DevOps Assignment
**Student:** Harshkumar Patle  
**Platform:** Linux (Ubuntu/Debian recommended)  
**Project:** Flask To-Do application with JSON API and MongoDB-compatible storage

## Project features
- Flask home page with a To-Do form.
- `GET /api` returns the API configuration JSON.
- `POST /submittodoitem` accepts `itemName` and `itemDescription`, then stores the item in MongoDB when configured; otherwise it uses a local JSON file.
- Item ID, UUID, and SHA-256 item hash fields.
- `GET /items` lists saved items.
- Git task walkthrough for SSH, branches, merge-conflict resolution, sequential commits, `git reset --soft`, and rebase.

## Requirements
- Python 3.10+
- Git
- Optional: MongoDB Atlas or a local MongoDB instance

## Run locally
```bash
cd Git_and_GitHub_Harshkumar_Patle
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
python app.py
```
Open http://127.0.0.1:5000.

Without `MONGO_URI`, the app stores data in `data/items.json`. To use MongoDB, set `MONGO_URI` and optionally `MONGO_DB` in `.env`.

## Important submission note
The documentation includes screenshot instructions and evidence placeholders. Capture your own terminal/browser screenshots while executing the commands; do not submit blank placeholders as evidence. Replace `YOUR_GITHUB_REPOSITORY_URL` in `docs/assignment_report.md` with your actual repository URL.
