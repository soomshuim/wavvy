const task = await taskSpace("wavvy-2300-suno-regenerate");
const page = task.page("p1");
const info = await page.evaluate(() => {
  const lab = [...document.querySelectorAll('*')].find(e => e.children.length === 0 && e.textContent.trim() === 'More Options' && e.getBoundingClientRect().width > 0);
  if (!lab) return { err: "no label" };
  const chain = []; let e = lab;
  for (let i = 0; i < 6 && e; i++) { chain.push({ tag: e.tagName, role: e.getAttribute('role'), ae: e.getAttribute('aria-expanded'), ds: e.getAttribute('data-state'), cls: (e.className || '').toString().slice(0, 60), h: Math.round(e.getBoundingClientRect().height) }); e = e.parentElement; }
  const s = [...document.querySelectorAll('[role=slider]')].filter(x => x.getBoundingClientRect().width > 0 && x.getAttribute('aria-label') === 'Weirdness')[0];
  const r = s.getBoundingClientRect();
  const clip = []; let p = s;
  for (let i = 0; i < 12 && p; i++) { const cs = getComputedStyle(p); clip.push({ tag: p.tagName, h: Math.round(p.getBoundingClientRect().height), ov: cs.overflow, ds: p.getAttribute('data-state'), hid: p.getAttribute('hidden') }); p = p.parentElement; }
  return { chain, slider: { top: Math.round(r.top), h: Math.round(r.height), w: Math.round(r.width) }, clip, vh: innerHeight };
});
console.log(JSON.stringify(info, null, 1));
