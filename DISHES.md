# Beepo's Kitchen — Ingredients & Dish Catalog

Companion to **PLAN.md**. Source of truth for the ingredient set and every dish that needs a **fun name + image + taste verdict**. Machine-readable copy: `dishes.json`.

## The 9 ingredients

Chosen from the original 12 for the richest, most recognizable toddler combos while keeping one **gross** ingredient (comedy) and one **magic** ingredient (wow). **Cut:** Carrot, Cheese, Stinky Sock. *(Easy to swap — say the word and this regenerates.)*

| Ingredient | | Role | Effect on taste |
|---|---|---|---|
| Apple | 🍎 | food | normal — **Yummy** |
| Banana | 🍌 | food | normal — **Yummy** |
| Blueberry | 🫐 | food | normal — **Yummy** |
| Egg | 🥚 | food | normal — **Yummy** |
| Chocolate | 🍫 | food | normal — **Yummy** |
| Cookie | 🍪 | food | normal — **Yummy** |
| Ice Cream | 🍦 | food | normal — **Yummy** |
| Wiggly Worm | 🪱 | gross | makes any dish **Yucky** (Beepo refuses — the gross-out gag) |
| Rainbow | 🌈 | magic | makes any dish **Magical** (wow tier) when no worm present |

## Taste rule (drives the "tasty or not")

1. Any dish containing **Wiggly Worm 🪱 → Yucky 🤢** (Beepo gags/refuses — kids will chase this on purpose).
2. Otherwise, any dish containing **Rainbow 🌈 → Magical 🤩** (extra-celebratory "wow" reaction).
3. Everything else → **Yummy 😋** (Beepo happily eats).

The verdict is a simple rule, so it costs nothing to assign — only the **names** and **images** are real production work.

## Totals

- **129 distinct dishes** = 9 single + 36 pairs + 84 triples (order-independent, no repeated ingredients).
- Taste split: **63 Yummy 😋 · 29 Magical 🤩 · 37 Yucky 🤢**.
- So ~71% are tasty rewards and ~29% are the funny "yuck" outcome — a good balance for ages 2–5.

Singles + all pairs are hand-named; triples use a themed name generator (easy to hand-tune later — override any name in `dishes.json`).

---

## 1-ingredient dishes (9)

| # | Ingredients | Dish name | Taste | Image concept |
|---|---|---|---|---|
| 1 | Apple | Apple Squish Sauce | 😋 Yummy | red apple (yummy, glossy) |
| 2 | Banana | Mushy Banana Mash | 😋 Yummy | banana (yummy, glossy) |
| 3 | Blueberry | Blueberry Squish Jam | 😋 Yummy | blueberry (yummy, glossy) |
| 4 | Egg | Wobbly Egg Custard | 😋 Yummy | soft egg (yummy, glossy) |
| 5 | Chocolate | Choco Goo Pudding | 😋 Yummy | chocolate (yummy, glossy) |
| 6 | Cookie | Giant Cookie Mush | 😋 Yummy | cookie (yummy, glossy) |
| 7 | Ice Cream | Melty Ice-Cream Mountain | 😋 Yummy | ice cream scoop (yummy, glossy) |
| 8 | Wiggly Worm | Wormy Wiggle Noodles | 🤢 Yucky | green wiggly worm (slimy, funny-gross) |
| 9 | Rainbow | Sparkle Rainbow Soup | 🤩 Magical | rainbow sparkles (sparkly, glowing) |

## 2-ingredient dishes (36)

