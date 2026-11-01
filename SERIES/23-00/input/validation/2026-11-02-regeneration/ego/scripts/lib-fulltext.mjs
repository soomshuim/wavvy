const fs = await import("node:fs/promises");
const EVDIR = "/Users/zenkim_office/Project/wavvy/SERIES/23-00/input/validation/2026-11-02-regeneration";
const WS_URL = "https://suno.com/create?wid=f578d3c2-f43f-462e-8e05-44d022edd480";
const payloads = JSON.parse(await fs.readFile(EVDIR + "/payloads.json", "utf8"));
const norm = (s) => s.replace(/\r\n?/g, "\n").trim();

async function readForm(page) {
  return await page.evaluate(() => {
    const q = (s) => document.querySelector(s);
    const ed = q('div[role=textbox][aria-label="Lyrics editor"]');
    const lyricsLines = ed ? [...ed.querySelectorAll(':scope > p')].map(p => p.textContent) : null;
    const style = [...document.querySelectorAll('textarea[maxlength="1000"]:not([aria-label])')].find(i => i.getBoundingClientRect().width > 0) || null;
    const excl = q('input[placeholder="Exclude styles"]');
    const titleEl = [...document.querySelectorAll('input[placeholder="Song Title (Optional)"]')].find(i => i.getBoundingClientRect().width > 0);
    const createBtn = [...document.querySelectorAll('button')].find(b => b.getAttribute('aria-label') === 'Create song');
    const credBtn = [...document.querySelectorAll('button')].find(b => (b.getAttribute('aria-label') || '').startsWith('Credits remaining'));
    const tabs = [...document.querySelectorAll('[role=tab]')].map(t => t.textContent.trim() + '=' + t.getAttribute('aria-selected'));
    const sliders = [...document.querySelectorAll('[role=slider]')].filter(s => s.getBoundingClientRect().width > 0).map(s => ({ label: s.getAttribute('aria-label'), now: s.getAttribute('aria-valuenow'), text: s.getAttribute('aria-valuetext'), min: s.getAttribute('aria-valuemin'), max: s.getAttribute('aria-valuemax'), rowText: s.parentElement.parentElement.innerText.replace(/\n/g, ' | ') }));
    const rowState = (label) => {
      const lab = [...document.querySelectorAll('*')].find(e => e.children.length === 0 && e.textContent.trim() === label && e.getBoundingClientRect().width > 0);
      if (!lab) return null;
      let row = lab; for (let i = 0; i < 4 && row.parentElement; i++) { row = row.parentElement; if (row.querySelectorAll('button').length >= 2 || row.querySelectorAll('[role=radio],[role=switch],[role=tab]').length >= 2) break; }
      return [...row.querySelectorAll('button,[role=radio],[role=tab],[role=switch],[role=checkbox]')].filter(b => b.getBoundingClientRect().width > 0).map(b => ({ text: b.textContent.trim(), ariaPressed: b.getAttribute('aria-pressed'), ariaChecked: b.getAttribute('aria-checked'), ariaSelected: b.getAttribute('aria-selected'), dataState: b.getAttribute('data-state'), cls: (b.className || '').toString().slice(0, 120) }));
    };
    const saveBtn = (() => { const cands = [...document.querySelectorAll('*')].filter(e => /^Save to/.test(e.textContent.trim()) && e.getBoundingClientRect().width > 0 && e.textContent.length < 40); if (!cands.length) return null; cands.sort((a, b) => a.textContent.length - b.textContent.length); return cands.map(e => e.textContent.trim().replace(/\n/g, ' | ')).slice(0, 3); })();
    const header = (() => { const h = [...document.querySelectorAll('button')].find(b => b.textContent.trim() === 'Workspaces'); if (!h) return null; let r = h.parentElement; return r.innerText.replace(/\n/g, ' | '); })();
    const modelBtn = [...document.querySelectorAll('button')].find(b => /^v\d/i.test(b.textContent.trim()));
    return {
      url: location.href, tabs, credits: credBtn ? credBtn.getAttribute('aria-label') : null, model: modelBtn ? modelBtn.textContent.trim() : null,
      header, saveTo: saveBtn, lyricsLines, style: style ? style.value : null, exclude: excl ? excl.value : null, title: titleEl ? titleEl.value : null,
      createDisabled: createBtn ? createBtn.disabled : null, sliders,
      gender: rowState('Vocal Gender'), duration: rowState('Duration'), maxMode: rowState('Max Mode'), personalize: rowState('Personalize'),
    };
  });
}

function compare(P, f) {
  const lyrics = f.lyricsLines ? f.lyricsLines.join("\n") : null;
  return {
    lyrics: lyrics !== null && norm(lyrics) === norm(P.lyrics),
    style: f.style !== null && norm(f.style) === norm(P.style),
    exclude: f.exclude !== null && norm(f.exclude) === norm(P.exclude),
    title: f.title !== null && f.title === P.title,
    lyricsLenForm: lyrics ? lyrics.length : null, lyricsLenSrc: P.lyrics.length,
  };
}

