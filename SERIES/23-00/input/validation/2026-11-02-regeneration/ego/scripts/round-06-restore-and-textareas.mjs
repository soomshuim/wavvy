const task = await taskSpace("wavvy-2300-suno-regenerate");
const page = task.page("p1");
const val = async (label) => page.evaluate((label) => { const s = [...document.querySelectorAll('[role=slider]')].filter(e => e.getBoundingClientRect().width > 0 && e.getAttribute('aria-label') === label); return s.map(e => e.getAttribute('aria-valuenow')); }, label);
await page.evaluate(() => { const s = [...document.querySelectorAll('[role=slider]')].filter(e => e.getBoundingClientRect().width > 0 && e.getAttribute('aria-label') === "Weirdness"); s[0].focus(); });
for (let i = 0; i < 50; i++) await page.keyboard.press("ArrowLeft");
await page.waitForTimeout(400);
console.log("restored", await val("Weirdness"), await val("Style Influence"), await val("Variety"));
const tas = await page.evaluate(() => [...document.querySelectorAll('textarea,input')].map(e => ({ tag: e.tagName, ph: e.getAttribute('placeholder'), al: e.getAttribute('aria-label'), w: Math.round(e.getBoundingClientRect().width), maxlen: e.getAttribute('maxlength'), val: (e.value || '').slice(0, 30) })));
console.log(JSON.stringify(tas, null, 1));
