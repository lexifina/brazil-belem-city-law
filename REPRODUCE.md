# How this repository was made (Belém)

This file is written by the build on 2026-10-31, the day the source data was retrieved.

## Sources

| Source | Address | Retrieved | Licence |
| --- | --- | --- | --- |
| Câmara Municipal de Belém: Lei Orgânica do Município, atualizada em setembro de 2026 (PDF) | <https://www.cmb.pa.gov.br/portal-da-transparencia/lei-organica-do-municipio> | 2026-10-31 | Text: Câmara Municipal de Belém, Lei Orgânica do Município de Belém (LOMB), atualizada em setembro de 2026, www.cmb.pa.gov.br. Lei 9.610/1998 art. 8 IV: the texts of laws and other official acts are not protected by copyright. Non-official text: only the Diário Oficial do Município is authoritative. |

Every word of law in this repository comes from these sources. Lexifina reads them and records each act's dated versions, and the laws that made each change, in one corpus file. This repository is built from that file.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `lei-organica` | Lei Orgânica do Município de Belém | 1 | 2026-09-09 to 2026-09-09 |

The build made 1 commits:

| Commits | Kind |
| ---: | --- |
| 1 | first version of an act |
| 0 | one law on its in-force day |
| 0 | changes no amendment note explains, credited to the publisher |

Other counts:
- 0 commits on the branch `futuro`: laws not yet in force on 2026-10-31.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 1 laws in the record.
- 1 tags.

## Dates

Each commit is dated at noon (America/Belem) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: The Lei Orgânica and its amendments are promulgated by the Mesa da Câmara and take effect on promulgation; this record holds only the updated text, dated by the latest amendment it cites. https://www.cmb.pa.gov.br/portal-da-transparencia/lei-organica-do-municipio

## How the history is built

`tools/build.py` turns the corpus into this history in one pass: one commit per law, on the day it took effect. The same corpus always gives the same commit hashes. `tools/check_repo.py` reads every version back from git and compares it with the corpus. `tools/on.py` shows the law as it stood on any date. The corpus format is described in `tools/SCHEMA.md`.

- Corpus: sha256 `665f50fc8ae46e8c054803c67b079eb777d13615755edb28f635e4e2cd70d16b` (234268 bytes).
- Builder blob hashes (`git hash-object`): `build.py` `a4faa25af85facb64b956b372f6b528aafdd7ec1`, `check.py` `3d00541d258745461ab52b1b0cb4e1716a27a95d`, `on.py` `644a6c0857fbcc72562032b58d57aa113fee0641`.
- Python 3.12.10; git version 2.46.0.windows.1.

## Checks

1 versions of 1 acts read back from git on the day each took effect and on the day before: 0 mismatches. Trailers: 0 commits whose trailers git cannot parse. Health: 0 merge commits on main, 0 commit dates that go backwards, 0 commits dated after the build.

No second build of this corpus has been compared yet.

## Decisions made by hand

- The Lei Orgânica is given only as the Câmara's updated edition ("LOMB atualizada em setembro de 2026"), credited to the Câmara as the oldest version available and dated by the latest date among the amendments its notes cite. The text as promulgated on 30 March 1990 and the wordings the amendments replaced are not in the edition, so no earlier version is given.
- The alteration notes in parentheses ("(Com Redação dada pela Emenda nº ...)", "(Redação incluída pela ...)", "(Suprimida pela ...)") are left out of the text; markers such as "(AC)" that the edition prints as part of a provision are kept. A paragraph broken across two pages is joined again; where the edition runs several provisions into one paragraph, they stay one line.
- One file per Art.; headings stand above the first article under them. Text after the last article (place and date) stays with the last article.

## What AI did and did not do

The scripts that read the sources and build this repository were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- Claude Code (claude-opus-5-5) wrote Lexifina's code and chose the sources. No model output is used as legal text or dates: every word comes from the Câmara's PDF.
