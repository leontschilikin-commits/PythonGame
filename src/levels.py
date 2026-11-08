from runner import REZEPTE

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
ELIF = {"pattern": r"\belif\b", "label": "Benutze elif"}
ZAEHLER = {"pattern": r"\w+\s*\+=\s*1\b", "label": "Zähle mit (z.B. anzahl += 1)"}
RETURN = {"pattern": r"\breturn\b", "label": "Gib mit return ein Ergebnis zurück"}
REZEPT = {"pattern": r"rezepte\[", "label": "Lies das Rezept aus rezepte[...]"}
UNDODER = {"pattern": r"\b(and|or)\b", "label": "Verknüpfe zwei Bedingungen mit and oder or"}
APPEND = {"pattern": r"\.append\(", "label": "Hänge mit .append() an eine Liste an"}
LEN = {"pattern": r"\blen\(", "label": "Benutze len()"}
DICT_SET = {"pattern": r"\w+\[[^\]]+\]\s*\+?=(?!=)", "label": "Schreibe in ein Dictionary (z.B. bedarf[ware] = ...)"}
VERSCHACHTELT = {"pattern": r"^\s+for\b", "label": "Schreibe eine for-Schleife in eine for-Schleife"}
ZWEI_PARAM = {"pattern": r"\bdef\s+\w+\s*\(\s*\w+\s*,\s*\w+", "label": "Schreibe eine Funktion mit zwei Parametern"}

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
    {"id": "tiegel", "name": "Kupfertiegel", "icon": "🫕", "preis": {"gold": 2, "holz": 4}, "level": 11,
     "text": "Damit fördert abbauen() Kupfer, und dein Ofen macht daraus Draht."},
    {"id": "lagerbuch", "name": "Lagerbuch", "icon": "📒", "preis": {"brett": 4, "draht": 3}, "level": 13,
     "text": "Schaltet im_lager(ware) frei: Wie viel davon liegt gerade im Lager?"},
    {"id": "montage", "name": "Montagehalle", "icon": "🏭", "preis": {"stahl": 4, "draht": 3, "brett": 4}, "level": 14,
     "text": "Gebäude, du wählst den Platz. Schaltet hole(ware) und baue(produkt) frei: Aus Teilen werden Produkte."},
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
        "next": "Welt 1 ist geschafft! In Welt 2 baust du eine Fabrik. Kauf zuerst den Kupfertiegel im Shop.",
        "start": "def sammle(art):\n    print(art)\n\nfor art in [\"baum\", \"stein\", \"gold\", \"diamant\"]:\n    sammle(art)\n",
        "solution": "def sammle(art):\n    for x, y in finde(art):\n        gehe_zu(x, y)\n        while was_ist_hier() == art:\n            if art == \"baum\":\n                hacke()\n            else:\n                abbauen()\n        zum_lager()\n        abliefern()\n\nfor art in [\"baum\", \"stein\", \"gold\", \"diamant\"]:\n    sammle(art)\n",
    },
]


# ---------- Welt 2: Die Fabrik ----------
def reihe(**arten):
    """Karte mit Feldern nur in der Reihe y = 3, z.B. reihe(T=[1, 5], C=[2, 6])."""
    return karte(**{ch: [(x, 3) for x in xs] for ch, xs in arten.items()})


def rezepte_mit(**neu):
    r = {k: dict(v) for k, v in REZEPTE.items()}
    r.update(neu)
    return r


