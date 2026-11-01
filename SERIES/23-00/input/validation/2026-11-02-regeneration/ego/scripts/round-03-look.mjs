const task = await taskSpace("wavvy-2300-suno-regenerate");
const page = task.page("p1");
await page.screenshot({ path: EVDIR + "/ego/r03-screen.png" });
const info = await page.evaluate(() => {
  const btns = [...document.querySelectorAll('button,[role=tab],[role=combobox]')].filter(b => b.getBoundingClientRect().width > 0).map(b => (b.getAttribute('aria-label') || '') + '#' + b.textContent.trim().slice(0, 30) + '#' + (b.getAttribute('aria-selected') || b.getAttribute('aria-pressed') || ''));
  return { btns: btns.slice(0, 120) };
});
console.log(JSON.stringify(info));
