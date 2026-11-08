/* Client-side filtering of curated local metadata. No provider requests. */
(function (root) {
  'use strict';
  function normalize(value) { return String(value || '').normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase(); }
  function matches(record, filters) {
    if (filters.free && !record.access.free_data_available) return false;
    if (filters.topic && !record.topics.includes(filters.topic)) return false;
    if (filters.level && !record.data_levels.includes(filters.level)) return false;
    if (filters.access && record.access.status !== filters.access) return false;
    if (filters.kind && record.kind !== filters.kind) return false;
    if (filters.geo) {
      const [type, value] = filters.geo.split(':');
      if (type === 'country' && !record.geography.country_codes.includes(value)) return false;
      if (type === 'region' && !record.geography.regions.includes(value)) return false;
    }
    const text = normalize(JSON.stringify(record));
    return normalize(filters.q).trim().split(/\s+/).filter(Boolean).every(term => text.includes(term));
  }
  if (typeof module !== 'undefined' && module.exports) { module.exports = { matches, normalize }; return; }
  const scriptURL = document.currentScript.src;
  async function start() {
    const form = document.getElementById('atlas-form');
    if (!form) return;
    const status = document.getElementById('atlas-status');
    const results = document.getElementById('atlas-results');
    const fields = Object.fromEntries(['q','topic','geo','level','access','kind','free'].map(k => [k, document.getElementById('atlas-' + k)]));
    const base = new URL('../', scriptURL);
    function node(tag, text, className) { const el = document.createElement(tag); if (text) el.textContent = text; if (className) el.className = className; return el; }
    function option(parent, value, label) { const el = node('option', label); el.value = value; parent.append(el); }
    try {
      const response = await fetch(new URL('catalog.json', scriptURL));
      if (!response.ok) throw new Error('Catalog unavailable');
      const data = await response.json();
      data.topics.forEach(t => option(fields.topic, t.id, t.id + ' · ' + t.name));
      const regions = node('optgroup'); regions.label = 'Regions / scope'; fields.geo.append(regions);
      data.geography.regions.forEach(r => option(regions, 'region:' + r, r));
      const countries = node('optgroup'); countries.label = 'Confirmed country examples'; fields.geo.append(countries);
      data.geography.countries.sort((a,b) => a.name.localeCompare(b.name)).forEach(c => option(countries, 'country:' + c.code, c.name));
      const params = new URLSearchParams(location.search);
      for (const [key, el] of Object.entries(fields)) {
        if (key === 'free') el.checked = params.get('free') !== '0';
        else if (params.has(key)) el.value = params.get(key);
      }
      function render() {
        const filters = Object.fromEntries(Object.entries(fields).map(([k,v]) => [k,k === 'free' ? v.checked : v.value]));
        const found = data.records.filter(r => matches(r, filters)).sort((a,b) => a.name.localeCompare(b.name));
        results.replaceChildren();
        status.textContent = found.length + ' matching records · ' + (filters.free ? 'documented free data routes' : 'includes reference-only entries');
        const p = new URLSearchParams();
        for (const [k,v] of Object.entries(filters)) { if (k==='free') { if (!v) p.set(k,'0'); } else if (v) p.set(k,v); }
        history.replaceState(null,'',location.pathname + (p.size ? '?' + p.toString() : '') + location.hash);
        if (!found.length) { results.append(node('p','No matching seed records. Clear a filter or try a broader keyword. Missing coverage is not proof that data do not exist.','atlas-empty')); return; }
        for (const r of found) {
          const card = node('article', '', 'atlas-card');
          card.append(node('span',r.access.status + (r.access.free_data_available ? '' : ' · REFERENCE ONLY'),'atlas-badge' + (r.access.free_data_available ? '' : ' reference')));
          const h=node('h2'); const a=node('a',r.name); a.href=new URL(r.card_url,base);h.append(a);card.append(h);
          card.append(node('div',r.organization_name+' · '+r.kind,'atlas-meta'));
          card.append(node('p',r.description));
          card.append(node('div',r.topic_labels.join(' · '),'atlas-meta'));
          card.append(node('div',r.data_levels.join(', ')+' · '+r.observation_units.join(', ')+' · '+r.geography.regions.join(', '),'atlas-meta'));
          const footer=node('div','','atlas-card-footer');const detail=node('a','Read card');detail.href=a.href;const original=node('a','Original source ↗');original.href=r.links[0].url;original.rel='noopener';footer.append(detail,original);card.append(footer);results.append(card);
        }
      }
      form.addEventListener('submit',e => e.preventDefault());
      form.addEventListener('input',render);
      form.addEventListener('change',event => {
        if (event.target === fields.access && fields.access.value === 'METADATA_ONLY') fields.free.checked = false;
        render();
      });
      document.getElementById('atlas-clear').addEventListener('click',()=>{form.reset(); fields.free.checked=true; render();});
      render();
    } catch (error) {
      status.textContent='The interactive index could not load. Use Browse by source or Browse by topic above; all cards remain available.';
    }
  }
  if (document.readyState==='loading') document.addEventListener('DOMContentLoaded',start); else start();
})(typeof globalThis !== 'undefined' ? globalThis : this);
