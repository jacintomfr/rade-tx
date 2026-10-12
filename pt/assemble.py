"""Assemble the single-file page from its source and the two WebAssembly
modules, as build/build.sh does, but without Emscripten.

Upstream published an index.html newer than build/rade-tx.src.html, so the
source of this fork is taken from the published page itself:

  python pt/assemble.py extract   # once: upstream index.html -> pt/rade-pt.src.html
                                  #       + pt/modules/rade_{tx,rx}_single.js
  python pt/assemble.py build     # pt/rade-pt.src.html + modules -> index.html

The two modules are the two large <script> blocks (transmit first, then
receive); in the source they are replaced by the same markers build.sh uses.
"""
import sys, os, re, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(HERE, 'rade-pt.src.html')
OUT = os.path.join(ROOT, 'index.html')
MARKS = ('/*__RADE_TX_MODULE__*/', '/*__RADE_RX_MODULE__*/')
MODS = [os.path.join(HERE, 'modules', n) for n in ('rade_tx_single.js', 'rade_rx_single.js')]


def read(p):
    return open(p, encoding='utf-8', newline='').read()


def write(p, s):
    open(p, 'w', encoding='utf-8', newline='').write(s)


def extract(page_path):
    page = read(page_path)
    blocks = [(m.start(1), m.end(1)) for m in re.finditer(r'<script>(.*?)</script>', page, re.S)]
    big = sorted(sorted(blocks, key=lambda b: b[1] - b[0], reverse=True)[:2])
    (s1, e1), (s2, e2) = big
    assert e1 - s1 > 1000000 and e2 - s2 > 1000000, 'modules not found'
    src = page[:s1] + MARKS[0] + page[e1:s2] + MARKS[1] + page[e2:]
    os.makedirs(os.path.dirname(MODS[0]), exist_ok=True)
    write(MODS[0], page[s1:e1])
    write(MODS[1], page[s2:e2])
    write(SRC, src)
    print('source', len(src), 'tx module', e1 - s1, 'rx module', e2 - s2)


def build():
    page = read(SRC)
    for mark, fn in zip(MARKS, MODS):
        m = read(fn)
        assert '</script' not in m.lower() and page.count(mark) == 1
        page = page.replace(mark, m)
    write(OUT, page)
    print(OUT, len(page), hashlib.sha256(page.encode('utf-8')).hexdigest())


if __name__ == '__main__':
    if sys.argv[1] == 'extract':
        extract(sys.argv[2] if len(sys.argv) > 2 else OUT)
    else:
        build()
