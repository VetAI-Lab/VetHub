let catalog = null;
let activeTheme = null;

const q = (id) => document.getElementById(id);

function searchableText(item) {
  return [
    item.full_name,
    item.description,
    item.language,
    ...(item.topics || []),
    ...(item.domains || []),
    ...(item.species || []),
    ...(item.tasks || []),
    ...(item.resource_types || []),
    ...(item.modalities || []),
  ]
    .filter(Boolean)
    .join(" ")
    .toLowerCase();
}


function getThemes(resources) {
  const counts = {};

  resources.forEach((item) => {
    (item.domains || []).forEach((domain) => {
      counts[domain] = (counts[domain] || 0) + 1;
    });
  });

  return Object.entries(counts)
    .sort((a, b) => b[1] - a[1]);
}


function renderThemes() {

  const themes = getThemes(catalog.resources || []);

  q("themes").innerHTML = `
    <div style="
      display:flex;
      gap:8px;
      flex-wrap:wrap;
      margin-bottom:24px;
    ">

      <button
        class="theme-button"
        data-theme=""
      >
        All
      </button>

      ${themes.map(([theme, count]) => `
        <button
          class="theme-button"
          data-theme="${theme}"
        >
          ${theme.replaceAll("-", " ")} (${count})
        </button>
      `).join("")}

    </div>
  `;

  document.querySelectorAll(".theme-button")
    .forEach((button) => {

      button.addEventListener("click", () => {

        activeTheme =
          button.dataset.theme || null;

        render();

      });

    });

}


function render() {

  if (!catalog) return;

  const query =
    q("search").value.trim().toLowerCase();

  let items = [...(catalog.resources || [])];

  if (activeTheme) {
    items = items.filter(
      (item) =>
        (item.domains || []).includes(activeTheme)
    );
  }

  if (query) {
    items = items.filter(
      (item) =>
        searchableText(item).includes(query)
    );
  }

  q("stats").textContent =
    `${catalog.counts.accepted} reviewed resources · ${items.length} shown`;

  q("results").innerHTML =
    items.map((item) => {

      const tags = [
        ...(item.domains || []),
        ...(item.species || []),
        ...(item.tasks || []),
        ...(item.topics || []).slice(0, 4),
      ].slice(0, 10);

      return `
        <article class="card">

          <h2>
            <a
              href="${item.url}"
              target="_blank"
              rel="noopener"
            >
              ${item.full_name}
            </a>
          </h2>

          <p class="description">
            ${item.description || "No description available."}
          </p>

          <div class="meta">

            ${
              item.language
                ? `<span>${item.language}</span>`
                : ""
            }

            ${
              item.license
                ? `<span>${item.license}</span>`
                : ""
            }

            ${
              Number.isFinite(item.stars)
                ? `<span>★ ${item.stars}</span>`
                : ""
            }

            ${
              item.archived
                ? `<span>Archived</span>`
                : ""
            }

          </div>

          <div class="tags">

            ${tags.map(
              (tag) =>
                `<span class="tag">${tag}</span>`
            ).join("")}

          </div>

        </article>
      `;

    }).join("");

}


fetch("catalog.json")
  .then((response) => response.json())
  .then((data) => {

    catalog = data;

    renderThemes();
    render();

  })
  .catch((error) => {

    q("results").textContent =
      `Unable to load catalog: ${error}`;

  });


q("search")
  .addEventListener("input", render);
