# -*- coding: utf-8 -*-
"""Background-removal pass: beepo_food/*.png -> transparent, tight-trimmed cutouts in cutout/.
Run with the rembg venv python. CPU, non-destructive (originals untouched)."""
import os, glob, io, sys
from PIL import Image
from rembg import remove, new_session

SRC = r"C:\Users\gusta\ComfyUI\output\beepo_food"
DST = os.path.join(SRC, "cutout")
os.makedirs(DST, exist_ok=True)
PAD = 12  # px of transparent margin around content (PLAN sec 3.3: tight but not clipped)

session = new_session("u2net")  # solid general saliency; good for single centered subjects

def cut(path):
    im = Image.open(path).convert("RGBA")
    res = remove(im, session=session)
    out = (Image.open(io.BytesIO(res)) if isinstance(res, (bytes, bytearray)) else res).convert("RGBA")
    bbox = out.split()[-1].getbbox()  # bbox of non-transparent alpha
    if bbox:
        l, t, r, b = bbox
        l, t = max(0, l - PAD), max(0, t - PAD)
        r, b = min(out.width, r + PAD), min(out.height, b + PAD)
        out = out.crop((l, t, r, b))
    out.save(os.path.join(DST, os.path.basename(path)))
    return out.size

files = sorted(
    glob.glob(os.path.join(SRC, "ing_*.png")) +
    glob.glob(os.path.join(SRC, "dish_*.png")) +
    glob.glob(os.path.join(SRC, "ui_*.png"))
)
print(f"cutting {len(files)} images -> {DST}")
for i, f in enumerate(files, 1):
    try:
        sz = cut(f)
    except Exception as e:
        print(f"  [ERR] {os.path.basename(f)}: {e}"); continue
    if i % 20 == 0 or i == len(files):
        print(f"  [{i}/{len(files)}] {os.path.basename(f)} -> {sz}")
print("done")
