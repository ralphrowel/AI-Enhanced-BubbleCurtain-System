(function () {
  const STORAGE_KEY = "admin_theme";
  const LIGHT_THEME = "flatly";
  const DARK_THEME = "darkly";

  const themeLink = document.getElementById("jazzmin-theme");

  function getThemeUrl(theme) {
    return `https://bootswatch.com/5/${theme}/bootstrap.min.css`;
  }

  function applyTheme(theme) {
    if (themeLink) {
      themeLink.href = getThemeUrl(theme);
    }
    document.body.setAttribute("data-theme", theme);
    localStorage.setItem(STORAGE_KEY, theme);

    const btn = document.getElementById("theme-toggle-btn");
    if (btn) {
      btn.innerHTML =
        theme === DARK_THEME
          ? '<i class="fas fa-sun"></i> Light Mode'
          : '<i class="fas fa-moon"></i> Dark Mode';
    }
  }

  function toggleTheme() {
    const current = localStorage.getItem(STORAGE_KEY) || LIGHT_THEME;
    applyTheme(current === LIGHT_THEME ? DARK_THEME : LIGHT_THEME);
  }

  function injectButtons() {
    const navbar = document.querySelector(".navbar-nav.ml-auto, .navbar-nav.ms-auto");
    if (!navbar) return;

    // ✅ Dark/Light toggle button
    const themeLi = document.createElement("li");
    themeLi.className = "nav-item";
    themeLi.innerHTML = `
      <a class="nav-link" href="#" id="theme-toggle-btn" title="Toggle Theme">
        <i class="fas fa-moon"></i> Dark Mode
      </a>
    `;
    navbar.prepend(themeLi);

    // ✅ UI Settings shortcut button
    const settingsLi = document.createElement("li");
    settingsLi.className = "nav-item";
    settingsLi.innerHTML = `
    <a class="nav-link" href="/admin/ui-settings/" id="settings-btn" title="Settings">
        <i class="fas fa-sliders-h"></i> Settings
    </a>
    `;
    navbar.prepend(settingsLi);

    document.getElementById("theme-toggle-btn").addEventListener("click", function (e) {
      e.preventDefault();
      toggleTheme();
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) applyTheme(saved);
    injectButtons();
  });
})();