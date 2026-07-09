# -*- coding: utf-8 -*-
"""v3: worm -> DIRTY SMELLY SOCK (id 'worm' kept) + punchier fruit-triple gags.
   - ingredient renamed Wiggly Worm -> Stinky Sock (kid preference).
   - all 37 worm-dish names + prompts rewritten as grubby-sock scenes.
   - all 56 fruit-triples get a punchier gag: bespoke real-dessert scenes for the
     ones whose name implies a real treat, a rich physical-comedy pool for the rest
     (replaces the repetitive tower/conga/hug/snowman rotation from v2).
   Patches dishes.json, regenerates dishes.js + art-map.js, seds DISHES.md.
   Prints the render list (all worm dishes + all triples)."""
import json, re, os, zlib

REPO = r"C:\Users\gusta\OneDrive\Desktop\Claude\Beepos kitchen\Beepos kitchen"
d = json.load(open(os.path.join(REPO, 'dishes.json'), encoding='utf-8'))

# ---- 1) ingredient swap: worm -> sock (id 'worm' unchanged) ----------------
for i in d['ingredients']:
    if i['id'] == 'worm':
        i['name'] = 'Stinky Sock'; i['emoji'] = '\U0001F9E6'; i['vis'] = 'grubby dirty tube sock'

# ---- 2) explicit sock names for the 37 worm dishes -------------------------
NAMES = {
  8:'Stinky Sock Noodles', 16:'Apple Sock Surprise', 23:'Stinky Banana Sock Slime',
  29:'Stinky Berry Sock Sludge', 34:'Slimy Sock Scramble', 38:'Choco-Dipped Socks',
  41:'Smelly Sock Burger', 43:'Stinky Sock Ice Scream', 45:'Sparkly Rainbow Sock Goo',
  51:'Apple & Banana Sock Swamp Stew', 57:'Soggy Apple & Blueberry Sock Mush',
  62:'Smelly Apple & Egg Sock Sludge', 66:'Stinky Apple & Chocolate Sock Surprise',
  69:'Slimy Apple & Cookie Sock Goo', 71:'Apple & Ice Cream Sock Swamp Stew',
  73:'Smelly Apple Sock Sludge', 78:'Smelly Banana & Blueberry Sock Sludge',
  83:'Stinky Banana & Egg Sock Surprise', 87:'Slimy Banana & Chocolate Sock Goo',
  90:'Banana & Cookie Sock Swamp Stew', 92:'Soggy Banana & Ice Cream Sock Mush',
  94:'Stinky Banana Sock Surprise', 98:'Slimy Blueberry & Egg Sock Goo',
  102:'Blueberry & Chocolate Sock Swamp Stew', 105:'Soggy Blueberry & Cookie Sock Mush',
  107:'Smelly Blueberry & Ice Cream Sock Sludge', 109:'Slimy Blueberry Sock Goo',
  112:'Soggy Egg & Chocolate Sock Mush', 115:'Smelly Egg & Cookie Sock Sludge',
  117:'Stinky Egg & Ice Cream Sock Surprise', 119:'Egg Sock Swamp Stew',
  121:'Stinky Chocolate & Cookie Sock Surprise', 123:'Slimy Chocolate & Ice Cream Sock Goo',
  125:'Soggy Chocolate Sock Mush', 126:'Cookie & Ice Cream Sock Swamp Stew',
  128:'Smelly Cookie Sock Sludge', 129:'Stinky Ice Cream Sock Surprise',
}

