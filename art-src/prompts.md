# Beepo's Kitchen — AI art pipeline (v0 draft, 2026-07-05)

How the ingredient / dish / UI art was generated. Companion to PLAN.md §3.

## Model & settings (validated)
- **Base:** `flux1-dev-fp8.safetensors` via ComfyUI HTTP API (`/prompt`). **No LoRA** — the
  `beepo_flux_v2` character LoRA is the robot, wrong for food; house style comes from the suffix.
- **Sampler:** 1024×1024, 24 steps, euler / simple, FluxGuidance 3.5, cfg 1.0, empty negative
  (Flux ignores negatives at cfg 1). ~12 s/image on a 5090; full 143-image batch ≈ 29 min.

## Style suffix (appended to every prompt)
PLAN §3.4 master suffix, **nudged to semi-3D** per Gustav's reference burger (2026-07-05):

> adorable kawaii toddler picture-book illustration, cute semi-3D render with soft volume and
> depth, plump rounded chunky shapes, thick dark charcoal outline, glossy highlights, warm soft
> lighting, pastel candy palette, big sparkly eyes, rosy cheeks, soft cel shading with smooth
> gradients, centered single subject, plain flat white background, appetizing, high quality, super cute

Dish prompts come from `../dishes.json` (`image_prompt`) — but they only *reference* the suffix
(`(apply PLAN sec 3.4 …)`), so the driver strips that literal text and appends the real suffix.

## Scripts
- **`gen_food.py`** — builds prompts + queues to ComfyUI. Modes: `ingredients`, `ui`, `pilot`,
  `full` (9 ing + 129 dishes), `all` (+5 UI), `dishes --dishes 1,9,…|all`. Writes to
  `ComfyUI/output/beepo_food/`.
- **`cutout.py`** — rembg `u2net` background removal → transparent, tight-trimmed cutouts.
- **`montage.py` / `montage_cut.py`** — labelled contact sheets (white / checkerboard).

## Layout in this repo
- `../assets/{ing,dish,ui}/` — transparent cutouts, clean names (game-ready).
- `masters/{ing,dish,ui}/` — on-white originals (PLAN §3.3 masters).
- `sheets/`, `manifest.json` — review artifacts.

## ⚠️ v0 caveat — dishes are vessel-baked (must regenerate food-only)
Per **HANDOFF-2026-07-05.md §5**, dish renders should be **food-only** (`"food only, no bowl, no
plate, isolated"`) with vessels as a shared ~6-sprite library, because the B#14 four-layer split
means the bowl is never eaten. These v0 dishes have the bowl/plate baked in — lovely as a draft,
but re-render food-only before real integration. Ingredients (standalone) and UI are unaffected.

## Follow-ups
- WebP + downscale to the <4 MB asset budget (PLAN §3.3) — masters are heavy.
- Game integration: swap `iconSVG()` → `<img>` (PLAN §3.6).
- Optional rerolls: UI `ingredient_board` reads as a cracker; `book_icon` is a character not a flat icon.
- Tighten loose dishes (e.g. Banana Split → generic swirl) via ControlNet-from-SVG if wanted.
