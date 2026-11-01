const ids = new Set();
for (const f of await fs.readdir(EVDIR)) {
  if (/^track-\d\d-post-submit\.json$/.test(f)) {
    const j = JSON.parse(await fs.readFile(EVDIR + "/" + f, "utf8"));
    for (const r of (j.newRows || [])) if (r.href) ids.add(r.href);
  }
}
const task = await taskSpace("wavvy-2300-suno-regenerate");
const page = task.page("p1");
let last = null, allDone = false;
for (let i = 0; i < ITER; i++) {
  const { hasScroller, rows } = await readAllList(page);
  const mine = rows.filter(r => ids.has(r.href));
  const done = mine.filter(r => /^\d+:\d\d \|/.test(r.text));
  last = { at: new Date().toISOString(), hasScroller, total: rows.length, expected: ids.size, mine: mine.length, done: done.length };
  console.log(JSON.stringify(last));
  if (mine.length === ids.size && done.length === ids.size) { allDone = true; await fs.writeFile(EVDIR + "/list-all-complete.json", JSON.stringify({ at: last.at, rows }, null, 1)); console.log("ALL_COMPLETE"); break; }
  await page.waitForTimeout(30000);
}
const f = await readForm(page);
const { rows } = await readAllList(page);
await fs.writeFile(EVDIR + "/list-latest.json", JSON.stringify({ at: new Date().toISOString(), credits_ui: f.credits, header: f.header, total_rows: rows.length, rows }, null, 1));
for (const r of rows.filter(r => ids.has(r.href))) console.log(JSON.stringify({ label: r.label, id: r.href.replace("/song/", ""), head: r.text.slice(0, 40) }));
console.log(JSON.stringify({ credits: f.credits, header: f.header, allDone }));
