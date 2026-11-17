"""Génère la police pixel « CloudBlocks » (style blocs, inspirée de Minecraft, dessin original)
et l'injecte en base64 dans index.html.  Usage : python3 outils/police.py
Chaque glyphe = lignes de haut (hauteur 6) en bas (hauteur 0) ; une 8e ligne = jambage (hauteur -1).
"""
import base64, io, re, sys, pathlib
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen

P = 125  # taille d'un pixel en unités (em = 8 pixels)
G = {
 'A': ".###. #...# #...# ##### #...# #...# #...#", 'B': "####. #...# ####. #...# #...# #...# ####.",
 'C': ".###. #...# #.... #.... #.... #...# .###.", 'D': "####. #...# #...# #...# #...# #...# ####.",
 'E': "##### #.... ###.. #.... #.... #.... #####", 'F': "##### #.... ###.. #.... #.... #.... #....",
 'G': ".#### #.... #..## #...# #...# #...# .###.", 'H': "#...# #...# ##### #...# #...# #...# #...#",
 'I': "### .#. .#. .#. .#. .#. ###",              'J': "....# ....# ....# ....# ....# #...# .###.",
 'K': "#...# #..#. ###.. #..#. #...# #...# #...#", 'L': "#.... #.... #.... #.... #.... #.... #####",
 'M': "#...# ##.## #.#.# #...# #...# #...# #...#", 'N': "#...# ##..# #.#.# #..## #...# #...# #...#",
 'O': ".###. #...# #...# #...# #...# #...# .###.", 'P': "####. #...# ####. #.... #.... #.... #....",
 'Q': ".###. #...# #...# #...# #...# #..#. .##.#", 'R': "####. #...# ####. #...# #...# #...# #...#",
 'S': ".#### #.... .###. ....# ....# #...# .###.", 'T': "##### ..#.. ..#.. ..#.. ..#.. ..#.. ..#..",
 'U': "#...# #...# #...# #...# #...# #...# .###.", 'V': "#...# #...# #...# #...# #...# .#.#. ..#..",
 'W': "#...# #...# #...# #...# #.#.# ##.## #...#", 'X': "#...# .#.#. ..#.. .#.#. #...# #...# #...#",
 'Y': "#...# .#.#. ..#.. ..#.. ..#.. ..#.. ..#..", 'Z': "##### ....# ...#. ..#.. .#... #.... #####",
 'a': "..... ..... .###. ....# .#### #...# .####", 'b': "#.... #.... #.##. ##..# #...# #...# ####.",
 'c': "..... ..... .###. #...# #.... #...# .###.", 'd': "....# ....# .##.# #..## #...# #...# .####",
 'e': "..... ..... .###. #...# ##### #.... .####", 'f': "..## .#.. #### .#.. .#.. .#.. .#..",
 'g': "..... ..... .#### #...# #...# .#### ....# ####.", 'h': "#.... #.... #.##. ##..# #...# #...# #...#",
 'i': "# . # # # # #", 'j': "...# .... ...# ...# ...# ...# #..# .##.",
 'k': "#... #... #..# #.#. ##.. #.#. #..#", 'l': "#. #. #. #. #. #. .#",
 'm': "..... ..... ##.#. #.#.# #.#.# #...# #...#", 'n': "..... ..... ####. #...# #...# #...# #...#",
 'o': "..... ..... .###. #...# #...# #...# .###.", 'p': "..... ..... #.##. ##..# #...# ##..# #.##. #....",
 'q': "..... ..... .##.# #..## #...# #..## .##.# ....#", 'r': "..... ..... #.##. ##..# #.... #.... #....",
 's': "..... ..... .#### #.... .###. ....# ####.", 't': ".#. .#. ### .#. .#. .#. ..#",
 'u': "..... ..... #...# #...# #...# #...# .####", 'v': "..... ..... #...# #...# #...# .#.#. ..#..",
 'w': "..... ..... #...# #...# #.#.# #.#.# .####", 'x': "..... ..... #...# .#.#. ..#.. .#.#. #...#",
 'y': "..... ..... #...# #...# #...# .#### ....# ####.", 'z': "..... ..... ##### ...#. ..#.. .#... #####",
 '0': ".###. #...# #..## #.#.# ##..# #...# .###.", '1': "..#.. .##.. ..#.. ..#.. ..#.. ..#.. #####",
 '2': ".###. #...# ....# ..##. .#... #.... #####", '3': ".###. #...# ....# ..##. ....# #...# .###.",
 '4': "...## ..#.# .#..# #...# ##### ....# ....#", '5': "##### #.... ####. ....# ....# #...# .###.",
 '6': "..##. .#... #.... ####. #...# #...# .###.", '7': "##### #...# ....# ...#. ..#.. ..#.. ..#..",
 '8': ".###. #...# #...# .###. #...# #...# .###.", '9': ".###. #...# #...# .#### ....# ...#. .##..",
 '!': "# # # # # . #", '?': ".###. #...# ....# ...#. ..#.. ..... ..#..",
 '.': ". . . . . . #", ',': ". . . . . . # #", ':': ". . # . . . #", ';': ". . # . . . # #",
 "'": "# # . . . . .", '"': "#.# #.# ... ... ... ... ...",
 '-': ".... .... .... #### .... .... ....", '+': "..... ..#.. ..#.. ##### ..#.. ..#.. .....",
 '(': "..# .#. #.. #.. #.. .#. ..#", ')': "#.. .#. ..# ..# ..# .#. #..",
 '/': "....# ...#. ...#. ..#.. .#... .#... #....", '%': "#...# ....# ...#. ..#.. .#... #.... #...#",
 '*': "..#.. #.#.# .###. #.#.# ..#.. ..... .....", '_': "..... ..... ..... ..... ..... ..... ..... #####",
 '#': ".#.#. ##### .#.#. .#.#. ##### .#.#. .....", '=': "..... ..... ##### ..... ##### ..... .....",
 '<': "...# ..#. .#.. #... .#.. ..#. ...#", '>': "#... .#.. ..#. ...# ..#. .#.. #...",
 '·': ". . . # . . .", '…': "..... ..... ..... ..... ..... ..... #.#.#",
 '—': "...... ...... ...... ###### ...... ...... ......",
}
ALIAS = {'’': "'", '‘': "'", '“': '"', '”': '"', '–': '-', '✶': '*', '×': 'x'}
# Accents posés sur les minuscules (2 lignes au-dessus de la hauteur d'x)
ACC = {'aigu': ["...#.", "..#.."], 'grave': [".#...", "..#.."], 'circ': ["..#..", ".#.#."],
       'trema': [".#.#.", "....."], 'tilde': [".##.#", "#.##."]}