# ---- 3) prompt kit v3 ------------------------------------------------------
CHAR = {
  'apple':    'a glossy red apple character',
  'banana':   'a curvy yellow banana character',
  'berry':    'a plump round deep-blue blueberry character with a tiny leafy star crown',
  'egg':      'a jiggly fried-egg character with a golden yolk',
  'choco':    'a melty dark-chocolate bar character',
  'cookie':   'a chocolate-chip cookie character',
  'icecream': 'a swirly soft-serve ice-cream character',
  'worm':     'a grubby cartoon tube sock character with a ribbed red cuff and red toe, dirt-spotted cream body and wavy green stink lines',
  'rainbow':  'a small glowing rainbow arc',
}
SINGLE = {
  'apple':    'a happy glossy red apple character melting into a smooth shiny puddle of applesauce, proud grin',
  'banana':   'a blissful banana character flopped backwards into a soft creamy banana-mash swirl',
  'berry':    'a plump blueberry character sitting in a glossy puddle of deep-blue jam, licking its lips',
  'egg':      'a wobbly golden egg-custard character caught mid-jiggle, swirl top leaning sideways',
  'choco':    'a swirl of glossy melted chocolate pudding with a happy face, a chocolate-bar corner poking out like a fin',
  'cookie':   'a giant crumbly cookie character with a big bite taken out, grinning, crumbs bouncing around it',
  'icecream': 'a tall melty soft-serve mountain character with a drippy happy smile, one drip like a tear of joy',
  'worm':     'a steaming bowl of grubby sock-noodles, one dirty cream tube sock with a red cuff popping up from the tangle grinning, wavy green stink lines',
  'rainbow':  'a glossy swirled rainbow soup blob levitating tiny stars, serene sparkly face',
}
PAIRS = {
  'apple+banana':   'a swirling smoothie tornado of red and yellow with a happy apple character and banana character spinning inside it',
  'apple+berry':    'a wobbly translucent jelly dome with red and deep-blue layers, an apple character and blueberry character suspended inside mid-wave',
  'apple+egg':      'a jiggly golden custard swirl with a glossy red apple character sitting on top like a king on a throne',
  'apple+choco':    'a glossy red apple character dunked waist-deep in melted chocolate, licking its cheek, thick chocolate drips',
  'apple+cookie':   'a cozy little lattice apple pie with a rosy apple character relaxing in the middle like a bathtub',
  'apple+icecream': 'a warm apple pie slice and a melting soft-serve swirl character leaning on each other like best friends',
  'apple+worm':     'a glossy red apple with a round bite-hole, a cheeky dirty sock with a red cuff flopping out of the hole waving, green stink wisps',
  'apple+rainbow':  'a glossy red apple character surfing a small rainbow arc, fizzy sparkle bubbles splashing',
  'banana+berry':   'a swirling deep-blue smoothie tornado with a banana character and a blueberry character spinning happily inside',
  'banana+egg':     'a stack of fluffy golden pancakes with a banana character doing a victory pose on top',
  'banana+choco':   'three chocolate-dipped banana pop characters standing in a row striking poses like a band',
  'banana+cookie':  'a teetering stack of cookies with a banana character surfing on top, arms out for balance',
  'banana+icecream':'a smiling banana boat cradling three scoops of ice cream like sleeping babies, cherry on top',
  'banana+worm':    'a grubby red-cuffed sock sliding down a long banana curve into a splash of green slime, gleeful face, stink lines',
  'banana+rainbow': 'a banana character asleep in a small rainbow arc hammock, dream sparkles floating up',
  'berry+egg':      'a jiggly golden custard swirl with blueberry characters cannonballing into it, blue splashes mid-air',
  'berry+choco':    'a tiny chocolate layer cake with plump blueberry characters peeking out between the layers',
  'berry+cookie':   'a big crumbly cookie with blueberry characters bouncing on it like a trampoline, blue jam splats',
  'berry+icecream': 'a soft-serve swirl character holding out its arms while blueberry characters rain gently down, blue syrup drips',
  'berry+worm':     'a dirty cream sock with a red cuff lounging in a deep-blue blueberry-sludge hot tub, one end draped lazily over the rim, stink wisps',
  'berry+rainbow':  'a blueberry character sliding down a small rainbow arc into a splash of blue sparkle jam',
  'choco+egg':      'a tiny chocolate birthday cake with one candle, a fried-egg character bursting out of the top like a surprise party',
  'cookie+egg':     'a small cute hamburger, golden sesame-seed bun, brown patty, melty yellow cheese drips, ruffled green lettuce, a fried egg peeking out',
  'egg+icecream':   'a fried-egg character and a soft-serve swirl character twisted together into one creamy tornado, dizzy happy faces',
  'egg+worm':       'a grubby sock tangled up in ribbons of fluffy scrambled egg like a cozy scarf, red toe poking out, cheeky grin',
  'egg+rainbow':    'a fluffy cloud-shaped omelette character napping on a small rainbow arc, golden yolk shining like a sun',
  'choco+cookie':   'a glossy chocolate-glazed donut character with thick dripping frosting, winking, rainbow sprinkles',
  'choco+icecream': 'a chocolate-and-cream twist soft-serve character striking a proud superhero pose, cape of chocolate drips',
  'choco+worm':     'a dirty tube sock dunked into a swirl of melted chocolate fondue, chocolate dripping off its red toe, sneaky grin',
  'choco+rainbow':  'a melted chocolate swirl with a small rainbow arc rising out of it like a fountain, sparkles',
  'cookie+icecream':'two cookie characters hugging a soft-serve filling between them, cream squishing out the sides, all three giggling',
  'cookie+worm':    'a small hamburger with a cheeky dirty sock flopping out between the sesame buns instead of the patty, red cuff showing, green stink wisps',
  'cookie+rainbow': 'a big cookie character juggling rainbow sprinkles, a small rainbow arc overhead like a circus tent',
  'icecream+worm':  'a soft-serve swirl character screaming comically wide-eyed as a grubby red-cuffed sock pops out of the top of its swirl, stink lines',
  'icecream+rainbow':'a soft-serve sundae character proudly wearing a small rainbow arc as a hat, gentle sparkle rain',
  'rainbow+worm':   'a cheeky dirty sock wearing a tiny rainbow arc as a superhero cape, red cuff flapping, striking a flex pose, sparkle-and-stink trail',
}

