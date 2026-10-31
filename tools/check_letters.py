"""Independent letters-and-digits check of the Lei Orgânica against the PDF, read with a second PDF reader (pypdf, not
the builder's PyMuPDF) and none of the builder's code.

    python -X utf8 check_letters.py [part.json ...]

The whole PDF text, with the alteration notes in parentheses removed (a parenthesis starting "Com Redação",
"Redação", "Suprimid-", "Revogad-", "Incluíd-", "Acrescid-", "Acrescentad-" or "Alterad-", or one naming an
amendment by number), reduced to letters and digits, must equal the version's unit files reduced the same way, each
unit found at its place in document order.
"""
import hashlib, io, json, re, sys
from pathlib import Path

import pypdf

HERE = Path(__file__).resolve().parent


def sp(*alts):
    """pypdf sometimes puts spaces inside words ("R edação"): allow whitespace between letters."""
    return '(?:' + '|'.join(r'\s*'.join(re.escape(ch) for ch in w) for w in alts) + ')'


OPEN = (r'\(\s*(?:' + sp('Com') + r'\s*)?(?:' + sp('Redação', 'Redacao', 'Suprimid', 'Revogad', 'Incluíd', 'Includ',
                                                  'Acrescid', 'Acrescentad', 'Alterad') + ')')
EMENDA = r'\([^()]*' + sp('emenda') + r'[^()]*n\s*[º°.o]\s*\d[^()]*\)'


def ld(s):
    return ''.join(ch for ch in s if ch.isalnum())


def pdf_text(raw):
    t = '\n'.join(p.extract_text() for p in pypdf.PdfReader(io.BytesIO(raw)).pages)
    while True:  # nested notes go from the inside out
        u = re.sub(EMENDA, ' ', re.sub(OPEN + r'[^()]*\)', ' ', t, flags=re.I), flags=re.I)
        if u == t:
            return t
        t = u


def main(paths):
    bad = total = 0
    for p in paths:
        for a in json.load(open(p, encoding='utf-8'))['acts']:
            for v in a['versions']:
                raw = (HERE / '.cache' / 'lom.pdf').read_bytes()
                assert hashlib.sha256(raw).hexdigest() == v['sha256'], (a['slug'], 'sha256')
                src = ld(pdf_text(raw))
                rest = {k: ld(re.sub(r'(?m)^#+ ', '', u['text'])) for k, u in v['units'].items()}
                pos = 0
                while rest:
                    hit = None
                    for k, t in rest.items():
                        if t and src.startswith(t, pos) and (hit is None or len(t) > len(rest[hit])):
                            hit = k
                    if hit is None:
                        break
                    pos += len(rest.pop(hit))
                total += 1
                if rest or pos != len(src):
                    bad += 1
                    print(f'MISMATCH {a["slug"]} {v["from"]}: matched {pos}/{len(src)}; next source: '
                          f'{src[pos:pos + 80]!r}; unplaced: {list(rest)[:5]}')
    print(f'{total} versions checked, {bad} mismatches')
    return bad


if __name__ == '__main__':
    sys.exit(1 if main(sys.argv[1:] or sorted(str(p) for p in (HERE / 'corpus.d').glob('*.json'))) else 0)
