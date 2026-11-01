// requires: const ORDER defined before; lib.mjs content before
const P = payloads.find(p => p.order === ORDER);
const NN = String(ORDER).padStart(2, "0");
const marker = `${EVDIR}/track-${NN}-submit-marker.json`;
let markerExists = false;
try { await fs.access(marker); markerExists = true; } catch (e) {}
if (markerExists) throw new Error(`REFUSING: marker exists for track ${NN}; a submission may already have been made`);

const task = await taskSpace("wavvy-2300-suno-generate");
const page = task.page("p1");
const startedAt = new Date().toISOString();
const listBefore = await readList(page);
const beforeKeys = new Set(listBefore.map(r => r.href || ("noid:" + r.text)));

await clearAndFill(page, P);
const f = await readForm(page);
const c = compare(P, f);
const sel = (arr, text) => { const b = (arr || []).find(x => x.text === text); return b ? /standard-legacy/.test(b.cls) : null; };
const guards = {
  inputMatch: c.lyrics && c.style && c.exclude && c.title,
  workspaceHeader: f.header === "Workspaces | [23:00]",
  saveTo: Array.isArray(f.saveTo) && f.saveTo.some(s => s.includes("[23:00]")),
  urlWid: f.url.includes("wid=f578d3c2-f43f-462e-8e05-44d022edd480"),
  advancedMode: f.tabs.includes("Advanced=true"),
  model: f.model === "v6",
  createEnabled: f.createDisabled === false,
  genderUnset: sel(f.gender, "Male") === false && sel(f.gender, "Female") === false,
  durationAuto: sel(f.duration, "Auto") === true,
  maxModeOff: sel(f.maxMode, "Off") === true,
  personalizeOff: sel(f.personalize, "Off") === true,
  sliders: f.sliders.map(s => s.label + "=" + s.now).join(",") === "Weirdness=50,Style Influence=50,Variety=1",
};
const pre = { order: ORDER, title: P.title, source_txt: P.source_txt, source_sha256: P.sha256, startedAt, checkedAt: new Date().toISOString(), compare: c, guards, form: { ...f, lyricsLines: undefined, lyrics_joined: f.lyricsLines ? f.lyricsLines.join("\n") : null }, listBeforeCount: listBefore.length };
await page.screenshot({ path: `${EVDIR}/track-${NN}-pre-submit.png` });
await fs.writeFile(`${EVDIR}/track-${NN}-pre-submit.json`, JSON.stringify(pre, null, 1));
const allOk = Object.values(guards).every(v => v === true);
console.log(JSON.stringify({ order: ORDER, title: P.title, compare: c, guards, credits: f.credits, allOk }));
if (!allOk) { console.log("GUARD FAILED - NOT SUBMITTING"); throw new Error("guard failed; no submission made"); }

// ---- single submission ----
await fs.writeFile(marker, JSON.stringify({ order: ORDER, title: P.title, clickedAt: new Date().toISOString(), note: "Create clicked once; do not click again" }, null, 1));
const receipt = await page.click('button[aria-label="Create song"]', { label: "Submit one song generation" });
const clickedAt = new Date().toISOString();
console.log("CLICKED", JSON.stringify(receipt).slice(0, 400));

// ---- observe (no more clicks) ----
let rows = [], newRows = [], formAfter = null, polls = [];
for (let i = 0; i < 40; i++) {
  await page.waitForTimeout(3000);
  rows = await readList(page);
  newRows = rows.filter(r => !beforeKeys.has(r.href || ("noid:" + r.text)));
  polls.push({ i, t: new Date().toISOString(), rows: rows.length, newRows: newRows.length });
  if (newRows.filter(r => r.href && r.label === P.title).length >= 2) break;
}
formAfter = await readForm(page);
await page.screenshot({ path: `${EVDIR}/track-${NN}-post-submit.png` });
const post = { order: ORDER, title: P.title, clickedAt, receipt, polls, creditsAfter: formAfter.credits, formAfterSummary: { title: formAfter.title, style_len: (formAfter.style || "").length, lyricsLines: formAfter.lyricsLines && formAfter.lyricsLines.length, createDisabled: formAfter.createDisabled }, listAfterCount: rows.length, newRows, topRows: rows.slice(0, 6) };
await fs.writeFile(`${EVDIR}/track-${NN}-post-submit.json`, JSON.stringify(post, null, 1));
console.log(JSON.stringify({ creditsAfter: formAfter.credits, polls: polls.length, newRows, formAfterSummary: post.formAfterSummary }, null, 1));
const titledRows = newRows.filter(r => r.href && r.label === P.title);
const unexpectedRows = newRows.filter(r => r.href && r.label !== P.title);
const transientRows = newRows.filter(r => !r.href);
console.log(JSON.stringify({ titledIds: titledRows.map(r => r.href), unexpected: unexpectedRows.length, transientNoIdRows: transientRows.length }));
const okRows = titledRows.length === 2 && unexpectedRows.length === 0;
console.log(okRows ? `TRACK_OK ${ORDER}` : `TRACK_UNCERTAIN ${ORDER}`);
if (!okRows) throw new Error(`track ${ORDER}: new rows != 2 titled '${P.title}' with ids; STOP, do not resubmit`);
