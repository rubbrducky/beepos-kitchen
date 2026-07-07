# -*- coding: utf-8 -*-
"""Fresh-take v2: strawberry -> blueberry + rewrite every image_prompt as a character
SCENE with a gag (weak dishes were 'bowl contents' prompts -> beige blobs).
Patches dishes.json, regenerates dishes.js + art-map.js (webp), seds DISHES.md.
Prints the render list (berry dishes + all non-keepers)."""
import json, re, os

REPO = r"C:\Users\gusta\OneDrive\Desktop\Claude\Beepos kitchen\Beepos kitchen"
d = json.load(open(os.path.join(REPO, 'dishes.json'), encoding='utf-8'))

# Laugh-out-loud winners -> keep current art, do NOT re-render (none contain berry)
KEEPERS = {8, 16, 22, 23, 32, 34, 41, 45, 51, 90, 94, 119, 125, 126}

# ---- 1) ingredient swap: strawberry -> blueberry (id 'berry' unchanged) ----
for i in d['ingredients']:
    if i['id'] == 'berry':
        i['name'] = 'Blueberry'; i['emoji'] = '\U0001FAD0'; i['vis'] = 'plump blue blueberry'

def fixname(s):
    return (s.replace('Strawberry', 'Blueberry').replace('strawberry', 'blueberry')
             .replace('Pink Monkey', 'Blue Monkey'))

# ---- 2) prompt kit v2: characters + scenes ----
CHAR = {
  'apple':    'a glossy red apple character',
  'banana':   'a curvy yellow banana character',
  'berry':    'a plump round deep-blue blueberry character with a tiny leafy star crown',
  'egg':      'a jiggly fried-egg character with a golden yolk',
  'choco':    'a melty dark-chocolate bar character',
  'cookie':   'a chocolate-chip cookie character',
  'icecream': 'a swirly soft-serve ice-cream character',
  'worm':     'a cheeky green wiggly worm',
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
  'worm':     'a pile of wiggly green noodle-worms, one cheeky worm popping up from the middle with a grin',
  'rainbow':  'a glossy swirled rainbow soup blob levitating tiny stars, serene sparkly face',
}
# hand-written scenes for ALL pairs, matched to their dish names (keepers included, for future regens)
PAIRS = {
  'apple+banana':   'a swirling smoothie tornado of red and yellow with a happy apple character and banana character spinning inside it',
  'apple+berry':    'a wobbly translucent jelly dome with red and deep-blue layers, an apple character and blueberry character suspended inside mid-wave',
  'apple+egg':      'a jiggly golden custard swirl with a glossy red apple character sitting on top like a king on a throne',
  'apple+choco':    'a glossy red apple character dunked waist-deep in melted chocolate, licking its cheek, thick chocolate drips',
  'apple+cookie':   'a cozy little lattice apple pie with a rosy apple character relaxing in the middle like a bathtub',
  'apple+icecream': 'a warm apple pie slice and a melting soft-serve swirl character leaning on each other like best friends',
  'apple+worm':     'a glossy red apple with a round window hole, a cheeky green worm popping out waving',
  'apple+rainbow':  'a glossy red apple character surfing a small rainbow arc, fizzy sparkle bubbles splashing',
  'banana+berry':   'a swirling deep-blue smoothie tornado with a banana character and a blueberry character spinning happily inside',
  'banana+egg':     'a stack of fluffy golden pancakes with a banana character doing a victory pose on top',
  'banana+choco':   'three chocolate-dipped banana pop characters standing in a row striking poses like a band',
  'banana+cookie':  'a teetering stack of cookies with a banana character surfing on top, arms out for balance',
  'banana+icecream':'a smiling banana boat cradling three scoops of ice cream like sleeping babies, cherry on top',
  'banana+worm':    'a cheeky green worm water-sliding down a long banana curve into a splash of slime',
  'banana+rainbow': 'a banana character asleep in a small rainbow arc hammock, dream sparkles floating up',
  'berry+egg':      'a jiggly golden custard swirl with blueberry characters cannonballing into it, blue splashes mid-air',
  'berry+choco':    'a tiny chocolate layer cake with plump blueberry characters peeking out between the layers',
  'berry+cookie':   'a big crumbly cookie with blueberry characters bouncing on it like a trampoline, blue jam splats',
  'berry+icecream': 'a soft-serve swirl character holding out its arms while blueberry characters rain gently down, blue syrup drips',
  'berry+worm':     'a cheeky green worm lounging in a puddle of deep-blue berry sludge like a hot tub, one arm on the edge',
  'berry+rainbow':  'a blueberry character sliding down a small rainbow arc into a splash of blue sparkle jam',
  'choco+egg':      'a tiny chocolate birthday cake with one candle, a fried-egg character bursting out of the top like a surprise party',
  'cookie+egg':     'a small cute hamburger, golden sesame-seed bun, brown patty, melty yellow cheese drips, ruffled green lettuce, a fried egg peeking out',
  'egg+icecream':   'a fried-egg character and a soft-serve swirl character twisted together into one creamy tornado, dizzy happy faces',
  'egg+worm':       'a cheeky green worm tangled in ribbons of fluffy scrambled egg like a scarf, grinning',
  'egg+rainbow':    'a fluffy cloud-shaped omelette character napping on a small rainbow arc, golden yolk shining like a sun',
  'choco+cookie':   'a glossy chocolate-glazed donut character with thick dripping frosting, winking, rainbow sprinkles',
  'choco+icecream': 'a chocolate-and-cream twist soft-serve character striking a proud superhero pose, cape of chocolate drips',
  'choco+worm':     'cheeky green worms dipped in a chocolate fondue swirl, one worm grinning with a chocolate mustache',
  'choco+rainbow':  'a melted chocolate swirl with a small rainbow arc rising out of it like a fountain, sparkles',
  'cookie+icecream':'two cookie characters hugging a soft-serve filling between them, cream squishing out the sides, all three giggling',
  'cookie+worm':    'a small hamburger with a cheeky green cartoon worm poking out between the buns, golden sesame bun',
  'cookie+rainbow': 'a big cookie character juggling rainbow sprinkles, a small rainbow arc overhead like a circus tent',
  'icecream+worm':  'a soft-serve swirl character screaming comically, eyes wide, as a cheeky green worm pops out of the top of its swirl',
  'icecream+rainbow':'a soft-serve sundae character proudly wearing a small rainbow arc as a hat, gentle sparkle rain',
  'rainbow+worm':   'a cheeky green worm wearing a tiny rainbow arc as a superhero cape, flexing, sparkle trail',
}
TRIPLE_SCENES = [
  'a wobbly tower: {a} stacked on {b} stacked on {c}, all giggling',
  '{a}, {b} and {c} dancing in a happy conga line',
  '{a} and {b} carrying {c} overhead like a champion',
  'a giggling group-hug pile of {a}, {b} and {c}, cheeks squished together',
  '{a}, {b} and {c} stacked like a snowman, the top one saluting',
  '{a} and {c} high-fiving over {b}, who looks delighted',
]
VSTYLE = {
  'Yucky':   ', dripping with silly green slime, the worm giggling mischievously, gross-but-adorable, little green stink wisps',
  'Magical': ', glowing with soft magical aurora light, sparkles and tiny stars floating all around, dreamy shimmer',
  'Yummy':   ', glossy and appetizing, one tiny heart-shaped steam wisp rising',
}

