const task = await taskSpace("wavvy-2300-suno-regenerate");
const page = task.page("p1");
const f0 = await readForm(page);
await page.waitForTimeout(15000);
const f1 = await readForm(page);
console.log("credits", f0.credits, "->", f1.credits);
await page.click('button:has-text("Filters")', { label: "Open filters popover (read only)" }).catch(async e => { console.log("click err", String(e).slice(0,200)); });
await page.waitForTimeout(1200);
await page.screenshot({ path: EVDIR + "/ego/r04-filters.png" });
const txt = await page.evaluate(() => {
  const pops = [...document.querySelectorAll('[role=dialog],[role=menu],[data-radix-popper-content-wrapper],[role=listbox]')].filter(e => e.getBoundingClientRect().width > 0);
  return pops.map(p => p.innerText.replace(/\n/g, ' | ').slice(0, 800));
});
console.log(JSON.stringify(txt));
await page.keyboard.press("Escape");
await page.waitForTimeout(600);
await page.screenshot({ path: EVDIR + "/ego/r04-after-escape.png" });
