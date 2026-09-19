/* =====================================================================
   DR LANDING → SHOPIFY CHECKOUT — FluidXtract
   Único sitio de verdad: CONFIG. El HTML se rellena desde aquí.
   Reglas: precios = precios de Shopify · pack intermedio default ·
   nunca hardcodear precios fuera de CONFIG.
   ===================================================================== */

const CONFIG = {
  brand: 'FluidXtract',
  shopDomain: 'https://TU-TIENDA.com',       // ⚠️ SUSTITUIR por el dominio real de tu tienda Shopify (sin barra final)
  pixelId: 'PIXEL_ID',                       // ⚠️ SUSTITUIR por tu Pixel ID — debe coincidir con el snippet del <head>
  currency: 'USD',
  splitProvider: 'Klarna',                   // '' para ocultar el split
  packs: [
    { key: 'single', label: '1 unit',  name: 'FluidXtract 1-Pack', qty: 1, price: 29.99, compare: 49.99,  tag: 'One vehicle',   variantId: 'VARIANT_ID_1PACK' },
    { key: 'duo',    label: '2-Pack',  name: 'FluidXtract 2-Pack', qty: 2, price: 39.99, compare: 79.99,  tag: 'Car + bike',    variantId: 'VARIANT_ID_2PACK', badge: 'MOST POPULAR', default: true },
    { key: 'trio',   label: '3-Pack',  name: 'FluidXtract 3-Pack', qty: 3, price: 49.99, compare: 119.99, tag: 'Whole yard',    variantId: 'VARIANT_ID_3PACK', badge: 'BEST VALUE' },
  ],
  toasts: [
    { who: 'Mark D.', where: 'Tulsa, OK', pack: '2-Pack' },
    { who: 'Ray S.', where: 'Boise, ID', pack: '1-Pack' },
    { who: 'Curtis W.', where: 'Knoxville, TN', pack: '3-Pack' },
    { who: 'Hank P.', where: 'Fresno, CA', pack: '2-Pack' },
  ],
};

/* ---------- helpers ---------- */
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const money = n => '$' + n.toFixed(2);
const pct = p => Math.round((1 - p.price / p.compare) * 100);
const perUnit = p => money(p.price / p.qty);
const split = p => money(p.price / 4);

let active = CONFIG.packs.find(p => p.default) || CONFIG.packs[1] || CONFIG.packs[0];

/* ---------- pixel ---------- */
function fbTrack(ev, pack) {
  if (typeof fbq !== 'function') return;
  fbq('track', ev, {
    content_name: pack.name,
    content_ids: [pack.variantId],
    content_type: 'product',
    value: pack.price,
    currency: CONFIG.currency,
  });
}

/* ---------- checkout (cart permalink) ---------- */
function checkout(pack) {
  fbTrack('AddToCart', pack);
  const url = `${CONFIG.shopDomain}/cart/${pack.variantId}:1`;
  setTimeout(() => { location.href = url; }, 150); // deja salir el evento
}

/* ---------- render ---------- */
function renderPacks() {
  const box = $('#packs');
  box.innerHTML = CONFIG.packs.map(p => `
    <button class="pack${p === active ? ' active' : ''}" data-key="${p.key}" type="button">
      ${p.badge ? `<span class="badge">${p.badge}</span>` : ''}
      <span class="pack-label">${p.label}</span>
      <span class="pack-months">${p.tag}</span>
      <span class="pack-price">${money(p.price)}</span>
      <span class="pack-compare">${money(p.compare)}</span>
      <span class="pack-save">SAVE ${pct(p)}%</span>
      <span class="pack-unit">${perUnit(p)} / each</span>
    </button>`).join('');
  $$('.pack', box).forEach(b => b.addEventListener('click', () => {
    active = CONFIG.packs.find(p => p.key === b.dataset.key);
    renderPacks(); renderActive();
  }));
}

function renderActive() {
  $$('[data-cta]').forEach(b => b.textContent = `Add to cart — ${money(active.price)}`);
  $$('[data-hero-price]').forEach(e => e.textContent = money(active.price));
  $$('[data-hero-compare]').forEach(e => e.textContent = money(active.compare));
  $$('[data-hero-save]').forEach(e => e.textContent = `SAVE ${pct(active)}%`);
  $$('[data-hero-sub]').forEach(e => e.textContent = `${active.label} · ${active.tag}`);
  $$('[data-sticky-name]').forEach(e => e.textContent = active.name);
  $$('[data-sticky-price]').forEach(e => e.textContent = money(active.price));
  const sp = $('[data-split]');
  if (sp) {
    sp.hidden = !CONFIG.splitProvider;
    sp.textContent = `or 4 × ${split(active)} with ${CONFIG.splitProvider}`;
  }
}

/* ---------- sticky ATC ---------- */
function initSticky() {
  const sticky = $('#stickyAtc'), hero = $('.hero');
  if (!sticky || !hero) return;
  addEventListener('scroll', () => {
    const past = scrollY > hero.offsetHeight;
    sticky.classList.toggle('show', past);
    document.body.classList.toggle('has-sticky', past);
  }, { passive: true });
}

/* ---------- FAQ ---------- */
function initFaq() {
  $$('.faq-q').forEach(q => q.addEventListener('click', () => q.parentElement.classList.toggle('open')));
}

/* ---------- toasts ---------- */
function initToasts() {
  const el = $('#toast');
  if (!el || !CONFIG.toasts.length) return;
  let i = 0;
  const show = () => {
    const t = CONFIG.toasts[i++ % CONFIG.toasts.length];
    el.innerHTML = `<b>${t.who}</b> from ${t.where} ordered <b>${t.pack}</b>`;
    el.classList.add('show');
    setTimeout(() => el.classList.remove('show'), 4500);
  };
  setTimeout(show, 6000);
  setInterval(show, 22000);
}

/* ---------- boot ---------- */
document.addEventListener('DOMContentLoaded', () => {
  renderPacks();
  renderActive();
  $$('[data-checkout]').forEach(b => b.addEventListener('click', e => { e.preventDefault(); checkout(active); }));
  $$('[data-scroll-offer]').forEach(b => b.addEventListener('click', e => { e.preventDefault(); $('#offer').scrollIntoView({ behavior: 'smooth' }); }));
  initSticky(); initFaq(); initToasts();
  fbTrack('ViewContent', active);
});