render = []
for x in d['dishes']:
    x['name'] = fixname(x['name']); x['image_concept'] = fixname(x['image_concept'])
    ids, n = x['ids'], x['n']
    if x['size'] == 1:
        scene = SINGLE[ids[0]]
    elif x['size'] == 2:
        scene = PAIRS['+'.join(sorted(ids))]
    else:
        scene = TRIPLE_SCENES[n % len(TRIPLE_SCENES)].format(
            a=CHAR[ids[0]], b=CHAR[ids[1]], c=CHAR[ids[2]])
    x['image_prompt'] = scene + VSTYLE[x['verdict']]
    if ('berry' in ids) or (n not in KEEPERS):
        render.append(n)

json.dump(d, open(os.path.join(REPO, 'dishes.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

# ---- 3) regenerate dishes.js (name + verdict map) ----
lines = ['/* AUTO-GENERATED from dishes.json - do not edit by hand.',
         '   129 dishes; key = sorted ingredient ids joined by +. v: yummy|magical|yucky */',
         'const DISH_CATALOG = {']
for x in d['dishes']:
    key = '+'.join(sorted(x['ids']))
    nm = x['name'].replace('"', '\\"')
    lines.append(f'  "{key}": {{n:"{nm}", v:"{x["verdict"].lower()}"}},')
lines.append('};')
open(os.path.join(REPO, 'dishes.js'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')

# ---- 4) regenerate art-map.js (webp, new slugs) ----
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
am = ['/* AUTO-GENERATED (from dishes.json): combo key -> assets/dish WebP. */', 'const DISH_ART = {']
for x in d['dishes']:
    am.append(f'  "{"+".join(sorted(x["ids"]))}": "{x["n"]:03d}-{slug(x["name"])}.webp",')
am.append('};')
open(os.path.join(REPO, 'art-map.js'), 'w', encoding='utf-8').write('\n'.join(am) + '\n')

# ---- 5) DISHES.md: mechanical rename ----
mdp = os.path.join(REPO, 'DISHES.md')
md = open(mdp, encoding='utf-8').read()
md = (md.replace('Strawberry', 'Blueberry').replace('strawberry', 'blueberry')
        .replace('Pink Monkey', 'Blue Monkey').replace('\U0001F353', '\U0001FAD0'))
open(mdp, 'w', encoding='utf-8').write(md)

print('patched dishes.json / dishes.js / art-map.js / DISHES.md')
print('render list (%d):' % len(render), ','.join(map(str, render)))
print('\nsample v2 prompts:')
for n in (3, 19, 43, 47):
    x = d['dishes'][n-1]
    print(f'  #{n} {x["name"]}: {x["image_prompt"][:130]}')