WELT2 = [
    {
        "title": "Kupfer: elif",
        "task": "Lauf die Reihe bis x = 8 ab. Hacke Bäume, baue Kupfer und Eisen ab, und lass leere Felder aus. Verarbeite alles und liefere es ab.",
        "lesson": "Willkommen in der Fabrik! Kupfer baust du mit <code>abbauen()</code> ab, und der Ofen macht daraus <b>Draht</b>. "
                  "Gibt es mehr als zwei Fälle, prüfst du mit <b>elif</b> (else if) weiter. Nur der erste passende Block läuft:"
                  "<pre>wetter = \"regen\"\nif wetter == \"sonne\":\n    print(\"Sonnenbrille\")\nelif wetter == \"regen\":\n    print(\"Schirm\")</pre>"
                  "Mit <code>else</code> statt <code>elif</code> würde er auch auf leeren Feldern abbauen wollen.",
        "tip": "Eine for-Schleife über 8 Felder: rechts(), dann if baum / elif kupfer / elif eisen. Danach Sägewerk, Ofen, Lager.",
        "grid": reihe(T=[1, 5], C=[2, 6], I=[4, 8]),
        "tragkraft": 6, "ziel": {"brett": 2, "stahl": 2, "draht": 2}, "belohnung": {"draht": 4, "stahl": 2}, "needs": [ELIF],
        "varianten": [{"text": "andere Reihenfolge in der Reihe", "grid": reihe(C=[1, 6], T=[3, 7], I=[4, 8])},
                      {"text": "noch eine Reihenfolge", "grid": reihe(I=[1, 2], T=[3, 8], C=[5, 7])}],
        "braucht": ["tiegel", "saegewerk", "ofen", "spitzhacke"],
        "start": "for i in range(8):\n    rechts()\n",
        "solution": "for i in range(8):\n    rechts()\n    if was_ist_hier() == \"baum\":\n        hacke()\n    elif was_ist_hier() == \"kupfer\":\n        abbauen()\n    elif was_ist_hier() == \"eisen\":\n        abbauen()\nzum_werk(\"saegewerk\")\nverarbeite()\nzum_werk(\"ofen\")\nverarbeite()\nzum_lager()\nabliefern()\n",
    },
    {
        "title": "Genau 5: Zählen",
        "task": "Die Fabrik bestellt genau 5 Draht, nicht mehr und nicht weniger. Wie viel Kupfer in einer Ader steckt, ist bei jedem Auftrag anders. Zähle mit.",
        "lesson": "Ein <b>Zähler</b> ist eine Variable, die bei 0 startet und mit <code>+= 1</code> wächst. Eine while-Schleife kann ihn prüfen:"
                  "<pre>anzahl = 0\nwhile anzahl < 3:\n    print(\"Runde\", anzahl)\n    anzahl += 1</pre>"
                  "<code>finde(\"kupfer\")[0]</code> ist die erste Ader, in der noch Kupfer steckt. So bekommst du ihre Position:"
                  "<pre>x, y = finde(\"kupfer\")[0]</pre>",
        "tip": "anzahl = 0, dann while anzahl < 5: erste Ader suchen, hingehen, einmal abbauen(), anzahl += 1. Danach Ofen und Lager.",
        "grid": karte(C=[(4, 1), (5, 5), (8, 6)]),
        "tragkraft": 5, "mengen": {"C": 3}, "exakt": True, "ziel": {"draht": 5}, "belohnung": {"draht": 4, "brett": 2},
        "needs": [ZAEHLER, WHILE],
        "varianten": [{"text": "in jeder Ader stecken nur 2 Kupfer", "mengen": {"C": 2}},
                      {"text": "in jeder Ader stecken 5 Kupfer", "mengen": {"C": 5}}],
        "braucht": ["tiegel", "ofen", "spitzhacke", "karte"],
        "next": "Mit dem Lagerbuch aus dem Shop siehst du, was im Lager liegt.",
        "start": "anzahl = 0\n",
        "solution": "anzahl = 0\nwhile anzahl < 5:\n    x, y = finde(\"kupfer\")[0]\n    gehe_zu(x, y)\n    abbauen()\n    anzahl += 1\nzum_werk(\"ofen\")\nverarbeite()\nzum_lager()\nabliefern()\n",
    },
    {
        "title": "Was fehlt? return",
        "task": "Im Lager sollen am Ende 6 Bretter liegen. Ein paar sind schon da, wie viele, ist bei jedem Auftrag anders. Schreibe eine Funktion, die ausrechnet, wie viele noch fehlen.",
        "lesson": "<code>im_lager(\"brett\")</code> sagt dir, wie viele Bretter im Lager liegen. Eine Funktion kann mit <b>return</b> ein Ergebnis zurückgeben, mit dem du weiterrechnest:"
                  "<pre>def doppelt(zahl):\n    return zahl * 2\n\nprint(doppelt(4) + 1)   # 9</pre>"
                  "<code>print</code> zeigt einen Wert nur an. <code>return</code> gibt ihn an die Stelle zurück, wo die Funktion aufgerufen wurde.",
        "tip": "def fehlt(ware, ziel): return ziel - im_lager(ware). Dann for i in range(fehlt(\"brett\", 6)): ersten Baum suchen, hingehen, hacken. Danach Sägewerk und Lager.",
        "grid": karte(T=[(3, 0), (7, 0), (5, 1), (8, 4), (4, 5), (6, 6)]),
        "tragkraft": 6, "lager": {"brett": 2}, "ziel": {"brett": 6}, "belohnung": {"brett": 6, "stahl": 3}, "needs": [DEF, RETURN],
        "varianten": [{"text": "5 Bretter liegen schon im Lager", "lager": {"brett": 5}},
                      {"text": "das Lager ist leer", "lager": {}},
                      {"text": "3 Bretter liegen schon im Lager", "lager": {"brett": 3}}],
        "braucht": ["lagerbuch", "saegewerk", "karte"],
        "next": "Zeit für die Montagehalle! Sie baut aus Teilen fertige Produkte.",
        "start": "print(im_lager(\"brett\"))\n",
        "solution": "def fehlt(ware, ziel):\n    return ziel - im_lager(ware)\n\nfor i in range(fehlt(\"brett\", 6)):\n    x, y = finde(\"baum\")[0]\n    gehe_zu(x, y)\n    hacke()\nzum_werk(\"saegewerk\")\nverarbeite()\nzum_lager()\nabliefern()\n",
    },
    {
        "title": "Montage: Rezepte lesen",
        "task": "Baue 2 Werkzeuge. Was in ein Werkzeug gehört, steht im Dictionary rezepte, und das ändert sich je nach Auftrag. Lies es aus, statt es abzuschreiben.",
        "lesson": "Im Lager holst du mit <code>hole(\"brett\")</code> ein Teil in die Hände. In der Montagehalle macht <code>baue(\"werkzeug\")</code> daraus ein Produkt. "
                  "Die Rezepte stehen im <b>Dictionary</b> <code>rezepte</code>. Mit eckigen Klammern liest du einen Wert, und eine for-Schleife über ein Dictionary gibt dir die Schlüssel:"
                  "<pre>print(rezepte[\"kiste\"])   # {'brett': 2}\nfor ware in rezepte[\"motor\"]:\n    print(ware)</pre>"
                  "In diesem Auftrag braucht ein Werkzeug von jeder Zutat genau 1 Stück.",
        "tip": "for ware in rezepte[\"werkzeug\"]: zweimal hole(ware). Dann zum_werk(\"montage\"), zweimal baue(\"werkzeug\"), zum_lager(), abliefern().",
        "grid": karte(),
        "tragkraft": 6, "lager": {"brett": 4, "stahl": 4, "gold": 2, "draht": 2}, "ziel": {"werkzeug": 2},
        "belohnung": {"werkzeug": 2, "draht": 3, "brett": 3}, "needs": [REZEPT],
        "varianten": [{"text": "ein Werkzeug braucht Brett, Stahl und Gold", "rezepte": rezepte_mit(werkzeug={"brett": 1, "stahl": 1, "gold": 1})},
                      {"text": "ein Werkzeug braucht Stahl und Draht", "rezepte": rezepte_mit(werkzeug={"stahl": 1, "draht": 1})}],
        "braucht": ["montage"],
        "start": "print(rezepte[\"werkzeug\"])\n",
        "solution": "for ware in rezepte[\"werkzeug\"]:\n    hole(ware)\n    hole(ware)\nzum_werk(\"montage\")\nbaue(\"werkzeug\")\nbaue(\"werkzeug\")\nzum_lager()\nabliefern()\n",
    },
    {
        "title": "Nur wenn alles da ist: and",
        "task": "Baue so viele Werkzeuge, wie die Bretter und der Stahl im Lager hergeben. Er trägt nur 2 Teile, also ein Werkzeug pro Runde. Der Lagerbestand ist bei jedem Auftrag anders.",
        "lesson": "Mit <b>and</b> müssen beide Bedingungen stimmen, mit <b>or</b> reicht eine. <code>not</code> dreht eine Bedingung um:"
                  "<pre>geld = 5\nhunger = True\nif hunger and geld >= 3:\n    print(\"Pizza!\")</pre>"
                  "Auch eine while-Schleife darf so eine verknüpfte Bedingung haben.",
        "tip": "while im_lager(\"brett\") > 0 and im_lager(\"stahl\") > 0: Brett und Stahl holen, zur Montage, bauen, zurück, abliefern.",
        "grid": karte(),
        "tragkraft": 2, "lager": {"brett": 3, "stahl": 5}, "ziel": {"werkzeug": 3}, "belohnung": {"stahl": 4, "draht": 2}, "needs": [UNDODER, WHILE],
        "varianten": [{"text": "4 Bretter und 2 Stahl im Lager", "lager": {"brett": 4, "stahl": 2}, "ziel": {"werkzeug": 2}},
                      {"text": "nur 1 Brett und 1 Stahl im Lager", "lager": {"brett": 1, "stahl": 1}, "ziel": {"werkzeug": 1}}],
        "braucht": ["montage", "lagerbuch"],
        "start": "print(im_lager(\"brett\"), im_lager(\"stahl\"))\n",
        "solution": "while im_lager(\"brett\") > 0 and im_lager(\"stahl\") > 0:\n    hole(\"brett\")\n    hole(\"stahl\")\n    zum_werk(\"montage\")\n    baue(\"werkzeug\")\n    zum_lager()\n    abliefern()\n",
    },
    {
        "title": "Der Korb: append und len",
        "task": "Hol alles Holz und Kupfer von der Karte. Er trägt 3 Teile. Führe in einer Liste mit, was im Korb liegt: Ist er voll, bring ihn nur zu den Werken, die du wirklich brauchst, und dann ins Lager.",
        "lesson": "Eine Liste kann wachsen: <code>.append(wert)</code> hängt hinten an, <code>len(liste)</code> zählt die Einträge, und <code>in</code> prüft, ob etwas drin ist:"
                  "<pre>korb = []\nkorb.append(\"apfel\")\nkorb.append(\"birne\")\nprint(len(korb))          # 2\nprint(\"apfel\" in korb)   # True\nkorb = []                 # wieder leer</pre>"
                  "Zwei Listen verbindest du mit <code>+</code>, zum Beispiel <code>finde(\"baum\") + finde(\"kupfer\")</code>.",
        "tip": "Für jedes Feld: art = was_ist_hier(), passend abbauen, korb.append(art). Wenn len(korb) == 3: if \"baum\" in korb → Sägewerk, if \"kupfer\" in korb → Ofen, dann Lager und korb = [].",
        "grid": karte(T=[(2, 1), (5, 0), (7, 2), (3, 5)], C=[(6, 4), (8, 6)]),
        "tragkraft": 3, "ziel": {"brett": 4, "draht": 2}, "belohnung": {"draht": 4, "brett": 4}, "needs": [APPEND, LEN],
        "varianten": [{"text": "2 Bäume und 4 Kupferadern", "grid": karte(T=[(3, 1), (6, 5)], C=[(5, 0), (8, 2), (2, 5), (7, 6)]), "ziel": {"brett": 2, "draht": 4}},
                      {"text": "5 Bäume und 1 Kupferader", "grid": karte(T=[(2, 0), (7, 1), (4, 2), (8, 4), (5, 5)], C=[(3, 6)]), "ziel": {"brett": 5, "draht": 1}}],
        "braucht": ["tiegel", "saegewerk", "ofen", "spitzhacke", "karte"],
        "start": "korb = []\nfor x, y in finde(\"baum\") + finde(\"kupfer\"):\n    gehe_zu(x, y)\n",
        "solution": "korb = []\nfor x, y in finde(\"baum\") + finde(\"kupfer\"):\n    gehe_zu(x, y)\n    art = was_ist_hier()\n    if art == \"baum\":\n        hacke()\n    else:\n        abbauen()\n    korb.append(art)\n    if len(korb) == 3:\n        if \"baum\" in korb:\n            zum_werk(\"saegewerk\")\n            verarbeite()\n        if \"kupfer\" in korb:\n            zum_werk(\"ofen\")\n            verarbeite()\n        zum_lager()\n        abliefern()\n        korb = []\n",
    },
    {
        "title": "Einkaufszettel: Dictionary füllen",
        "task": "Baue 2 Werkzeuge und 1 Motor, und zwar in einer einzigen Runde. Rechne vorher in einem Dictionary aus, wie viel du von jeder Ware brauchst. Die Rezepte ändern sich je nach Auftrag.",
        "lesson": "In ein Dictionary kannst du auch <b>schreiben</b>. <code>.get(schluessel, 0)</code> liefert 0, wenn es den Eintrag noch nicht gibt. So addierst du auf:"
                  "<pre>zettel = {}\nfor obst in [\"apfel\", \"birne\", \"apfel\"]:\n    zettel[obst] = zettel.get(obst, 0) + 1\nprint(zettel)   # {'apfel': 2, 'birne': 1}</pre>"
                  "Mit <code>.items()</code> gehst du danach Ware und Menge zusammen durch.",
        "tip": "bedarf = {}. Für jede Ware im Werkzeug-Rezept: bedarf[ware] = bedarf.get(ware, 0) + menge * 2. Dasselbe für den Motor mit menge. Dann alles holen, zur Montage, dreimal bauen, zurück.",
        "grid": karte(),
        "tragkraft": 8, "lager": {"brett": 6, "stahl": 6, "draht": 4}, "ziel": {"werkzeug": 2, "motor": 1},
        "belohnung": {"motor": 1, "stahl": 4, "draht": 3}, "needs": [DICT_SET],
        "varianten": [{"text": "ein Werkzeug braucht 2 Bretter und 1 Stahl", "rezepte": rezepte_mit(werkzeug={"brett": 2, "stahl": 1})},
                      {"text": "ein Motor braucht 1 Stahl und 2 Draht", "rezepte": rezepte_mit(motor={"stahl": 1, "draht": 2})}],
        "braucht": ["montage"],
        "start": "bedarf = {}\n",
        "solution": "bedarf = {}\nfor ware, menge in rezepte[\"werkzeug\"].items():\n    bedarf[ware] = bedarf.get(ware, 0) + menge * 2\nfor ware, menge in rezepte[\"motor\"].items():\n    bedarf[ware] = bedarf.get(ware, 0) + menge\nfor ware, menge in bedarf.items():\n    for i in range(menge):\n        hole(ware)\nzum_werk(\"montage\")\nbaue(\"werkzeug\")\nbaue(\"werkzeug\")\nbaue(\"motor\")\nzum_lager()\nabliefern()\n",
    },
    {
        "title": "Die Bestellung: Schleifen in Schleifen",
        "task": "Im Dictionary bestellung steht, was der Kunde will, zum Beispiel {\"werkzeug\": 2, \"kiste\": 1}. Arbeite die ganze Bestellung ab, ein Produkt nach dem anderen. Sie ist bei jedem Auftrag anders.",
        "lesson": "Eine Schleife in einer Schleife: Die innere läuft bei jeder Runde der äußeren komplett durch."
                  "<pre>for tisch, gaeste in {\"A\": 2, \"B\": 1}.items():\n    for i in range(gaeste):\n        print(\"Teller für Tisch\", tisch)</pre>"
                  "Hier sind es drei Ebenen: jedes Produkt der Bestellung, jede Ware im Rezept, jedes einzelne Stück.",
        "tip": "for produkt, anzahl in bestellung.items(): für jede Ware im Rezept menge * anzahl Stück holen, dann zur Montage, anzahl-mal bauen, zurück, abliefern.",
        "grid": karte(),
        "tragkraft": 6, "lager": {"brett": 10, "stahl": 6, "draht": 4}, "vars": {"bestellung": {"werkzeug": 2, "kiste": 1, "motor": 1}},
        "ziel": {"werkzeug": 2, "kiste": 1, "motor": 1}, "belohnung": {"kiste": 1, "brett": 4, "stahl": 3}, "needs": [VERSCHACHTELT],
        "varianten": [{"text": "bestellung = {\"kiste\": 3, \"werkzeug\": 1}", "vars": {"bestellung": {"kiste": 3, "werkzeug": 1}}, "ziel": {"kiste": 3, "werkzeug": 1}},
                      {"text": "bestellung = {\"motor\": 2, \"kabel\": 1}", "vars": {"bestellung": {"motor": 2, "kabel": 1}}, "ziel": {"motor": 2, "kabel": 1}}],
        "braucht": ["montage"],
        "start": "print(bestellung)\nfor produkt, anzahl in bestellung.items():\n    print(produkt, rezepte[produkt])\n",
        "solution": "for produkt, anzahl in bestellung.items():\n    for ware, menge in rezepte[produkt].items():\n        for i in range(menge * anzahl):\n            hole(ware)\n    zum_werk(\"montage\")\n    for i in range(anzahl):\n        baue(produkt)\n    zum_lager()\n    abliefern()\n",
    },
    {
        "title": "Roboter: zwei Parameter",
        "task": "Baue 2 Roboter. Ein Roboter braucht einen Motor und ein Kabel, die du erst selbst bauen musst. Schreibe eine Funktion fertige(produkt, anzahl) und rufe sie für jede Stufe auf.",
        "lesson": "Eine Funktion kann mehrere <b>Parameter</b> haben, getrennt durch Komma. Beim Aufruf gibst du die Werte in derselben Reihenfolge an:"
                  "<pre>def bestelle(gericht, anzahl):\n    print(anzahl, \"mal\", gericht)\n\nbestelle(\"Pizza\", 2)\nbestelle(\"Salat\", 1)</pre>"
                  "Fertige Produkte landen im Lager, und von dort holst du sie mit <code>hole()</code> für die nächste Stufe.",
        "tip": "In fertige(produkt, anzahl): alle Waren aus rezepte[produkt] menge * anzahl mal holen, zur Montage, anzahl-mal baue(produkt), zurück, abliefern. Dann: Motor, Kabel, Roboter.",
        "grid": karte(),
        "tragkraft": 6, "lager": {"stahl": 5, "draht": 7}, "ziel": {"roboter": 2}, "belohnung": {"roboter": 1, "stahl": 4, "draht": 4}, "needs": [ZWEI_PARAM],
        "braucht": ["montage"],
        "next": "Letzter Auftrag: Diesmal ist das Lager leer. Alles beginnt in der Mine.",
        "start": "def fertige(produkt, anzahl):\n    print(produkt, anzahl, rezepte[produkt])\n\nfertige(\"motor\", 2)\n",
        "solution": "def fertige(produkt, anzahl):\n    for ware, menge in rezepte[produkt].items():\n        for i in range(menge * anzahl):\n            hole(ware)\n    zum_werk(\"montage\")\n    for i in range(anzahl):\n        baue(produkt)\n    zum_lager()\n    abliefern()\n\nfertige(\"motor\", 2)\nfertige(\"kabel\", 2)\nfertige(\"roboter\", 2)\n",
    },
    {
        "title": "Großauftrag: Die Roboterfabrik",
        "task": "Baue 2 Roboter, diesmal ganz von vorne: Das Lager ist leer. Erz abbauen, im Ofen schmelzen, Teile bauen, Roboter bauen. Teile die Arbeit in Funktionen auf.",
        "lesson": "Jetzt kommt alles zusammen. Große Aufgaben zerlegt man in kleine <b>Funktionen</b>, die jeweils eine Sache gut können. Jede ist für sich einfach, und zusammen bauen sie eine ganze Fabrik."
                  "<pre>def schritt_1():\n    print(\"Erz holen\")\n\ndef schritt_2(teil, anzahl):\n    print(anzahl, teil, \"bauen\")\n\nschritt_1()\nschritt_2(\"motor\", 2)</pre>",
        "tip": "Eine Funktion abbau(art): alle Adern dieser Art leeren, Ofen, Lager. Dazu fertige(produkt, anzahl) aus dem letzten Level. Dann: abbau(\"eisen\"), abbau(\"kupfer\"), Motor, Kabel, Roboter.",
        "grid": karte(I=[(6, 1)], C=[(4, 5), (8, 4)]),
        "tragkraft": 6, "mengen": {"I": 4, "C": 3}, "ziel": {"roboter": 2}, "belohnung": {"roboter": 2, "diamant": 1}, "needs": [DEF, FOR],
        "braucht": ["montage", "ofen", "tiegel", "spitzhacke", "karte"],
        "start": "def abbau(art):\n    for x, y in finde(art):\n        gehe_zu(x, y)\n",
        "solution": "def abbau(art):\n    for x, y in finde(art):\n        gehe_zu(x, y)\n        while was_ist_hier() == art:\n            abbauen()\n    zum_werk(\"ofen\")\n    verarbeite()\n    zum_lager()\n    abliefern()\n\ndef fertige(produkt, anzahl):\n    for ware, menge in rezepte[produkt].items():\n        for i in range(menge * anzahl):\n            hole(ware)\n    zum_werk(\"montage\")\n    for i in range(anzahl):\n        baue(produkt)\n    zum_lager()\n    abliefern()\n\nabbau(\"eisen\")\nabbau(\"kupfer\")\nfertige(\"motor\", 2)\nfertige(\"kabel\", 2)\nfertige(\"roboter\", 2)\n",
    },
]
for lv in WELT2:
    lv["welt"] = 2
