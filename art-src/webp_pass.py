# -*- coding: utf-8 -*-
"""Ship-optimization: downscale the transparent cutouts in assets/ to a generous target
size and encode WebP (q92, alpha) — visually lossless, ~1/6 the weight. Removes the shipped
PNGs (the on-white masters stay in art-src/masters/). Run with ComfyUI venv python (Pillow)."""
import os, glob
from PIL import Image

ASSETS = r"C:\Users\gusta\OneDrive\Desktop\Claude\Beepos kitchen\Beepos kitchen\assets"
# longest-edge target px — generous (well above on-screen size) since we err toward quality.
TARGETS = {"ing": 384, "dish": 640, "vessel": 448, "ui": 512}
Q = 92   # lossy WebP quality (with alpha) — visually lossless for this art

def mb(n): return f"{n/1048576:.1f} MB"

before = after = 0
for grp, tgt in TARGETS.items():
    d = os.path.join(ASSETS, grp)
    pngs = glob.glob(os.path.join(d, "*.png"))
    gb = ga = 0
    for f in pngs:
        before += os.path.getsize(f); gb += os.path.getsize(f)
        im = Image.open(f).convert("RGBA")
        w, h = im.size
        s = tgt / max(w, h)
        if s < 1:
            im = im.resize((max(1, round(w*s)), max(1, round(h*s))), Image.LANCZOS)
        out = f[:-4] + ".webp"
        im.save(out, "WEBP", quality=Q, method=6)   # method 6 = best compression
        after += os.path.getsize(out); ga += os.path.getsize(out)
        os.remove(f)   # ship WebP only; on-white masters remain in art-src/masters/
    print(f"{grp:8} {len(pngs):3} files  {mb(gb)} -> {mb(ga)}  (target {tgt}px)")
print(f"\nTOTAL assets: {mb(before)} -> {mb(after)}  ({after/before*100:.0f}% of original)")
