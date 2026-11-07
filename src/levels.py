W, H = 10, 7
LAGER = (0, 3)


def karte(**arten):
    """Baut eine Karte: karte(T=[(4, 3)], S=[...])."""
    rows = [["."] * W for _ in range(H)]
    rows[LAGER[1]][LAGER[0]] = "L"
    for ch, felder in arten.items():
        for x, y in felder:
            rows[y][x] = ch
    return ["".join(r) for r in rows]


FOR = {"pattern": r"\bfor\b", "label": "Benutze eine for-Schleife"}
VAR = {"pattern": r"^\s*\w+\s*=\s*\d+", "label": "Benutze eine Variable (z.B. abstand = 3)"}
DEF = {"pattern": r"\bdef\s+\w+\s*\(", "label": "Schreibe eine eigene Funktion mit def"}
IF = {"pattern": r"\bif\b", "label": "Benutze if"}
WHILE = {"pattern": r"\bwhile\b", "label": "Benutze eine while-Schleife"}
LISTE = {"pattern": r"\bfinde\b", "label": "Benutze finde(...)"}
DICT = {"pattern": r"\{", "label": "Benutze ein Dictionary"}

# id, Name, Icon, Preis, Text, nötig für Level (0-basiert) oder None
SHOP = [
    {"id": "saegewerk", "name": "Sägewerk", "icon": "🪚", "preis": {"holz": 12}, "level": 4,
     "text": "Gebäude, du wählst den Platz. Schaltet verarbeite() frei (Holz zu Brett), dazu zum_werk() und zum_lager()."},
    {"id": "spitzhacke", "name": "Spitzhacke", "icon": "⛏️", "preis": {"holz": 10, "brett": 3}, "level": 5,
     "text": "Schaltet abbauen() und was_ist_hier() frei. Jetzt gibt es Stein."},
    {"id": "karte", "name": "Karte", "icon": "🗺️", "preis": {"holz": 6, "stein": 5}, "level": 6,
     "text": "Schaltet finde() und gehe_zu() frei."},
    {"id": "ofen", "name": "Schmelzofen", "icon": "🔥", "preis": {"holz": 8, "stein": 3}, "level": 7,
     "text": "Gebäude, du wählst den Platz. verarbeite() macht dort aus Eisen Stahl."},
    {"id": "sieb", "name": "Goldsieb", "icon": "🥘", "preis": {"stahl": 3, "stein": 3}, "level": 8,
     "text": "Damit kann abbauen() auch Gold fördern."},
    {"id": "bohrer", "name": "Diamantbohrer", "icon": "💠", "preis": {"gold": 4, "stahl": 4}, "level": 10,
     "text": "Damit kann abbauen() auch Diamanten fördern."},
    {"id": "rucksack", "name": "Rucksack", "icon": "🎒", "preis": {"holz": 6}, "level": None,
     "text": "Dein Mitarbeiter trägt 1 Stück mehr."},
    {"id": "stiefel", "name": "Schnelle Stiefel", "icon": "🥾", "preis": {"holz": 5}, "level": None,
     "text": "Dein Mitarbeiter läuft sichtbar schneller."},
    {"id": "holzhuette", "name": "Holzfäller-Hütte", "icon": "🛖", "preis": {"holz": 10, "brett": 2}, "level": None,
     "text": "Gebäude, du wählst den Platz. Bringt bei jedem neuen Auftrag 2 Holz extra."},
    {"id": "steinhuette", "name": "Steinbruch-Hütte", "icon": "🏚️", "preis": {"stein": 8}, "level": None,
     "text": "Gebäude, du wählst den Platz. Bringt bei jedem neuen Auftrag 2 Stein extra."},
    {"id": "lagerausbau", "name": "Lager-Ausbau", "icon": "🏰", "preis": {"brett": 5, "stein": 5}, "level": None,
     "text": "Dein Lager wird größer und bekommt eine Flagge. Reine Angeberei."},
]

