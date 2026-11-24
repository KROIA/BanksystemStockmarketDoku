# Makes the pictures of the "Default events" page:
#   items/<name>.png   64x64 inventory-style icons from the Minecraft client jar (flat items, blocks as cubes)
#   charts/<type>-<up|down>.svg and charts/story.svg   small effect curves (shapes from NewsImpactEnvelope)
# Usage: python make_news_icons.py <minecraft-1.21.1-client.jar> <docs/assets/images/stockmarket/news>
import io, json, math, os, sys, zipfile
from PIL import Image, ImageEnhance

JAR, OUT = sys.argv[1], sys.argv[2]
z = zipfile.ZipFile(JAR)
ITEMS = """amethyst_shard ancient_debris baked_potato basalt beef beetroot beetroot_soup black_dye blackstone blaze_powder
blaze_rod bread brown_mushroom cake calcite carrot carved_pumpkin chorus_fruit cobbled_deepslate cobblestone cocoa_beans cod
cooked_cod cooked_rabbit cooked_salmon cookie copper_block copper_ingot crying_obsidian deepslate diamond diamond_block
dragon_breath dripstone_block egg elytra emerald emerald_block ender_eye ender_pearl feather ghast_tear glowstone glowstone_dust
gold_ingot honey_bottle honeycomb ink_sac iron_block iron_ingot lapis_block lapis_lazuli leather magenta_dye magma_cream melon
melon_slice milk_bucket mushroom_stew mutton nether_wart netherite_ingot netherite_scrap obsidian paper phantom_membrane pink_dye
pointed_dripstone popped_chorus_fruit potato prismarine prismarine_crystals prismarine_shard pumpkin pumpkin_pie purple_dye
quartz quartz_block rabbit rabbit_hide raw_copper raw_iron red_mushroom redstone salmon shulker_shell soul_sand stone string
sugar sugar_cane sweet_berries tropical_fish tuff wheat white_dye wither_skeleton_skull
iron_ore coal oak_log oak_planks white_wool red_bed""".split()   # last row: stand-ins for tags and patterns

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

os.makedirs(f"{OUT}/items", exist_ok=True)
for it in ITEMS:
    icon(it).save(f"{OUT}/items/{it}.png", optimize=True)

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
print("items", len(ITEMS), "charts", len(TYPES) * 2 + 1)
