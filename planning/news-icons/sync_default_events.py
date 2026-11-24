# Rebuilds the "Default events" page from the StockMarket repo (only reads it):
#   docs/assets/images/stockmarket/news/events/  the news pictures, copied from the mod
#   docs/assets/images/stockmarket/news/items/   64x64 inventory-style icons from the Minecraft client jar
#   docs/assets/images/stockmarket/news/charts/  small effect curves (shapes from NewsImpactEnvelope)
#   docs/admin/stockmarket/news/default-events.md  the event tables with each event's JSON, the event
#                                                count and the admin-only list
#   docs/admin/stockmarket/news/default-events.de.md  the same in German: the events' de_de headlines,
#                                                German item names from Minecraft's de_de.json
# The rest of both pages stays hand-written; the script names chained events Storylines doesn't mention.
# Usage: python planning/news-icons/sync_default_events.py [StockMarket repo] [minecraft-1.21.1-client.jar]
#   defaults: ../StockMarket/MC_1.21.1_StockMarket next to the Docs folder, the Prism Launcher client jar.
# Check: run it twice; the second run must leave `git status` unchanged. Then mkdocs build --strict.
import filecmp, io, json, math, os, re, shutil, sys, zipfile
from PIL import Image, ImageEnhance

DOCS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
REPO = sys.argv[1] if len(sys.argv) > 1 else os.path.join(DOCS, "..", "StockMarket", "MC_1.21.1_StockMarket")
JAR = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.environ.get("APPDATA", ""), "PrismLauncher", "libraries",
                                                         "com", "mojang", "minecraft", "1.21.1", "minecraft-1.21.1-client.jar")
NEWS = os.path.join(REPO, "common", "src", "main", "resources", "news")
OUT = os.path.join(DOCS, "docs", "assets", "images", "stockmarket", "news")
PAGE = os.path.join(DOCS, "docs", "admin", "stockmarket", "news", "default-events.md")
# Minecraft's German names: 1.21.1 uses asset index 17 in Prism's shared asset store
ASSETS = os.path.join(os.environ.get("APPDATA", ""), "PrismLauncher", "assets")
_h = json.load(open(os.path.join(ASSETS, "indexes", "17.json"), encoding="utf-8"))["objects"]["minecraft/lang/de_de.json"]["hash"]
MC_DE = json.load(open(os.path.join(ASSETS, "objects", _h[:2], _h), encoding="utf-8"))
IMG = "../../../assets/images/stockmarket/news"   # as the page links it

# Tags and patterns get one example item as their icon
STAND_INS = {"#c:ores": "iron_ore", "#minecraft:coals": "coal", "#minecraft:logs": "oak_log",
             "#minecraft:planks": "oak_planks", "#minecraft:wool": "white_wool",
             "*_bed": "red_bed", "*_ore": "iron_ore", "*_planks": "oak_planks", "raw_*": "raw_iron"}

# ---- item icons from the client jar
z = zipfile.ZipFile(JAR)

def model(path):
    return json.loads(z.read(f"assets/minecraft/models/{path}.json"))

def textures(path):
    """Resolve a model's texture variables through its parents."""
    tex, cur = {}, path
    while cur:
        m = model(cur.replace("minecraft:", ""))
        for k, v in m.get("textures", {}).items():
            tex.setdefault(k, v)
        cur = m.get("parent", "")
        if cur.startswith("builtin"):
            break
    for _ in range(5):   # "#side" style references
        tex = {k: (tex.get(v[1:], v) if v.startswith("#") else v) for k, v in tex.items()}
    return tex

def png(name, crop=None):
    im = Image.open(io.BytesIO(z.read(f"assets/minecraft/textures/{name.replace('minecraft:', '')}.png"))).convert("RGBA")
    if crop:
        return im.crop(crop)
    return im.crop((0, 0, im.width, im.width))   # animated strips: first frame