| # | Ingredients | Dish name | Taste | Image concept |
|---|---|---|---|---|
| 10 | Apple + Banana | Sunny Fruit Smoothie | 😋 Yummy | red apple + banana (yummy, glossy) |
| 11 | Apple + Blueberry | Berry-Apple Jelly | 😋 Yummy | red apple + blueberry (yummy, glossy) |
| 12 | Apple + Egg | Apple Custard Cup | 😋 Yummy | red apple + soft egg (yummy, glossy) |
| 13 | Apple + Chocolate | Choco-Dunked Apple | 😋 Yummy | red apple + chocolate (yummy, glossy) |
| 14 | Apple + Cookie | Grandma's Apple Pie | 😋 Yummy | red apple + cookie (yummy, glossy) |
| 15 | Apple + Ice Cream | Apple Pie a la Mode | 😋 Yummy | red apple + ice cream scoop (yummy, glossy) |
| 16 | Apple + Wiggly Worm | Wiggly Apple Wormhole | 🤢 Yucky | red apple + green wiggly worm (slimy, funny-gross) |
| 17 | Apple + Rainbow | Rainbow Apple Fizz | 🤩 Magical | red apple + rainbow sparkles (sparkly, glowing) |
| 18 | Banana + Blueberry | Blue Monkey Smoothie | 😋 Yummy | banana + blueberry (yummy, glossy) |
| 19 | Banana + Egg | Banana Pancakes | 😋 Yummy | banana + soft egg (yummy, glossy) |
| 20 | Banana + Chocolate | Choco-Banana Pops | 😋 Yummy | banana + chocolate (yummy, glossy) |
| 21 | Banana + Cookie | Banana Cookie Stack | 😋 Yummy | banana + cookie (yummy, glossy) |
| 22 | Banana + Ice Cream | Banana Split | 😋 Yummy | banana + ice cream scoop (yummy, glossy) |
| 23 | Banana + Wiggly Worm | Wiggle-Waggle Banana Slime | 🤢 Yucky | banana + green wiggly worm (slimy, funny-gross) |
| 24 | Banana + Rainbow | Rainbow Banana Dream | 🤩 Magical | banana + rainbow sparkles (sparkly, glowing) |
| 25 | Blueberry + Egg | Blueberry Custard Cup | 😋 Yummy | blueberry + soft egg (yummy, glossy) |
| 26 | Blueberry + Chocolate | Blueberry-Choco Cake | 😋 Yummy | blueberry + chocolate (yummy, glossy) |
| 27 | Blueberry + Cookie | Blueberry Cookie Crumble | 😋 Yummy | blueberry + cookie (yummy, glossy) |
| 28 | Blueberry + Ice Cream | Blueberry Sundae | 😋 Yummy | blueberry + ice cream scoop (yummy, glossy) |
| 29 | Blueberry + Wiggly Worm | Wormy Berry Sludge | 🤢 Yucky | blueberry + green wiggly worm (slimy, funny-gross) |
| 30 | Blueberry + Rainbow | Rainbow Berry Sparkle | 🤩 Magical | blueberry + rainbow sparkles (sparkly, glowing) |
| 31 | Egg + Chocolate | Chocolate Birthday Cake | 😋 Yummy | soft egg + chocolate (yummy, glossy) |
| 32 | Egg + Cookie | Beepo Burger | 😋 Yummy | cute hamburger: sesame bun, patty, cheese, lettuce (yummy, glossy) |
| 33 | Egg + Ice Cream | Frozen Custard Swirl | 😋 Yummy | soft egg + ice cream scoop (yummy, glossy) |
| 34 | Egg + Wiggly Worm | Slimy Worm Scramble | 🤢 Yucky | soft egg + green wiggly worm (slimy, funny-gross) |
| 35 | Egg + Rainbow | Rainbow Cloud Omelette | 🤩 Magical | soft egg + rainbow sparkles (sparkly, glowing) |
| 36 | Chocolate + Cookie | Double-Choc Donut | 😋 Yummy | chocolate + cookie (yummy, glossy) |
| 37 | Chocolate + Ice Cream | Choco Swirl Cone | 😋 Yummy | chocolate + ice cream scoop (yummy, glossy) |
| 38 | Chocolate + Wiggly Worm | Choco-Dipped Wigglers | 🤢 Yucky | chocolate + green wiggly worm (slimy, funny-gross) |
| 39 | Chocolate + Rainbow | Magic Choco Rainbow Swirl | 🤩 Magical | chocolate + rainbow sparkles (sparkly, glowing) |
| 40 | Cookie + Ice Cream | Ice-Cream Sandwich | 😋 Yummy | cookie + ice cream scoop (yummy, glossy) |
| 41 | Cookie + Wiggly Worm | Wiggly Worm Burger | 🤢 Yucky | hamburger with a cheeky worm poking out between the buns (funny-gross) |
| 42 | Cookie + Rainbow | Rainbow Sprinkle Cookie | 🤩 Magical | cookie + rainbow sparkles (sparkly, glowing) |
| 43 | Ice Cream + Wiggly Worm | Wormy Ice Scream | 🤢 Yucky | ice cream scoop + green wiggly worm (slimy, funny-gross) |
| 44 | Ice Cream + Rainbow | Rainbow Sparkle Sundae | 🤩 Magical | ice cream scoop + rainbow sparkles (sparkly, glowing) |
| 45 | Wiggly Worm + Rainbow | Sparkly Rainbow Worm Goo | 🤢 Yucky | green wiggly worm + rainbow sparkles (slimy, funny-gross) |

