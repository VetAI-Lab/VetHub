let catalog = null;
let currentView = "accepted";

const q = (id) => document.getElementById(id);

function textFor(item) {
  return [
    item.full_name,
    item.description,
    item.language,
    ...(item.topics || []),
    ...(item.domains || []),
    ...(item.species || []),
    ...(item.tasks || []),
    ...(item.resource_types || []),
  ].filter(Boolean).join(" ").toLowerCase();
}

function render() {
  if (!catalog) return;

  const query = q("search").value.trim().toLowerCase();
  let items = [];

  if (currentView === "accepted") items = catalog.accepted || [];
  else if (currentView === "candidates") items = catalog.candidates || [];
  else items = [...(catalog.accepted || []), ...(catalog.candidates || [])];

  if (query) items = items.filter((item) => textFor(item).includes(query));

  q("stats").textContent =
    `${catalog.counts.accepted} reviewed · ${catalog.counts.candidates} candidates · ${items.length} shown`;

  q("results").innerHTML = items.map((item) => {
    const tags = [
      ...(item.domains || []),
      ...(item.species || []),
      ...(item.tasks || []),
      ...(item.topics || []).slice(0, 4),
    ].slice(0, 8);

    return `
      <article class="card">
        <h2><a href="${item.url}" target="_blank" rel="noopener">${item.full_name}</a></h2>
        <p class="description">${item.description || "No description available."}</p>
        <div class="meta">
          ${item.language ? `<span>${item.language}</span>` : ""}
          ${item.license ? `<span>${item.license}</span>` : ""}
          ${Number.isFinite(item.stars) ? `<span>★ ${item.stars}</span>` : ""}
          ${item.archived ? `<span>Archived</span>` : ""}
        </div>
        <div class="tags">${tags.map((x) => `<span class="tag">${x}</span>`).join("")}</div>
      </article>
    `;
  }).join("");
}

fetch("catalog.json")
  .then((response) => response.json())
  .then((data) => {
    catalog = data;
    render();
  })
  .catch((error) => {
    q("results").textContent = `Unable to load catalog: ${error}`;
  });

q("search").addEventListener("input", render);

document.querySelectorAll("#filters button").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll("#filters button").forEach((b) => b.classList.remove("active"));
    button.classList.add("active");
    currentView = button.dataset.view;
    render();
  });
});
