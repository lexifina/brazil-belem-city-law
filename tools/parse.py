"""Builds corpus.d/10-lei-organica.json for the Município de Belém from the Câmara Municipal's updated edition of the
Lei Orgânica (PDF with a text layer, "LOMB atualizada em setembro de 2026"; no network).

    python -X utf8 parse.py --today YYYY-MM-DD

Read with PyMuPDF line by line; lines are joined into paragraphs (see text_and_notes). The alteration notes in parentheses ("(Com Redação dada pela Emenda nº 28, de 20 de
dezembro de 2006)", "(Redação incluída pela ...)", "(Suprimida pela ...)") are left out of the text and give the version
its date: the latest date they cite. A paragraph broken across two pages is joined again.
"""
import argparse, re, sys
from pathlib import Path

import pymupdf

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from br_lib import units_of, write_part, sha, norm, LONG, MONTHS  # noqa: E402

PDF_URL = 'https://www.cmb.pa.gov.br/uploads/blocos/2026/09/lomb-atualizada-em-setembro-de-2026_1790767468_cf5e136c.pdf'
PAGE_URL = 'https://www.cmb.pa.gov.br/portal-da-transparencia/lei-organica-do-municipio'
PDF = HERE / '.cache' / 'lom.pdf'
NOTE = re.compile(r'\(\s*(?:Com\s+)?(?:Reda[çc][ãa]o|Suprimid|Revogad|Inclu[íi]d|Acrescid|Acrescentad|Alterad)[^()]*\)'
                  r'|\([^()]*\bemendas?\b[^()]*n[º°.o]\s*\d[^()]*\)', re.I)
STARTS = re.compile(r'^(?:Art\.|§|Par[áa]grafo|[IVXLC]+\s*[-–]|[a-z]\)|T[ÍI]TULO|CAP[ÍI]TULO|Se[çc][ãa]o|Subse[çc][ãa]o|ATO\b)')


HEADING = re.compile(r'^(?:T[ÍI]TULO|CAP[ÍI]TULO|SE[ÇC][ÃA]O|Se[çc][ãa]o|Subse[çc][ãa]o|SUBSE[ÇC][ÃA]O|ATO\b)')


def text_and_notes():
    """The PDF read with PyMuPDF line by line (pdftotext misplaces a word in one line), lines joined into paragraphs:
    a paragraph starts at a provision label ("Art.", "§", "Parágrafo", "I -", "a)"), at a heading line (all capitals,
    or "Seção"/"Subseção"), or after a line ending in ".", ";" or ":"; a line ending in "-" joins the next without a
    space."""
    doc = pymupdf.open(PDF)
    raw = [norm(l) for p in doc for l in p.get_text().split('\n')]
    paras = []
    for l in raw:
        if not l:
            continue
        head = HEADING.match(l) or (l == l.upper() and re.search(r'[A-ZÀ-Ý]{3}', l))
        prev = paras[-1] if paras else None
        if prev is None or STARTS.match(l) or head or re.search(r'[.;:]["”]?$', prev[1]) or prev[0]:
            paras.append([bool(head), l])
        elif prev[1].endswith('-'):
            prev[1] += l
        else:
            prev[1] += ' ' + l
    s = '\n'.join(p[1] for p in paras)
    notes = []
    while NOTE.search(s):  # notes can nest: "((Redação incluída pela ...) e Redação alterada pela ...)"
        notes += [re.sub(r'\s+', ' ', n) for n in NOTE.findall(s)]
        s = NOTE.sub(' ', s)
    out = [norm(l) for l in s.split('\n')]
    return [l for l in out if l and re.search(r'\w', l)], notes


DMY = re.compile(r'(\d{1,2})[./](\d{1,2})[./](\d{4})')


def dates(s):
    out = [f'{int(y):04d}-{MONTHS[mo.lower()]:02d}-{int(d):02d}' for d, mo, y in LONG.findall(s)]
    return out + [f'{int(y):04d}-{int(m):02d}-{int(d):02d}' for d, m, y in DMY.findall(s) if 1 <= int(m) <= 12]


