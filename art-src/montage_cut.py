# -*- coding: utf-8 -*-
"""Verification sheets for the cutouts — pasted on a checkerboard so transparency shows.
Run with ComfyUI venv python (has Pillow)."""
import os, re, glob, json
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Users\gusta\ComfyUI\output\beepo_food"
CUT = os.path.join(OUT, "cutout")
SHEETS = os.path.join(OUT, "_sheets")
os.makedirs(SHEETS, exist_ok=True)
DISHES = r"C:\Users\gusta\OneDrive\Desktop\Claude\Beepos kitchen\Beepos kitchen\dishes.json"

d = json.load(open(DISHES, encoding="utf-8"))
ing_name = {i["id"]: i["name"] for i in d["ingredients"]}
dish_by_n = {x["n"]: x for x in d["dishes"]}
try:
    FB = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 16)
    FR = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 14)
except Exception:
    FB = FR = ImageFont.load_default()

THUMB, PAD, CAP = 230, 10, 40

def checker(w, h, s=16):
    img = Image.new("RGB", (w, h), (255, 255, 255))
    dr = ImageDraw.Draw(img)
    for y in range(0, h, s):
        for x in range(0, w, s):
            if (x//s + y//s) % 2:
                dr.rectangle([x, y, x+s, y+s], fill=(214, 214, 222))
    return img

def latest(pattern):
    fs = glob.glob(os.path.join(CUT, pattern))
    return sorted(fs)[-1] if fs else None

def cell(path, label, sub=""):
    c = Image.new("RGB", (THUMB + 2*PAD, THUMB + CAP + PAD), (248, 246, 250))
    dr = ImageDraw.Draw(c)
    board = checker(THUMB, THUMB)
    try:
        im = Image.open(path).convert("RGBA")
        im.thumbnail((THUMB, THUMB), Image.LANCZOS)
        board.paste(im, ((THUMB-im.width)//2, (THUMB-im.height)//2), im)
    except Exception as e:
        ImageDraw.Draw(board).text((6, 6), f"[missing]\n{e}", fill=(200, 0, 0), font=FR)
    c.paste(board, (PAD, PAD))
    y = THUMB + PAD + 2
    dr.text((PAD, y), label[:34], fill=(30, 20, 30), font=FB)
    if sub:
        dr.text((PAD, y+18), sub[:40], fill=(110, 90, 110), font=FR)
    return c

def grid(cells, cols, title, fname):
    if not cells:
        return
    cw, ch = cells[0].size
    rows = (len(cells)+cols-1)//cols
    TH = 46
    sheet = Image.new("RGB", (cols*cw, rows*ch+TH), (255, 255, 255))
    dr = ImageDraw.Draw(sheet)
    dr.rectangle([0, 0, sheet.width, TH], fill=(60, 45, 65))
    dr.text((14, 12), title, fill=(255, 255, 255), font=FB)
    for i, c in enumerate(cells):
        r, col = divmod(i, cols)
        sheet.paste(c, (col*cw, TH+r*ch))
    p = os.path.join(SHEETS, fname)
    sheet.save(p); print("wrote", p, sheet.size)

ing_ids = ["apple","banana","berry","egg","choco","cookie","icecream","worm","rainbow"]
grid([cell(latest(f"ing_{i}_*.png"), ing_name[i]) for i in ing_ids], 3,
     "CUTOUTS — 9 INGREDIENTS (on checkerboard = transparent)", "sheet_cut_ingredients.png")

ui = [("book_closed","Recipe book (closed)"),("book_open","Recipe book (open)"),
      ("book_icon","Book button icon"),("recipe_card","Recipe card"),("ingredient_board","Ingredient board")]
grid([cell(latest(f"ui_{k}_*.png"), lab) for k, lab in ui], 3,
     "CUTOUTS — UI DRAFTS", "sheet_cut_ui.png")

files = {int(re.search(r"dish_(\d+)_", os.path.basename(f)).group(1)): f
         for f in glob.glob(os.path.join(CUT, "dish_*.png"))}
PER = 36
nums = sorted(files)
pages = [nums[i:i+PER] for i in range(0, len(nums), PER)]
for pi, page in enumerate(pages, 1):
    cells = [cell(files[n], f"#{n} {dish_by_n[n]['name']}", dish_by_n[n]["verdict"]) for n in page]
    grid(cells, 6, f"CUTOUT DISHES (page {pi}/{len(pages)})  #{page[0]}-#{page[-1]}", f"sheet_cut_dishes_p{pi}.png")
print("done")
