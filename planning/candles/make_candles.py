"""Draws the pixel candlestick charts used as decoration on the site.

    python planning/candles/make_candles.py

header-candles.svg   top bar, wide, one rising chart, shown once (no repeat)
heading-candles.svg  under each h2, a short chart that repeats; it ends at the price it
                     started at, so the repeat has no jump

Rules every chart follows (checked below): each candle opens at the previous close,
green = close above open, red = below, the wick reaches at least to the body's top and bottom.
"""
import random
from pathlib import Path

OUT = Path(__file__).resolve().parents[2] / "docs/assets/images/shared"
GREEN, RED = "#32cc6f", "#e74c3c"


def closes(n, seed, drift, vol, pull, loop):
    """n+1 prices (start + n closes) that swing around a slowly rising line, so the swings stay
    big next to the whole range (pull: how hard it returns to the line). loop=True bends it to end
    where it began."""
    rnd = random.Random(seed)
    p = [0.0]
    for i in range(n):
        p.append(p[-1] + rnd.gauss(drift, vol) - pull * (p[-1] - drift * i))
    if loop:
        p = [v - p[-1] * i / n for i, v in enumerate(p)]
    return p


def svg(n, step, body, height, margin, seed, drift, vol, pull, loop):
    rnd = random.Random(seed + 1)
    p = closes(n, seed, drift, vol, pull, loop)
    lo, hi = min(p), max(p)
    # price -> pixel row, rounded once per price, so a close and the next open share a row
    y = [round(height - margin - (v - lo) / (hi - lo) * (height - 2 * margin)) for v in p]
    if loop:
        y[-1] = y[0]
    rects, candles = [], []
    for i in range(n):
        o, c = y[i], y[i + 1]
        top, bot = min(o, c), max(o, c)
        wt = max(0, top - rnd.randint(1, margin))
        wb = min(height, bot + rnd.randint(1, margin))
        col = GREEN if c <= o else RED          # smaller row = higher price
        x = i * step + (step - body) // 2
        w = 2 if body >= 6 else 1
        rects.append(f'<rect x="{x + (body - w) // 2}" y="{wt}" width="{w}" height="{wb - wt}" fill="{col}"/>')
        rects.append(f'<rect x="{x}" y="{top}" width="{body}" height="{max(bot - top, 1)}" fill="{col}"/>')
        candles.append((o, c, wt, wb, col))
    check(candles, loop)
    w = n * step
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" '
            f'shape-rendering="crispEdges">' + "".join(rects) + "</svg>\n")


def check(candles, loop):
    for i, (o, c, wt, wb, col) in enumerate(candles):
        assert wt <= min(o, c) and wb >= max(o, c), f"candle {i}: wick shorter than body"
        assert col == (GREEN if c <= o else RED), f"candle {i}: wrong colour"
        if i:
            assert o == candles[i - 1][1], f"candle {i}: opens at {o}, previous closed at {candles[i - 1][1]}"
    if loop:
        assert candles[0][0] == candles[-1][1], "repeating chart does not end where it starts"


if __name__ == "__main__":
    (OUT / "header-candles.svg").write_text(
        svg(n=80, step=24, body=12, height=96, margin=10, seed=11, drift=0.05, vol=1.0, pull=0.5, loop=False), encoding="utf-8")
    (OUT / "heading-candles.svg").write_text(
        svg(n=32, step=9, body=6, height=20, margin=3, seed=5, drift=0.0, vol=1.0, pull=0.9, loop=True), encoding="utf-8")
    print("written to", OUT)