LEVELS = [
    {
        "title": "Der erste Baum",
        "task": "Geh zum Baum, hacke ihn und bring das Holz ins Lager.",
        "lesson": "Das ist dein Mitarbeiter. Er macht genau das, was im Code steht, Zeile für Zeile. Jeder Befehl ist eine <b>Funktion</b>, die du mit Klammern aufrufst:"
                  "<pre>rechts()     # ein Feld nach rechts\nhacke()      # den Baum hier fällen\nabliefern()  # im Lager abgeben</pre>"
                  "Mit <code>links()</code> kommt er zurück. Für jeden Auftrag bekommst du Rohstoffe, die du im Shop ausgeben kannst.",
        "tip": "Viermal rechts(), einmal hacke(), viermal links(), einmal abliefern().",
        "grid": karte(T=[(4, 3)]),
        "tragkraft": 1, "ziel": {"holz": 1}, "belohnung": {"holz": 4}, "needs": [],
        "start": "rechts()\n",
        "solution": "rechts()\nrechts()\nrechts()\nrechts()\nhacke()\nlinks()\nlinks()\nlinks()\nlinks()\nabliefern()\n",
    },
    {
        "title": "Weit weg: Schleifen",
        "task": "Hol das Holz vom Baum oben rechts. Nutze for-Schleifen statt alles einzeln zu tippen.",
        "lesson": "Siebenmal dieselbe Zeile ist mühsam. Eine <b>for-Schleife</b> wiederholt den eingerückten Block:"
                  "<pre>for i in range(7):\n    rechts()</pre>"
                  "Vergiss den Doppelpunkt und die Einrückung nicht. Neu sind auch <code>hoch()</code> und <code>runter()</code>.",
        "tip": "Der Baum steht 7 nach rechts und 2 nach oben. Danach denselben Weg zurück.",
        "grid": karte(T=[(7, 1)]),
        "tragkraft": 1, "ziel": {"holz": 1}, "belohnung": {"holz": 5}, "needs": [FOR],
        "start": "for i in range(7):\n    rechts()\n",
        "solution": "for i in range(7):\n    rechts()\nhoch()\nhoch()\nhacke()\nrunter()\nrunter()\nfor i in range(7):\n    links()\nabliefern()\n",
    },
    {
        "title": "Variablen und Rechnen",
        "task": "Zwei Bäume, immer 3 Felder Abstand. Speichere den Abstand in einer Variable, hacke beide und rechne den Rückweg aus.",
        "lesson": "Eine <b>Variable</b> ist ein Name für einen Wert, und du kannst mit ihr rechnen:"
                  "<pre>abstand = 3\nprint(abstand * 2)   # zeigt 6 im Terminal</pre>"
                  "Auch in <code>range(...)</code> darf eine Rechnung stehen. Ändert sich der Abstand, änderst du nur eine Zeile.",
        "tip": "Hinweg zweimal range(abstand), Rückweg einmal range(abstand * 2).",
        "grid": karte(T=[(3, 3), (6, 3)]),
        "tragkraft": 2, "ziel": {"holz": 2}, "belohnung": {"holz": 6}, "needs": [VAR],
        "next": "Du hast genug verdient: Schau in den Shop und kauf bald dein erstes Gebäude!",
        "start": "abstand = 3\n",
        "solution": "abstand = 3\nfor i in range(abstand):\n    rechts()\nhacke()\nfor i in range(abstand):\n    rechts()\nhacke()\nfor i in range(abstand * 2):\n    links()\nabliefern()\n",
    },
    {
        "title": "Mehrere Zeilen pro Runde",
        "task": "Vier Bäume stehen auf x = 2, 4, 6 und 8. Hacke alle und bring das Holz ins Lager.",
        "lesson": "Im Schleifenblock dürfen <b>mehrere Zeilen</b> stehen, sie laufen in jeder Runde nacheinander:"
                  "<pre>for i in range(3):\n    print(\"Runde\", i)\n    print(\"fertig\")</pre>"
                  "Überlege dir: Was wiederholt sich von Baum zu Baum genau?",
        "tip": "Eine Runde besteht aus zweimal rechts() und einmal hacke().",
        "grid": karte(T=[(2, 3), (4, 3), (6, 3), (8, 3)]),
        "tragkraft": 4, "ziel": {"holz": 4}, "belohnung": {"holz": 8}, "needs": [FOR],
        "next": "Für das nächste Level brauchst du das Sägewerk aus dem Shop.",
        "start": "",
        "solution": "for i in range(4):\n    rechts()\n    rechts()\n    hacke()\nfor i in range(8):\n    links()\nabliefern()\n",
    },
    {
        "title": "Sägewerk und Funktionen",
        "task": "Liefere 3 Bretter. Pro Runde: zum Baum, hacken, im Sägewerk verarbeiten, im Lager abliefern. Er trägt nur 1 Stamm, also schreib eine Funktion für eine Runde.",
        "lesson": "Dein Sägewerk steht dort, wo du es gebaut hast. <code>zum_werk(\"saegewerk\")</code> läuft hin, <code>verarbeite()</code> macht aus Holz Bretter und <code>zum_lager()</code> läuft zurück. Weil sich der Ablauf wiederholt, gibst du ihm mit <code>def</code> einen Namen. <code>weg</code> ist ein <b>Parameter</b>:"
                  "<pre>def runde(weg):\n    print(\"Der Weg ist\", weg)\n\nrunde(3)\nrunde(5)</pre>",
        "tip": "Die Bäume stehen 3, 5 und 7 Felder rechts vom Lager. In die Funktion gehören: hinlaufen, hacke(), zurücklaufen, zum_werk(\"saegewerk\"), verarbeite(), zum_lager(), abliefern().",
        "grid": karte(T=[(3, 3), (5, 3), (7, 3)]),
        "tragkraft": 1, "ziel": {"brett": 3}, "belohnung": {"holz": 6, "brett": 4}, "needs": [DEF],
        "braucht": ["saegewerk"],
        "next": "Mit der Spitzhacke aus dem Shop kommst du an Stein!",
        "start": "def runde(weg):\n    for i in range(weg):\n        rechts()\n",
        "solution": "def runde(weg):\n    for i in range(weg):\n        rechts()\n    hacke()\n    for i in range(weg):\n        links()\n    zum_werk(\"saegewerk\")\n    verarbeite()\n    zum_lager()\n    abliefern()\n\nrunde(3)\nrunde(5)\nrunde(7)\n",
    },
    {
        "title": "Stein: Entscheidungen mit if",
        "task": "Bäume und Steine wechseln sich auf den 6 Feldern ab x = 2 ab. Lauf alles ab, nimm überall das richtige Werkzeug und liefere ab.",
        "lesson": "Steine baust du mit <code>abbauen()</code> ab. <code>was_ist_hier()</code> verrät dir, worauf du stehst, und mit <b>if</b> entscheidet dein Code:"
                  "<pre>if was_ist_hier() == \"baum\":\n    print(\"Axt\")\nelse:\n    print(\"Spitzhacke\")</pre>"
                  "Achtung: Vergleichen schreibt man mit <b>zwei</b> Gleichheitszeichen.",
        "tip": "Erst ein Schritt nach rechts, dann die Schleife über 6 Felder. Der Rückweg ist 7 Felder lang.",
        "grid": karte(T=[(2, 3), (4, 3), (6, 3)], S=[(3, 3), (5, 3), (7, 3)]),
        "tragkraft": 6, "ziel": {"holz": 3, "stein": 3}, "belohnung": {"holz": 3, "stein": 8}, "needs": [IF],
        "braucht": ["spitzhacke"],
        "next": "Die Karte aus dem Shop zeigt dir den ganzen Wald.",
        "start": "rechts()\n",
        "solution": "rechts()\nfor i in range(6):\n    rechts()\n    if was_ist_hier() == \"baum\":\n        hacke()\n    else:\n        abbauen()\nfor i in range(7):\n    links()\nabliefern()\n",
    },
    {
        "title": "Listen: Der Wald ist groß",
        "task": "Hacke alle 6 Bäume. Er trägt höchstens 3 Stämme, also muss er zwischendurch ins Lager. Zähle in einer Variable mit, wie viel er trägt.",
        "lesson": "<code>finde(\"baum\")</code> gibt dir eine <b>Liste</b> aller Positionen als Paare (x, y). <code>gehe_zu(x, y)</code> läuft hin, <code>zum_lager()</code> zurück:"
                  "<pre>for x, y in finde(\"baum\"):\n    gehe_zu(x, y)\n    print(x, y)</pre>"
                  "Mitzählen geht mit <code>anzahl += 1</code>, zurücksetzen mit <code>anzahl = 0</code>.",
        "tip": "Vor der Schleife anzahl = 0. Nach jedem hacke() anzahl += 1. Wenn anzahl == 3: zum Lager, abliefern, wieder auf 0 setzen.",
        "grid": karte(T=[(3, 1), (6, 0), (8, 2), (4, 4), (7, 5), (2, 6)]),
        "tragkraft": 3, "ziel": {"holz": 6}, "belohnung": {"holz": 8}, "needs": [LISTE, IF],
        "braucht": ["karte"],
        "next": "Im Berg wartet Eisen. Dafür brauchst du den Schmelzofen.",
        "start": "anzahl = 0\nfor x, y in finde(\"baum\"):\n    gehe_zu(x, y)\n",
        "solution": "anzahl = 0\nfor x, y in finde(\"baum\"):\n    gehe_zu(x, y)\n    hacke()\n    anzahl += 1\n    if anzahl == 3:\n        zum_lager()\n        abliefern()\n        anzahl = 0\n",
    },
    {
        "title": "Stahl: while-Schleifen",
        "task": "Leere die Eisenader auf (7, 2), schmelze alles in deinem Ofen zu Stahl und liefere es ab.",
        "lesson": "Bei <code>for</code> weißt du vorher, wie oft es läuft. Eine <b>while-Schleife</b> läuft, solange die Bedingung stimmt:"
                  "<pre>while was_ist_hier() == \"eisen\":\n    print(\"noch Eisen da\")\n    break  # sonst hört das hier nie auf</pre>"
                  "Baust du in der Schleife ab, wird die Ader leer und die Schleife endet von selbst, ganz ohne <code>break</code>.",
        "tip": "gehe_zu, die while-Schleife mit abbauen(), zum_werk(\"ofen\"), verarbeite(), zum_lager(), abliefern().",
        "grid": karte(I=[(7, 2)]),
        "tragkraft": 4, "mengen": {"I": 4}, "ziel": {"stahl": 4}, "belohnung": {"stahl": 5, "stein": 4}, "needs": [WHILE],
        "braucht": ["ofen", "spitzhacke", "karte"],
        "next": "Jetzt wird es wertvoll: Mit dem Goldsieb kannst du Gold fördern!",
        "start": "gehe_zu(7, 2)\n",
        "solution": "gehe_zu(7, 2)\nwhile was_ist_hier() == \"eisen\":\n    abbauen()\nzum_werk(\"ofen\")\nverarbeite()\nzum_lager()\nabliefern()\n",
    },
    {
        "title": "Gold: Alles zusammen",
        "task": "Drei Goldadern, in jeder stecken 2 Nuggets. Er trägt höchstens 3. Schreibe eine Funktion, die eine Ader leert und das Gold abliefert.",
        "lesson": "Jetzt kombinierst du alles: Eine <b>Funktion</b> mit zwei Parametern, darin eine <b>while-Schleife</b>, aufgerufen in einer <b>for-Schleife</b>."
                  "<pre>def leere_ader(x, y):\n    print(\"Ader bei\", x, y)\n\nfor x, y in finde(\"gold\"):\n    leere_ader(x, y)</pre>",
        "tip": "In die Funktion gehören: gehe_zu, die while-Schleife für \"gold\", zum_lager, abliefern.",
        "grid": karte(G=[(8, 0), (5, 2), (7, 6)]),
        "tragkraft": 3, "mengen": {"G": 2}, "ziel": {"gold": 6}, "belohnung": {"gold": 6, "holz": 4}, "needs": [DEF, WHILE],
        "braucht": ["sieb", "spitzhacke", "karte"],
        "start": "def leere_ader(x, y):\n    gehe_zu(x, y)\n",
        "solution": "def leere_ader(x, y):\n    gehe_zu(x, y)\n    while was_ist_hier() == \"gold\":\n        abbauen()\n    zum_lager()\n    abliefern()\n\nfor x, y in finde(\"gold\"):\n    leere_ader(x, y)\n",
    },
    {
        "title": "Produktion: Dictionaries",
        "task": "Liefere 2 Bretter und 2 Stahl. Speichere in einem Dictionary, zu welchem Werk jede Art gehört, und arbeite beide Arten in einer Schleife ab. Er trägt nur 1 Stück.",
        "lesson": "Ein <b>Dictionary</b> ordnet Schlüsseln Werte zu. Mit <code>.items()</code> bekommst du beide:"
                  "<pre>werke = {\"baum\": \"saegewerk\", \"eisen\": \"ofen\"}\nfor art, werk in werke.items():\n    print(art, werk)</pre>",
        "tip": "Zwei Schleifen ineinander: außen über werke.items(), innen über finde(art). Innen: hingehen, mit if das Werkzeug wählen, zum_werk(werk), verarbeite(), zum_lager(), abliefern().",
        "grid": karte(T=[(4, 1), (6, 2)], I=[(5, 5), (8, 4)]),
        "tragkraft": 1, "ziel": {"brett": 2, "stahl": 2}, "belohnung": {"brett": 6, "stahl": 4}, "needs": [DICT, FOR],
        "braucht": ["saegewerk", "ofen", "spitzhacke", "karte"],
        "next": "Ganz unten glitzert etwas: Kauf den Diamantbohrer!",
        "start": "werke = {\"baum\": \"saegewerk\", \"eisen\": \"ofen\"}\n",
        "solution": "werke = {\"baum\": \"saegewerk\", \"eisen\": \"ofen\"}\nfor art, werk in werke.items():\n    for x, y in finde(art):\n        gehe_zu(x, y)\n        if art == \"baum\":\n            hacke()\n        else:\n            abbauen()\n        zum_werk(werk)\n        verarbeite()\n        zum_lager()\n        abliefern()\n",
    },
    {
        "title": "Diamanten: Der Großauftrag",
        "task": "Bring von allem etwas ins Lager: Holz, Stein, Gold und den Diamanten. Schreibe eine Funktion sammle(art) und rufe sie für jede Art auf.",
        "lesson": "Eine Liste kannst du auch selbst schreiben, und Parameter dürfen auch Text sein:"
                  "<pre>for art in [\"baum\", \"stein\", \"gold\", \"diamant\"]:\n    print(art)</pre>"
                  "In <code>sammle(art)</code> gehst du alle Felder aus <code>finde(art)</code> durch. Bäume brauchen <code>hacke()</code>, alles andere <code>abbauen()</code>.",
        "tip": "for x, y in finde(art): gehe_zu, dann while was_ist_hier() == art: mit if/else das Werkzeug wählen, danach zum_lager und abliefern.",
        "grid": karte(T=[(3, 0), (2, 5)], S=[(5, 1), (6, 5)], G=[(8, 0)], D=[(9, 6)]),
        "tragkraft": 4, "mengen": {"G": 2}, "ziel": {"holz": 2, "stein": 2, "gold": 2, "diamant": 1}, "belohnung": {"diamant": 1}, "needs": [DEF, FOR],
        "braucht": ["bohrer", "sieb", "spitzhacke", "karte"],
        "start": "def sammle(art):\n    print(art)\n\nfor art in [\"baum\", \"stein\", \"gold\", \"diamant\"]:\n    sammle(art)\n",
        "solution": "def sammle(art):\n    for x, y in finde(art):\n        gehe_zu(x, y)\n        while was_ist_hier() == art:\n            if art == \"baum\":\n                hacke()\n            else:\n                abbauen()\n        zum_lager()\n        abliefern()\n\nfor art in [\"baum\", \"stein\", \"gold\", \"diamant\"]:\n    sammle(art)\n",
    },
]


