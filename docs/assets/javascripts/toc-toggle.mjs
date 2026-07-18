const storageKey = "academia-toc-collapsed";
const collapsedClass = "toc-collapsed";

function preferenceIsCollapsed() {
  return window.localStorage.getItem(storageKey) === "true";
}

function updateButton(button, collapsed) {
  button.setAttribute("aria-expanded", String(!collapsed));
  button.setAttribute(
    "aria-label",
    collapsed ? "Mostrar índice" : "Recolher índice",
  );
  button.textContent = collapsed ? "Mostrar índice" : "Recolher índice";
}

function mountTocToggle() {
  const sidebar = document.querySelector(".md-sidebar--secondary");
  if (!sidebar || sidebar.querySelector("#academia-toc-toggle")) return;

  const button = document.createElement("button");
  button.id = "academia-toc-toggle";
  button.className = "academia-toc-toggle";
  button.type = "button";

  const collapsed = preferenceIsCollapsed();
  document.documentElement.classList.toggle(collapsedClass, collapsed);
  updateButton(button, collapsed);

  button.addEventListener("click", () => {
    const nextCollapsed = !document.documentElement.classList.contains(collapsedClass);
    document.documentElement.classList.toggle(collapsedClass, nextCollapsed);
    window.localStorage.setItem(storageKey, String(nextCollapsed));
    updateButton(button, nextCollapsed);
  });

  sidebar.prepend(button);
}

document$.subscribe(mountTocToggle);