COMPO = {'á': ('a', 'aigu'), 'à': ('a', 'grave'), 'â': ('a', 'circ'), 'ä': ('a', 'trema'), 'ã': ('a', 'tilde'),
         'é': ('e', 'aigu'), 'è': ('e', 'grave'), 'ê': ('e', 'circ'), 'ë': ('e', 'trema'),
         'ó': ('o', 'aigu'), 'ò': ('o', 'grave'), 'ô': ('o', 'circ'), 'ö': ('o', 'trema'), 'õ': ('o', 'tilde'),
         'ú': ('u', 'aigu'), 'ù': ('u', 'grave'), 'û': ('u', 'circ'), 'ü': ('u', 'trema'),
         'í': ('i', 'aigu'), 'ì': ('i', 'grave'), 'î': ('i', 'circ'), 'ï': ('i', 'trema')}

def lignes(car):
    return G[car].split()
def compose(base, acc):
    b = lignes(base)[2:7] if base != 'i' else ['.#.'] * 5
    w = len(b[0]); a = [l[:w] if w >= 5 else l[1:4] for l in ACC[acc]]
    return a + b
# Vietnamien : ơ (o cornu), ở (ơ + crochet), ế / ố (circonflexe + aigu)
G['ơ'] = "...... ....#. .###.# #...#. #...#. #...#. .###.."
G['ở'] = ".##... ...#.# .###.# #...#. #...#. #...#. .###.."
G['ế'] = "...#. ..#.# .###. #...# ##### #.... .####"
G['ố'] = "...#. ..#.# .###. #...# #...# #...# .###."

def main():
    fb = FontBuilder(1000, isTTF=True)
    carte = {**{c: c for c in G}, **{c: c for c in COMPO}, **{a: b for a, b in ALIAS.items()}}
    noms = {c: f"g{ord(c):04X}" for c in list(G) + list(COMPO)}
    ordre = ['.notdef', 'space'] + list(noms.values())
    glyphes, metriques = {}, {}
    def dessin(rows):
        pen = TTGlyphPen(None); w = max(len(r) for r in rows)
        for i, r in enumerate(rows):
            h = 6 - i; x = 0
            while x < len(r):
                if r[x] == '#':
                    x1 = x
                    while x1 < len(r) and r[x1] == '#': x1 += 1
                    y0, y1 = h * P, (h + 1) * P
                    pen.moveTo((x * P, y0)); pen.lineTo((x * P, y1)); pen.lineTo((x1 * P, y1)); pen.lineTo((x1 * P, y0)); pen.closePath()
                    x = x1
                else: x += 1
        return pen.glyph(), (w + 1) * P
    vide = TTGlyphPen(None).glyph()
    glyphes['.notdef'] = vide; metriques['.notdef'] = (4 * P, 0)
    glyphes['space'] = TTGlyphPen(None).glyph(); metriques['space'] = (4 * P, 0)
    for c, n in noms.items():
        rows = compose(*COMPO[c]) if c in COMPO else lignes(c)
        g, adv = dessin(rows); glyphes[n] = g; metriques[n] = (adv, 0)
    cmap = {32: 'space', 160: 'space'}
    for c, n in noms.items(): cmap[ord(c)] = n
    for a, b in ALIAS.items(): cmap[ord(a)] = noms[b]
    fb.setupGlyphOrder(ordre); fb.setupCharacterMap(cmap); fb.setupGlyf(glyphes)
    fb.setupHorizontalMetrics(metriques); fb.setupHorizontalHeader(ascent=875, descent=-125)
    fb.setupNameTable({'familyName': 'CloudBlocks', 'styleName': 'Regular'})
    fb.setupOS2(sTypoAscender=875, sTypoDescender=-125, sTypoLineGap=0, usWinAscent=875, usWinDescent=125)
    fb.setupPost()
    buf = io.BytesIO(); fb.save(buf); b64 = base64.b64encode(buf.getvalue()).decode()
    html = pathlib.Path(__file__).resolve().parent.parent / 'index.html'
    s = html.read_text()
    bloc = ("/* POLICE-DEBUT : police pixel générée par outils/police.py (ne pas éditer à la main) */\n"
            f"  @font-face {{ font-family: 'CloudBlocks'; src: url(data:font/ttf;base64,{b64}) format('truetype'); font-display: block; }}\n"
            "  /* POLICE-FIN */")
    if 'POLICE-DEBUT' in s: s = re.sub(r"/\* POLICE-DEBUT.*?POLICE-FIN \*/", lambda m: bloc, s, flags=re.S)
    else: s = s.replace('<style>\n', '<style>\n  ' + bloc + '\n', 1)
    html.write_text(s); print('police :', len(buf.getvalue()), 'octets,', len(noms), 'glyphes')
main()
