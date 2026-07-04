# Beepo's Kitchen — Redesign Plan (handoff to Sonnet)

**Goal:** make the game *more fun*, *more streamlined*, and *cuter*.
**Direction chosen by the owner (Gustav):**
- **Art:** full AI-art overhaul using **ComfyUI** (installed on this machine).
- **Audience:** toddlers / preschool, **ages 2–5**. Sensory delight, **no fail states**, endless play.
- **Build:** an **assets folder / small build is allowed** (no longer required to be a single file).

This document is the brief. It explains the current game, the target experience, the exact art pipeline, a finalized feature/animation spec, the proposed project structure, and a batched plan (including the publishing workstream). Read it top-to-bottom before touching code.

**Two things this revision locks in:**

- **Fun before art.** The gameplay, animations, sound, and "feel" are finalized as **Milestone 1 (Section 4)** and built entirely on the *existing SVG art*. Because the later art swap happens *underneath* the same DOM wrappers and CSS classes (§3.6), the AI-art overhaul becomes a pure **reskin** of an already-approved game. Nothing in Milestone 1 needs new art. Ship a fully fun, playable build first; generate art second.
- **What runs where.** All coding is Sonnet's. The ComfyUI *image generation* itself runs on Gustav's machine (its GPU) — Sonnet sets it up, curates, optimizes, and integrates, but the "press generate" step happens host-side. See the Division of Labor note below.

**Do not mass-generate art until Milestone 1 is signed off and the Beepo style pilot is approved.**

### Division of labor — what Sonnet runs vs. what runs on your machine

Be clear-eyed about this. **All of the coding is fully Sonnet's** — the refactor, every Milestone 1 feature, animations, sound, the SVG→PNG exporter, curating outputs, PNG optimization, and wiring the finished art into the game.

The **one step Sonnet cannot execute from its sandbox is the ComfyUI image generation itself.** ComfyUI needs your machine's GPU and runs as a local app/server the sandbox can't reach, so the actual "generate" happens host-side. Realistic options, best first:

- **Sonnet hands you a one-click workflow + prompt sheet; you run the batch** in ComfyUI and drop the PNGs into `assets/` (or a watched folder). Fastest and most reliable — Sonnet does everything before and after.
- **Sonnet drives the ComfyUI web UI via the Claude-in-Chrome extension** (open `localhost:8188`, queue prompts). Works, but clicking a node graph for ~60 assets is slow — fine for the small pilot, tedious for the full batch.
- **Computer-use** (screenshot + click the desktop app) — same trade-off, slower still.

Net: treat Sonnet as the engineer/art-director who hands you a press-the-button workflow, then takes the raw PNGs the rest of the way. **Milestone 1 has none of this dependency — it is 100% Sonnet, start to finish.**

---

## 0. BUILD STATUS (2026-07-04)

