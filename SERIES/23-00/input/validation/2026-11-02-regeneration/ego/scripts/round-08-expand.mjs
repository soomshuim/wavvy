const task = await taskSpace("wavvy-2300-suno-regenerate");
const page = task.page("p1");
console.log(JSON.stringify(await ensureMoreOptionsOpen(page)));
const f = await readForm(page);
console.log(f.sliders.map(s => s.label + "=" + s.now).join(","), f.sliders[0].rowText);
await page.screenshot({ path: EVDIR + "/ego/r08-expanded.png" });