LEVELS += WELT2


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
# Welt 2. "minimal": False heißt, der Code ist besser als die Musterlösung, aber nicht nachweislich der kürzeste Weg
BESTE += [
    ("for i in range(8):\n    rechts()\n    if was_ist_hier() == \"baum\":\n        hacke()\n    elif was_ist_hier() in [\"kupfer\", \"eisen\"]:\n        abbauen()\nzum_werk(\"saegewerk\")\nverarbeite()\nzum_werk(\"ofen\")\nverarbeite()\nzum_lager()\nabliefern()\n",
     "Der Weg ist schon der kürzeste. Sparen kannst du nur Zeilen: Mit in fragst du zwei Erze in einer Bedingung ab, weil beide mit abbauen() gehen."),
    ("anzahl = 0\nwhile anzahl < 5:\n    x, y = finde(\"kupfer\")[0]\n    gehe_zu(x, y)\n    abbauen()\n    anzahl += 1\nzum_werk(\"ofen\")\nverarbeite()\nzum_lager()\nabliefern()\n",
     "Die Musterlösung ist hier schon optimal: Er leert zuerst die nächste Ader und holt den Rest aus der Ader auf dem Weg zum Ofen. gehe_zu() läuft gar nicht, wenn er schon auf dem Feld steht."),
    ("def fehlt(ware, ziel):\n    return ziel - im_lager(ware)\n\nfor i in range(fehlt(\"brett\", 6)):\n    x, y = finde(\"baum\")[0]\n    gehe_zu(x, y)\n    hacke()\nzum_werk(\"saegewerk\")\nverarbeite()\nzum_lager()\nabliefern()\n",
     "Kürzer geht es nur mit einer geschickteren Reihenfolge der Bäume: Auf dieser Karte wären 30 Aktionen möglich. finde() liefert die Bäume aber von oben nach unten, und eine bessere Reihenfolge allgemein auszurechnen ist ein schweres Problem (das Problem des Handlungsreisenden). Hier zählt vor allem, dass dein Code bei jedem Lagerbestand stimmt."),
    ("for ware, menge in rezepte[\"werkzeug\"].items():\n    for i in range(menge * 2):\n        hole(ware)\nzum_werk(\"montage\")\nbaue(\"werkzeug\")\nbaue(\"werkzeug\")\nzum_lager()\nabliefern()\n",
     "Weniger als 11 Aktionen geht nicht. Diese Version ist aber robuster: Sie liest mit .items() auch die Menge aus und funktioniert deshalb auch, wenn ein Rezept einmal 2 Stück von etwas verlangt."),
    ("while im_lager(\"brett\") > 0 and im_lager(\"stahl\") > 0:\n    hole(\"brett\")\n    hole(\"stahl\")\n    zum_werk(\"montage\")\n    baue(\"werkzeug\")\n    zum_lager()\n    abliefern()\n",
     "Er trägt nur 2 Teile, also braucht jedes Werkzeug eine eigene Runde. Die Musterlösung ist damit schon optimal. Das and sorgt dafür, dass er aufhört, sobald eine der beiden Zutaten fehlt."),
    ("korb = []\nfor x, y in sorted(finde(\"baum\")[:3], reverse=True) + finde(\"kupfer\") + finde(\"baum\")[3:]:\n    gehe_zu(x, y)\n    art = was_ist_hier()\n    if art == \"baum\":\n        hacke()\n    else:\n        abbauen()\n    korb.append(art)\n    if len(korb) == 3:\n        if \"kupfer\" in korb:\n            zum_werk(\"ofen\")\n            verarbeite()\n        if \"baum\" in korb:\n            zum_werk(\"saegewerk\")\n            verarbeite()\n        zum_lager()\n        abliefern()\n        korb = []\n",
     "Die Touren sind nach Gegend geordnet statt nach Art: oben die drei Bäume, von rechts nach links (sorted mit reverse=True), unten erst das Kupfer, dann den Baum auf dem Rückweg. Und vom Ofen aus liegt das Sägewerk auf dem Heimweg. Das spart 14 Aktionen. Die Reihenfolge ist aber auf diese Karte zugeschnitten."),
    ("bedarf = {}\nfor produkt, anzahl in {\"werkzeug\": 2, \"motor\": 1}.items():\n    for ware, menge in rezepte[produkt].items():\n        bedarf[ware] = bedarf.get(ware, 0) + menge * anzahl\nfor ware, menge in bedarf.items():\n    for i in range(menge):\n        hole(ware)\nzum_werk(\"montage\")\nfor produkt in [\"werkzeug\", \"werkzeug\", \"motor\"]:\n    baue(produkt)\nzum_lager()\nabliefern()\n",
     "Eine Runde ist das Minimum, das schafft schon die Musterlösung. Diese Version steckt die Bestellung selbst in ein Dictionary und rechnet den Bedarf mit einer Schleife in der Schleife aus. So musst du für ein drittes Produkt keinen neuen Block schreiben. Genau das ist das nächste Level."),
    ("gebaut = []\ntraegt = 0\nfor produkt, anzahl in bestellung.items():\n    teile = sum(rezepte[produkt].values())\n    for i in range(anzahl):\n        if traegt + teile > 6:\n            zum_werk(\"montage\")\n            for p in gebaut:\n                baue(p)\n            zum_lager()\n            abliefern()\n            gebaut = []\n            traegt = 0\n        for ware, menge in rezepte[produkt].items():\n            for j in range(menge):\n                hole(ware)\n        gebaut.append(produkt)\n        traegt += teile\nzum_werk(\"montage\")\nfor p in gebaut:\n    baue(p)\nzum_lager()\nabliefern()\n",
     "Statt für jedes Produkt eine eigene Runde zu laufen, packt er die Hände so voll wie möglich und baut dann alles auf einmal. sum() zählt, wie viele Teile ein Rezept braucht. Das spart eine ganze Runde, kostet aber mehr als doppelt so viele Zeilen."),
    ("def fertige(produkt, anzahl):\n    for ware, menge in rezepte[produkt].items():\n        if im_lager(ware) > 0:\n            for i in range(menge * anzahl):\n                hole(ware)\n    zum_werk(\"montage\")\n    for i in range(anzahl):\n        baue(produkt)\n    zum_lager()\n\nfertige(\"motor\", 2)\nfertige(\"kabel\", 2)\nfertige(\"roboter\", 2)\nabliefern()\n",
     "Der Trick: Motoren und Kabel muss er gar nicht abliefern. Er behält sie in der Hand und holt nur, was im Lager liegt. Erst die fertigen Roboter gibt er ab. Das spart 6 Aktionen und kostet nur eine Zeile mehr."),
    ("def abbau(art):\n    for x, y in finde(art):\n        gehe_zu(x, y)\n        while was_ist_hier() == art:\n            abbauen()\n    zum_werk(\"ofen\")\n    verarbeite()\n    zum_lager()\n    abliefern()\n\ndef fertige(produkt, anzahl):\n    for ware, menge in rezepte[produkt].items():\n        if im_lager(ware) > 0:\n            for i in range(menge * anzahl):\n                hole(ware)\n    zum_werk(\"montage\")\n    for i in range(anzahl):\n        baue(produkt)\n    zum_lager()\n\nabbau(\"eisen\")\nabbau(\"kupfer\")\nfertige(\"motor\", 2)\nfertige(\"kabel\", 2)\nfertige(\"roboter\", 2)\nabliefern()\n",
     "Derselbe Trick wie im letzten Level: Zwischenprodukte bleiben in der Hand, statt ins Lager und wieder heraus zu wandern. Noch weniger Aktionen wären möglich, wenn er den Draht gar nicht erst abliefert. Dann wird der Code aber schnell unübersichtlich."),
]
MINIMAL_NICHT = {13, 18, 19, 20}   # 0-basierte Level, bei denen der Weg nicht nachweislich der kürzeste ist
assert len(BESTE) == len(LEVELS)
for i, (lv, (code, warum)) in enumerate(zip(LEVELS, BESTE)):
    lv["beste"] = code
    lv["warum"] = warum
    lv["minimal"] = i not in MINIMAL_NICHT
