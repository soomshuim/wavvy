const task = await taskSpace("wavvy-2300-suno-regenerate");
const page = task.page("p1");
const f = await readForm(page);
const { hasScroller, rows } = await readAllList(page);
const extra = await page.evaluate(() => {
  const out = {};
  for (const g of document.querySelectorAll('[role=group]')) {
    const a = g.querySelector('a[href^="/song/"]'); if (!a) continue;
    const btns = [...g.querySelectorAll('button')].map(b => ({ al: b.getAttribute('aria-label'), dis: b.disabled, txt: b.textContent.trim().slice(0, 12) }));
    out[a.getAttribute('href')] = btns;
  }
  return out;
});
for (const r of rows) r.buttons = extra[r.href] || null;
await fs.writeFile(EVDIR + "/list-final-fulltext.json", JSON.stringify({ at: new Date().toISOString(), credits_ui: f.credits, header: f.header, hasScroller, total_rows: rows.length, rows }, null, 1));
console.log(rows.length, f.credits, f.header);
console.log(JSON.stringify(rows[0]).slice(0, 1500));
