(() => {
  const catalogue = document.getElementById('site-catalogue');
  const nav = document.getElementById('catalogue-pagination');
  const status = document.getElementById('catalogue-status');
  if (!catalogue || !nav || !status) return;
  const entries = Array.from(catalogue.children);
  const size = Math.max(1, Number.parseInt(catalogue.dataset.pageSize, 10) || 8);
  const total = Math.max(1, Math.ceil(entries.length / size));

  function pageUrl(page) {
    const url = new URL(window.location.href);
    if (page === 1) url.searchParams.delete('page');
    else url.searchParams.set('page', String(page));
    return url;
  }
  function render() {
    const value = new URL(window.location.href).searchParams.get('page') || '1';
    const requested = /^\d+$/.test(value) ? Number(value) : 1;
    const current = Math.min(total, Math.max(1, requested));
    // Normalise invalid, out-of-range and redundant page-one URLs.
    if (value !== String(current) || new URL(window.location.href).searchParams.get('page') === '1') {
      window.history.replaceState(null, '', pageUrl(current));
    }
    entries.forEach((entry, index) => {
      entry.hidden = index < (current - 1) * size || index >= current * size;
    });
    nav.replaceChildren();
    nav.hidden = total <= 1;
    function link(label, page) {
      const anchor = document.createElement('a');
      anchor.href = pageUrl(page).href;
      anchor.textContent = label;
      anchor.dataset.page = String(page);
      nav.append(anchor);
    }
    if (current > 1) link('← Previous', current - 1);
    const label = document.createElement('span');
    label.textContent = `Page ${current} of ${total}`;
    nav.append(label);
    if (current < total) link('Next →', current + 1);
    status.textContent = entries.length
      ? `Showing experiments ${(current - 1) * size + 1}–${Math.min(current * size, entries.length)} of ${entries.length}.`
      : 'No experiments published yet.';
  }
  nav.addEventListener('click', (event) => {
    const anchor = event.target.closest('a[data-page]');
    if (!anchor || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    window.history.pushState(null, '', anchor.href);
    render();
    const heading = catalogue.querySelector('.experiment:not([hidden]) h3');
    if (heading) {
      heading.setAttribute('tabindex', '-1');
      heading.focus({ preventScroll: true });
      heading.scrollIntoView({ block: 'center', behavior: 'instant' });
    }
  });
  window.addEventListener('popstate', render);
  render();
})();
