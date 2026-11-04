import json, pathlib, sys
base = pathlib.Path(sys.argv[1])
def load(label, s, kind):
    p = base / label / f"{s}.{kind}.json"
    try: return json.loads(p.read_text())
    except Exception: return {}
rows = []
series = sorted({p.name[:-len('.gate.json')] for p in (base/'before').glob('*.gate.json')})
flips = 0
print("| series | gate before | gate after | state-check before | state-check after | audio_source after | changed? |")
print("|---|---|---|---|---|---|---|")
for s in series:
    gb, ga = load('before', s, 'gate'), load('after', s, 'gate')
    sb, sa = load('before', s, 'state'), load('after', s, 'state')
    r = lambda d: d.get('result', '?')
    src_after = sa.get('state', {}).get('artifact_status', {}).get('audio_source')
    changed = (r(gb), r(sb)) != (r(ga), r(sa)) or gb.get('blockers') != ga.get('blockers') or sb.get('blockers') != sa.get('blockers')
    bad = (r(gb) == 'PASS' and r(ga) != 'PASS') or (r(sb) == 'PASS' and r(sa) != 'PASS')
    if bad: flips += 1
    print(f"| {s} | {r(gb)} | {r(ga)} | {r(sb)} | {r(sa)} | {src_after} | {'CHANGED' if changed else 'same'}{' **PASS->FAIL**' if bad else ''} |")
print(f"\nPASS->FAIL flips: {flips}")
