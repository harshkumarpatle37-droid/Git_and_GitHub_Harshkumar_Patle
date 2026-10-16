const form = document.querySelector("#todo-form");
const message = document.querySelector("#message");
const itemsContainer = document.querySelector("#items");

async function loadItems() {
  itemsContainer.textContent = "Loading items…";
  try {
    const response = await fetch("/items");
    const result = await response.json();
    itemsContainer.replaceChildren();
    if (!result.items.length) {
      const empty = document.createElement("p");
      empty.className = "muted";
      empty.textContent = "No items yet. Add your first task above.";
      itemsContainer.append(empty);
      return;
    }
    result.items.forEach(item => {
      const article = document.createElement("article");
      article.className = "item";
      const title = document.createElement("h3");
      title.textContent = `${item.itemId}. ${item.itemName}`;
      const description = document.createElement("p");
      description.textContent = item.itemDescription;
      const meta = document.createElement("p");
      meta.className = "meta";
      meta.textContent = `UUID: ${item.itemUUID} | SHA-256: ${item.itemHash}`;
      article.append(title, description, meta);
      itemsContainer.append(article);
    });
  } catch {
    itemsContainer.textContent = "Could not load items. Check that the Flask server is running.";
  }
}

form.addEventListener("submit", async event => {
  event.preventDefault();
  message.className = "";
  message.textContent = "Saving…";
  const payload = {
    itemName: form.elements.itemName.value.trim(),
    itemDescription: form.elements.itemDescription.value.trim()
  };
  try {
    const response = await fetch("/submittodoitem", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload)
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "Unable to save item");
    message.className = "success";
    message.textContent = `Saved successfully using ${result.storage} storage.`;
    form.reset();
    await loadItems();
  } catch (error) {
    message.className = "error";
    message.textContent = error.message;
  }
});

document.querySelector("#refresh").addEventListener("click", loadItems);
loadItems();
