#!/usr/bin/env python3
"""Build a self-contained single-file game at deploy/index.html (for Netlify Drop etc.).
Inlines styles.css, dishes.js and game.js into index.html. Rerun after any change."""
import os, re
h = open('index.html').read()
css = open('styles.css').read()
dishes = open('dishes.js').read()
game = open('game.js').read()
for js in (dishes, game):
    assert '</script' not in js, 'script content would break inlining'
h = h.replace('<link rel="stylesheet" href="styles.css">', '<style>\n'+css+'</style>')
h = h.replace('<script src="dishes.js"></script>', '<script>\n'+dishes+'</script>')
h = h.replace('<script src="game.js"></script>', '<script>\n'+game+'</script>')
assert 'src="dishes.js"' not in h and 'src="game.js"' not in h and 'styles.css' not in h
assert not re.search(r'(src|href)="https?://', h), 'external reference found'
os.makedirs('deploy', exist_ok=True)
open('deploy/index.html','w').write(h)
print('deploy/index.html written:', len(h), 'bytes, fully self-contained')