**Batches 0–4 (§8) are built and committed.** The playable Milestone-1 game is `index.html` + `game.js` + `styles.css` + `dishes.js`; the original one-file game lives on as `beepos-kitchen.legacy.html` (git history in the folder). Playtest revisions already folded in: **pointerdown input** (multi-touch overlapping flyers — iOS suppresses synthesized clicks during multi-touch), **tap-the-pot stirring** (no stir button; see B#3), pot-glow + fast hand-nudge stir cues, **visual hierarchy** (stove muted to counter-wood, pot enlarged + idle breathe), **robot-ier Beepo SVG** (segmented head/torso, screen face, tread feet, grippers, visible antenna), and **burger dishes** (cookie+egg = Beepo Burger w/ bespoke `dish-burger` symbol; cookie+worm = Wiggly Worm Burger). **Waiting on the Batch 5 device-test gate. The art track (§3) has not started.**

Later same-day playtest rounds: proper index-finger guide hand (first draft read as a rude gesture); icon-only shelf (80px food, labels removed); icon-only circular Cook-again button (replay arrow — last reading-gated step removed); reveal rebalanced (small text, 300px plate); bounce-off now clearly rejects over-limit ingredients; Comic Sans dropped for the system rounded stack; **single-tap cooking with a flame badge** (counting retired, B#3 v3); **automatic rhythm eating** (taps = bonus bites only, B#1 revision).

---

## 1. What the game is today

> **Note (2026-07-04):** this section describes the *original* game, now preserved as `beepos-kitchen.legacy.html`. It remains accurate as the design baseline, but the current build (§0) has replaced the stir button with pot-tapping, dropped tap-to-remove, and uses 9 ingredients / the 129-dish catalog.

`beepos-kitchen.html` (now `beepos-kitchen.legacy.html`) is a single, self-contained file (~1190 lines): inline SVG art, procedural Web Audio sound, CSS animations, zero dependencies, mobile-first (viewport locked, touch-optimized), with `prefers-reduced-motion` support. It is already charming and well-built — we are re-skinning and enriching it, not rescuing it.

**Core loop**

1. A cute robot mascot, **Beepo** (teal, chef hat, red antenna, expressive face), stands beside a pot on a stove.
2. A **shelf of 12 ingredients** sits at the bottom: apple, banana, strawberry, carrot, cheese, egg, chocolate, cookie, ice cream, plus three "silly" ones — **stinky sock**, **wiggly worm** (tagged `stinky`) and **rainbow** (tagged `magic`).
3. Tap an ingredient → it **flies into the pot** (max **4** items). Tap an item in the pot to remove it.
4. A **stir button** appears → **stir 3×** → a cooking/sizzle animation.
5. A **cloche (serving cover)** slides in → tap it (or wait 4.5s) → it lifts to **reveal the dish**.
6. Beepo **reacts and eats** (yum / wow), or **refuses** if the dish is stinky.
7. **"Cook again"** resets everything.

**Recipe logic** (`RECIPES`, ~37 entries + `MYSTERY` fallback): specific 2-ingredient combos map to named dishes (Banana Split, Apple Pie, etc.); single ingredients map to simpler dishes; unknown combos → "Mystery Mush". Reaction **tier** is decided in `reveal()`:
- any `stinky` item → **`refuse`** (Beepo pushes the plate away),
- `magic` or a 2+ combo → **`vor`** (voracious: fast chomping, burp, confetti),
- otherwise → **`ok`** (normal nomming).
Rainbow prepends "Rainbow " to the dish name and adds sparkles.

**Key code anchors** (so you can navigate):
- `INGREDIENTS` array and `RECIPES` array — data, top of the `<script>`.
- `iconSVG(id,size,color)` — the single choke-point that renders every icon via `<use href="#id">`. **This is where raster swaps happen.**
- `addIngredient()` / `landInPot()` / `removeFromPot()` — shelf → pot flow and the fly animation.
- stir handler + `cook()` — the 3-stir gate.
- `reveal()` / `liftCover()` / `finishReveal()` — the cloche reveal and tier decision.
- `startEating()` / `crumbs()` — the eating sequence.
- Sound: `beep()/tone()` + the `s*` one-shot functions (procedural, no files).
- Effects done in code (keep these): steam, bubbles, confetti, crumbs, stink lines.

**The art system in one sentence:** every visible object is an SVG `<symbol>` in a hidden `<defs>` library, drawn with a consistent look — chunky `#4A3B47` outlines, warm candy palette, a reusable `#g-face`. That consistency is exactly what we must reproduce in the AI art.

---

## 2. Design principles for the 2–5 audience

Keep these pinned; every decision serves them.

- **No losing, ever.** There is no wrong move — only different silly outcomes. The stinky "refuse" path is a *punchline*, not a failure.
- **They can't read.** This is the biggest UX insight. Today the game leans on text ("Tap goodies to toss them in!", "Pot is full! Stir it!", dish names, the "Tap the lid!" hint). A 2–5 year-old can't use any of it. Shift all *instruction* to **audio + visual cues** (pointing hand, wiggle, glow, Beepo gestures). Keep dish names on screen for the watching parent, but never make progress depend on reading.
- **Cause and effect is the whole toy.** Every tap must produce an immediate, oversized, delightful reaction (squash, sound, sparkle, Beepo hops). "Juice" is the point.
- **Huge, forgiving targets.** Big tap zones, generous spacing, no precision required, no timeouts that punish inaction.
- **Never stall.** Auto-advance safeguards must exist at every step (the current 4.5s cloche auto-lift is a good example — keep that philosophy everywhere).
- **Repetition is a feature.** Toddlers replay the same action for joy. Make the reset instant and inviting.

**Art north star (cuteness spec):** plump rounded shapes, oversized sparkly eyes, rosy cheeks, chunky dark outlines, glossy highlights, soft candy-pastel palette, warm friendly lighting — "kawaii sticker meets Pixar-toddler picture book." Nothing sharp, dark, or scary. Every object should look like it wants a hug.

---

## 3. Workstream A — CUTER: the ComfyUI art overhaul

This is the largest workstream and the reason for the handoff. The challenge with AI game art is **consistency** — every sprite must look like it belongs in the same world, and Beepo must stay the *same character* across every expression. The plan below is built around solving that.

### 3.0 First: inventory the ComfyUI install (do this before anything else)

Before designing a workflow, look at what's actually installed and adapt — do not assume specific models exist. Check:
- **Checkpoints** in `ComfyUI/models/checkpoints` (looking for an SDXL or Flux base, and any "cute/cartoon/anime" fine-tunes).
- **Custom nodes** in `ComfyUI/custom_nodes` — specifically **ComfyUI Manager**, **IPAdapter (ipadapter_plus)**, **ControlNet aux/preprocessors**, and a **background-removal** node (`rembg` / "Image Remove Background", or SAM).
- **ControlNet models** in `ComfyUI/models/controlnet` (want a **lineart** or **canny** model).
- **Upscalers** in `ComfyUI/models/upscale_models`.

Report back what's present. If IPAdapter / ControlNet-lineart / rembg are missing, installing them via ComfyUI Manager is the first task — they are load-bearing for the strategy below.

### 3.1 The consistency strategy (important)

Use three levers together:

1. **ControlNet from the existing SVG.** The current SVGs already define the perfect silhouette, proportions, and *registration point* of every object. Export each `<symbol>` to a transparent PNG (script below), then feed it as a **ControlNet lineart/canny** input. The AI then "paints" a cute rendered version *inside the existing shape*. Payoffs: shapes stay on-model, and sprites drop into the **same on-screen position/size** the SVGs occupied, so the existing CSS animations keep working with minimal layout surgery.
2. **A locked master style string + fixed sampler settings** appended to every prompt (same checkpoint, CFG, sampler, steps). See 3.4.
3. **IPAdapter style/character reference.** Once Beepo's canonical look is approved, use that image as an IPAdapter reference on *all* subsequent generations to lock the palette/shading, and specifically to keep **Beepo identical** across his expression frames. Best practice for the character: generate all Beepo expressions from the **same seed + same reference**, ideally as a single multi-pose sheet, then slice.

### 3.2 Asset manifest

Rendered *content* becomes AI art. Tiny procedural **effects stay in code** (steam, bubbles, confetti, crumbs, stink lines, sparkles) — they're cheap, animated, and already good.

| Group | Assets | Count | Notes |
|---|---|---|---|
| **Beepo** | normal, blink, yum, yuck, wow, eat-open, eat-closed, wave, sleepy | ~9 frames | One character sheet, same seed+reference. Frames swap like the current `.fx` groups. |
| **Ingredients** | the **9** selected (see `DISHES.md`) | 9 | Each a plump smiling character. Optional "squished" variant later. |
| **Dishes** | one per combo (see `DISHES.md`) | **129** | 1–3 distinct ingredients per dish. Names + verdicts already written; batch-render from the per-dish `image_prompt` in `dishes.json` (§3.4). |
| **Big UI** | pot, stove/counter (keep it *muted* — pot is the hero, see §0), cloche, plate, serving-dome shine, pot spoon, guide hand | ~7 | Illustrated to match. Pot interior must still allow the soup-color tint + floating items on top. No stir button exists anymore (B#3). |
| **Backgrounds** | cozy kitchen scene, title-screen art | 2 | Warm wood, sunny window, hanging utensils, soft depth. |
| **Audio (optional stretch)** | gentle music loop | 1 | See Workstream B. |

### 3.3 Export / format specs

- **Transparent PNG** (alpha), tightly trimmed to content — as the *working/master* format.
- Generate large (≈1024 px long edge), then downscale to target with crisp edges: **characters ~512 px**, **ingredients ~256 px**, **dishes ~384 px**. Optionally keep `@2x` for retina.
- **Ship WebP, not PNG.** ~150 transparent PNGs at these sizes land at 5–9 MB even after `pngquant`; lossy WebP with alpha roughly halves that with no visible loss at toddler-game detail levels. Convert as a build step (`cwebp`), keep PNG masters in `art-src/`. Budget: aim **< ~4 MB** shipped; if heavy, drop to @1x only.
- Keep a consistent internal padding so sprites align when swapped in.

### 3.4 Prompt kit (starting point — tune after the pilot)

**Master style suffix (append to every prompt):**
> `adorable kawaii toddler picture-book illustration, soft rounded chunky shapes, thick dark charcoal outline, glossy highlights, pastel candy palette, warm soft lighting, big sparkly eyes, rosy cheeks, cel shaded with soft gradients, sticker style, centered, plain flat background, high quality, super cute`

**Negative (every prompt):**
> `realistic, photoreal, scary, creepy, dark, gritty, harsh shadows, text, watermark, signature, extra limbs, deformed, low quality, jpeg artifacts, cluttered background, clutter`

**Beepo (canonical):**
> `Beepo, a cute friendly little robot chef, big boxy rounded teal head with side bolts, face on an inset screen panel, small teal chest unit with a yellow indicator light, segmented stubby arms with round steel gripper hands, boxy tread feet, tiny white chef hat with a glowing red antenna ball poking through the top, big happy eyes, standing, full body` + master suffix. *(Updated 2026-07-04 to match the robot-ier SVG redesign — the ControlNet linerefs come from the new SVG, so prompt and silhouette agree.)*
Then per frame, vary only the expression phrase: `big open happy smile, tongue out (yum)` / `disgusted green face, tongue out (yuck)` / `star-shaped sparkling eyes, mouth open in awe (wow)` / `eyes closed mouth wide open mid-bite (eating)` / `eyes closed peaceful (sleepy)` / `waving one arm, winking (wave)`. Keep seed + reference fixed.

**Ingredient template** (fill `[X]` for each of the 9):
> `a single cute [X] character with a happy smiling face, big shiny eyes, rosy cheeks, plump and glossy, one object centered` + master suffix.
For the silly three lean into the comedy: `stinky old sock with a mischievous grin and little green stink swirls`; `friendly wiggly green worm poking up with a cheeky smile`; `magical rainbow with a face, sparkling and glowing`.

**Dish template** (fill `[dish]` from the recipe name):
> `a small [dish] served in a bowl or on a plate, adorable, glossy, appetizing, tiny wisp of steam, one serving centered` + master suffix.

### 3.5 The SVG→PNG line-reference exporter (utility to build first)

Write a small script that loads `index.html` (the current build — its `<defs>` now also contain the `ui-*` icons and `dish-burger`), and for each `<symbol id="...">` renders it to a transparent PNG at ~1024². Two viable routes:
- **Headless browser** (Playwright/Puppeteer): inject an `<svg><use href="#id"></svg>` at fixed size, screenshot the element with a transparent background. Most faithful.
- **`sharp`/`resvg`/Inkscape CLI**: wrap each symbol's markup in a standalone SVG and rasterize.

Output to `art-src/linerefs/<id>.png`. These feed ControlNet in 3.1 and double as the fallback if any single AI asset doesn't come out cute enough.

### 3.6 Integrating raster art without losing the animation

The game's charm is its motion. Raster sprites keep it via the **same CSS transforms** (they animate the wrapper, not the SVG internals) plus **frame swaps** for expressions.

- **Ingredients / dishes:** change `iconSVG(id,size,color)` to return an `<img src="assets/ing/<id>.png">` (keep the same class + size). The existing `floaty`, `hop`, fly-to-pot, and swirl animations act on wrappers and keep working untouched.
- **Beepo expressions:** today `setExp()` toggles opacity between stacked `.fx` groups. Mirror that exactly with **stacked `<img>` layers** (one per expression) toggled by opacity, or swap a single `<img>.src`. Keep the class names (`exp-yum`, `exp-eat`, `fast`, etc.) so all the keyframe motion (`joyBounce`, `chomp`, `lunge`, `refuseTurn`) still fires. Blink = brief swap to the blink frame on the existing timer.
- **Pot soup:** the soup surface is tinted by `blendColors()` and floating items sit on top. Keep the tintable soup ellipse as SVG/CSS *over* an illustrated pot rim, or bake a neutral pot and overlay a semi-transparent color layer. Preserve `soupEl.style.fill` behavior.
- **Effects:** leave steam/bubbles/confetti/crumbs/stink **as code**. Optionally add a couple of small PNG particles (heart, star) for extra sparkle.

Net: swap the render target, keep the choreography.

### 3.7 The 129-dish batch

The full dish set — every distinct 1–3 ingredient combo — is enumerated with fun names, taste verdicts, and per-dish image prompts in **`DISHES.md`** / **`dishes.json`** (9 singles + 36 pairs + 84 triples = **129**; taste split 63 Yummy · 29 Magical · 37 Yucky). On a 5090 the whole batch renders comfortably, so there's no need to permanently subset. Still, generate a **~3-dish style pilot first** (the art-track pilot, §8) to lock the look, then batch the rest straight from the `image_prompt` field. Route any single asset that doesn't come out cute enough to the "Mystery Mush" fallback until it's regenerated.

---

## 4. Workstream B — MORE FUN: Milestone 1 (Fun & Feel), built on the current SVG art

**This is the part we finalize and build first, with zero new art.** The existing SVG Beepo, ingredients, and dishes are the stand-ins. Because the art swap (§3.6) happens under the same DOM wrappers and CSS classes, everything below survives the later reskin untouched. **Exit criterion:** a fully playable, fully delightful build Gustav signs off on *before* any ComfyUI work — at which point animations, timings, and sound are locked.

Each item lists **behavior · animation · sound · code hook**. Art needed: **none**, everywhere in this section.

**P0 — the core feel**

0. **Kill the tap lockout — overlapping flyers.** Remove the `busy` gate in `addIngredient()` entirely (and the `body.busy` shelf-dimming CSS): any number of ingredients can be mid-flight at once, and the shelf never dims, locks, or flickers. Shorten the flight to ~450 ms. The pot-full check moves to *landing* time — an over-limit item bounces off the rim back toward the shelf with the forgiving cue from Workstream C #4 (happy wiggle, never a "no"). Rationale: today every tap locks the shelf for ~1.45 s and taps in that window are silently ignored — a direct violation of the cause-and-effect principle, and the first thing a mashing toddler will find. Three fruits arcing into the pot at once is *more* delightful, not less. *Hook:* `addIngredient()` / `landInPot()`.
1. **Interactive tap-to-feed** *(the big one).* At the reveal, a pulsing pointing hand invites the child to tap Beepo/plate; **each tap = one bite** (dish shrinks a step, crumbs fly), then a gulp + celebration. Cause-and-effect feeding is peak toddler joy and turns today's passive eat animation into play. *Animation:* reuse `lunge` + `chomp`, add a squash on Beepo per bite. *Sound:* `sChomp` per tap, `sGulp` to finish. *Safeguard:* auto-advance a bite after ~2.5s idle so it never stalls. *Hook:* rework `startEating()` from timer-driven to tap-driven with the idle fallback (keep the `refuse` tier as-is: no feeding).
   **REVISED (2026-07-04, playtest): eating is automatic again, with beat delays.** Requiring taps to feed didn't earn its keep; bites now run on a rhythm (~1.05s apart, first at 0.9s; voracious tier ~0.48s) via `armAutoBite()`. Plate taps still trigger bonus bites — interaction is possible, never required. The feed-hand cue was removed.
2. **Tap-to-start title.** Opening overlay: big Beepo waving beside a pulsing "play" pot; tap anywhere to start, Beepo hops into place. Doubles as wordless onboarding. *Animation:* reuse `bob` + antenna pulse + `pulse`; overlay fade. *Sound:* soft chime. *Hook:* new start overlay gating the first `say('Feed the pot!')`; this first tap also **creates/unlocks the Web Audio context** (iOS requires a user gesture before audio can play), so sound works from the first moment on every device. (Title *illustration* drops in behind this later — the behavior is built now.)
3. **Counting stir — REVISED after playtest (2026-07-04): tap the pot, no button.** A separate stir button (even with progress ring + self-stirring spoon) wasn't toddler-obvious — the pot is where their attention lives. Now: once an ingredient lands, a **wiggling spoon pops out of the pot**; **tapping the pot anywhere = one stir** (pot rocks, spoon swirls, sparkles, extra steam puffs escalate per stir) while Beepo counts "One!/Two!/Three!"; the 3rd triggers `cook()`. Progress is physical (growing steam/sparkles), not an abstract ring. Tapping the *empty* pot gives a friendly wobble + "Feed the pot!". **Consequence: tap-to-remove-from-pot is dropped** — it conflicted with pot-mashing, and the no-fail design makes removal unnecessary. *Hook:* `doStir()` / `puffSteam()` / `#potSpoon`.
   **Second revision (2026-07-04, playtest v3): counting removed — ONE tap cooks.** Even star-socket progress wasn't obvious enough; the step is now a single pot tap. A flickering **flame badge** (`#cookFlame`) lights under the pot as the "cook me" symbol, the tap does one big swirl + sparkles and goes straight to `cook()` (flame flares during the sizzle). The counting-stir learning beat is retired; star sockets and numerals removed. *Hook:* `cookNow()` / `#cookFlame`.
4. **Ingredient personality.** On tap, the ingredient **boings in place** and plays **its own sound motif**; Beepo may say its name ("Apple!") — early word learning. *Animation:* a squash-boing keyframe on `.ing`. *Sound:* a unique 2–3 note motif per ingredient (table below), via the existing `tone()` system. *Hook:* `addIngredient()` just before the fly-to-pot.

**P1 — strong additions**

5. **Idle "attract" loop.** After ~8s of no input, Beepo waves / peeks in the pot / yawns and a **bouncing pointing hand** nudges toward the next thing to tap; clears on any interaction. Pulls a distracted toddler back in and teaches the next action wordlessly. *Hook:* a global idle timer reset on every interaction. (Hand can be an SVG/emoji now.)
6. **Gross-out upgrade (stinky refuse).** Lean into the comedy — nose-pinch, dramatic faint, a couple of cartoon flies, extra green stink lines, then bounce back to "Cook again." Zero fail; it's the *best* silly outcome. *Animation:* extend `refuseTurn` + the existing `stinkLine`.
7. **Procedural background music.** A gentle looping melody built with the **existing Web Audio system — no audio file needed**, so it's fully asset-independent. Respects and **persists** the mute button. *Hook:* extend the sound module; `localStorage` for the mute/music setting.
8. **Anticipation beat.** Beepo leans toward the cloche with an "ooh?" bubble and a rising tone just before it lifts, heightening the payoff. *Animation + sound only.*

**P2 — delight sprinkles**

9. **More lines & variety.** Expand `ADD_LINES`, the stinky lines, reveal words, and eating lines; add **dish-specific one-liners** keyed to the dish name; randomize so repeat plays stay fresh. *Pure data.*
10. **Global juice pass.** Squash/stretch on every pop, soft bounce easing throughout, a touch of screen-shake on big reveals, richer confetti, and `navigator.vibrate()` haptic taps where supported (toddler tablets often are). *CSS/JS only.*
11. **Emoji → inline SVG.** Replace every UI emoji (🍳 title, 👆 hands, 💚 stink hearts, 🤢/🙊/🤩/😋 reaction faces, 🥄, 👩‍🍳) with small inline-SVG equivalents drawn in the house style. Emoji render differently on every platform and instantly read as "web page," not "app." No art pipeline needed — code-drawn like the existing effects.

**Per-ingredient sound motifs (built; the 9 selected only):** apple = bright two-note ding ↑; banana = playful downward slide; strawberry = light triple sparkle; egg = hollow pop; chocolate = warm mellow tone; cookie = crumbly double-tap; ice cream = cool glissando ↑; worm = wobble bend; rainbow = happy arpeggio (`sSparkle`).

**Milestone 1 sign-off gate:** Gustav plays the build on a real phone/tablet; the loop is fully fun and legible with **no reading required**. Approve → animations/timings/sound are **locked** → the art overhaul proceeds as a pure reskin.

---

## 5. Workstream C — MORE STREAMLINED

Friction reduction, all in service of Section 2. **These ship inside Milestone 1** (same pre-art build) — several are already implied by Section 4 (counting stir, title/onboarding, forgiving fullness). No new art required for any of them.

1. **Kill the reading dependency.** Convert every *instructional* text moment to audio + visual: the "tap goodies" shelf title → a bouncing hand/arrow; "Pot is full!" → see #3 below; "Tap the lid!" → a big animated pointing hand on the cloche. Keep dish names as on-screen flavor for parents only.
2. **Onboarding via the title + first-run guiding hand** (Workstream B #2 and #5) instead of instructions.
3. **Make the stir step legible** — implemented as tap-the-pot stirring with physical escalation (see B#3 revision).
4. **Forgiving "pot full."** Replace the rejecting burp/"Pot is full!" with an *inviting* cue — built: the over-limit item bounces off the rim, the pot wiggles happily and glows, the guide hand points at the pot. Never a "no."
5. **Bigger tap targets & spacing** across the shelf and controls; thumb-proof. Verify on a real phone/tablet, not just desktop.
6. **Never-stall safeguards at every step** (extend the existing cloche auto-lift philosophy to any new interactive beat, e.g. auto-feed in B #1).
7. **Accessibility:** keep `prefers-reduced-motion`; keep the mute toggle and **persist** it (localStorage) plus any music setting; ensure everything is reachable with large touch zones; avoid flashing.

---

## 6. Workstream D — SHIP IT: packaging & publishing

New workstream (added 2026-07-04). Goal: publish as a **~$1 paid app** — primarily to learn the publishing pipeline; the kid already loves it. Set expectations accordingly: a $0.99 single-activity toddler app with no marketing will sell a handful of copies to strangers. Success = shipped, compliant, kid-approved. Everything here is deliberately boring and low-risk.

### 6.1 Decisions (locked by Gustav, 2026-07-04)

- **Platform: iOS only.** ✅ LOCKED. Apple Kids Category review is the real lesson (~$99/yr developer account). Android stays possible later from the same Capacitor project, but is out of scope.
- **Price: $0.99, paid upfront.** ✅ LOCKED — symbolic. No IAP, no ads, no subscriptions; keeps Kids Category compliance near-trivial.
- **VO: deferred.** ✅ DECIDED — no recording possible right now. v1.0 ships fully wordless-legible (tones + gestures + speech-bubble text for parents), which the design already targets. Build the audio system so VO clips can drop in later as a v1.x update (see §9).
- **App name: deferred** to Batch 7. Search the App Store for "Beepo" conflicts before committing to store assets — nothing blocks on it until then.

### 6.2 Packaging (Capacitor)

- Wrap the finished static build in **Capacitor**. The game stays a plain web build — no framework changes; the same files keep working in a browser.
- App icon + splash screen (SVG Beepo works fine; the art track can upgrade them later).
- **Bundle a rounded display font** (Baloo 2, OFL license — download the woff2, `@font-face` it locally, keep zero-network). Until then the game uses the system rounded stack (SF Rounded on iOS); Comic Sans was removed from the stack 2026-07-04.
- Configure the **native audio session** so the iOS mute/ring switch doesn't silence gameplay; verify the title-tap AudioContext unlock (§4 B#2) inside the wrapper.
- Lock **portrait orientation**, respect **safe-area insets** (notch), suppress system edge-gestures where possible.
- Offline is automatic (all assets local) — verify the app makes **zero network requests**; that's also a compliance claim (§6.3).

### 6.3 Compliance — the kids-app part

The game's zero-data, zero-dependency nature makes this almost free. **Keep it that way:** no analytics, no crash-reporting SDKs, no third-party code, no external links, ever.

- **COPPA / GDPR-K:** trivially satisfied by collecting nothing. Do not add "just a little" telemetry later.
- **Apple Kids Category + Google "Designed for Families":** declare target age (2–5); no ads, no outbound links, no purchases → no parental gate needed.
- **Privacy policy URL** — required by both stores even for zero-data apps. A one-pager ("this app collects nothing; a mute setting is stored on-device") is enough.
- **Apple privacy nutrition label** (all "Data Not Collected") and **Google Data safety form** to match.

### 6.4 Store presence & release

- Screenshots for required phone + tablet sizes (lean on the reveal moment and Beepo eating), short promo line, description, keywords.
- **TestFlight** build first; the kid is QA.
- Expect at least one review rejection on the first submission — part of the lesson, not a setback.

## 7. Proposed project structure

Moving from one file to a small static project (no server, still openable offline by double-clicking `index.html`):

```
beepos-kitchen/
  index.html            # markup + boot + SVG defs library
  game.js               # logic (extracted from the inline <script>)
  styles.css            # styles (extracted from <style>)
  dishes.js             # generated 129-dish catalog (regenerate from dishes.json)
  /assets
    /beepo   normal.png blink.png yum.png yuck.png wow.png eat-open.png eat-closed.png wave.png sleepy.png
    /ing     apple.png banana.png … rainbow.png            (12)
    /dish    banana-split.png apple-pie.png …              (all 129 from DISHES.md)
    /ui      pot.png stove.png cloche.png plate.png spoon.png hand.png
    /bg      kitchen.png title.png
    /audio   music-loop.mp3            (optional)
  /art-src                # not shipped; the art pipeline
    prompts.md            # the final tuned prompt kit
    workflow.json         # the ComfyUI graph
    export-linerefs.mjs   # SVG→PNG exporter (3.5)
    /linerefs             # PNG line refs for ControlNet
  beepos-kitchen.legacy.html   # the current file, kept as a working baseline
  PLAN.md
```

**Build:** none required to run. Add one optional npm script (`optimize`) that runs `pngquant`/`oxipng` over `/assets`, and — if Gustav later wants the single-file convenience back — an `inline` script that base64-embeds assets into a standalone HTML. Keep everything working offline.

---

## 8. Batched sequencing (revised 2026-07-04)

Do these in order — **fun first, ship second, art whenever it's ready.** The art track is *off the ship-critical path*: v1.0 may ship on polished SVG art, with the AI reskin as a v1.1 update (which also teaches the update pipeline — half of what "publishing" means in practice). Each batch ends in something playable. Get sign-off at the gates.

- **Batch 0 — Scaffold.** Copy the current file to `beepos-kitchen.legacy.html`; `git init`; extract the inline code into `index.html` / `game.js` / `styles.css` so features stay maintainable. The legacy file must stay runnable throughout.
- **Batch 1 — Core interaction rework** *(the big one)*. Overlapping flyers (§4 B#0); the new data model — the **9 selected ingredients** (cut carrot/cheese/sock per `DISHES.md`), `MAX_ITEMS` → **3**, recipes driven by `dishes.json` (129 names + verdicts; dishes without SVG art render as Mystery Mush until the reskin); tap-to-start title + audio unlock (B#2); tap-to-feed eating (B#1); counting stir (B#3); ingredient boing + sound motifs (B#4).
- **Batch 2 — Wordless guidance & streamlining.** Pointing-hand cue system + first-run onboarding (B#5, C#1–2); idle attract loop (B#5); forgiving pot-full (C#4); gross-out refuse upgrade (B#6); anticipation beat (B#8); never-stall audit of every step (C#6); mute persistence (C#7).
- **Batch 3 — Sound.** Procedural music loop + persisted toggle (B#7); polish the per-ingredient motifs and one-shots. **VO is deferred (§6.1)** — structure the audio module so recorded clips (counting, ingredient names, Beepo reactions) can drop in later as a v1.x update: a single `playVoice(id)` choke-point that no-ops when no clip exists, falling back to the tone motif.
- **Batch 4 — Juice & hardening.** Global juice pass (B#10); more lines & variety (B#9); emoji → inline SVG (B#11); multi-touch tolerance (extra simultaneous touches handled gracefully); safe-area insets; portrait lock; performance check on an old/cheap tablet.
- **Batch 5 — GATE: device sign-off (= Milestone 1).** Gustav + kid test on a real phone **and** tablet; run the Section 10 checklist. Approve → animations, timings, and sound are **locked**. The art track may fork off from here.
- **Art track** *(post-gate, parallel to Batches 6–7, not ship-blocking)*. (a) **Pilot (GATE):** inventory ComfyUI (§3.0), build the SVG→PNG exporter (§3.5), establish canonical Beepo + one ingredient + one dish, confirm the locked animations still feel great with raster — **stop for Gustav's approval before mass generation.** (b) **Full generation:** batch the 9 ingredients, all 129 dishes (§3.7 / `DISHES.md`), big UI, backgrounds; curate; WebP pass (§3.3). (c) **Reskin integration** (§3.6). Ships in v1.0 only if ready before Batch 7; otherwise v1.1.
- **Batch 6 — Package.** Capacitor wrap, icon + splash, native audio session, orientation/safe-area verification, zero-network check (§6.2).
- **Batch 7 — Publish.** Developer account, name check, privacy policy page, Kids Category compliance + privacy labels, TestFlight with the kid as tester, screenshots + listing, submit (§6.3–6.4).

---

## 9. Risks & open decisions

- **Character consistency (biggest risk).** AI struggles to keep Beepo identical across frames. Mitigation: ControlNet-from-SVG + fixed seed/style + IPAdapter reference + one-sheet generation (3.1). If it still drifts, fall back to keeping **Beepo as refined SVG** while everything else goes raster — an acceptable hybrid that preserves his expressive rig. Flag to Gustav if you hit this.
- **Losing animation richness in raster.** Mitigation is the whole of 3.6 — keep CSS transforms + frame swaps + procedural effects. Watch for it during the art-track pilot (§8); that's what the pilot is for.
- **129-dish workload.** Comfortable on the 5090; names + verdicts are pre-written (`DISHES.md`). Still gate on the art-track style pilot before the full batch so a late style change doesn't waste renders.
- **Art batch delaying the ship.** The reskin is the most fun and least necessary part of publishing. Mitigation: it's off the ship-critical path (§8) — v1.0 may ship on the existing SVG art, which is already coherent, distinctive, and weightless; the reskin becomes v1.1.
- **Asset weight vs. offline/instant-load.** Keep the <4 MB budget; @1x if needed; optimize hard.
- **Voice acting — recommended, but DEFERRED (Gustav, 2026-07-04: can't record right now).** For pre-readers, voice is the single biggest gap vs. professional competitors: procedural tones can't count "One! Two! Three!" or say "Apple!". v1.0 therefore ships wordless (tones + gestures — already the design target); the standing recommendation for a v1.x update is Gustav self-recording, **Swedish + English**. Batch 3 must leave the `playVoice(id)` hook in place so adding clips later is a pure asset drop.
- **Music source.** Generated vs. royalty-free vs. none. Decision for Gustav.

## 10. Definition of done / QA checklist

- [ ] Runs offline by opening `index.html`; legacy file still runs too.
- [ ] All 9 ingredients, Beepo's expressions, and the 129 dishes are on-style and cute; nothing scary/sharp.
- [ ] Every tap yields immediate visual + audio feedback; every step has a no-stall safeguard.
- [ ] No progress step requires reading; a non-reading child can complete the loop guided only by audio/visual cues.
- [ ] Interactive feeding works and auto-completes if idle.
- [ ] Stinky path is funny and clearly *not* a failure.
- [ ] Mute (and music, if added) persists across reloads; `prefers-reduced-motion` respected.
- [ ] Tested on a real phone **and** tablet: big targets, no accidental mis-taps, good performance.
- [ ] Total asset weight within budget; shipped images WebP-optimized.
- [ ] Shelf never locks or dims: mashing several ingredients in quick succession produces overlapping flyers; every tap responds.
- [ ] Wrapped build (Capacitor) runs on device: audio survives the mute switch (§6.2), portrait locked, safe areas respected.
- [ ] Zero network requests; privacy labels/policy accurately say "collects nothing."

## 11. First actions for Sonnet

1. Batch 0: copy the legacy file, scaffold the folder/files (§7).
2. **Build Batches 1–4 (Section 4 + Section 5) on the current SVG art** — this is the immediate work and needs no art. Bring the fun, playable build to Gustav for the Batch 5 sign-off.
3. After the gate, fork: the **art track** (§3 — inventory, exporter, Beepo style pilot, approval before mass generation) and/or go straight to **Batches 6–7** (§6) to ship v1.0 on SVG art.

*Keep the tone of the whole thing warm, silly, and safe — if a change wouldn't make a 3-year-old grin, cut it.*
