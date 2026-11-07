import json, sys
sys.path.insert(0, ".")
from levels import LEVELS, SHOP
from runner import run
from book import BOOK

out = sys.argv[1]
t = open("template.html", encoding="utf-8").read()
runner = open("runner.py", encoding="utf-8").read()
assert "</script" not in runner

# Referenzwerte für die Bonus-Sterne kommen aus der Musterlösung
alle = [s["id"] for s in SHOP]
for lv in LEVELS:
    r = json.loads(run(lv["solution"], json.dumps(dict(lv, owned=alle))))
    assert r["won"], lv["title"]
    lv["par_steps"] = len(r["events"])
    lv["par_lines"] = len([l for l in lv["solution"].splitlines() if l.strip() and not l.strip().startswith("#")])

def js(x):
    return json.dumps(x, ensure_ascii=False).replace("</", "<\\/")

for k, v in (("/*LEVELS*/", js(LEVELS)), ("/*SHOP*/", js(SHOP)), ("/*BOOK*/", js(BOOK)), ("/*RUNNER*/", runner)):
    assert k in t, k
    t = t.replace(k, v)
open(out, "w", encoding="utf-8").write(t)
print("ok", len(t))
