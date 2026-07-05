#!/usr/bin/env python3
"""Build deploy/: index.html with CSS + JS inlined, plus a copy of the assets/ folder.
Since the raster reskin (§3.6) the game uses AI PNGs in assets/, so this is no longer a
single self-contained file — it's index.html + assets/. Rerun after any change.
(deploy/assets is gitignored; regenerate it here. Netlify Drop takes the deploy/ folder.)"""
import os, re, shutil
h      = open('index.html', encoding='utf-8').read()
css    = open('styles.css', encoding='utf-8').read()
dishes = open('dishes.js', encoding='utf-8').read()
artmap = open('art-map.js', encoding='utf-8').read()
game   = open('game.js', encoding='utf-8').read()
for js in (dishes, artmap, game):
    assert '</script' not in js, 'script content would break inlining'
h = h.replace('<link rel="stylesheet" href="styles.css">', '<style>\n'+css+'</style>')
h = h.replace('<script src="dishes.js"></script>', '<script>\n'+dishes+'</script>')
h = h.replace('<script src="art-map.js"></script>', '<script>\n'+artmap+'</script>')
h = h.replace('<script src="game.js"></script>', '<script>\n'+game+'</script>')
assert not any(s in h for s in ('src="dishes.js"', 'src="art-map.js"', 'src="game.js"', 'styles.css'))
assert not re.search(r'(src|href)="https?://', h), 'external http reference found'
os.makedirs('deploy', exist_ok=True)
open('deploy/index.html', 'w', encoding='utf-8').write(h)
dst = os.path.join('deploy', 'assets')
shutil.rmtree(dst, ignore_errors=True)             # best-effort clean (OneDrive can lock files mid-sync)
shutil.copytree('assets', dst, dirs_exist_ok=True) # overwrite in place — no hard delete required
print(f'deploy/index.html: {len(h)} bytes (code inlined) + deploy/assets/ copied')
