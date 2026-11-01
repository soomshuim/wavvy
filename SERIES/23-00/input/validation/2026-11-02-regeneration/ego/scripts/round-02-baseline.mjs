const task = await taskSpace("wavvy-2300-suno-regenerate");
const page = task.page("p1");
const f = await readForm(page);
const { hasScroller, rows } = await readAllList(page);
await fs.writeFile(EVDIR + "/list-baseline-before-first-submit.json", JSON.stringify({ at: new Date().toISOString(), credits_ui: f.credits, header: f.header, url: f.url, hasScroller, total_rows: rows.length, rows }, null, 1));
console.log(JSON.stringify({ credits: f.credits, header: f.header, total: rows.length }));
for (const r of rows) console.log(r.y, r.label, r.href, "|", r.text.slice(0, 60));
const tabs = await task.tabs();
console.log(JSON.stringify(tabs.map(t => ({ label: t.label, url: t.url, openedBy: t.openedBy, active: t.active }))));
