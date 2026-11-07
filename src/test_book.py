import contextlib, io, sys
sys.path.insert(0, ".")
from book import BOOK

total = bad = 0
for sec in BOOK:
    for it in sec["items"]:
        if "code" not in it:
            continue
        total += 1
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                exec(it["code"], {"__name__": "__main__"})
            got = buf.getvalue()
        except Exception as e:
            got = "EXC %r" % e
        if got != it["out"]:
            bad += 1
            print("FALSCH:", sec["title"], "/", it["name"], repr(got), "!=", repr(it["out"]))
print("Beispiele:", total, "falsch:", bad)
sys.exit(bad)