COUNTRY = {
    'code': 'BR-PA-BELEM', 'name': 'Belém', 'slug': 'brazil-belem-city', 'lang': 'pt', 'tz': 'America/Belem',
    'future_branch': 'futuro',
    'publisher': {'name': 'Câmara Municipal de Belém', 'email': 'cmb@cmb.pa.gov.br.invalid'},
    'default_in_force_rule': {
        'text': 'The Lei Orgânica and its amendments are promulgated by the Mesa da Câmara and take effect on '
                'promulgation; this record holds only the updated text, dated by the latest amendment it cites.',
        'source': PAGE_URL},
    'licence_note': 'Text: Câmara Municipal de Belém, Lei Orgânica do Município de Belém (LOMB), atualizada em '
                    'setembro de 2026, www.cmb.pa.gov.br. Lei 9.610/1998 art. 8 IV: the texts of laws and other '
                    'official acts are not protected by copyright. Non-official text: only the Diário Oficial do '
                    'Município is authoritative.',
}
DECISIONS = [
    'The Lei Orgânica is given only as the Câmara\'s updated edition ("LOMB atualizada em setembro de 2026"), credited '
    'to the Câmara as the oldest version available and dated by the latest date among the amendments its notes cite. '
    'The text as promulgated on 30 March 1990 and the wordings the amendments replaced are not in the edition, so no '
    'earlier version is given.',
    'The alteration notes in parentheses ("(Com Redação dada pela Emenda nº ...)", "(Redação incluída pela ...)", '
    '"(Suprimida pela ...)") are left out of the text; markers such as "(AC)" that the edition prints as part of a '
    'provision are kept. A paragraph broken across two pages is joined again; where the edition runs several '
    'provisions into one paragraph, they stay one line.',
    'One file per Art.; headings stand above the first article under them. Text after the last article (place and '
    'date) stays with the last article.',
]
AI = ["Claude Code (claude-opus-5-5) wrote Lexifina's code and chose the sources. No model output is used as legal "
      "text or dates: every word comes from the Câmara's PDF."]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--today', required=True)
    a = ap.parse_args()
    lines, notes = text_and_notes()
    ds = sorted(d for n in notes for d in dates(n) if d <= a.today)
    units = units_of([('p', l) for l in lines], adt=False)
    b = PDF.read_bytes()
    key = 'lei-organica-1990'
    laws = {key: {'label': 'Lei Orgânica do Município de Belém, de 30 de março de 1990',
                  'title': 'Lei Orgânica do Município de Belém', 'kind': 'law', 'enacted': '1990-03-30',
                  'published': None, 'url': PAGE_URL, 'temporary_until': None, 'restores': None, 'note': None}}
    v = {'from': ds[-1], 'source_url': PDF_URL, 'sha256': sha(b), 'units': units,
         'note': f'Text in force as updated by the Câmara Municipal de Belém (edition of September 2026); its notes cite '
                 f'amendments of {len(set(ds))} dates, the latest {ds[-1]}.'}
    act = {'slug': 'lei-organica', 'short': 'LOMB', 'title': 'Lei Orgânica do Município de Belém', 'url': PAGE_URL,
           'first_law': None, 'earlier_laws': [key], 'versions': [v]}
    c = {'country': COUNTRY,
         'sources': [{'name': 'Câmara Municipal de Belém: Lei Orgânica do Município, atualizada em setembro de 2026 '
                              '(PDF)', 'url': PAGE_URL, 'retrieved': a.today, 'licence': COUNTRY['licence_note'],
                      'notes': '1 act.'}],
         'laws': laws, 'acts': [act], 'applies': [], 'decisions': DECISIONS, 'ai_use': AI}
    print(write_part(HERE / 'corpus.d', '10-lei-organica', c), len(units), ds[-1], len(notes))


if __name__ == '__main__':
    main()
