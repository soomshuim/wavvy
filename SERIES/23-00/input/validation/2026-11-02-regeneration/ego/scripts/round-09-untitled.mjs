const task = await taskSpace("wavvy-2300-suno-regenerate");
const page = task.page("p1");
const info = await page.evaluate(() => {
  const all = [...document.querySelectorAll('[role=group]')];
  const noHref = all.filter(g => !g.querySelector('a[href^="/song/"]'));
  return { totalGroups: all.length, withHref: all.length - noHref.length, noHref: noHref.map(g => ({ label: g.getAttribute('aria-label'), w: Math.round(g.getBoundingClientRect().width), h: Math.round(g.getBoundingClientRect().height), top: Math.round(g.getBoundingClientRect().top), text: g.innerText.replace(/\n/g, ' | ').slice(0, 120), parentRole: g.parentElement && g.parentElement.getAttribute('role'), nestedInGroup: !!g.parentElement.closest('[role=group]') })).slice(0, 30) };
});
console.log(JSON.stringify(info, null, 1));
await page.screenshot({ path: EVDIR + "/ego/r09-list-now.png" });
