# Exports the home corner of a world into a vanilla structure template (home-hero.nbt).
# Usage: python export_corner.py "<world dir>" <out.nbt>   (read only on the world; no extra packages)
# The box below is the corner in the DemoCorner world; change it if the corner moves or grows.

import glob, gzip, io, math, os, struct, sys, zlib

def _r(f, fmt):
    return struct.unpack(">" + fmt, f.read(struct.calcsize(">" + fmt)))[0]

def _payload(f, t):
    if t == 1: return _r(f, "b")
    if t == 2: return _r(f, "h")
    if t == 3: return _r(f, "i")
    if t == 4: return _r(f, "q")
    if t == 5: return _r(f, "f")
    if t == 6: return _r(f, "d")
    if t == 7: n = _r(f, "i"); return f.read(n)
    if t == 8: n = _r(f, "H"); return f.read(n).decode("utf-8", "replace")
    if t == 9:
        et = _r(f, "b"); n = _r(f, "i")
        return [_payload(f, et) for _ in range(n)]
    if t == 10:
        d = {}
        while True:
            ct = _r(f, "b")
            if ct == 0: return d
            name = f.read(_r(f, "H")).decode("utf-8", "replace")
            d[name] = _payload(f, ct)
    if t == 11: n = _r(f, "i"); return list(struct.unpack(">%di" % n, f.read(4 * n)))
    if t == 12: n = _r(f, "i"); return list(struct.unpack(">%dq" % n, f.read(8 * n)))
    raise ValueError("tag %d" % t)

def nbt(data):
    f = io.BytesIO(data)
    t = _r(f, "b"); f.read(_r(f, "H"))
    return _payload(f, t)

def level(world):
    return nbt(gzip.open(os.path.join(world, "level.dat")).read())

def chunks(path):
    with open(path, "rb") as fh:
        buf = fh.read()
    for i in range(1024):
        off = int.from_bytes(buf[i*4:i*4+3], "big"); cnt = buf[i*4+3]
        if not off or not cnt: continue
        o = off * 4096
        ln = struct.unpack(">i", buf[o:o+4])[0]; comp = buf[o+4]
        raw = buf[o+5:o+4+ln]
        data = zlib.decompress(raw) if comp == 2 else gzip.decompress(raw) if comp == 1 else raw
        yield nbt(data)

def blocks(chunk):
    """Yield (x, y, z, name, props) for every non-air block in a chunk."""
    cx, cz = chunk["xPos"], chunk["zPos"]
    for sec in chunk.get("sections", []):
        bs = sec.get("block_states")
        if not bs: continue
        pal = bs["palette"]
        if len(pal) == 1 and pal[0]["Name"] in ("minecraft:air",): continue
        sy = sec["Y"]
        if len(pal) == 1:
            idx = [0] * 4096
        else:
            bits = max(4, math.ceil(math.log2(len(pal))))
            per = 64 // bits; mask = (1 << bits) - 1
            idx = []
            for word in bs["data"]:
                w = word & 0xFFFFFFFFFFFFFFFF
                for k in range(per):
                    idx.append((w >> (k * bits)) & mask)
            idx = idx[:4096]
        for n, p in enumerate(idx):
            b = pal[p]; name = b["Name"]
            if name in ("minecraft:air", "minecraft:cave_air", "minecraft:void_air"): continue
            x = n & 15; z = (n >> 4) & 15; y = n >> 8
            yield cx*16 + x, sy*16 + y, cz*16 + z, name, b.get("Properties", {})


# --- typed NBT: every value is (tag_type, payload); lists are (tag_type 9, (elem_type, [payloads])) ---
def _tp(f, t):
    if t in (1, 2, 3, 4, 5, 6, 7, 8, 11, 12): return _payload(f, t)
    if t == 9:
        et = _r(f, "b"); n = _r(f, "i")
        return (et, [_tp(f, et) for _ in range(n)])
    if t == 10:
        d = {}
        while True:
            ct = _r(f, "b")
            if ct == 0: return d
            name = f.read(_r(f, "H")).decode("utf-8")
            d[name] = (ct, _tp(f, ct))
    raise ValueError(t)

def tnbt(data):
    f = io.BytesIO(data); t = _r(f, "b"); f.read(_r(f, "H"))
    return (t, _tp(f, t))

