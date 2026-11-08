import io, re, json, sys, copy, traceback, contextlib

MAX_LINES = 200000
MAX_ACTIONS = 3000
DIRS = {"rechts": (1, 0), "links": (-1, 0), "hoch": (0, -1), "runter": (0, 1)}
# Feldzeichen -> (Name auf der Karte, Ware)
TILES = {"T": ("baum", "holz"), "S": ("stein", "stein"), "I": ("eisen", "eisen"),
         "G": ("gold", "gold"), "D": ("diamant", "diamant"), "C": ("kupfer", "kupfer")}
# Gebäude: was sie verarbeiten und wo sie stehen, wenn das Level nichts anderes sagt
WERKE = {"saegewerk": {"holz": "brett"}, "ofen": {"eisen": "stahl", "kupfer": "draht"}}
STANDARD = {"saegewerk": (1, 1), "ofen": (1, 5), "montage": (0, 1)}
# Welt 2: Was die Montagehalle aus welchen Teilen baut
REZEPTE = {"werkzeug": {"brett": 1, "stahl": 1}, "kiste": {"brett": 2}, "kabel": {"draht": 2},
           "motor": {"stahl": 1, "draht": 1}, "roboter": {"motor": 1, "kabel": 1, "stahl": 1}}
# Befehl -> Kauf, der ihn freischaltet
FREI = {"abbauen": ("spitzhacke", "die Spitzhacke"), "was_ist_hier": ("spitzhacke", "die Spitzhacke"),
        "finde": ("karte", "die Karte"), "gehe_zu": ("karte", "die Karte"), "zum_lager": ("saegewerk", "das Sägewerk"),
        "zum_werk": ("saegewerk", "das Sägewerk"), "verarbeite": ("saegewerk", "das Sägewerk"),
        "im_lager": ("lagerbuch", "das Lagerbuch"), "hole": ("montage", "die Montagehalle"), "baue": ("montage", "die Montagehalle")}
# Diese Werte darf ein Level je Variante austauschen
VARIABEL = ("grid", "mengen", "lager", "rezepte", "vars", "ziel")


class Fehler(Exception):
    pass


def erklaere(msg):
    if msg.startswith("expected an indented block"):
        return "Nach einer Zeile mit Doppelpunkt muss ein eingerückter Block kommen. Rücke die Zeile darunter mit Tab ein."
    if msg == "unexpected indent":
        return "Diese Zeile ist zu weit eingerückt: Darüber steht kein Doppelpunkt, der einen neuen Block öffnet. Shift+Tab nimmt die Einrückung zurück."
    if msg.startswith("unindent does not match"):
        return "Diese Zeile steht nicht genau unter einem Block darüber. Setze sie mit Tab oder Shift+Tab auf die gleiche Höhe."
    if msg == "expected ':'":
        return "Am Ende dieser Zeile fehlt der Doppelpunkt :"
    return msg


def run(code, level_json):
    level = json.loads(level_json)
    r = _run(code, level)
    tests = level.get("varianten")
    if tests and "events" in r:
        hinweis = None
        if r["error"] is None and r["reached"]:
            for v in tests:
                t = _run(code, dict(level, **{k: v[k] for k in VARIABEL if k in v}))
                if t["error"] is not None or not t["reached"]:
                    grund = ("Fehler: " + t["error"]["msg"]) if t["error"] else "Am Ende sind %s." % t["fehlt"]
                    hinweis = "Der Auftrag auf der Karte klappt. Dein Code muss aber auch bei anderen Aufträgen funktionieren.\nTest „%s“: %s" % (v["text"], grund)
                    break
            ok = hinweis is None
        else:
            ok = False
        r["checks"].append({"label": "Klappt auch bei anderen Aufträgen (%d Tests)" % len(tests), "ok": ok})
        r["won"] = r["won"] and ok
        r["hinweis"] = hinweis
    r.pop("fehlt", None)
    return json.dumps(r)


