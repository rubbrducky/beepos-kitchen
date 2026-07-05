# -*- coding: utf-8 -*-
"""Build labelled contact sheets from the beepo_food outputs. Run with ComfyUI venv python."""
import os, re, glob, json, textwrap
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Users\gusta\ComfyUI\output\beepo_food"
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
BG = (248, 246, 250)

def latest(pattern):
    fs = glob.glob(os.path.join(OUT, pattern))
    return sorted(fs)[-1] if fs else None

def cell(img_path, label, sub=""):
    c = Image.new("RGB", (THUMB + 2*PAD, THUMB + CAP + PAD), BG)
    dr = ImageDraw.Draw(c)
    try:
        im = Image.open(img_path).convert("RGBA")
        im.thumbnail((THUMB, THUMB), Image.LANCZOS)
        bg = Image.new("RGBA", (THUMB, THUMB), (255, 255, 255, 255))
        bg.paste(im, ((THUMB - im.width)//2, (THUMB - im.height)//2), im)
        c.paste(bg.convert("RGB"), (PAD, PAD))
    except Exception as e:
        dr.text((PAD, PAD), f"[missing]\n{e}", fill=(200, 0, 0), font=FR)
    y = THUMB + PAD + 2
    dr.text((PAD, y), label[:34], fill=(30, 20, 30), font=FB)
    if sub:
        dr.text((PAD, y + 18), sub[:40], fill=(110, 90, 110), font=FR)
    return c

def grid(cells, cols, title, fname):
    if not cells:
        return
    cw, ch = cells[0].size
    rows = (len(cells) + cols - 1)//cols
    TH = 46
    sheet = Image.new("RGB", (cols*cw, rows*ch + TH), (255, 255, 255))
    dr = ImageDraw.Draw(sheet)
    dr.rectangle([0, 0, sheet.width, TH], fill=(60, 45, 65))
    dr.text((14, 12), title, fill=(255, 255, 255), font=FB)
    for i, c in enumerate(cells):
        r, col = divmod(i, cols)
        sheet.paste(c, (col*cw, TH + r*ch))
    p = os.path.join(SHEETS, fname)
    sheet.save(p)
    print("wrote", p, sheet.size)

# --- ingredients ---
ing_ids = ["apple","banana","berry","egg","choco","cookie","icecream","worm","rainbow"]
cells = [cell(latest(f"ing_{i}_*.png"), ing_name[i]) for i in ing_ids]
grid(cells, 3, "BEEPO'S KITCHEN — 9 INGREDIENTS", "sheet_ingredients.png")

# --- UI ---
ui = [("book_closed","Recipe book (closed)"),("book_open","Recipe book (open)"),
      ("book_icon","Book button icon"),("recipe_card","Recipe card (blank)"),
      ("ingredient_board","Ingredient board")]
cells = [cell(latest(f"ui_{k}_*.png"), lab) for k, lab in ui]
grid(cells, 3, "NEW-MECHANICS UI (DRAFTS)", "sheet_ui.png")

# --- dishes, paginated, ordered by number ---
VEMO = {"Yummy": "Yummy", "Magical": "Magical", "Yucky": "Yucky"}
files = {int(re.search(r"dish_(\d+)_", os.path.basename(f)).group(1)): f
         for f in glob.glob(os.path.join(OUT, "dish_*.png"))}
PER = 36
nums = sorted(files)
pages = [nums[i:i+PER] for i in range(0, len(nums), PER)]
for pi, page in enumerate(pages, 1):
    cells = []
    for n in page:
        x = dish_by_n[n]
        cells.append(cell(files[n], f"#{n} {x['name']}", VEMO.get(x["verdict"], x["verdict"])))
    grid(cells, 6, f"DISHES  (page {pi}/{len(pages)})  #{page[0]}-#{page[-1]}", f"sheet_dishes_p{pi}.png")

print("done")
