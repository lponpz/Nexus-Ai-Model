const $ = (id) => document.getElementById(id);

async function api(path, options={}) {
  const response = await fetch(path, {headers:{"Content-Type":"application/json"}, ...options});
  const data = await response.json().catch(()=>({}));
  if (!response.ok) throw new Error(data.detail || "Request failed");
  return data;
}

function addMessage(text, role, provider="") {
  const node = document.createElement("div");
  node.className = "bubble " + role;
  node.textContent = provider ? text + "\n\nProvider: " + provider : text;
  $("messages").appendChild(node);
  $("messages").scrollTop = $("messages").scrollHeight;
}

async function loadChatHistory() {
  const history = await api("/api/chat/history");
  const list = $("messages");
  list.replaceChildren();
  if (!history.length) {
    addMessage("Hi! I’m Your AI. Ask me something to get started.", "assistant");
    return;
  }
  for (const item of history) addMessage(item.content, item.role, item.provider);
}

async function refreshProjects() {
  const projects = await api("/api/projects");
  const list = $("project-list");
  list.replaceChildren();
  if (!projects.length) {
    const empty = document.createElement("p");
    empty.className = "muted";
    empty.textContent = "No projects yet — create your first one.";
    list.appendChild(empty);
    return;
  }
  for (const project of projects) {
    const item = document.createElement("div");
    item.className = "project-item";
    const name = document.createElement("strong");
    name.textContent = project.name;
    const category = document.createElement("small");
    category.textContent = project.category;
    item.append(name, category);
    list.appendChild(item);
  }
}

$("chat-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const input = $("chat-input");
  const message = input.value.trim();
  if (!message) return;
  addMessage(message, "user");
  input.value = "";
  const pending = document.createElement("div");
  pending.className = "bubble assistant";
  pending.textContent = "Thinking…";
  $("messages").appendChild(pending);
  try {
    const result = await api("/api/chat", {
      method: "POST",
      body: JSON.stringify({message})
    });
    pending.textContent = result.reply + "\n\nProvider: " + result.provider;
  } catch (error) {
    pending.textContent = "Could not reach an AI provider. Check your .env settings and make sure Ollama is running if using offline mode.\n" + error.message;
  }
});

$("project-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    await api("/api/projects", {
      method: "POST",
      body: JSON.stringify({
        name: $("project-name").value.trim(),
        category: $("project-category").value
      })
    });
    $("project-name").value = "";
    await refreshProjects();
  } catch (error) {
    alert(error.message);
  }
});

(async () => {
  try {
    $("status").textContent = "Backend online";
    await Promise.all([refreshProjects(), loadChatHistory()]);
  } catch (error) {
    $("status").textContent = "Backend unavailable";
  }
})();