def _run(code, level):
    rows = level["grid"]
    H, W = len(rows), len(rows[0])
    capacity = level["tragkraft"]
    owned = set(level.get("owned", []))
    mengen = level.get("mengen", {})
    plaetze = dict(STANDARD, **level.get("plots", {}))
    werke = {tuple(plaetze[w]): w for w in list(WERKE) + ["montage"] if w in owned}
    rezepte = level.get("rezepte", REZEPTE)
    left = {}
    lager = None
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == "L":
                lager = (x, y)
            elif ch in TILES:
                left[(x, y)] = mengen.get(ch, 1)

    pos = list(lager)
    carry = []
    stock = dict(level.get("lager", {}))
    events = []

    def add(ev):
        if len(events) >= MAX_ACTIONS:
            raise Fehler("Dein Mitarbeiter ist erschöpft: viel zu viele Aktionen. Steckt eine Endlosschleife drin?")
        events.append(ev)

    def step(name):
        dx, dy = DIRS[name]
        nx, ny = pos[0] + dx, pos[1] + dy
        if not (0 <= nx < W and 0 <= ny < H):
            raise Fehler("Mit %s() würde dein Mitarbeiter die Karte verlassen. Er steht auf (%d, %d)." % (name, pos[0], pos[1]))
        add(["walk", nx, ny])
        pos[0], pos[1] = nx, ny

    def make_step(name):
        def f():
            step(name)
        f.__name__ = name
        return f

    def here():
        p = (pos[0], pos[1])
        if p == lager:
            return "lager"
        if left.get(p, 0) > 0:
            return TILES[rows[p[1]][p[0]]][0]
        return werke.get(p)

    def take(verb):
        p = (pos[0], pos[1])
        if len(carry) >= capacity:
            raise Fehler("Die Hände sind voll, mehr als %d kann dein Mitarbeiter nicht tragen. Bring erst alles mit abliefern() ins Lager." % capacity)
        ware = TILES[rows[p[1]][p[0]]][1]
        left[p] -= 1
        carry.append(ware)
        add([verb, p[0], p[1], ware, left[p]])

    def hacke():
        name = here()
        if name == "baum":
            take("hack")
        elif name in ("stein", "eisen", "gold", "diamant", "kupfer"):
            raise Fehler("Hier ist %s, kein Baum. Dafür brauchst du abbauen()." % name)
        else:
            raise Fehler("Hier steht kein Baum. Dein Mitarbeiter steht auf (%d, %d)." % (pos[0], pos[1]))

    def abbauen():
        name = here()
        if name == "baum":
            raise Fehler("Das ist ein Baum, den fällst du mit hacke().")
        if name == "gold" and "sieb" not in owned:
            raise Fehler("Für Gold brauchst du das Goldsieb. Kauf es im Shop.")
        if name == "diamant" and "bohrer" not in owned:
            raise Fehler("Für Diamanten brauchst du den Diamantbohrer. Kauf ihn im Shop.")
        if name == "kupfer" and "tiegel" not in owned:
            raise Fehler("Für Kupfer brauchst du den Kupfertiegel. Kauf ihn im Shop.")
        if name in ("stein", "eisen", "gold", "diamant", "kupfer"):
            take("mine")
        else:
            raise Fehler("Hier gibt es nichts abzubauen. Dein Mitarbeiter steht auf (%d, %d)." % (pos[0], pos[1]))

    def verarbeite():
        p = (pos[0], pos[1])
        if p not in werke:
            raise Fehler("Hier steht kein Werk. Mit zum_werk(\"saegewerk\") oder zum_werk(\"ofen\") kommst du hin. Dein Mitarbeiter steht auf (%d, %d)." % p)
        if werke[p] == "montage":
            raise Fehler("In der Montagehalle wird nicht verarbeitet, sondern gebaut: baue(\"werkzeug\") zum Beispiel.")
        plan = WERKE[werke[p]]
        if not any(w in plan for w in carry):
            raise Fehler("Dein Mitarbeiter trägt nichts, was hier verarbeitet werden kann. Dieses Werk braucht %s." % " oder ".join(plan))
        carry[:] = [plan.get(w, w) for w in carry]
        add(["process", p[0], p[1], list(carry)])

    def abliefern():
        if here() != "lager":
            raise Fehler("Abliefern geht nur im Lager. Dein Mitarbeiter steht auf (%d, %d)." % (pos[0], pos[1]))
        for w in carry:
            stock[w] = stock.get(w, 0) + 1
        add(["deliver", list(carry)])
        del carry[:]

    def was_ist_hier():
        return here()

    def im_lager(ware):
        return stock.get(ware, 0)

    def hole(ware):
        if here() != "lager":
            raise Fehler("hole() geht nur im Lager. Dein Mitarbeiter steht auf (%d, %d)." % (pos[0], pos[1]))
        if stock.get(ware, 0) <= 0:
            raise Fehler("Im Lager liegt nichts mehr von \"%s\". Mit im_lager(\"%s\") kannst du vorher nachsehen." % (ware, ware))
        if len(carry) >= capacity:
            raise Fehler("Die Hände sind voll, mehr als %d kann dein Mitarbeiter nicht tragen." % capacity)
        stock[ware] -= 1
        carry.append(ware)
        add(["take", ware])

    def baue(produkt):
        p = (pos[0], pos[1])
        if werke.get(p) != "montage":
            raise Fehler("baue() geht nur in der Montagehalle. Mit zum_werk(\"montage\") kommst du hin. Dein Mitarbeiter steht auf (%d, %d)." % p)
        if produkt not in rezepte:
            raise Fehler("Für %r gibt es kein Rezept. Bekannt sind: %s" % (produkt, ", ".join('"%s"' % n for n in rezepte)))
        rest, fehlt = list(carry), []
        for ware, menge in rezepte[produkt].items():
            for i in range(menge):
                if ware in rest:
                    rest.remove(ware)
                else:
                    fehlt.append(ware)
        if fehlt:
            raise Fehler("Für %s fehlt noch: %s. Dein Mitarbeiter trägt: %s" % (produkt, ", ".join(fehlt), ", ".join(carry) or "nichts"))
        carry[:] = rest + [produkt]
        add(["build", p[0], p[1], list(carry), produkt])

    def finde(art):
        names = [v[0] for v in TILES.values()]
        if art not in names:
            raise Fehler("finde kennt nur: %s" % ", ".join('"%s"' % n for n in names))
        return [(x, y) for y in range(H) for x in range(W)
                if rows[y][x] in TILES and TILES[rows[y][x]][0] == art and left[(x, y)] > 0]

    def gehe_zu(x, y):
        if not (isinstance(x, int) and isinstance(y, int) and 0 <= x < W and 0 <= y < H):
            raise Fehler("gehe_zu braucht eine Position auf der Karte (x: 0 bis %d, y: 0 bis %d)." % (W - 1, H - 1))
        while pos[0] != x:
            step("rechts" if pos[0] < x else "links")
        while pos[1] != y:
            step("runter" if pos[1] < y else "hoch")

    def zum_lager():
        gehe_zu(lager[0], lager[1])

    def zum_werk(name):
        if name not in ("saegewerk", "ofen", "montage"):
            raise Fehler('zum_werk kennt nur: "saegewerk", "ofen", "montage"')
        if name not in owned:
            raise Fehler("Du hast noch kein Gebäude %s. Kauf es im Shop." % name)
        gehe_zu(*plaetze[name])

    commands = {"zum_werk": zum_werk, "hacke": hacke, "abliefern": abliefern, "abbauen": abbauen, "was_ist_hier": was_ist_hier,
                "finde": finde, "gehe_zu": gehe_zu, "zum_lager": zum_lager, "verarbeite": verarbeite,
                "im_lager": im_lager, "hole": hole, "baue": baue}
    for d in DIRS:
        commands[d] = make_step(d)

    def locked(name, item):
        def f(*a, **k):
            raise Fehler("%s() ist noch gesperrt. Kauf erst %s im Shop." % (name, item))
        return f

    env = {"__name__": "__firma__", "rezepte": copy.deepcopy(rezepte)}
    env.update(copy.deepcopy(level.get("vars", {})))
    for name, fn in commands.items():
        if name in FREI and FREI[name][0] not in owned:
            if FREI[name][0] == "saegewerk" and ("ofen" in owned or "montage" in owned):
                env[name] = fn
            else:
                env[name] = locked(name, FREI[name][1])
        else:
            env[name] = fn

    count = [0]

    def tracer(frame, event, arg):
        if frame.f_code.co_filename != "<firma>":
            return None

        def local(frame, event, arg):
            if event == "line":
                count[0] += 1
                if count[0] > MAX_LINES:
                    raise Fehler("Dein Code läuft viel zu lange. Steckt eine Endlosschleife drin?")
            return local
        return local

    out = io.StringIO()
    error = None
    try:
        compiled = compile(code, "<firma>", "exec")
    except SyntaxError as e:
        return {"error": {"kind": "syntax", "line": e.lineno, "msg": "%s: %s" % (type(e).__name__, erklaere(e.msg))},
                "output": "", "won": False}

    sys.settrace(tracer)
    try:
        with contextlib.redirect_stdout(out):
            exec(compiled, env)
    except BaseException as e:
        line = None
        for fr in traceback.extract_tb(e.__traceback__):
            if fr.filename == "<firma>":
                line = fr.lineno
        msg = str(e) if isinstance(e, Fehler) else "%s: %s" % (type(e).__name__, e)
        hints = {"NameError": "Ein Name ist unbekannt: Tippfehler, oder die Variable ist noch nicht definiert?",
                 "TypeError": "Ein Befehl hat falsche oder fehlende Argumente bekommen."}
        if type(e).__name__ in hints:
            msg += "\n" + hints[type(e).__name__]
        error = {"kind": "runtime", "line": line, "msg": msg}
    finally:
        sys.settrace(None)

    plain = re.sub(r"#.*", "", code)
    output = out.getvalue()[:2000]
    checks = []
    for n in level.get("needs", []):
        checks.append({"label": n["label"], "ok": bool(re.search(n["pattern"], plain, re.M))})
    exakt = level.get("exakt")
    reached = all(stock.get(k, 0) == v if exakt else stock.get(k, 0) >= v for k, v in level["ziel"].items())
    fehlt = ", ".join("%d %s im Lager statt %s%d" % (stock.get(k, 0), k, "genau " if exakt else "", v)
                      for k, v in level["ziel"].items() if stock.get(k, 0) != v and (exakt or stock.get(k, 0) < v))
    zuviel = [k for k, v in level["ziel"].items() if exakt and stock.get(k, 0) > v]
    won = reached and error is None and all(c["ok"] for c in checks)
    return {"error": error, "output": output, "checks": checks, "won": won, "reached": reached, "zuviel": zuviel,
            "events": events, "start": list(lager), "carried": len(carry), "fehlt": fehlt}
