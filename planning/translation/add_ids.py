"""Gives every German heading the anchor of the English heading at the same position, so links
like page.md#some-heading work in both languages. Reads the anchors from the English build in
site/, so build first. Safe to run again (it replaces the ids it wrote before).

    .venv/Scripts/mkdocs build
    python planning/translation/add_ids.py                     every page.de.md
    python planning/translation/add_ids.py docs/x/page.de.md   only these
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCS, SITE = ROOT / "docs", ROOT / "site"
FENCE = re.compile(r"^[ \t]*(`{3,}|~{3,}).*?^[ \t]*\1[ \t]*$", re.M | re.S)
HEADING = re.compile(r"^[ \t]*#{1,6} [^\r\n]+", re.M)


def english_ids(de):
    rel = de.relative_to(DOCS).with_name(de.name[:-len(".de.md")])
    page = SITE / (rel.parent if rel.name == "index" else rel) / "index.html"
    h = page.read_text(encoding="utf-8")
    return re.findall(r'<h[1-6] id="([^"]+)"', h[h.index("<article"):h.index("</article>")])


bad = 0
for de in [Path(f).resolve() for f in sys.argv[1:]] or sorted(DOCS.rglob("*.de.md")):
    t = de.read_bytes().decode("utf-8")
    code = [m.span() for m in FENCE.finditer(t)]
    heads = [m for m in HEADING.finditer(t) if not any(a <= m.start() < b for a, b in code)]
    ids = english_ids(de)
    if len(heads) != len(ids):
        print(f"{de.relative_to(DOCS)}: {len(heads)} headings, the English page has {len(ids)}")
        bad += 1
        continue
    for m, i in reversed(list(zip(heads, ids))):
        line = re.sub(r"\s*\{ #[\w-]+ \}\s*$", "", m.group(0))
        t = t[:m.start()] + f"{line} {{ #{i} }}" + t[m.end():]
    de.write_bytes(t.encode("utf-8"))
print(f"{bad} pages skipped" if bad else "all headings have their English anchor")
sys.exit(1 if bad else 0)