# bespoke real-dessert triples (keyed by sorted ids) -------------------------
TRIPLE_BESPOKE = {
  'apple+banana+berry':    'a bouncy fruit-salad party: an apple character, a banana character and a blueberry character doing a joyful jumping high-five, juice droplets and confetti flying',
  'banana+berry+icecream': 'a classic banana-split boat: a smiling banana cradling three ice-cream scoops piled with blueberries, a cherry on top, rainbow drizzle and sparkles',
  'banana+choco+egg':      'a chocolate birthday cake with one lit candle and a banana character popping out of the top like a party surprise, confetti and streamers',
  'banana+choco+icecream': 'a deluxe banana-split boat loaded with chocolate ice-cream scoops and thick chocolate drizzle, a banana character striking a proud pose, sparkles',
  'banana+cookie+icecream':'a tall sundae glass stacked with banana slices, ice-cream scoops and cookie shards, a cherry on top, happy little faces peeking over the rim',
  'apple+cookie+icecream': 'a warm apple-pie slice with a melting ice-cream scoop sliding off the top, an apple character and ice-cream character leaning together happily, cozy steam wisps',
  'berry+choco+icecream':  'a sundae glass layered with chocolate sauce, blueberries and swirled ice cream, blueberry characters peeking over the rim, glossy chocolate drizzle',
  'berry+cookie+icecream': 'a blueberry-shortcake sundae with layers of cookie crumble, blueberries and whipped cream, a blueberry character on top waving a tiny spoon like a flag',
  'choco+cookie+egg':      'a giant chocolate-chip cookie-cake with a slice lifting out in a gooey chocolate stretch, a cookie character cheering, crumbs bouncing everywhere',
  'choco+cookie+icecream': 'a cookies-and-cream sundae, swirled ice cream loaded with cookie chunks and chocolate drizzle, little cookie characters cannonballing in, joyful splashes',
}

# rich physical-comedy pool for the remaining triples ------------------------
POOL = [
  '{a}, {b} and {c} blasting off on a fizzy soda-bottle rocket together, faces of pure joy, whoosh trails',
  '{a} and {b} launching {c} off a spoon see-saw, {c} flying up giggling in a sparkle arc',
  'a wobbly circus-acrobat tower of {a} balancing {b} balancing {c}, tiny flags, arms out',
  '{a}, {b} and {c} cannonball-diving into a big happy splash together, splash crown flying up',
  '{a}, {b} and {c} in a giggling belly-laugh dogpile, little legs kicking in the air',
  '{a} and {c} bouncing {b} sky-high on a stretchy trampoline, {b} whooping mid-air',
  '{a}, {b} and {c} squished into one cozy sandwich hug, cheeks smooshed, all three giggling',
  '{a}, {b} and {c} riding a curling whipped-cream wave like surfers, arms out, joyful',
  '{a}, {b} and {c} posing as a proud superhero trio, capes fluttering, a sparkle burst behind them',
  '{a} conducting while {b} and {c} sing into spoons like a tiny band, music notes floating up',
  '{a}, {b} and {c} tumbling downhill piled on a rolling ice-cream scoop like a snowball, laughing',
  '{a}, {b} and {c} bursting out of a party popper together, confetti and curly streamers everywhere',
  '{a} giving {b} and {c} a wobbly double piggyback, grinning, little motion lines',
  '{a}, {b} and {c} clinking cups in a happy cheers toast, sparkly droplets flying',
  '{a}, {b} and {c} doing a synchronized swimming pose in a puddle of syrup, legs pointed up',
  '{a} and {b} swinging {c} in a blanket like a trampoline, {c} bouncing up delighted, sparkles',
]