def _w(o, t, v):
    P = struct.pack
    if t == 1: o += P(">b", v)
    elif t == 2: o += P(">h", v)
    elif t == 3: o += P(">i", v)
    elif t == 4: o += P(">q", v)
    elif t == 5: o += P(">f", v)
    elif t == 6: o += P(">d", v)
    elif t == 7: o += P(">i", len(v)) + v
    elif t == 8: b = v.encode("utf-8"); o += P(">H", len(b)) + b
    elif t == 9:
        et, items = v
        o += P(">bi", et if items else 0, len(items))
        for it in items: _w(o, et, it)
    elif t == 10:
        for k, (ct, cv) in v.items():
            b = k.encode("utf-8"); o += P(">bH", ct, len(b)) + b; _w(o, ct, cv)
        o += b"\x00"
    elif t == 11: o += P(">i%di" % len(v), len(v), *v)
    elif t == 12: o += P(">i%dq" % len(v), len(v), *v)
    else: raise ValueError(t)

def write_tnbt(root):
    o = bytearray(); o += struct.pack(">bH", 10, 0); _w(o, 10, root[1]); return bytes(o)

def raw_chunks(path):
    with open(path, "rb") as fh:
        buf = fh.read()
    for i in range(1024):
        off = int.from_bytes(buf[i*4:i*4+3], "big"); cnt = buf[i*4+3]
        if not off or not cnt: continue
        o = off * 4096
        ln = struct.unpack(">i", buf[o:o+4])[0]; comp = buf[o+4]
        raw = buf[o+5:o+4+ln]
        yield zlib.decompress(raw) if comp == 2 else gzip.decompress(raw) if comp == 1 else raw


W, OUT = sys.argv[1], sys.argv[2]
X0, Y0, Z0, X1, Y1, Z1 = 6, -60, -13, 26, -55, 6   # inclusive box
SIZE = (X1 - X0 + 1, Y1 - Y0 + 1, Z1 - Z0 + 1)
inside = lambda x, y, z: X0 <= x <= X1 and Y0 <= y <= Y1 and Z0 <= z <= Z1

# writer round-trip check on every chunk we read
found, bes, ents = {}, {}, []
for r in glob.glob(W + "/region/*.mca"):
    for raw in raw_chunks(r):
        t = tnbt(raw)
        assert write_tnbt(t) == raw, "NBT writer round-trip failed"
        ch = nbt(raw)
        if ch.get("Status") != "minecraft:full": continue
        for x, y, z, n, pr in blocks(ch):
            if inside(x, y, z): found[(x, y, z)] = (n, pr)
        for be in t[1].get("block_entities", (9, (10, [])))[1][1]:
            x, y, z = be["x"][1], be["y"][1], be["z"][1]
            if inside(x, y, z): bes[(x, y, z)] = be
for r in glob.glob(W + "/entities/*.mca"):
    for raw in raw_chunks(r):
        for e in tnbt(raw)[1]["Entities"][1][1]:
            pos = [v for v in e["Pos"][1][1]]
            if inside(math.floor(pos[0]), math.floor(pos[1]), math.floor(pos[2])): ents.append(e)

# palette, air included so placing clears the space like a structure block would
palette, index, out_blocks = [], {}, []
for x in range(X0, X1 + 1):
    for y in range(Y0, Y1 + 1):
        for z in range(Z0, Z1 + 1):
            n, pr = found.get((x, y, z), ("minecraft:air", {}))
            key = (n, tuple(sorted(pr.items())))
            if key not in index:
                index[key] = len(palette)
                st = {"Name": (8, n)}
                if pr: st["Properties"] = (10, {k: (8, v) for k, v in sorted(pr.items())})
                palette.append(st)
            b = {"pos": (9, (3, [x - X0, y - Y0, z - Z0])), "state": (3, index[key])}
            be = bes.get((x, y, z))
            if be is not None:
                be = {k: v for k, v in be.items() if k not in ("x", "y", "z", "keepPacked")}
                if be["id"][1] == "banksystem:bank_terminal_block_entity":
                    be["banksystem"][1]["PlayerData"] = (9, (10, []))   # drops the player's UUID
                b["nbt"] = (10, be)
            out_blocks.append(b)

out_ents = []
for e in ents:
    e = {k: v for k, v in e.items() if k != "UUID"}
    px, py, pz = e["Pos"][1][1]
    rel = [px - X0, py - Y0, pz - Z0]
    out_ents.append({"pos": (9, (6, rel)), "blockPos": (9, (3, [math.floor(v) for v in rel])), "nbt": (10, e)})

dv = level(W)["Data"]["DataVersion"]
root = (10, {
    "DataVersion": (3, dv),
    "size": (9, (3, list(SIZE))),
    "palette": (9, (10, palette)),
    "blocks": (9, (10, out_blocks)),
    "entities": (9, (10, out_ents)),
})
with gzip.open(OUT, "wb") as f:
    f.write(write_tnbt(root))
print("DataVersion", dv, "size", SIZE, "palette", len(palette), "blocks", len(out_blocks),
      "block entities", len(bes), "entities", len(out_ents))
