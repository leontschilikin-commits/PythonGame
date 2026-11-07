import json, sys
sys.path.insert(0, ".")
from runner import run
from levels import LEVELS, SHOP
from minimum import minimum

ALLE = [s["id"] for s in SHOP]
bad = 0


def go(i, code, owned=None):
    lv = dict(LEVELS[i], owned=ALLE if owned is None else owned)
    return json.loads(run(code, json.dumps(lv)))


print("--- Lösungen, nur mit den für das Level nötigen Käufen")
for i, lv in enumerate(LEVELS):
    nur_noetig = [s["id"] for s in SHOP if s["level"] is not None and s["level"] <= i]
    r = go(i, lv["solution"], nur_noetig)
    s = go(i, lv["start"], nur_noetig)
    print(i + 1, lv["title"], "won=", r["won"], "aktionen=", len(r["events"]), "err=", r["error"], "| start won=", s["won"], s["error"])
    bad += (not r["won"]) + bool(s["won"]) + (1 if s["error"] and s["error"]["kind"] == "syntax" and i not in () else 0)

print("--- Gesperrt ohne Kauf: jedes Level mit braucht muss ohne Kauf scheitern")
for i, lv in enumerate(LEVELS):
    for fehlt in lv.get("braucht", []):
        owned = [x for x in ALLE if x != fehlt]
        r = go(i, lv["solution"], owned)
        ok = not r["won"]
        print(i + 1, "ohne", fehlt, "->", "gesperrt" if ok else "GEWINNT TROTZDEM", "|", (r["error"] or {}).get("msg"))
        bad += not ok

print("--- Wirtschaft: nur Pflichtkäufe, Reihenfolge wie im Spiel, nie negativ")
bank = {}
kaeufe = {s["level"]: s for s in SHOP if s["level"] is not None}
for i, lv in enumerate(LEVELS):
    if i in kaeufe:
        s = kaeufe[i]
        for k, v in s["preis"].items():
            if bank.get(k, 0) < v:
                print("ZU TEUER", s["name"], "vor Level", i + 1, bank)
                bad += 1
            bank[k] = bank.get(k, 0) - v
    for k, v in lv["belohnung"].items():
        bank[k] = bank.get(k, 0) + v
    print("nach Level", i + 1, bank)
print("Pflicht-Level:", sorted(s["level"] + 1 for s in kaeufe.values()), "alle braucht vorhanden:",
      all(set(lv.get("braucht", [])) <= {s["id"] for s in SHOP} for lv in LEVELS))

print("--- Freier Bauplatz: jede Lösung gewinnt, auch wenn Werke auf Rohstoffen oder in Ecken stehen")
faelle = [("Ecken", {"saegewerk": [9, 0], "ofen": [0, 6]}), ("rechts", {"saegewerk": [9, 6], "ofen": [9, 5]})]
for i, lv in enumerate(LEVELS):
    f = [(x, y) for y, r in enumerate(lv["grid"]) for x, c in enumerate(r) if c in "TSIGD"]
    if len(f) > 1:
        faelle.append(("auf Rohstoff L%d" % (i + 1), {"saegewerk": list(f[0]), "ofen": list(f[-1])}))
for name, plots in faelle:
    fehl = []
    for i, lv in enumerate(LEVELS):
        r = json.loads(run(lv["solution"], json.dumps(dict(lv, owned=ALLE, plots=plots))))
        if not r["won"]:
            fehl.append((i + 1, r["error"]))
    print(name, "ok" if not fehl else fehl)
    bad += len(fehl)

print("--- Effizienteste Lösungen: gewinnen mit Pflichtkäufen und erreichen das Aktions-Minimum, auch bei anderem Bauplan")
for i, lv in enumerate(LEVELS):
    nur_noetig = [s["id"] for s in SHOP if s["level"] is not None and s["level"] <= i]
    zeilen = len([l for l in lv["beste"].splitlines() if l.strip()])
    teile = []
    for plots in ({"saegewerk": [1, 1], "ofen": [1, 5]}, {"saegewerk": [9, 0], "ofen": [9, 6]}, {"saegewerk": [5, 3], "ofen": [5, 1]}):
        r = json.loads(run(lv["beste"], json.dumps(dict(lv, owned=nur_noetig, plots=plots))))
        m = minimum(lv, plots)
        ok = r["won"] and len(r["events"]) == m
        teile.append("%d/%d%s" % (len(r["events"]), m, "" if ok else " FEHLER %s" % r["error"]))
        bad += not ok
    print(i + 1, "Zeilen", zeilen, "(Muster", lv["par_lines"] if "par_lines" in lv else "-", ") Aktionen/Minimum:", ", ".join(teile))

print("--- Fehlerfälle")
for i, c in [(0, "hacke()"), (0, "abbauen()"), (0, "verarbeite()"), (0, "while True:\n    pass"), (4, "verarbeite()"),
             (4, "hoch()\nhoch()\nrechts()\nverarbeite()"), (7, "gehe_zu(1, 5)\nverarbeite()"), (6, "hacke()\nhacke()"),
             (4, 'zum_werk("ofen")'), (7, 'zum_werk("bla")')]:
    r = go(i, c)
    print(i + 1, repr(c[:34]), "->", (r["error"] or {}).get("msg"))
sys.exit(bad)
