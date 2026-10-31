# Belém (city): law history in git

The municipal law of the Município de Belém, the city of Belém (Pará) (Brazil) as a git history: one file per Artigo, one paragraph per line, so `git blame`, `git log` and `git diff` work line by line. The text is Portuguese, the only official language.

It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law).

## What this repository holds

| Folder | Act | Versions |
| --- | --- | ---: |
| `lei-organica/` | Lei Orgânica do Município de Belém (LOMB, 1990), as updated by the Câmara in September 2026 | 1 |

**Lei Orgânica only.** The Câmara's list of municipal laws gives numbers, dates and summaries but no texts, so no ordinary or complementary law is in yet. The text is given **only as the edition's text in force**, credited to the Câmara as the oldest version available. State law is in [brazil-para-law](https://github.com/lexifina/brazil-para-law); federal law in [brazil-law](https://github.com/lexifina/brazil-law).

## Source

[Câmara Municipal de Belém, Lei Orgânica do Município](https://www.cmb.pa.gov.br/portal-da-transparencia/lei-organica-do-municipio), published by the Câmara Municipal de Belém. Each version names the page it was taken from and that page's sha256, in `data/versions.json`.

## Dates

The one version is dated by the latest date among the amendments the edition's notes cite (an amendment of 9 September 2026). Commits are at noon in Belém.

## How it is built

Lexifina reads the sources listed here and records each act's dated versions, and the laws that made each change, in one corpus file. `tools/build.py` writes this repository from that file, and the same corpus always gives the same commit hashes; `REPRODUCE.md` gives the details and the checks. A model (Claude) wrote Lexifina's code; it wrote no legal text, and no model runs when the history is built.

The PDF's text layer is read with PyMuPDF line by line and the lines are joined into paragraphs (a new paragraph at each provision label, heading, or after a line ending in ".", ";" or ":"). The alteration notes in parentheses ("(Com Redação dada pela Emenda nº 28, de 20 de dezembro de 2006)", "(Redação incluída pela ...)", "(Suprimida pela ...)" and other notes naming an amendment by number) are left out; markers the edition prints as part of a provision, such as "(NR)" and "(AC)", are kept. One file per Art.; headings stand above the first article under them.

## How it is checked

Every version is read back from git on the day it took effect (`tools/check_repo.py`) and must match the corpus; an independent letters-and-digits comparison of every version against the source page must show no difference. Results are in `REPRODUCE.md`.

## What "author" means

The author of each commit is the law that made the text, or, for a consolidated text, the publisher, with an e-mail address that cannot exist; the committer is always Lexifina.

## Limits

Not a history: the Lei Orgânica as promulgated on 30 March 1990 and the wordings its amendments replaced are not in the edition. Where the edition runs several provisions into one paragraph, they stay one line. The text is not the official version: only the Diário Oficial do Município is authoritative.

## Licence

See [LICENSE](LICENSE): Brazilian law texts are not protected by copyright (Lei 9.610/1998, art. 8, IV). Fonte: Câmara Municipal de Belém, Lei Orgânica do Município, Câmara Municipal de Belém.
