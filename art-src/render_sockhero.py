# -*- coding: utf-8 -*-
"""Sock-HERO re-roll of all 37 sock dishes -> TEST render prefixes (sockh_NNN).
   Sock is always the big dominant subject; other ingredients are small sidekicks.
   Non-destructive: renders to ComfyUI output only; cutout step writes to sock_test/."""
import time, glob, os, json, zlib
import gen_food as g

OUT = r"C:\Users\gusta\ComfyUI\output\beepo_food"
REPO = r"C:\Users\gusta\OneDrive\Desktop\Claude\Beepos kitchen\Beepos kitchen"
SOCK = ("a grubby cream tube sock character with a chunky ribbed RED cuff and a red toe, "
        "clearly a dirty smelly sock, big and front-and-center as the main hero")
SLIME = ", green slime oozing and dripping, little wavy green stink squiggles rising"

CHAR = {'apple':'red apple character','banana':'banana character','berry':'blue blueberry character',
        'egg':'fried-egg character','choco':'chocolate-bar character','cookie':'cookie character',
        'icecream':'soft-serve ice-cream character','rainbow':'rainbow arc'}

# hand-authored single + pairs (sock hero)
HAND = {
 8:  f"{SOCK} lounging back happily in a big bowl of yellow spaghetti noodles",
 16: f"{SOCK} climbing out of a big round bite-hole in a shiny red apple and waving hello",
 23: f"{SOCK} draped over a big yellow banana like a hammock, grinning",
 29: f"{SOCK} taking a bubble bath in a tub of deep-blue blueberry sludge, a small blueberry character beside it",
 34: f"{SOCK} sitting tangled in a small nest of fluffy yellow scrambled egg, grinning",
 38: f"{SOCK} being dunked head-first into a mug of melted chocolate, thick chocolate dripping off it, grinning",
 41: f"a sesame-seed burger with its top bun lifted to reveal {SOCK} inside instead of a meat patty, flopping out huge, melty cheese and lettuce",
 43: f"{SOCK} standing tall on top of a swirly soft-serve ice cream in a red cup, the ice cream shrieking in shock",
 45: f"{SOCK} flying like a proud little superhero wearing a small rainbow arc as a cape",
}
# triple poses (sock hero + 2 sidekicks)
POOL = [
 "{S} as the giant hero in the middle, with a small {c1} and a small {c2} cheering beside it",
 "{S} sitting in a bowl of green slime as the big main subject, a small {c1} and a small {c2} peeking over the rim beside it",
 "{S} held up high like a trophy by a small {c1} and a small {c2}, the sock huge in the center",
 "{S} flopped across the middle as the star, a small {c1} and a small {c2} bouncing playfully on it",
]

d = json.load(open(os.path.join(REPO,'dishes.json'), encoding='utf-8'))
socks = [x for x in d['dishes'] if 'worm' in x['ids']]

prompts = {}
for x in socks:
    n, ids = x['n'], x['ids']
    if n in HAND:
        body = HAND[n]
    else:
        others = [i for i in ids if i != 'worm']
        pose = POOL[zlib.crc32(('+'.join(sorted(ids))).encode()) % len(POOL)]
        body = pose.format(S=SOCK, c1=CHAR[others[0]], c2=CHAR[others[1]])
    prompts[n] = body + SLIME

print(f"rendering {len(prompts)} sock-hero test dishes")
before = {n: set(glob.glob(os.path.join(OUT, f"sockh_{n:03d}_*.png"))) for n in prompts}
for n, body in prompts.items():
    g.queue_prompt(g.workflow(g.full_prompt(body), g.stable_seed(f"sockh_{n:03d}"), f"beepo_food/sockh_{n:03d}"))
print("all queued; polling...")
done = {}; dl = time.time() + 900
while len(done) < len(prompts) and time.time() < dl:
    time.sleep(6)
    for n in prompts:
        if n in done: continue
        new = set(glob.glob(os.path.join(OUT, f"sockh_{n:03d}_*.png"))) - before[n]
        if new: done[n] = sorted(new)[-1]
    if len(done) % 10 == 0 and done: print(f"  {len(done)}/{len(prompts)} done", flush=True)
print(f"landed {len(done)}/{len(prompts)}")
miss = [n for n in prompts if n not in done]
if miss: print("MISSING:", miss)
