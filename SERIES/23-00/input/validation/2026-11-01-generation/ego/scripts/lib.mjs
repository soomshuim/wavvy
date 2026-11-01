const fs = await import("node:fs/promises");
const EVDIR = "/Users/zenkim_office/Project/wavvy/SERIES/23-00/input/validation/2026-11-01-generation";
const WS_URL = "https://suno.com/create?wid=f578d3c2-f43f-462e-8e05-44d022edd480";
const payloads = JSON.parse(await fs.readFile(EVDIR + "/payloads.json", "utf8"));
const norm = (s) => s.replace(/\r\n?/g, "\n").trim();

async function readForm(page) {
  return await page.evaluate(() => {
    const q = (s) => document.querySelector(s);
    const ed = q('div[role=textbox][aria-label="Lyrics editor"]');
    const lyricsLines = ed ? [...ed.querySelectorAll(':scope > p')].map(p => p.textContent) : null;
    const style = q('textarea[placeholder^="plaintive"]');
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

async function clearAndFill(page, P) {
  await page.click('div[role=textbox][aria-label="Lyrics editor"]', { label: "Focus lyrics editor" });
  await page.keyboard.press("ControlOrMeta+a");
  await page.keyboard.press("Delete");
  await page.keyboard.paste({ text: P.lyrics });
  await page.waitForTimeout(600);
  await page.fill('textarea[placeholder^="plaintive"]', "");
  await page.fill('textarea[placeholder^="plaintive"]', P.style);
  await page.fill('input[placeholder="Exclude styles"]', "");
  if (P.exclude) await page.fill('input[placeholder="Exclude styles"]', P.exclude);
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
        seen.set(id, { label: g.getAttribute('aria-label'), href: id, y, text: g.innerText.replace(/\n/g, ' | ').slice(0, 400) });
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