## 3-ingredient dishes (84)

| # | Ingredients | Dish name | Taste | Image concept |
|---|---|---|---|---|
| 46 | Apple + Banana + Blueberry | Tutti-Frutti Salad | 😋 Yummy | red apple + banana + blueberry (yummy, glossy) |
| 47 | Apple + Banana + Egg | Apple-Banana-Egg Yum-Bowl | 😋 Yummy | red apple + banana + soft egg (yummy, glossy) |
| 48 | Apple + Banana + Chocolate | Apple-Banana-Chocolate Medley | 😋 Yummy | red apple + banana + chocolate (yummy, glossy) |
| 49 | Apple + Banana + Cookie | Triple Treat: Apple, Banana & Cookie | 😋 Yummy | red apple + banana + cookie (yummy, glossy) |
| 50 | Apple + Banana + Ice Cream | Apple-Banana-Ice Cream Mash-Up | 😋 Yummy | red apple + banana + ice cream scoop (yummy, glossy) |
| 51 | Apple + Banana + Wiggly Worm | Apple & Banana Worm Swamp Stew | 🤢 Yucky | red apple + banana + green wiggly worm (slimy, funny-gross) |
| 52 | Apple + Banana + Rainbow | Magical Apple & Banana Shimmer | 🤩 Magical | red apple + banana + rainbow sparkles (sparkly, glowing) |
| 53 | Apple + Blueberry + Egg | Apple-Blueberry-Egg Medley | 😋 Yummy | red apple + blueberry + soft egg (yummy, glossy) |
| 54 | Apple + Blueberry + Chocolate | Triple Treat: Apple, Blueberry & Chocolate | 😋 Yummy | red apple + blueberry + chocolate (yummy, glossy) |
| 55 | Apple + Blueberry + Cookie | Apple-Blueberry-Cookie Mash-Up | 😋 Yummy | red apple + blueberry + cookie (yummy, glossy) |
| 56 | Apple + Blueberry + Ice Cream | Chef's Apple-Blueberry-Ice Cream Surprise | 😋 Yummy | red apple + blueberry + ice cream scoop (yummy, glossy) |
| 57 | Apple + Blueberry + Wiggly Worm | Squirmy Apple & Blueberry Mush | 🤢 Yucky | red apple + blueberry + green wiggly worm (slimy, funny-gross) |
| 58 | Apple + Blueberry + Rainbow | Apple & Blueberry Rainbow Delight | 🤩 Magical | red apple + blueberry + rainbow sparkles (sparkly, glowing) |
| 59 | Apple + Egg + Chocolate | Apple-Egg-Chocolate Mash-Up | 😋 Yummy | red apple + soft egg + chocolate (yummy, glossy) |
| 60 | Apple + Egg + Cookie | Chef's Apple-Egg-Cookie Surprise | 😋 Yummy | red apple + soft egg + cookie (yummy, glossy) |
| 61 | Apple + Egg + Ice Cream | Apple-Egg-Ice Cream Yum-Bowl | 😋 Yummy | red apple + soft egg + ice cream scoop (yummy, glossy) |
| 62 | Apple + Egg + Wiggly Worm | Wiggly Apple & Egg Sludge | 🤢 Yucky | red apple + soft egg + green wiggly worm (slimy, funny-gross) |
| 63 | Apple + Egg + Rainbow | Enchanted Apple & Egg Twinkle Treat | 🤩 Magical | red apple + soft egg + rainbow sparkles (sparkly, glowing) |
| 64 | Apple + Chocolate + Cookie | Apple-Chocolate-Cookie Yum-Bowl | 😋 Yummy | red apple + chocolate + cookie (yummy, glossy) |
| 65 | Apple + Chocolate + Ice Cream | Apple-Chocolate-Ice Cream Medley | 😋 Yummy | red apple + chocolate + ice cream scoop (yummy, glossy) |
| 66 | Apple + Chocolate + Wiggly Worm | Wormy Apple & Chocolate Surprise | 🤢 Yucky | red apple + chocolate + green wiggly worm (slimy, funny-gross) |
| 67 | Apple + Chocolate + Rainbow | Rainbow Apple & Chocolate Sparkle Dream | 🤩 Magical | red apple + chocolate + rainbow sparkles (sparkly, glowing) |
| 68 | Apple + Cookie + Ice Cream | Apple Pie a la Mode Deluxe | 😋 Yummy | red apple + cookie + ice cream scoop (yummy, glossy) |
| 69 | Apple + Cookie + Wiggly Worm | Slimy Apple & Cookie Wriggle-Goo | 🤢 Yucky | red apple + cookie + green wiggly worm (slimy, funny-gross) |
| 70 | Apple + Cookie + Rainbow | Magical Apple & Cookie Shimmer | 🤩 Magical | red apple + cookie + rainbow sparkles (sparkly, glowing) |
| 71 | Apple + Ice Cream + Wiggly Worm | Apple & Ice Cream Worm Swamp Stew | 🤢 Yucky | red apple + ice cream scoop + green wiggly worm (slimy, funny-gross) |
| 72 | Apple + Ice Cream + Rainbow | Apple & Ice Cream Rainbow Delight | 🤩 Magical | red apple + ice cream scoop + rainbow sparkles (sparkly, glowing) |
| 73 | Apple + Wiggly Worm + Rainbow | Wiggly Apple Sludge | 🤢 Yucky | red apple + green wiggly worm + rainbow sparkles (slimy, funny-gross) |
| 74 | Banana + Blueberry + Egg | Triple Treat: Banana, Blueberry & Egg | 😋 Yummy | banana + blueberry + soft egg (yummy, glossy) |
| 75 | Banana + Blueberry + Chocolate | Banana-Blueberry-Chocolate Mash-Up | 😋 Yummy | banana + blueberry + chocolate (yummy, glossy) |
| 76 | Banana + Blueberry + Cookie | Chef's Banana-Blueberry-Cookie Surprise | 😋 Yummy | banana + blueberry + cookie (yummy, glossy) |
| 77 | Banana + Blueberry + Ice Cream | Double-Berry Banana Split | 😋 Yummy | banana + blueberry + ice cream scoop (yummy, glossy) |
| 78 | Banana + Blueberry + Wiggly Worm | Wiggly Banana & Blueberry Sludge | 🤢 Yucky | banana + blueberry + green wiggly worm (slimy, funny-gross) |
| 79 | Banana + Blueberry + Rainbow | Enchanted Banana & Blueberry Twinkle Treat | 🤩 Magical | banana + blueberry + rainbow sparkles (sparkly, glowing) |
| 80 | Banana + Egg + Chocolate | Choco-Banana Birthday Cake | 😋 Yummy | banana + soft egg + chocolate (yummy, glossy) |
| 81 | Banana + Egg + Cookie | Banana-Egg-Cookie Yum-Bowl | 😋 Yummy | banana + soft egg + cookie (yummy, glossy) |
| 82 | Banana + Egg + Ice Cream | Banana-Egg-Ice Cream Medley | 😋 Yummy | banana + soft egg + ice cream scoop (yummy, glossy) |
| 83 | Banana + Egg + Wiggly Worm | Wormy Banana & Egg Surprise | 🤢 Yucky | banana + soft egg + green wiggly worm (slimy, funny-gross) |
| 84 | Banana + Egg + Rainbow | Rainbow Banana & Egg Sparkle Dream | 🤩 Magical | banana + soft egg + rainbow sparkles (sparkly, glowing) |
| 85 | Banana + Chocolate + Cookie | Banana-Chocolate-Cookie Medley | 😋 Yummy | banana + chocolate + cookie (yummy, glossy) |
| 86 | Banana + Chocolate + Ice Cream | Choco-Banana Split Supreme | 😋 Yummy | banana + chocolate + ice cream scoop (yummy, glossy) |
| 87 | Banana + Chocolate + Wiggly Worm | Slimy Banana & Chocolate Wriggle-Goo | 🤢 Yucky | banana + chocolate + green wiggly worm (slimy, funny-gross) |
| 88 | Banana + Chocolate + Rainbow | Magical Banana & Chocolate Shimmer | 🤩 Magical | banana + chocolate + rainbow sparkles (sparkly, glowing) |
| 89 | Banana + Cookie + Ice Cream | Banana Cookie Sundae | 😋 Yummy | banana + cookie + ice cream scoop (yummy, glossy) |
| 90 | Banana + Cookie + Wiggly Worm | Banana & Cookie Worm Swamp Stew | 🤢 Yucky | banana + cookie + green wiggly worm (slimy, funny-gross) |
| 91 | Banana + Cookie + Rainbow | Banana & Cookie Rainbow Delight | 🤩 Magical | banana + cookie + rainbow sparkles (sparkly, glowing) |
| 92 | Banana + Ice Cream + Wiggly Worm | Squirmy Banana & Ice Cream Mush | 🤢 Yucky | banana + ice cream scoop + green wiggly worm (slimy, funny-gross) |
| 93 | Banana + Ice Cream + Rainbow | Enchanted Banana & Ice Cream Twinkle Treat | 🤩 Magical | banana + ice cream scoop + rainbow sparkles (sparkly, glowing) |
| 94 | Banana + Wiggly Worm + Rainbow | Wormy Banana Surprise | 🤢 Yucky | banana + green wiggly worm + rainbow sparkles (slimy, funny-gross) |
| 95 | Blueberry + Egg + Chocolate | Blueberry-Egg-Chocolate Yum-Bowl | 😋 Yummy | blueberry + soft egg + chocolate (yummy, glossy) |
| 96 | Blueberry + Egg + Cookie | Blueberry-Egg-Cookie Medley | 😋 Yummy | blueberry + soft egg + cookie (yummy, glossy) |
| 97 | Blueberry + Egg + Ice Cream | Triple Treat: Blueberry, Egg & Ice Cream | 😋 Yummy | blueberry + soft egg + ice cream scoop (yummy, glossy) |
| 98 | Blueberry + Egg + Wiggly Worm | Slimy Blueberry & Egg Wriggle-Goo | 🤢 Yucky | blueberry + soft egg + green wiggly worm (slimy, funny-gross) |
| 99 | Blueberry + Egg + Rainbow | Magical Blueberry & Egg Shimmer | 🤩 Magical | blueberry + soft egg + rainbow sparkles (sparkly, glowing) |
| 100 | Blueberry + Chocolate + Cookie | Triple Treat: Blueberry, Chocolate & Cookie | 😋 Yummy | blueberry + chocolate + cookie (yummy, glossy) |
| 101 | Blueberry + Chocolate + Ice Cream | Blueberry-Choco Sundae | 😋 Yummy | blueberry + chocolate + ice cream scoop (yummy, glossy) |
| 102 | Blueberry + Chocolate + Wiggly Worm | Blueberry & Chocolate Worm Swamp Stew | 🤢 Yucky | blueberry + chocolate + green wiggly worm (slimy, funny-gross) |
| 103 | Blueberry + Chocolate + Rainbow | Blueberry & Chocolate Rainbow Delight | 🤩 Magical | blueberry + chocolate + rainbow sparkles (sparkly, glowing) |
| 104 | Blueberry + Cookie + Ice Cream | Blueberry Shortcake Sundae | 😋 Yummy | blueberry + cookie + ice cream scoop (yummy, glossy) |
| 105 | Blueberry + Cookie + Wiggly Worm | Squirmy Blueberry & Cookie Mush | 🤢 Yucky | blueberry + cookie + green wiggly worm (slimy, funny-gross) |
| 106 | Blueberry + Cookie + Rainbow | Enchanted Blueberry & Cookie Twinkle Treat | 🤩 Magical | blueberry + cookie + rainbow sparkles (sparkly, glowing) |
| 107 | Blueberry + Ice Cream + Wiggly Worm | Wiggly Blueberry & Ice Cream Sludge | 🤢 Yucky | blueberry + ice cream scoop + green wiggly worm (slimy, funny-gross) |
| 108 | Blueberry + Ice Cream + Rainbow | Rainbow Blueberry & Ice Cream Sparkle Dream | 🤩 Magical | blueberry + ice cream scoop + rainbow sparkles (sparkly, glowing) |
| 109 | Blueberry + Wiggly Worm + Rainbow | Slimy Blueberry Wriggle-Goo | 🤢 Yucky | blueberry + green wiggly worm + rainbow sparkles (slimy, funny-gross) |
| 110 | Egg + Chocolate + Cookie | Chocolate-Chip Cookie Cake | 😋 Yummy | soft egg + chocolate + cookie (yummy, glossy) |
| 111 | Egg + Chocolate + Ice Cream | Chef's Egg-Chocolate-Ice Cream Surprise | 😋 Yummy | soft egg + chocolate + ice cream scoop (yummy, glossy) |
| 112 | Egg + Chocolate + Wiggly Worm | Squirmy Egg & Chocolate Mush | 🤢 Yucky | soft egg + chocolate + green wiggly worm (slimy, funny-gross) |
| 113 | Egg + Chocolate + Rainbow | Enchanted Egg & Chocolate Twinkle Treat | 🤩 Magical | soft egg + chocolate + rainbow sparkles (sparkly, glowing) |
| 114 | Egg + Cookie + Ice Cream | Egg-Cookie-Ice Cream Yum-Bowl | 😋 Yummy | soft egg + cookie + ice cream scoop (yummy, glossy) |
| 115 | Egg + Cookie + Wiggly Worm | Wiggly Egg & Cookie Sludge | 🤢 Yucky | soft egg + cookie + green wiggly worm (slimy, funny-gross) |
| 116 | Egg + Cookie + Rainbow | Rainbow Egg & Cookie Sparkle Dream | 🤩 Magical | soft egg + cookie + rainbow sparkles (sparkly, glowing) |
| 117 | Egg + Ice Cream + Wiggly Worm | Wormy Egg & Ice Cream Surprise | 🤢 Yucky | soft egg + ice cream scoop + green wiggly worm (slimy, funny-gross) |
| 118 | Egg + Ice Cream + Rainbow | Magical Egg & Ice Cream Shimmer | 🤩 Magical | soft egg + ice cream scoop + rainbow sparkles (sparkly, glowing) |
| 119 | Egg + Wiggly Worm + Rainbow | Egg Worm Swamp Stew | 🤢 Yucky | soft egg + green wiggly worm + rainbow sparkles (slimy, funny-gross) |
| 120 | Chocolate + Cookie + Ice Cream | Cookies-and-Cream Sundae | 😋 Yummy | chocolate + cookie + ice cream scoop (yummy, glossy) |
| 121 | Chocolate + Cookie + Wiggly Worm | Wormy Chocolate & Cookie Surprise | 🤢 Yucky | chocolate + cookie + green wiggly worm (slimy, funny-gross) |
| 122 | Chocolate + Cookie + Rainbow | Magical Chocolate & Cookie Shimmer | 🤩 Magical | chocolate + cookie + rainbow sparkles (sparkly, glowing) |
| 123 | Chocolate + Ice Cream + Wiggly Worm | Slimy Chocolate & Ice Cream Wriggle-Goo | 🤢 Yucky | chocolate + ice cream scoop + green wiggly worm (slimy, funny-gross) |
| 124 | Chocolate + Ice Cream + Rainbow | Chocolate & Ice Cream Rainbow Delight | 🤩 Magical | chocolate + ice cream scoop + rainbow sparkles (sparkly, glowing) |
| 125 | Chocolate + Wiggly Worm + Rainbow | Squirmy Chocolate Mush | 🤢 Yucky | chocolate + green wiggly worm + rainbow sparkles (slimy, funny-gross) |
| 126 | Cookie + Ice Cream + Wiggly Worm | Cookie & Ice Cream Worm Swamp Stew | 🤢 Yucky | cookie + ice cream scoop + green wiggly worm (slimy, funny-gross) |
| 127 | Cookie + Ice Cream + Rainbow | Enchanted Cookie & Ice Cream Twinkle Treat | 🤩 Magical | cookie + ice cream scoop + rainbow sparkles (sparkly, glowing) |
| 128 | Cookie + Wiggly Worm + Rainbow | Wiggly Cookie Sludge | 🤢 Yucky | cookie + green wiggly worm + rainbow sparkles (slimy, funny-gross) |
| 129 | Ice Cream + Wiggly Worm + Rainbow | Wormy Ice Cream Surprise | 🤢 Yucky | ice cream scoop + green wiggly worm + rainbow sparkles (slimy, funny-gross) |

---

## Notes for implementation

- Set the pot's `MAX_ITEMS` to **3** (dishes use 1-3 distinct ingredients). Duplicates of the same ingredient don't create new dishes — the dish is defined by the **distinct set**.
- Each dish's full ComfyUI prompt is in `dishes.json` (`image_prompt`), built to sit on the PLAN §3.4 master style suffix.
- `dishes.json` can feed both the game's recipe map (combo → name + verdict) and the image-generation batch.
- A 5090 handles all 129 renders comfortably; still do the Phase 2 style pilot on ~3 dishes first to lock the look before the full batch.
