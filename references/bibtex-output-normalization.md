# BibTeX output normalization

Apply this specification after bibliographic identity is verified and before corrected BibTeX is delivered.

## Author-name order

1. Render every personal author as `Family, Given`, separated by ` and `.
2. Preserve the official author sequence; normalize only each person's name representation.
3. Render suffixes as `Family, Jr., Given`.
4. Preserve particles and compound family names according to the official record.
5. Do not mechanically invert an ambiguous name. Verify it from the publisher, ORCID, or another primary source.
6. Preserve corporate or group authors as double-braced literals, such as `author = {{OpenAI}}`; do not invert them.
7. Use the same representation for the same established author throughout one output.

Correct:

```bibtex
author = {Christen, Sammy and Kocabas, Muhammed and Aksan, Emre},
```

Do not mix it with:

```bibtex
author = {Sammy Christen and Muhammed Kocabas and Emre Aksan},
```

## Minimal braces

1. Treat the outer `{...}` after `=` as the field-value delimiter, not as title protection.
2. Protect only case-sensitive tokens, for example `{D-Grasp}`, `{3D}`, `{AR}`, `{VR}`, `{NeRF}`, `{PointNet++}`, or `{FiLM}`.
3. Preserve braces required by LaTeX accents, commands, and mathematics.
4. Remove redundant whole-title wrappers such as `title = {{{D-Grasp}: ...}}`.
5. Prefer `title = {{D-Grasp}: Physically plausible ...}`: the outer pair delimits the value and `{D-Grasp}` protects only the branded token.
6. Never remove necessary acronym protection merely to reduce the brace count.
7. Never change title wording or capitalization while minimizing braces.

## Deterministic field order

Use one global field order for every entry type. Write only applicable fields, skip absent fields, and never change the relative order of the remaining fields based on entry type, publisher, source file, or original field order.

Sort fields by this exact priority:

```text
author
editor
title
journal or booktitle
publisher
institution
school
organization
address
edition
series
chapter
volume
number
pages
month
year
isbn
issn
eprint
archivePrefix
howpublished
doi
url
urldate
note
```

Use `journal` and `booktitle` mutually exclusively.

Examples derived from the same global priority:

```text
@article:       author, title, journal, volume, number, pages, year, doi, url, note
@inproceedings: author, title, booktitle, address, volume, number, pages, year, doi, url, note
@book:          author/editor, title, publisher, address, edition, series, volume, year, isbn, doi, url, note
@misc:          author, title, year, eprint, archivePrefix, howpublished, doi, url, urldate, note
@techreport:    author, title, institution, address, number, pages, year, doi, url, note
```

These are illustrations, not separate per-type ordering rules. Every example is produced by filtering the single global priority list above.

Place an indispensable nonstandard field not listed above immediately before `note`, document why it is retained, and use the same placement for every occurrence.

## Validation

Fail output validation when any of the following is true:

- personal authors mix `Family, Given` and `Given Family` conventions;
- official author sequence changes;
- a corporate author is inverted or loses literal protection;
- a multiword title has a redundant whole-title brace wrapper;
- a case-sensitive token loses necessary protection;
- title wording or capitalization changes during brace minimization;
- an entry's actual field-name sequence violates the priority above;
- different entry types use different relative ordering for fields they share;
- DOI/URL-inclusive and DOI/URL-free variants differ in any non-DOI/URL field or field order.
