# -*- coding: utf-8 -*-
"""Cutout the sockh_NNN test renders -> REPO/sock_test/ (webp, art-map-compatible
   names) WITHOUT touching shipped assets. Then build 2 review montages."""
import os, re, glob, io, json
from PIL import Image, ImageDraw, ImageFont
from rembg import remove, new_session

REPO = r"C:\Users\gusta\OneDrive\Desktop\Claude\Beepos kitchen\Beepos kitchen"
SRC  = r"C:\Users\gusta\ComfyUI\output\beepo_food"
TEST = os.path.join(REPO, "sock_test"); os.makedirs(TEST, exist_ok=True)
PAD, TGT, Q = 12, 640, 92
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

d = json.load(open(os.path.join(REPO,'dishes.json'), encoding='utf-8'))
socks = [x for x in d['dishes'] if 'worm' in x['ids']]
sess = new_session("u2net")
done, missing, made = [], [], {}
for x in socks:
    n = x['n']; base = f"{n:03d}-{slug(x['name'])}"
    cands = glob.glob(os.path.join(SRC, f"sockh_{n:03d}_*.png"))
    if not cands: missing.append(n); continue
    latest = max(cands, key=os.path.getmtime)
    im = Image.open(latest).convert("RGBA")
    res = remove(im, session=sess)
    out = (Image.open(io.BytesIO(res)) if isinstance(res,(bytes,bytearray)) else res).convert("RGBA")
    bb = out.split()[-1].getbbox()
    if bb:
        l,t,r,b = bb
        out = out.crop((max(0,l-PAD),max(0,t-PAD),min(out.width,r+PAD),min(out.height,b+PAD)))
    w,h = out.size; s = TGT/max(w,h)
    if s<1: out = out.resize((round(w*s),round(h*s)), Image.LANCZOS)
    out.save(os.path.join(TEST, base+".webp"), "WEBP", quality=Q, method=6)
    made[n] = os.path.join(TEST, base+".webp"); done.append(n)

print(f"cut {len(done)} -> {TEST}   missing: {missing}")

# ---- review montages (2 sheets) --------------------------------------------
def sheet(items, path, cols=4):
    cell=280; pad=8; rows=(len(items)+cols-1)//cols
    W=cols*cell+(cols+1)*pad; H=rows*(cell+26)+(rows+1)*pad
    sh=Image.new("RGB",(W,H),(247,247,249)); dr=ImageDraw.Draw(sh)
    try: f=ImageFont.truetype("arialbd.ttf",14)
    except: f=ImageFont.load_default()
    for i,(n,name) in enumerate(items):
        r,c=divmod(i,cols); x=pad+c*(cell+pad); y=pad+r*(cell+26+pad)
        p=made.get(n)
        if p:
            im=Image.open(p).convert("RGBA"); im.thumbnail((cell,cell))
            bg=Image.new("RGBA",(cell,cell),(255,255,255,255))
            bg.alpha_composite(im,((cell-im.width)//2,(cell-im.height)//2))
            sh.paste(bg.convert("RGB"),(x,y+26))
        dr.text((x+3,y+5),f"#{n} {name}"[:30],fill=(20,20,20),font=f)
    sh.save(path); print(path)

items=[(x['n'], x['name'].replace('Sock','Sk').replace(' ','')) for x in socks if x['n'] in made]
half=(len(items)+1)//2
SC=r"C:\Users\gusta\AppData\Local\Temp\claude\C--Users-gusta-OneDrive-Desktop-Claude-Beepos-kitchen-Beepos-kitchen\a97d3c2e-19c4-45d4-8ee3-a484ad4b5093\scratchpad"
sheet(items[:half], os.path.join(SC,"sockhero_1.png"))
sheet(items[half:], os.path.join(SC,"sockhero_2.png"))
