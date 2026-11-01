const task = await taskSpace("wavvy-2300-suno-generate");
const page = task.page("p1");
const titles = ["귤","라디오","스웨터","편지","기타","노을","여름밤","막차","벚꽃","그네","포근히"];
let last = null;
for (let i = 0; i < 8; i++) {
  const { hasScroller, rows } = await readAllList(page);
  const mine = rows.filter(r => titles.includes(r.label));
  const done = mine.filter(r => /^\d+:\d\d \|/.test(r.text));
  last = { at: new Date().toISOString(), hasScroller, total: rows.length, mine: mine.length, done: done.length };
  console.log(JSON.stringify(last));
  if (mine.length === 22 && done.length === 22) { await fs.writeFile(EVDIR + "/list-all-complete.json", JSON.stringify({ at: last.at, rows }, null, 1)); console.log("ALL_COMPLETE"); break; }
  await page.waitForTimeout(30000);
}
const { rows } = await readAllList(page);
await fs.writeFile(EVDIR + "/list-latest.json", JSON.stringify({ at: new Date().toISOString(), rows }, null, 1));
for (const r of rows.filter(r => titles.includes(r.label))) console.log(JSON.stringify({ label: r.label, id: r.href.replace("/song/",""), head: r.text.slice(0, 40) }));