def face(canvas, tex, o, u, v, shade):
    """Paint texture onto the parallelogram o + s*u + t*v (s, t in 0..1)."""
    tex = ImageEnhance.Brightness(tex).enhance(shade)
    w, h = tex.size
    det = u[0] * v[1] - u[1] * v[0]
    a, b = v[1] / det * w, -v[0] / det * w
    d, e = -u[1] / det * h, u[0] / det * h
    c, f = -(a * o[0] + b * o[1]), -(d * o[0] + e * o[1])
    layer = tex.transform(canvas.size, Image.AFFINE, (a, b, c, d, e, f), Image.NEAREST)
    mask = Image.new("L", tex.size, 255).transform(canvas.size, Image.AFFINE, (a, b, c, d, e, f), Image.NEAREST)
    layer.putalpha(Image.composite(layer.getchannel("A"), Image.new("L", canvas.size, 0), mask))
    canvas.alpha_composite(layer)

def cube(top, left, right, height=1.0):
    S = 256   # draw big, shrink at the end
    T, L, R, C = (128, 6), (14, 66), (242, 66), (128, 126)
    dy = 120 * height
    canvas = Image.new("RGBA", (S, S))
    sub = lambda p, q: (p[0] - q[0], p[1] - q[1])
    lift = lambda p: (p[0], p[1] + 120 - dy)
    Tt, Lt, Rt, Ct = (lift(p) for p in (T, L, R, C))
    face(canvas, top, Lt, sub(Tt, Lt), sub(Ct, Lt), 1.0)
    face(canvas, left, Lt, sub(Ct, Lt), (0, dy), 0.8)
    face(canvas, right, Ct, sub(Rt, Ct), (0, dy), 0.6)
    return canvas.resize((64, 64), Image.LANCZOS)

def icon(item):
    m = model(f"item/{item}")
    par = m.get("parent", "")
    if item == "wither_skeleton_skull":
        sk = "entity/skeleton/wither_skeleton"
        return cube(png(sk, (8, 0, 16, 8)), png(sk, (8, 8, 16, 16)), png(sk, (0, 8, 8, 16)), 0.6)
    if item == "red_bed":
        bed = "entity/bed/red"
        return cube(png(bed, (6, 6, 22, 22)), png(bed, (22, 22, 38, 28)), png(bed, (0, 28, 6, 44)).rotate(90, expand=True), 0.4)
    if par.endswith("item/generated") or par.endswith("item/handheld"):
        out = Image.new("RGBA", (16, 16))
        for k in sorted(m["textures"]):
            out.alpha_composite(png(m["textures"][k]).resize((16, 16), Image.NEAREST))
        return out.resize((64, 64), Image.NEAREST)
    t = textures(par.replace("minecraft:", ""))
    pick = lambda *keys: png(next(t[k] for k in keys if k in t))
    return cube(pick("up", "top", "end", "all", "texture"),
                pick("front", "north", "side", "all", "texture"),
                pick("east", "side", "all", "texture"))

# ---- effect charts: (ramp-up s, hold s, reversal, reversal s) from NewsImpactEnvelope.ImpactType
TYPES = {"shock": (5, 300, "exp", 300), "trend": (120, 600, "ramp", 600),
         "crash": (10, 120, "exp", 900), "permanent": (600, 0, "none", 0)}
COL = {"up": "#1f9d55", "down": "#e03e3e"}

def env(t, ramp, hold, mode, rev):
    if t < 0: return 0.0
    if t < ramp: return t / ramp
    t -= ramp
    if t < hold or mode == "none": return 1.0
    t -= hold
    return math.exp(-t / rev) if mode == "exp" else max(0.0, 1 - t / rev)

def svg(points, color, base):
    path = " ".join(f"{'M' if i == 0 else 'L'}{x:.1f} {y:.1f}" for i, (x, y) in enumerate(points))
    area = path + f" L{points[-1][0]:.1f} {base} L{points[0][0]:.1f} {base} Z"
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 32" width="64" height="32">'
            f'<line x1="2" y1="{base}" x2="62" y2="{base}" stroke="#9e9e9e" stroke-width="1" stroke-dasharray="2 2"/>'
            f'<path d="{area}" fill="{color}" fill-opacity="0.15"/>'
            f'<path d="{path}" fill="none" stroke="{color}" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/>'
            '</svg>')