# Effizienteste Lösung je Level: Aktions-Minimum (test.py prüft es mit minimum.py), dabei möglichst wenig Zeilen
BESTE = [
    ("for i in range(4):\n    rechts()\nhacke()\nfor i in range(4):\n    links()\nabliefern()\n",
     "Der Weg selbst geht nicht kürzer: 10 Aktionen sind das Minimum. Mit einer for-Schleife, die du in Level 2 lernst, schrumpft der Code aber von 10 auf 6 Zeilen."),
    ("for i in range(7):\n    rechts()\nhoch()\nhoch()\nhacke()\nrunter()\nrunter()\nfor i in range(7):\n    links()\nabliefern()\n",
     "Hin- und Rückweg sind die kürzesten Wege. Für die zwei Schritte nach oben lohnt sich keine Schleife: Sie bräuchte genauso viele Zeilen."),
    ("abstand = 3\nfor i in range(2):\n    for j in range(abstand):\n        rechts()\n    hacke()\nfor i in range(abstand * 2):\n    links()\nabliefern()\n",
     "Zweimal dasselbe Stück Weg ist eine Wiederholung. Eine Schleife in der Schleife spart deshalb zwei Zeilen, und die Zahl 3 steht weiter nur an einer Stelle."),
    ("for i in range(4):\n    rechts()\n    rechts()\n    hacke()\nfor i in range(8):\n    links()\nabliefern()\n",
     "Alle Bäume liegen auf einem Weg, und er trägt 4 Stämme. Also reicht eine einzige Tour, und der Rückweg ist einmal 8 Felder statt vieler kleiner Stücke."),
    ("def runde(weg):\n    for i in range(weg):\n        rechts()\n    hacke()\n    zum_werk(\"saegewerk\")\n    verarbeite()\n    zum_lager()\n    abliefern()\n\nfor weg in [3, 5, 7]:\n    runde(weg)\n",
     "Der Trick: Vom Baum geht er direkt zum Sägewerk statt erst zurück zum Lager. Und die Aufrufe laufen über eine Liste, das spart Zeilen, sobald es mehr Bäume werden."),
    ("for i in range(7):\n    rechts()\n    if was_ist_hier() == \"baum\":\n        hacke()\n    elif was_ist_hier() == \"stein\":\n        abbauen()\nfor i in range(7):\n    links()\nabliefern()\n",
     "Mit elif prüft der Code das leere Feld gleich mit. Deshalb fällt das einzelne rechts() vor der Schleife weg, und der Code funktioniert überall in der Reihe."),
    ("anzahl = 0\nbaeume = finde(\"baum\")\nfor x, y in sorted(baeume[:3]) + baeume[3:]:\n    gehe_zu(x, y)\n    hacke()\n    anzahl += 1\n    if anzahl == 3:\n        zum_lager()\n        abliefern()\n        anzahl = 0\n",
     "finde() sortiert von oben nach unten, das ist nicht immer der kürzeste Weg. sorted() ordnet die erste Tour von links nach rechts, damit er keinen Umweg läuft. Das kostet eine Zeile mehr, spart aber 6 Aktionen."),
    ("gehe_zu(7, 2)\nwhile was_ist_hier() == \"eisen\":\n    abbauen()\nzum_werk(\"ofen\")\nverarbeite()\nzum_lager()\nabliefern()\n",
     "Er nimmt die ganze Ader auf einmal mit und muss nur einmal laufen. Weil verarbeite() alles Eisen gleichzeitig schmilzt, gibt es hier nichts mehr zu sparen."),
    ("def leere_ader(x, y, anzahl):\n    gehe_zu(x, y)\n    while was_ist_hier() == \"gold\":\n        if anzahl == 3:\n            zum_lager()\n            abliefern()\n            anzahl = 0\n            gehe_zu(x, y)\n        abbauen()\n        anzahl += 1\n    return anzahl\n\nanzahl = 0\nfor x, y in finde(\"gold\"):\n    anzahl = leere_ader(x, y, anzahl)\nzum_lager()\nabliefern()\n",
     "Statt nach jeder Ader heimzulaufen, nutzt er die Tragkraft voll aus: 2 Touren statt 3. Die Funktion gibt mit return zurück, wie viel er trägt. Das spart 11 Aktionen, kostet aber deutlich mehr Zeilen. Effizient für den Mitarbeiter ist hier nicht dasselbe wie kurzer Code."),
    ("werke = {\"baum\": \"saegewerk\", \"eisen\": \"ofen\"}\nfor art, werk in werke.items():\n    for x, y in finde(art):\n        gehe_zu(x, y)\n        if art == \"baum\":\n            hacke()\n        else:\n            abbauen()\n        zum_werk(werk)\n        verarbeite()\n        zum_lager()\n        abliefern()\n",
     "Er trägt nur 1 Stück, also ist jede Tour fest vorgegeben, und die Aktionen sind schon das Minimum. Das Dictionary spart dir, den Ablauf für jede Art doppelt zu schreiben."),
    ("def runde(felder):\n    for x, y in felder:\n        gehe_zu(x, y)\n        art = was_ist_hier()\n        while was_ist_hier() == art:\n            if art == \"baum\":\n                hacke()\n            else:\n                abbauen()\n    zum_lager()\n    abliefern()\n\noben = finde(\"baum\")[:1] + finde(\"gold\") + finde(\"stein\")[:1]\nunten = finde(\"baum\")[1:] + finde(\"stein\")[1:] + finde(\"diamant\")\nrunde(oben)\nrunde(unten)\n",
     "Die größte Ersparnis im Spiel: Nicht nach Art sortieren, sondern nach Gegend. Eine Tour oben, eine unten, statt für jedes Feld heimzulaufen. Das halbiert die Aktionen fast, kostet aber ein paar Zeilen mehr."),
]
for lv, (code, warum) in zip(LEVELS, BESTE):
    lv["beste"] = code
    lv["warum"] = warum
