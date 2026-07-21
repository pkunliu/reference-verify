# Reference Verify

**English** | [简体中文](README.zh-CN.md)

`reference-verify` is a Codex skill for strict academic reference verification. It audits BibTeX, reference lists, and CSV/XLSX bibliographic data, with an emphasis on formal publication metadata, DOI identity, pagination, conference locations, and consistent journal or conference names.

## Core features

- Preserve original paper titles, BibTeX keys, and entry order.
- Prefer primary sources such as publisher records, official proceedings, and DOI landing pages.
- Check whether arXiv, OpenReview, or workshop papers have formal published versions.
- Accept a DOI only when its registered title matches the supplied title.
- Distinguish continuous page ranges, eLocators, ACM article numbers, and PDF-local pages.
- Verify conference `address` fields without guessing event locations.
- Apply one canonical name to every occurrence of the same journal or conference.
- Produce a verified CSV, corrected BibTeX, an XLSX with unresolved rows highlighted, and an audit report when needed.

## Installation

### Ask Codex to install it

Send the following request to Codex:

```text
Install the reference-verify skill from this GitHub repository:
https://github.com/pkunliu/reference-verify
```

When the repository is private, the installer must have permission to access it.

### Manual installation

```bash
git clone https://github.com/pkunliu/reference-verify.git ~/.codex/skills/reference-verify
```

Restart Codex or open a new task after installation so the skill can be discovered.

## Usage

Invoke the skill in Codex with `$reference-verify`.

### Audit a complete BibTeX file

```text
Use $reference-verify to audit references.bib.
Preserve every original title and citation key, and verify formal publication versions,
DOIs, pagination, conference addresses, and canonical venue names.
```

### Find formal versions of preprints

```text
Use $reference-verify to check whether these arXiv entries have been published
in formal journals or conference proceedings. Adopt formal metadata only when
the title identity is an exact match.
```

### Normalize journal and conference names

```text
Use $reference-verify to check whether each journal or conference has one
consistent canonical name throughout this BibTeX file, and verify the address
for every conference paper.
```

## Verification principles

1. Do not rewrite the supplied paper title.
2. Do not infer a DOI from authors, topic similarity, or neighboring page ranges.
3. Do not treat PDF-local page numbers as formal proceedings pagination.
4. If a formal version has a substantively different title, report it as a related publication instead of creating a hybrid citation.
5. Leave fields unresolved when they cannot be confirmed from official or primary sources.

## Repository structure

```text
reference-verify/
├── README.md
├── README.zh-CN.md
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   └── source-and-doi-rules.md
└── scripts/
    └── csv_to_bibtex.py
```

`SKILL.md` defines the complete verification workflow. `references/` contains source, DOI, pagination, conference-location, and venue-name rules. `scripts/` provides deterministic conversion utilities.
