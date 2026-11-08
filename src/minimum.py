"""Breitensuche: kleinstmögliche Zahl an Aktionen pro Level, ohne Tragkraft-Upgrade."""
import json, sys
from collections import deque
sys.path.insert(0, ".")
from levels import LEVELS, SHOP
from runner import run, TILES, WERKE, STANDARD

ALLE = [s["id"] for s in SHOP]


def minimum(lv, plaetze=STANDARD):
    rows = lv["grid"]
    H, W = len(rows), len(rows[0])
    felder, lager = [], None
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c == "L":
                lager = (x, y)
            elif c in TILES:
                felder.append((x, y, TILES[c][1], lv.get("mengen", {}).get(c, 1)))
    index = {(f[0], f[1]): i for i, f in enumerate(felder)}
    werke = {tuple(p): WERKE[w] for w, p in plaetze.items() if w in WERKE}
    ziel = lv["ziel"]
    start = (lager, tuple(f[3] for f in felder), (), ())
    seen = {start}
    q = deque([(start, 0)])
    while q:
        (pos, left, carry, stock), d = q.popleft()
        lager_voll = dict(stock)
        if all(lager_voll.get(k, 0) >= v for k, v in ziel.items()):
            return d
        nxt = []
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (pos[0] + dx, pos[1] + dy)
            if 0 <= n[0] < W and 0 <= n[1] < H:
                nxt.append((n, left, carry, stock))
        i = index.get(pos)
        if i is not None and left[i] > 0 and len(carry) < lv["tragkraft"]:
            l = list(left); l[i] -= 1
            nxt.append((pos, tuple(l), tuple(sorted(carry + (felder[i][2],))), stock))
        if pos in werke and any(w in werke[pos] for w in carry):
            nxt.append((pos, left, tuple(sorted(werke[pos].get(w, w) for w in carry)), stock))
        if pos == lager and carry:
            s = dict(stock)
            for w in carry:
                s[w] = s.get(w, 0) + 1
            nxt.append((pos, left, (), tuple(sorted(s.items()))))
        for st in nxt:
            if st not in seen:
                seen.add(st)
                q.append((st, d + 1))
    return None


if __name__ == "__main__":
    for i, lv in enumerate(LEVELS):
        r = json.loads(run(lv["solution"], json.dumps(dict(lv, owned=ALLE))))
        z = len([l for l in lv["solution"].splitlines() if l.strip()])
        print(i + 1, lv["title"], "| minimum", minimum(lv), "| Musterlösung", len(r["events"]), "Aktionen,", z, "Zeilen")