def write_charts():
    os.makedirs(f"{OUT}/charts", exist_ok=True)
    for name, (ramp, hold, mode, rev) in TYPES.items():
        span = ramp + hold + (4 * rev if mode == "exp" else rev) if mode != "none" else ramp * 2.5
        for d in ("up", "down"):
            base, amp = (26, -21) if d == "up" else (6, 21)
            pts = [(2 + 60 * i / 120, base + amp * env(span * (i / 120 - 0.1) / 0.85, ramp, hold, mode, rev)) for i in range(121)]
            open(f"{OUT}/charts/{name}-{d}.svg", "w").write(svg(pts, COL[d], base))
    # story: several steps, up and down
    st = [(0, 0), (0.12, 0), (0.35, 0.8), (0.5, 0.65), (0.7, -0.55), (1.0, 0)]
    open(f"{OUT}/charts/story.svg", "w").write(svg([(2 + 60 * x, 16 - 12 * y) for x, y in st], "#5c6bc0", 16))

# ---- page cells
def slug(s):   # Python-Markdown's toc slugify, for the English anchors the German headings keep
    return re.sub(r"[-\s]+", "-", re.sub(r"[^\w\s-]", "", s).strip().lower())

def de_item(shown):
    return MC_DE.get(f"item.minecraft.{shown}") or MC_DE.get(f"block.minecraft.{shown}") or shown

EN = dict(lang="en_us", page=PAGE, head=["Picture", "Headline", "ID", "Markets", "Effect"],
          item=lambda s: s.replace("_", " ").capitalize(), example="{nice}, an example of {name}",
          kinds={"shock": "moves at once, holds briefly, then fades back quickly",
                 "trend": "moves slowly, holds for a long time, then ramps back down",
                 "crash": "moves at once, holds briefly, then recovers very slowly",
                 "permanent": "moves to a new level and stays there"},
          chart_alt=lambda kind, up, desc: f"{kind.capitalize()} chart: the price {'rises' if up else 'falls'}, {desc}",
          permanent=", permanent", story_alt="Story chart: several steps up and down", story="story: ", or_=" or ",
          admin="admin only", requires="requirements", weight0="weight 0", chain="chain → ", undoes="undoes `{}`",
          before="news before the price moves", after="news after the price moves",
          either="news before or after the price moves",
          heading=lambda c, n: f"### {c.capitalize()} ({n})",
          events=r"(## The events\n\n).*?(?=## Storylines)", stories=("## Storylines", "## Events that never fire"),
          count=(r"StockMarket ships \d+ news events", "StockMarket ships {} news events"),
          words="No One Two Three Four Five Six Seven Eight Nine Ten Eleven Twelve".split(),
          admin_line=(r"\S+ events are admin only: [^.]*\.", "{} events are admin only: {} and {}."))
CATS_DE = {"commodities": "Rohstoffe", "markets": "Märkte", "politics": "Politik", "rumors": "Gerüchte",
           "crime": "Kriminalität", "technology": "Technologie", "economy": "Wirtschaft", "disaster": "Katastrophen",
           "labor": "Arbeit", "recovery": "Erholung", "cultural": "Kultur", "conflict": "Konflikte"}
def de_heading(c, n):
    if c not in CATS_DE:
        sys.exit(f"new category '{c}': add its German name to CATS_DE")
    return f"### {CATS_DE[c]} ({n}) {{ #{slug(f'{c.capitalize()} ({n})')} }}"
