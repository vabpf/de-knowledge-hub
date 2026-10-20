// Zensical's search lives in an open shadow root. Keep its panel opaque when
// backdrop blur is unavailable. Limit the override to this search component.
(() => {
  function init() {
    const selector = 'dialog[aria-label="Search"]';
    function apply(root) {
      if (!root.querySelector(selector)) return false;
      if (!root.getElementById('hub-search-readability')) {
        const style = document.createElement('style');
        style.id = 'hub-search-readability';
        style.textContent = `${selector} { --alpha-light: 1; }`;
        root.appendChild(style);
      }
      return true;
    }
    const observed = new WeakSet();
    function scan() {
      for (const host of document.querySelectorAll('body > div')) {
        const root = host.shadowRoot;
        if (!root || observed.has(root)) continue;
        observed.add(root);
        if (apply(root)) continue;
        const pending = new MutationObserver(() => {
          if (apply(root)) pending.disconnect();
        });
        pending.observe(root, { childList: true });
      }
    }
    new MutationObserver(scan).observe(document.body, { childList: true });
    scan();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else init();
})();
