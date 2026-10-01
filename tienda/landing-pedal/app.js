/* =====================================================================
   DR LANDING → SHOPIFY CHECKOUT · Pedal Resistance Band
   Único sitio de verdad: CONFIG. Precios = precios de Shopify.
   Sin reseñas ni toasts: se añaden solo cuando haya compras reales.
   ===================================================================== */

const CONFIG = {
  brand: 'The Pedal Band',
  shopDomain: 'https://DOMINIO-NEUTRO.com',  // ⚠️ SUSTITUIR por el dominio de la tienda Shopify (sin barra final)
  pixelId: 'PIXEL_ID',                       // ⚠️ SUSTITUIR — debe coincidir con el snippet del <head>
  currency: 'USD',
  splitProvider: '',                         // vacío: no consta que el checkout ofrezca Klarna/Afterpay
  // compare = qty × precio de 1 banda (ancla real, no un "precio antes" inventado)
  packs: [
    { key: 'one',   label: '1 band',  name: 'Pedal Band ×1', qty: 1, price: 24.99, compare: 24.99, note: 'Just for you',          variantId: 'VARIANT_ID_1' },
    { key: 'two',   label: '2 bands', name: 'Pedal Band ×2', qty: 2, price: 39.98, compare: 49.98, note: 'One to keep, one to gift', variantId: 'VARIANT_ID_2', badge: 'MOST POPULAR', default: true },
    { key: 'three', label: '3 bands', name: 'Pedal Band ×3', qty: 3, price: 54.99, compare: 74.97, note: 'Home, office, a friend', variantId: 'VARIANT_ID_3', badge: 'BEST VALUE' }, // PROPUESTA: borra esta línea si solo quieres 2 packs
  ],
};

/* ---------- helpers ---------- */
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const money = n => '$' + n.toFixed(2);
const pct = p => Math.round((1 - p.price / p.compare) * 100);
const perUnit = p => money(p.price / p.qty);

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
      <span class="pack-months">${p.note}</span>
      <span class="pack-price">${money(p.price)}</span>
      ${pct(p) > 0 ? `<span class="pack-compare">${money(p.compare)}</span><span class="pack-save">SAVE ${pct(p)}%</span>` : ''}
      <span class="pack-unit">${perUnit(p)} / band</span>
    </button>`).join('');
  $$('.pack', box).forEach(b => b.addEventListener('click', () => {
    active = CONFIG.packs.find(p => p.key === b.dataset.key);
    renderPacks(); renderActive();
  }));
}

function renderActive() {
  const save = pct(active) > 0;
  $$('[data-cta]').forEach(b => b.textContent = `Add to cart — ${money(active.price)}`);
  $$('[data-hero-price]').forEach(e => e.textContent = money(active.price));
  $$('[data-hero-compare]').forEach(e => { e.textContent = money(active.compare); e.hidden = !save; });
  $$('[data-hero-save]').forEach(e => { e.textContent = `SAVE ${pct(active)}%`; e.hidden = !save; });
  $$('[data-hero-sub]').forEach(e => e.textContent = `${active.label} · ${perUnit(active)} per band`);
  $$('[data-sticky-name]').forEach(e => e.textContent = active.name);
  $$('[data-sticky-price]').forEach(e => e.textContent = money(active.price));
  const sp = $('[data-split]');
  if (sp) sp.hidden = true;
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

/* ---------- boot ---------- */
document.addEventListener('DOMContentLoaded', () => {
  renderPacks();
  renderActive();
  $$('[data-checkout]').forEach(b => b.addEventListener('click', e => { e.preventDefault(); checkout(active); }));
  $$('[data-scroll-offer]').forEach(b => b.addEventListener('click', e => { e.preventDefault(); $('#offer').scrollIntoView({ behavior: 'smooth' }); }));
  initSticky(); initFaq();
  fbTrack('ViewContent', active);
});
