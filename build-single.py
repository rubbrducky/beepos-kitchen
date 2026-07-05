#!/usr/bin/env python3
"""Build deploy/: index.html with CSS + JS inlined, plus a complete copy of assets/.
Since the raster reskin (§3.6) the game uses AI WebP in assets/, so this is not a single
self-contained file — it's index.html + assets/. Rerun after any change.
(deploy/assets is gitignored; Netlify Drop takes the deploy/ folder.)

The asset copy retries on OneDrive file-locks and ASSERTS the copy is complete, so a
partial deploy (e.g. dishes but no ingredients) can never ship silently."""
import os, re, time, shutil
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
shutil.rmtree(dst, ignore_errors=True)          # best-effort clean (OneDrive can lock files)
for root, _, files in os.walk('assets'):
    rel = os.path.relpath(root, 'assets')
    tgt = dst if rel == '.' else os.path.join(dst, rel)
    os.makedirs(tgt, exist_ok=True)
    for f in files:
        s, d = os.path.join(root, f), os.path.join(tgt, f)
        for attempt in range(6):                # retry through transient OneDrive locks
            try:
                shutil.copy2(s, d); break
            except PermissionError:
                if attempt == 5: raise
                time.sleep(0.6)
src_n = sum(len(fs) for _, _, fs in os.walk('assets'))
dst_n = sum(len(fs) for _, _, fs in os.walk(dst))
assert src_n == dst_n, f'INCOMPLETE COPY: {dst_n}/{src_n} files copied — deploy would be broken, aborting'
print(f'deploy/index.html: {len(h)} bytes (code inlined) + deploy/assets/ {dst_n} files (complete)')
