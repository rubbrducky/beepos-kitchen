# -*- coding: utf-8 -*-
"""Post-render for the v3 sock+triple pass. For each re-rendered dish:
   pick newest ComfyUI render (matched by dish number, slug-agnostic) ->
   rembg cutout -> master PNG (art-src/masters/dish) + WebP (assets/dish, 640px q92).
   Then PRUNE orphaned old-slug webp/masters for those dish numbers.
   Run with the rembg venv python (has rembg + PIL)."""
import os, re, glob, io, json
from PIL import Image
from rembg import remove, new_session

REPO = r"C:\Users\gusta\OneDrive\Desktop\Claude\Beepos kitchen\Beepos kitchen"
SRC  = r"C:\Users\gusta\ComfyUI\output\beepo_food"
ASSET_DISH = os.path.join(REPO, "assets", "dish")
MASTER_DISH = os.path.join(REPO, "art-src", "masters", "dish")
os.makedirs(ASSET_DISH, exist_ok=True); os.makedirs(MASTER_DISH, exist_ok=True)
PAD, TGT, Q = 12, 640, 92

def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

d = json.load(open(os.path.join(REPO, 'dishes.json'), encoding='utf-8'))
# render list = all worm/sock dishes + all triples (must match patch_v3)
targets = [x for x in d['dishes'] if ('worm' in x['ids']) or (x['size'] == 3)]
print(f"processing {len(targets)} dishes")

sess = new_session("u2net")
done, missing = 0, []
for x in targets:
    n = x['n']; name_slug = slug(x['name']); base = f"{n:03d}-{name_slug}"
    cands = glob.glob(os.path.join(SRC, f"dish_{n:03d}_*_*.png"))
    if not cands:
        missing.append(n); continue
    latest = max(cands, key=os.path.getmtime)
    im = Image.open(latest).convert("RGBA")
    # master on-white
    im.convert("RGB").save(os.path.join(MASTER_DISH, base + ".png"))
    # cutout
    res = remove(im, session=sess)
    out = (Image.open(io.BytesIO(res)) if isinstance(res, (bytes, bytearray)) else res).convert("RGBA")
    bb = out.split()[-1].getbbox()
    if bb:
        l, t, r, b = bb
        out = out.crop((max(0, l-PAD), max(0, t-PAD), min(out.width, r+PAD), min(out.height, b+PAD)))
    w, h = out.size; s = TGT / max(w, h)
    if s < 1: out = out.resize((round(w*s), round(h*s)), Image.LANCZOS)
    out.save(os.path.join(ASSET_DISH, base + ".webp"), "WEBP", quality=Q, method=6)
    done += 1
    if done % 20 == 0: print(f"  [{done}/{len(targets)}]")

# ---- prune orphaned old-slug files for the re-rendered dish numbers --------
keep = {f"{x['n']:03d}-{slug(x['name'])}" for x in targets}
nums = {f"{x['n']:03d}" for x in targets}
pruned = []
for f in glob.glob(os.path.join(ASSET_DISH, "*.webp")) + glob.glob(os.path.join(MASTER_DISH, "*.png")):
    b = os.path.splitext(os.path.basename(f))[0]
    if b[:3] in nums and b not in keep:
        os.remove(f); pruned.append(os.path.basename(f))

print(f"\ndone: {done}  missing: {missing}")
print(f"pruned {len(pruned)} orphans:", pruned[:12], "..." if len(pruned) > 12 else "")