VSTYLE = {
  'Yucky':   ', everything drizzled in silly green slime, the grubby sock flopping about mischievously, gross-but-adorable, wavy green stink wisps',
  'Magical': ', glowing with soft magical aurora light, sparkles and tiny stars floating all around, dreamy shimmer',
  'Yummy':   ', glossy and appetizing, bright cheerful colours, one tiny heart-shaped sparkle rising',
}

def sock_words(s):
    """light cleanup for image_concept / md prose."""
    return (s.replace('Wiggly Worm','Stinky Sock').replace('wiggly worm','stinky sock')
             .replace('Worm','Sock').replace('worm','sock')
             .replace('Wiggly','Smelly').replace('wiggly','smelly')
             .replace('Wormy','Stinky').replace('Squirmy','Soggy').replace('squirmy','soggy'))

render = []
for x in d['dishes']:
    ids, n = x['ids'], x['n']
    combo = '+'.join(sorted(ids))
    if n in NAMES:
        x['name'] = NAMES[n]
    x['image_concept'] = sock_words(x['image_concept'])
    if x['size'] == 1:
        scene = SINGLE[ids[0]]
    elif x['size'] == 2:
        scene = PAIRS[combo]
    else:  # triple
        if combo in TRIPLE_BESPOKE:
            scene = TRIPLE_BESPOKE[combo]
        else:
            g = POOL[zlib.crc32(combo.encode()) % len(POOL)]
            scene = g.format(a=CHAR[ids[0]], b=CHAR[ids[1]], c=CHAR[ids[2]])
    x['image_prompt'] = scene + VSTYLE[x['verdict']]
    # render everything that changed: all worm/sock dishes + all triples
    if ('worm' in ids) or (x['size'] == 3):
        render.append(n)

json.dump(d, open(os.path.join(REPO, 'dishes.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

# ---- regenerate dishes.js --------------------------------------------------
lines = ['/* AUTO-GENERATED from dishes.json - do not edit by hand.',
         '   129 dishes; key = sorted ingredient ids joined by +. v: yummy|magical|yucky */',
         'const DISH_CATALOG = {']
for x in d['dishes']:
    key = '+'.join(sorted(x['ids']))
    nm = x['name'].replace('"', '\\"')
    lines.append(f'  "{key}": {{n:"{nm}", v:"{x["verdict"].lower()}"}},')
lines.append('};')
open(os.path.join(REPO, 'dishes.js'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')

# ---- regenerate art-map.js (new slugs) -------------------------------------
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
am = ['/* AUTO-GENERATED (from dishes.json): combo key -> assets/dish WebP. */', 'const DISH_ART = {']
for x in d['dishes']:
    am.append(f'  "{"+".join(sorted(x["ids"]))}": "{x["n"]:03d}-{slug(x["name"])}.webp",')
am.append('};')
open(os.path.join(REPO, 'art-map.js'), 'w', encoding='utf-8').write('\n'.join(am) + '\n')

# ---- DISHES.md: worm -> sock rename ----------------------------------------
mdp = os.path.join(REPO, 'DISHES.md')
if os.path.exists(mdp):
    md = open(mdp, encoding='utf-8').read()
    for n, nm in NAMES.items():
        pass  # names vary; do prose-level replace below
    md = sock_words(md).replace('\U0001FAB1', '\U0001F9E6')  # 🪱 -> 🧦 if present
    open(mdp, 'w', encoding='utf-8').write(md)

print('patched dishes.json / dishes.js / art-map.js / DISHES.md')
print('render list (%d):' % len(render), ','.join(map(str, render)))
print('\nsample v3 prompts:')
for n in (8, 16, 41, 46, 77, 60, 120):
    x = d['dishes'][n-1]
    print(f'  #{n} {x["name"]}: {x["image_prompt"][:140]}')