DE = dict(lang="de_de", page=PAGE.replace(".md", ".de.md"), head=["Bild", "Schlagzeile", "ID", "Märkte", "Wirkung"],
          item=de_item, example="{nice}, ein Beispiel für {name}",
          kinds={"shock": "bewegt sich sofort, hält kurz und geht dann schnell zurück",
                 "trend": "bewegt sich langsam, hält lange und geht dann langsam zurück",
                 "crash": "bewegt sich sofort, hält kurz und erholt sich dann sehr langsam",
                 "permanent": "geht auf ein neues Niveau und bleibt dort"},
          chart_alt=lambda kind, up, desc: f"Chart {'dauerhaft' if kind == 'permanent' else kind}: Der Preis {'steigt' if up else 'fällt'}, {desc}",
          permanent=", dauerhaft", story_alt="Chart Geschichte: mehrere Schritte auf und ab", story="Geschichte: ", or_=" oder ",
          admin="nur für Admins", requires="Bedingungen", weight0="Gewicht 0", chain="Kette → ", undoes="hebt `{}` auf",
          before="News vor der Preisbewegung", after="News nach der Preisbewegung",
          either="News vor oder nach der Preisbewegung", heading=de_heading,
          events=r"(## [^\n]*\{ #the-events \}\n\n).*?(?=## [^\n]*\{ #storylines \})",
          stories=("{ #storylines }", "{ #events-that-never-fire-at-random }"),
          count=(r"StockMarket liefert \d+ News-Ereignisse", "StockMarket liefert {} News-Ereignisse"),
          words="Keine Ein Zwei Drei Vier Fünf Sechs Sieben Acht Neun Zehn Elf Zwölf".split(),
          admin_line=(r"\S+ Ereignisse sind nur für Admins: [^.]*\.", "{} Ereignisse sind nur für Admins: {} und {}."))
icons = set()

def market(m, L):
    name = m["item"].removeprefix("minecraft:")
    shown = STAND_INS.get(name, name)
    if ":" in shown or "*" in shown or shown.startswith("#"):
        sys.exit(f"no icon for {m['item']}: add an example item to STAND_INS")
    icons.add(shown)
    nice = L["item"](shown)
    alt = L["example"].format(nice=nice, name=name) if name in STAND_INS else nice
    w = m.get("weightFactor", 1.0)
    factor = "" if w == 1 else f" ×{w:g}".replace("-", "−")
    return f'![{alt}]({IMG}/items/{shown}.png){{ .item-icon .no-zoom width="32" }} `{name}`{factor}'

def chart(file, alt):
    return f'![{alt}]({IMG}/charts/{file}.svg){{ .effect-chart .no-zoom width="64" }}'

def effect(e, L):
    if "sequences" in e:
        lines = [chart("story", L["story_alt"]),
                 L["story"] + L["or_"].join(f"`{s['name']}`" for s in e["sequences"])]
    else:
        im = e["impact"]
        kind = "permanent" if im.get("reversal") == "none" else im["type"]
        up = im["peakFactor"] > 0
        pct = round(abs(im["peakFactor"]) * 100)
        d = "up" if up else "down"
        arrows = f":material-arrow-{d}-bold:{{ .news-{d} }}" * (1 if pct < 25 else 2 if pct < 40 else 3)
        text = ("+" if up else "−") + f"{pct}%" + (L["permanent"] if kind == "permanent" else f" {kind}")
        lines = [chart(f"{kind}-{d}", L["chart_alt"](kind, up, L["kinds"][kind])),
                 f"{arrows} {text}"]
    notes = []
    if e.get("adminOnly"): notes.append(L["admin"])
    if e.get("requires"): notes.append(L["requires"])
    if e.get("weight") == 0: notes.append(L["weight0"])
    if e.get("chains"): notes.append(L["chain"] + ", ".join(f"`{c['eventId']}`" for c in e["chains"]))
    if e.get("undoes"): notes.append(L["undoes"].format(e["undoes"]))
    delay = e.get("announceDelayMs")
    if isinstance(delay, (int, float)):
        delay = {"min": delay, "max": delay}
    if delay and (delay["min"] or delay["max"]):   # delay >= 0: headline first, < 0: price first
        notes.append(L["before"] if delay["min"] >= 0 else L["after"] if delay["max"] < 0 else L["either"])
    if notes:
        lines.append("; ".join(notes))
    return "<br>".join(lines)

def rows(e, raw, L):
    h = e["headline"][L["lang"]]
    cells = [f'![{h}]({IMG}/events/{e["picture"]}){{ .news-pic width="96" loading="lazy" }}', h,
             f'`{e["id"]}`<br><details class="json-toggle"><summary>JSON</summary></details>',
             "<br>".join(market(m, L) for m in e["markets"]), effect(e, L)]
    return ("<tr markdown>\n" + "".join(f'<td markdown="span">{c}</td>\n' for c in cells) + "</tr>\n"
            '<tr class="event-json" markdown>\n<td colspan="5" markdown="block">\n\n'
            f"```json\n{raw}\n```\n\n</td>\n</tr>\n")