async function scrollToSel(page, sel) {
  return await page.evaluate((sel) => { const e = [...document.querySelectorAll(sel)].find(x => x.getBoundingClientRect().width > 0); if (!e) return false; e.scrollIntoView({ block: 'center' }); return true; }, sel);
}
async function clearAndFill(page, P) {
  if (!(await scrollToSel(page, 'div[role=textbox][aria-label="Lyrics editor"]'))) throw new Error("lyrics editor not found");
  await page.waitForTimeout(400);
  await page.click('div[role=textbox][aria-label="Lyrics editor"]', { label: "Focus lyrics editor" });
  await page.keyboard.press("ControlOrMeta+a");
  await page.keyboard.press("Delete");
  await page.keyboard.paste({ text: P.lyrics });
  await page.waitForTimeout(600);
  await scrollToSel(page, 'textarea[maxlength="1000"]:not([aria-label])');
  await page.fill('textarea[maxlength="1000"]:not([aria-label])', "");
  await page.fill('textarea[maxlength="1000"]:not([aria-label])', P.style);
  await scrollToSel(page, 'input[placeholder="Exclude styles"]');
  await page.fill('input[placeholder="Exclude styles"]', "");
  if (P.exclude) await page.fill('input[placeholder="Exclude styles"]', P.exclude);
  await scrollToSel(page, 'input[placeholder="Song Title (Optional)"]');
  await page.fill('input[placeholder="Song Title (Optional)"]', "");
  await page.fill('input[placeholder="Song Title (Optional)"]', P.title);
  await page.waitForTimeout(600);
}

async function readList(page) {
  return await page.evaluate(() => {
    const groups = [...document.querySelectorAll('[role=group]')].filter(g => g.querySelector('a[href^="/song/"]') || g.getAttribute('aria-label'));
    return groups.map(g => {
      const a = g.querySelector('a[href^="/song/"]');
      const play = [...g.querySelectorAll('button')].find(b => /^Play /.test(b.getAttribute('aria-label') || ''));
      return { label: g.getAttribute('aria-label'), href: a ? a.getAttribute('href') : null, anchorText: a ? a.textContent.trim() : null, playLabel: play ? play.getAttribute('aria-label') : null, text: g.innerText.replace(/\n/g, ' | ').slice(0, 260) };
    });
  });
}

async function readAllList(page) {
  return await page.evaluate(async () => {
    const sleep = (ms) => new Promise(r => setTimeout(r, ms));
    const g0 = document.querySelector('[role=group]');
    let sc = g0;
    while (sc && !(sc.scrollHeight > sc.clientHeight + 5 && /(auto|scroll)/.test(getComputedStyle(sc).overflowY))) sc = sc.parentElement;
    const seen = new Map();
    const grab = () => {
      for (const g of document.querySelectorAll('[role=group]')) {
        const a = g.querySelector('a[href^="/song/"]');
        if (!a) continue;
        const id = a.getAttribute('href');
        const y = Math.round(g.getBoundingClientRect().top + (sc ? sc.scrollTop - sc.getBoundingClientRect().top : 0));
        seen.set(id, { label: g.getAttribute('aria-label'), href: id, y, text: g.innerText.replace(/\n/g, ' | ') });
      }
    };
    if (sc) sc.scrollTop = 0;
    await sleep(500); grab();
    if (sc) {
      let guard = 0;
      while (guard++ < 40) {
        const before = sc.scrollTop;
        sc.scrollTop = before + Math.max(200, sc.clientHeight - 150);
        await sleep(450); grab();
        if (sc.scrollTop === before) break;
      }
      sc.scrollTop = 0;
      await sleep(300);
    }
    return { hasScroller: !!sc, rows: [...seen.values()].sort((a, b) => a.y - b.y) };
  });
}

async function setSlider(page, label, target) {
  const read = () => page.evaluate((label) => { const s = [...document.querySelectorAll('[role=slider]')].filter(e => e.getBoundingClientRect().width > 0 && e.getAttribute('aria-label') === label); return s.length === 1 ? Number(s[0].getAttribute('aria-valuenow')) : null; }, label);
  const foc = await page.evaluate((label) => { const s = [...document.querySelectorAll('[role=slider]')].filter(e => e.getBoundingClientRect().width > 0 && e.getAttribute('aria-label') === label); if (s.length !== 1) return "count=" + s.length; s[0].focus(); return document.activeElement === s[0] ? "focused" : "notfocused"; }, label);
  if (foc !== "focused") throw new Error("slider focus failed: " + label + " " + foc);
  for (let pass = 0; pass < 4; pass++) {
    const now = await read();
    if (now === target) return { label, value: now, passes: pass };
    const key = now < target ? "ArrowRight" : "ArrowLeft";
    for (let i = 0; i < Math.abs(target - now); i++) await page.keyboard.press(key);
    await page.waitForTimeout(250);
  }
  return { label, value: await read(), passes: 4 };
}

async function ensureMoreOptionsOpen(page) {
  const st = () => page.evaluate(() => {
    const lab = [...document.querySelectorAll('*')].find(e => e.children.length === 0 && e.textContent.trim() === 'More Options' && e.getBoundingClientRect().width > 0);
    if (!lab) return { found: false };
    let e = lab; while (e && e.getAttribute('role') !== 'button') e = e.parentElement;
    if (!e) return { found: false };
    e.setAttribute('data-wavvy-more', '1');
    const s = [...document.querySelectorAll('[role=slider]')].filter(x => x.getBoundingClientRect().width > 0 && x.getAttribute('aria-label') === 'Weirdness')[0];
    let clipped = true;
    if (s) { let p = s, minH = 1e9; while (p && p !== document.body) { const cs = getComputedStyle(p); if (cs.overflow === 'hidden' || cs.overflowY === 'hidden') minH = Math.min(minH, p.getBoundingClientRect().height); p = p.parentElement; } clipped = minH < 20; }
    return { found: true, expanded: e.getAttribute('aria-expanded'), clipped };
  });
  let s0 = await st();
  if (!s0.found) throw new Error("More Options header not found");
  if (s0.expanded !== "true") {
    await page.click('[data-wavvy-more="1"]', { label: "Expand More Options" });
    await page.waitForTimeout(700);
  }
  const s1 = await st();
  return { before: s0, after: s1 };
}
