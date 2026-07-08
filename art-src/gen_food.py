#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Beepo's Kitchen — Flux food-art generation driver.

Queues ingredient + completed-meal art to a local ComfyUI (Flux dev fp8) via its
HTTP API. No node-clicking. Mirrors the proven Beepo probe graph but drops the
character LoRA (we want the *house style*, not the robot) and renders square.

Prompts come from the game's own data (dishes.json) with the PLAN sec 3.4
master style suffix appended (the dish prompts only *reference* the suffix; the
literal text lives here).

Usage:
  python gen_food.py --dry-run                 # print prompts, POST nothing (safe anytime)
  python gen_food.py --mode ingredients        # 9 ingredient characters
  python gen_food.py --mode pilot              # 9 ingredients + curated pilot dishes
  python gen_food.py --mode dishes --dishes all
  python gen_food.py --mode dishes --dishes 22,32,41

Outputs land in  ComfyUI/output/beepo_food/  (ingredient / dish subprefixes).
"""
import argparse, json, os, sys, time, urllib.request, urllib.error, zlib, re

# ---- config ---------------------------------------------------------------
COMFY   = "http://127.0.0.1:8188"
DISHES  = r"C:\Users\gusta\OneDrive\Desktop\Claude\Beepos kitchen\Beepos kitchen\dishes.json"
CKPT    = "flux1-dev-fp8.safetensors"
STEPS   = 24
GUID    = 3.5           # FluxGuidance (matches the Beepo probe)
SAMPLER = "euler"
SCHED   = "simple"
W = H   = 1024          # square: centered single subject, ideal for stickers

# Style (PLAN sec 3.4, nudged to semi-3D per Gustav's reference burger 2026-07-05).
# Appended to every prompt. Leans "cute semi-3D render" over flat sticker.
MASTER = ("adorable kawaii toddler picture-book illustration, cute semi-3D render with soft "
          "volume and depth, plump rounded chunky shapes, thick dark charcoal outline, glossy "
          "highlights, warm soft lighting, pastel candy palette, big sparkly eyes, rosy cheeks, "
          "soft cel shading with smooth gradients, centered single subject, plain flat white "
          "background, appetizing, high quality, super cute")
# Flux dev at cfg 1.0 ignores negatives (empty cond), same as the Beepo graph.
NEG = ""

# Curated pilot: 3 verdict tiers x singles/pairs/triples + both bespoke burgers
# + a hero (banana split) + fallback "bowl-of-X" looks. 10 dishes.
PILOT_DISHES = [7, 8, 9, 22, 32, 41, 44, 46, 51, 52]

# Per-ingredient prompt bodies (PLAN sec 3.4 ingredient template; silly ones lean in).
ING_BODY = {
    "apple":    "a single cute red apple character with a happy smiling face, big shiny eyes, rosy cheeks, plump and glossy, one object centered",
    "banana":   "a single cute banana character with a happy smiling face, big shiny eyes, rosy cheeks, plump and glossy, one object centered",
    "berry":    "a single cute plump round blueberry character, deep blue with a tiny leafy star crown, happy smiling face, big shiny eyes, rosy cheeks, plump and glossy, one object centered",
    "egg":      "a single cute soft egg character with a happy smiling face, big shiny eyes, rosy cheeks, plump and glossy, one object centered",
    "choco":    "a single cute chocolate bar character with a happy smiling face, big shiny eyes, rosy cheeks, plump and glossy, one object centered",
    "cookie":   "a single cute chocolate-chip cookie character with a happy smiling face, big shiny eyes, rosy cheeks, plump and glossy, one object centered",
    "icecream": "a single cute ice cream scoop in a cone character with a happy smiling face, big shiny eyes, rosy cheeks, plump and glossy, one object centered",
    "worm":     "a single friendly wiggly green worm poking up with a cheeky smile, big shiny eyes, rosy cheeks, plump and glossy, one object centered",
    "rainbow":  "a single magical rainbow with a happy face, sparkling and glowing, big shiny eyes, rosy cheeks, one object centered",
}

# New-mechanics UI art (draft only — recipe book + ingredient-list feature).
# Flux tends to scribble on "blank" surfaces; prompts say no text, treat as drafts.
UI_ASSETS = {
    "book_closed":      "a cute chunky closed recipe cookbook standing upright, warm honey-brown hardcover with a golden fork-and-spoon emblem and a little red heart, a red bookmark ribbon, rounded corners, soft shadow, one object centered",
    "book_open":        "a cute open cookbook viewed from the front, chunky rounded cover, two blank cream-colored pages, a red bookmark ribbon, soft shadow, empty pages with no text and no writing, one object centered",
    "book_icon":        "a small simple bold cute closed recipe book button icon, honey-brown cover with a golden fork-and-spoon emblem, clean and clear, one object centered",
    "recipe_card":      "a cute blank recipe card, rounded cream parchment with a soft scalloped border and a tiny white chef-hat emblem at the top, completely empty, no text and no writing, one object centered",
    "spoon":            "a cute chunky wooden cooking spoon character with a tiny happy smiling face and rosy cheeks on the bowl of the spoon, warm honey wood, plump rounded handle, glossy, one object centered",
    "pot":              "a cute chunky cooking pot, soft steel blue-grey with a wide open top showing an empty interior, two round side handles, plump rounded shape, front three-quarter view, no shadow",
    "stove":            "a low wide cute toy kitchen stove, cream enamel with rounded corners, two small burner circles on top and two round pastel knobs on the front, simple, front view, no shadow (ship only the top crop above the oven door)",
    "ingredient_board": "a cute empty wooden menu board with rounded corners and a warm painted frame, blank flat surface, no text and no writing, ready to hold little food pictures, one object centered",
}

# Shared vessel sprites (HANDOFF sec 5.2) — rendered once; food sprites sit inside them.
# Vessels use their OWN style (NOT the kawaii master suffix, whose "big sparkly eyes, rosy
# cheeks" forced faces + fillings onto them). Empty, faceless, product-shot.
VESSEL_STYLE = ("cute semi-3D render, plump rounded chunky shape, thick dark charcoal outline, "
                "glossy highlights, soft warm lighting, pastel palette, completely empty with "
                "nothing inside, no face, no eyes, no mouth, no food, no contents, clean simple "
                "product illustration, centered single object, plain flat white background")
VESSELS = {
    "bowl":  "an empty rounded soup bowl, glossy pastel ceramic with a soft rim, gentle three-quarter front view, hollow empty interior",
    "plate": "an empty shallow round dinner plate, glossy pastel ceramic, gentle three-quarter front view, nothing on it",
    "glass": "an empty clear drinking glass, transparent, nothing inside, no liquid",
    "jar":   "an empty clear glass jar with a lid, transparent, nothing inside, no contents",
    # "stick": DROPPED — Flux stubbornly renders popsicles for any stick shape (2 re-rolls failed);
    #          the pops dish keeps the existing SVG stick instead. Not worth an AI sprite.
}

# ---- helpers --------------------------------------------------------------
def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def stable_seed(key):
    return zlib.crc32(key.encode("utf-8")) & 0x7fffffff

def clean_dish_prompt(p):
    # Drop the literal placeholder; MASTER suffix supplies the style.
    p = p.replace("(apply PLAN sec 3.4 master style suffix + negative)", "")
    # Strip the redundant style boilerplate — also removes 'sticker style' (die-cut white border).
    p = re.sub(r'Kawaii toddler picture-book sticker style.*$', '', p, flags=re.I)
    # FOOD-ONLY (HANDOFF sec 5): strip vessel language so the food sits inside a
    # separately-rendered shared vessel (B#14 four-layer split — Beepo never eats the bowl).
    p = re.sub(r'^\s*a small (plate or bowl|bowl|plate|cup|glass)\s+(containing|of)\s+', '', p, flags=re.I)
    p = re.sub(r'\bserved (in|on) a (small )?(plate or bowl|bowl|plate|cup|glass)\b', '', p, flags=re.I)
    p = re.sub(r'\b(in|on) a (small )?(plate or bowl|bowl|plate|cup|glass)\b', '', p, flags=re.I)
    p = re.sub(r"\s{2,}", " ", p).replace(" ,", ",").replace(" .", ".").strip(" ,.")
    # Front-load the food-only framing (Flux honours positive framing better than "no X").
    # v2: "food characters forming one dish" (not "single portion") — prompts are now scenes.
    return ("cute food characters forming one little dish, floating on a pure white background, "
            "nothing underneath them, no plate no bowl no dish, " + p + ", centered food cut-out")

def full_prompt(body):
    return f"{body.rstrip('. ')}. {MASTER}"

def workflow(prompt_text, seed, prefix):
    """API-format graph: Flux dev fp8, no LoRA. Node ids mirror the Beepo probe."""
    return {
        "4": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": CKPT}},
        "6": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt_text, "clip": ["4", 1]}},
        "22": {"class_type": "FluxGuidance", "inputs": {"guidance": GUID, "conditioning": ["6", 0]}},
        "7": {"class_type": "CLIPTextEncode", "inputs": {"text": NEG, "clip": ["4", 1]}},
        "5": {"class_type": "EmptySD3LatentImage", "inputs": {"width": W, "height": H, "batch_size": 1}},
        "3": {"class_type": "KSampler", "inputs": {
            "seed": seed, "steps": STEPS, "cfg": 1.0, "sampler_name": SAMPLER,
            "scheduler": SCHED, "denoise": 1.0,
            "model": ["4", 0], "positive": ["22", 0], "negative": ["7", 0], "latent_image": ["5", 0]}},
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["3", 0], "vae": ["4", 2]}},
        "9": {"class_type": "SaveImage", "inputs": {"filename_prefix": prefix, "images": ["8", 0]}},
    }

def post(path, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(COMFY + path, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))

def get(path):
    with urllib.request.urlopen(COMFY + path, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))

def queue_prompt(graph):
    return post("/prompt", {"prompt": graph})["prompt_id"]

# ---- build the job list ---------------------------------------------------
def build_jobs(mode, dish_arg):
    d = json.load(open(DISHES, encoding="utf-8"))
    ing_by_id = {i["id"]: i for i in d["ingredients"]}
    dishes = {x["n"]: x for x in d["dishes"]}
    jobs = []  # (label, prefix, prompt)

    def add_ingredients():
        for iid, ing in ing_by_id.items():
            jobs.append((f"ing:{iid}", f"beepo_food/ing_{iid}", full_prompt(ING_BODY[iid])))

    def add_dishes(nums):
        for n in nums:
            x = dishes[n]
            prefix = f"beepo_food/dish_{n:03d}_{slug(x['name'])}"
            jobs.append((f"dish#{n}:{x['name']}", prefix, full_prompt(clean_dish_prompt(x["image_prompt"]))))

    def add_ui():
        for k, body in UI_ASSETS.items():
            jobs.append((f"ui:{k}", f"beepo_food/ui_{k}", full_prompt(body)))

    def add_vessels():
        for k, body in VESSELS.items():
            vp = f"{body.rstrip('. ')}. {VESSEL_STYLE}"    # vessel style, NOT the kawaii master suffix
            jobs.append((f"vessel:{k}", f"beepo_food/vessel_{k}", vp))

    all_dishes = sorted(dishes)
    if mode == "ingredients":
        add_ingredients()
    elif mode == "ui":
        add_ui()
    elif mode == "vessels":
        add_vessels()
    elif mode == "regen":             # food-only re-render: 129 dishes (no vessels) + vessel library
        add_dishes(all_dishes); add_vessels()
    elif mode == "pilot":
        add_ingredients(); add_dishes(PILOT_DISHES)
    elif mode == "full":              # the whole catalog: 9 ingredients + 129 dishes
        add_ingredients(); add_dishes(all_dishes)
    elif mode == "all":               # everything: ingredients + dishes + UI art
        add_ingredients(); add_dishes(all_dishes); add_ui()
    elif mode == "dishes":
        nums = all_dishes if dish_arg == "all" else [int(x) for x in dish_arg.split(",") if x.strip()]
        add_dishes(nums)
    else:
        sys.exit(f"unknown mode {mode}")
    return jobs

# ---- run ------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="all", choices=["ingredients", "ui", "vessels", "pilot", "full", "all", "regen", "dishes"])
    ap.add_argument("--dishes", default="all", help="'all' or comma list of dish numbers (mode=dishes)")
    ap.add_argument("--dry-run", action="store_true", help="print prompts, POST nothing")
    args = ap.parse_args()

    jobs = build_jobs(args.mode, args.dishes)
    print(f"[gen_food] mode={args.mode}  jobs={len(jobs)}  {W}x{H}  steps={STEPS}  guid={GUID}\n")
    for label, prefix, prompt in jobs:
        print(f"  - {label}\n      -> {prefix}\n      {prompt[:150]}{'...' if len(prompt)>150 else ''}\n")

    if args.dry_run:
        print("[dry-run] nothing queued.")
        return

    # guard: refuse to queue if server unreachable
    try:
        get("/queue")
    except Exception as e:
        sys.exit(f"[gen_food] ComfyUI not reachable at {COMFY}: {e}")

    ids = {}
    for label, prefix, prompt in jobs:
        pid = queue_prompt(workflow(prompt, stable_seed(prefix), prefix))
        ids[pid] = (label, prefix)
        print(f"[queued] {label}  ({pid})")

    print(f"\n[gen_food] {len(ids)} queued. polling until done...")
    done = {}
    manifest = []
    t0 = time.time()
    MAX_WAIT = 3600  # hard stop so one stuck image can't hang forever
    while len(done) < len(ids) and time.time() - t0 < MAX_WAIT:
        time.sleep(4)
        for pid in list(ids):
            if pid in done:
                continue
            try:
                h = get(f"/history/{pid}")
            except Exception:
                continue
            if pid not in h:
                continue
            st_str = h[pid].get("status", {}).get("status_str", "")
            completed = h[pid].get("status", {}).get("completed", False)
            if completed or "outputs" in h[pid] or st_str == "error":
                label, prefix = ids[pid]
                imgs = [im["filename"] for node in h[pid].get("outputs", {}).values()
                        for im in node.get("images", [])]
                done[pid] = (label, imgs)
                manifest.append({"label": label, "prefix": prefix, "files": imgs})
                tag = "ERROR" if (st_str == "error" or not imgs) else "done"
                print(f"[{tag} {len(done)}/{len(ids)}] {label}  ->  {', '.join(imgs) or '(no file)'}")
    if len(done) < len(ids):
        print(f"[warn] stopped with {len(ids)-len(done)} unfinished after {MAX_WAIT}s")
    out_dir = r"C:\Users\gusta\ComfyUI\output\beepo_food"
    try:
        with open(os.path.join(out_dir, "_manifest.json"), "w", encoding="utf-8") as f:
            json.dump(sorted(manifest, key=lambda m: m["prefix"]), f, indent=2)
    except Exception as e:
        print(f"[warn] manifest not written: {e}")
    print(f"\n[gen_food] complete in {time.time()-t0:.0f}s. {len(done)} images in ComfyUI/output/beepo_food/")

if __name__ == "__main__":
    main()