def table(events, L):
    return ("<table markdown>\n<thead>\n<tr>" + "".join(f"<th>{h}</th>" for h in L["head"]) + "</tr>\n"
            "</thead>\n<tbody markdown>\n" + "".join(rows(e, raw, L) for e, raw in events) + "</tbody>\n</table>\n")

# ---- read the shipped events, in index.json order
ids = json.load(open(f"{NEWS}/index.json", encoding="utf-8"))
events = []
for i in ids:
    raw = open(f"{NEWS}/events/{i}.json", encoding="utf-8").read().replace("\r\n", "\n").strip()
    events.append((json.loads(raw), raw))
unlisted = {f[:-5] for f in os.listdir(f"{NEWS}/events") if f.endswith(".json")} - set(ids)
if unlisted:
    print("not in index.json, left out:", ", ".join(sorted(unlisted)))

cats = {}
for e, raw in events:
    cats.setdefault(e["category"], []).append((e, raw))
blocks = {L["lang"]: "".join(f"{L['heading'](c, len(es))}\n\n{table(es, L)}\n" for c, es in cats.items()) for L in (EN, DE)}

# ---- pictures, icons, charts
os.makedirs(f"{OUT}/events", exist_ok=True)
used = {e["picture"] for e, _ in events}
for p in sorted(used):
    src, dst = f"{NEWS}/pictures/{p}", f"{OUT}/events/{p}"
    if not os.path.exists(dst) or not filecmp.cmp(src, dst, shallow=False):
        shutil.copyfile(src, dst)
        print("picture", p)
os.makedirs(f"{OUT}/items", exist_ok=True)
for it in sorted(icons):
    try:
        icon(it).save(f"{OUT}/items/{it}.png", optimize=True)
    except KeyError:
        sys.exit(f"{it} isn't a vanilla 1.21.1 item: add an example item for it to STAND_INS")
for folder, keep in (("events", used), ("items", {f"{i}.png" for i in icons})):
    for f in sorted(set(os.listdir(f"{OUT}/{folder}")) - keep):
        os.remove(f"{OUT}/{folder}/{f}")
        print("removed", folder, f)
write_charts()

# ---- pages
admin = [f"`{e['id']}`" for e, _ in events if e.get("adminOnly")]
for L in (EN, DE):
    with open(L["page"], encoding="utf-8", newline="") as f:
        t = f.read()
    nl = "\r\n" if "\r\n" in t else "\n"
    t = t.replace("\r\n", "\n")
    t, n = re.subn(L["events"], lambda m: m.group(1) + blocks[L["lang"]], t, flags=re.S)
    if n != 1:
        sys.exit(f"{L['page']}: the events section between its two headings was not found")
    t = re.sub(L["count"][0], L["count"][1].format(len(events)), t)
    if len(admin) >= 2:
        count = L["words"][len(admin)] if len(admin) < len(L["words"]) else str(len(admin))
        t = re.sub(L["admin_line"][0], L["admin_line"][1].format(count, ", ".join(admin[:-1]), admin[-1]), t)
    else:
        print("fewer than two admin-only events: edit 'Events that never fire at random' by hand")
    with open(L["page"], "w", encoding="utf-8", newline="") as f:
        f.write(t.replace("\n", nl))
    story = t[t.index(L["stories"][0]):t.index(L["stories"][1])]
    linked = {e["id"] for e, _ in events if e.get("chains") or e.get("undoes")}
    linked |= {c["eventId"] for e, _ in events for c in e.get("chains", [])} | {e["undoes"] for e, _ in events if e.get("undoes")}
    missing = sorted(i for i in linked if f"`{i}`" not in story)
    if missing:
        print(f"{os.path.basename(L['page'])}: Storylines doesn't mention:", ", ".join(missing))
print(f"{len(events)} events, {len(icons)} icons")
