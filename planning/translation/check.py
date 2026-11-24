"""Compares German pages with their English originals: everything that must not change.

    python planning/translation/check.py                     every page.de.md under docs/
    python planning/translation/check.py docs/x/page.de.md   only these

Checks: front matter keys, code blocks (byte for byte), heading levels in order, link and picture
targets, inline code, { ... } attributes, admonition types, HTML tags, table rows.
Also lists English pages that have no German page yet. Exit code 1 if anything differs.
"""
import re
import sys
from collections import Counter
from pathlib import Path

DOCS = Path(__file__).resolve().parents[2] / "docs"
FENCE = re.compile(r"^[ \t]*(`{3,}|~{3,}).*?^[ \t]*\1[ \t]*$", re.M | re.S)


def parts(path):
    t = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    fm, body = "", t
    if t.startswith("---\n"):
        end = t.index("\n---\n", 4)
        fm, body = t[4:end], t[end + 5:]
    code = [m.group(0) for m in FENCE.finditer(body)]
    prose = FENCE.sub("", body)
    lines = prose.split("\n")
    return {
        "front matter keys": [l.split(":")[0] for l in fm.split("\n") if re.match(r"\w", l)],
        "code blocks": code,
        "heading levels": [len(m.group(1)) for l in lines if (m := re.match(r"^\s*(#{1,6}) \S", l))],
        "link/picture targets": Counter(re.findall(r"\]\(([^)\s]+)", prose)),
        "inline code": Counter(re.findall(r"`[^`\n]+`", prose)),
        "attributes": Counter(a for a in re.findall(r"\{[^{}\n]*\}", prose) if not a.startswith("{ #")),
        "admonitions": [m.group(1) for l in lines if (m := re.match(r"^\s*(?:!!!|\?\?\?\+?) (\w+)", l))],
        "html tags": Counter(re.findall(r"</?[a-z][a-z0-9]*", prose)),
        "table rows": sum(1 for l in lines if l.lstrip().startswith("|")),
    }


def compare(de):
    en = de.with_name(de.name.replace(".de.md", ".md"))
    a, b = parts(en), parts(de)
    out = []
    for k in a:
        if a[k] == b[k]:
            continue
        if isinstance(a[k], Counter):
            missing, extra = a[k] - b[k], b[k] - a[k]
            if missing: out.append(f"  {k} missing: {', '.join(missing.elements())}")
            if extra: out.append(f"  {k} extra: {', '.join(extra.elements())}")
        elif k == "code blocks":
            out.append(f"  code blocks differ (English {len(a[k])}, German {len(b[k])}); first difference:")
            for x, y in zip(a[k] + [""] * 99, b[k] + [""] * 99):
                if x != y:
                    out.append("    EN: " + x[:200].replace("\n", "⏎") + "\n    DE: " + y[:200].replace("\n", "⏎"))
                    break
        else:
            out.append(f"  {k}: English {a[k]}, German {b[k]}")
    fm = de.read_text(encoding="utf-8")
    for key in ("title", "description"):
        if not re.search(rf'^{key}: ".+"$', fm, re.M):
            out.append(f'  front matter: {key} missing or not in double quotes')
    return out


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    files = [Path(f).resolve() for f in sys.argv[1:]] or sorted(DOCS.rglob("*.de.md"))
    bad = 0
    for de in files:
        problems = compare(de)
        if problems:
            bad += 1
            print(de.relative_to(DOCS))
            print("\n".join(problems))
    if not sys.argv[1:]:
        todo = [p for p in sorted(DOCS.rglob("*.md")) if not p.name.endswith(".de.md")
                and not p.with_name(p.stem + ".de.md").exists()]
        if todo:
            print(f"{len(todo)} pages without German version")
    print(f"{len(files)} German pages checked, {bad} with differences")
    sys.exit(1 if bad else 0)
