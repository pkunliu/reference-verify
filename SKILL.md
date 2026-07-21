---
name: reference-verify
description: Strictly verify academic references, formal publication sources, canonical journal and conference names, conference locations, page ranges, published versions of preprints, and DOI-title consistency. Use for BibTeX or reference audits that must preserve every input title exactly, use one consistent name for each venue, require an address for each conference paper, and export ordered CSV, XLSX, and corrected BibTeX artifacts.
---

# Reference Verify

## When to use

Use this skill whenever the user asks to:

- verify BibTeX or reference metadata;
- check page ranges;
- find official publication sources;
- determine whether arXiv/OpenReview papers have formal publications;
- find DOI values by paper title;
- verify that a DOI belongs to the exact supplied title;
- export results to CSV or Excel-compatible format.

## Core non-negotiable rules

1. Never change the supplied paper title.
2. Preserve the original reference order and BibTeX key.
3. Search for formal publications using the exact supplied title first.
4. A DOI may be written into the result only when the DOI landing-page title matches the supplied title.
5. Do not infer or fabricate a DOI.
6. Do not use a DOI merely because the authors and topic appear similar.
7. If a formal version uses a materially different title, report it as a possible related publication but do not assign its DOI to the supplied title.
8. Do not treat PDF-local page numbers such as `1--14` as formal proceedings pages unless the official publisher record defines them that way.
9. Distinguish formal page ranges, article numbers/eLocators, ACM article numbers with article-local pages, and records with no formal continuous pages.
10. Prefer the final published version over arXiv only when identity is verified.
11. Every corrected field must have an official or primary source.
12. Unresolved items must remain unresolved; never guess.
13. Every verified conference paper must include a verified `address`; do not invent a location from the venue name or year.
14. Use exactly one verified canonical `journal` or `booktitle` spelling for every shared venue identity across the complete input.

## Accepted inputs

- `.bib`
- `.txt` containing BibTeX
- pasted BibTeX/reference list
- `.csv` or `.xlsx` reference table

If the input is a spreadsheet, preserve the original row order.

## Verification source priority

Read `references/source-and-doi-rules.md` before resolving venue-specific
source, DOI, pagination, conference-address, or canonical-name questions.

Use the highest available source:

1. Official publisher paper page.
2. Official conference proceedings individual paper page.
3. DOI landing page from the publisher.
4. Official proceedings table of contents.
5. OpenReview/PMLR/CVF/NeurIPS official record.
6. IEEE Xplore, ACM Digital Library, SpringerLink, ScienceDirect, Wiley, AAAI.
7. arXiv only when no formal publication exists.
8. DBLP or Crossref only as a cross-check, not the sole final authority when a primary source exists.

Do not use Google Scholar, Semantic Scholar, ResearchGate, random BibTeX repositories, or search snippets as final proof.

## Full workflow

### Step 1: Parse and preserve

Parse every entry in order and retain:

- sequence number;
- BibTeX key;
- entry type;
- authors;
- exact original title;
- journal;
- booktitle;
- address;
- volume;
- number;
- pages;
- year;
- DOI;
- URL;
- arXiv ID.

Count the entries and report the count before long verification work.

### Step 2: Find the exact-title record

For each entry:

1. Search the exact title in quotation marks.
2. Check the official publisher/proceedings record.
3. Confirm title identity before accepting metadata.
4. Compare authors and year as secondary evidence.
5. Record the direct official paper URL, not only the venue homepage.

Title comparison may normalize only non-semantic typography:

- remove BibTeX braces;
- normalize whitespace;
- normalize Unicode dashes and quotation marks;
- compare case-insensitively when needed;
- normalize LaTeX accents;
- preserve mathematical symbols and substantive wording.

Do not treat added, removed, or replaced substantive words as an exact title match.

### Step 3: Detect formal publication of preprints

For arXiv/OpenReview/workshop entries:

1. Search the exact title.
2. Determine whether a final journal or conference version exists.
3. Verify that it is the same work using exact title, authors, abstract, and arXiv linkage.
4. If the exact title is unchanged, use the final publication metadata.
5. If the formal title differs materially, do not attach the formal DOI to the original title.
6. Record the preprint ID, formal publication status, official final-version URL, and whether the title is unchanged.

### Step 4: Verify pages

Use the publisher/proceedings record as the primary page source.

For CVPR/ICCV/WACV:

- record CVF Open Access pages;
- when IEEE Xplore has a different formal page range, use IEEE pages in `pages`;
- save CVF pages in `Alternative official pages`;
- explain the discrepancy.

For ICLR:

- use official ICLR proceedings pagination when explicitly available;
- otherwise leave pages blank;
- never use PDF length as formal pages.

For ACM:

- distinguish article number and article-local pages;
- retain the official citation representation and record the article number separately.

For Elsevier/Wiley eLocators:

- put the eLocator in `article_number`;
- do not describe it as a conventional page range.

### Step 5: Verify conference address

For every conference paper (`@inproceedings` or a record with a non-empty `booktitle`):

1. Verify the event location from the official conference site, official proceedings front matter, publisher record, or official program.
2. Record the physical venue as `City, Country` using the English country name used by the official source when available.
3. Use `Online` only when the event was officially held fully online; do not use it merely because the paper or proceedings are online.
4. For hybrid or multi-site events, preserve the official location wording and explain it in `Changes / notes`.
5. Do not substitute the publisher's address, organizer's headquarters, authors' affiliations, or the next/previous edition's location.
6. If the location cannot be confirmed from an official or primary source, leave `address` blank, set `Address verification = unresolved`, and set `Needs review = YES`.

A conference record is not complete until its `address` is verified. Keep an unconfirmed address unresolved rather than guessing, and do not present the corrected BibTeX as complete while any conference address remains blank.

### Step 6: Canonicalize venue names across all records

After verifying individual records, run a collection-wide venue consistency pass:

1. Assign a stable lowercase `Venue ID` to every non-empty `journal` or `booktitle`, such as `acm-tog`, `cvpr`, or `iclr`.
2. Group all rows by `Venue ID` and choose one canonical name supported by the official publisher or proceedings.
3. Prefer the official unabbreviated venue name. Do not mix abbreviations, acronyms, parenthetical aliases, capitalization variants, or optional `Proceedings of` forms within one `Venue ID`.
4. Keep year, edition number, location, volume, and publisher series outside the canonical venue name when separate BibTeX fields already represent them.
5. Do not merge a workshop with its main conference, a journal with its conference, or two distinct venues with similar names.
6. When a venue was formally renamed, treat materially different official-name eras as separate `Venue ID` values rather than rewriting history inaccurately.
7. Copy the chosen canonical string exactly into every grouped row and set `Venue name verification` to `verified` or `corrected`.
8. If venue identity is ambiguous, leave it unresolved, explain the competing identities in `Changes / notes`, and set `Needs review = YES`.

Examples of inconsistency that must be resolved include `ACM Trans. Graph.`, `ACM Transactions on Graphics (TOG)`, and `ACM Transactions on Graphics` appearing for the same verified journal identity.

### Step 7: Verify DOI against the exact title

For every DOI candidate:

1. Open the DOI landing page or official publisher record.
2. Extract the registered publication title.
3. Compare it with the exact supplied title after non-semantic normalization.
4. Fill `DOI` only when the title matches.
5. Set `DOI title match = exact` and identify the DOI type.
6. If the title does not match, leave `DOI` blank and set `DOI title match = mismatch—not adopted`.

Prefer a formal publication DOI over an arXiv DOI. Use an arXiv DOI only when no formal DOI exists and persistent preprint identifiers are requested.

### Step 8: Do not alter titles

The CSV `Title` column must be copied from the input exactly.

If the official title differs only by capitalization or typography, keep the input title and record the official rendering in notes if needed.

If the official title differs substantively, keep the input title, do not silently replace it, and mark the record for review.

### Step 9: Output CSV

Create a UTF-8 BOM CSV for Excel with these columns in this exact order:

```text
No.
Key
Entry type
Authors
Title
Original journal
Original booktitle
Original address
Original volume
Original number
Original pages
Original year
Formal publication status
Venue ID
journal
booktitle
Venue name verification
address
volume
number
pages
article_number
year
Alternative official pages
Page verification
Address verification
DOI
DOI URL
DOI title match
DOI type
arXiv ID
Verified source
Official URL
Verification status
Changes / notes
```

Definitions:

- `Title`: exact original title, unchanged.
- `Venue ID`: stable lowercase identifier used to enforce one canonical venue name across rows.
- `Venue name verification`: `verified`, `corrected`, `not applicable`, or `unresolved`.
- `pages`: verified primary formal page range.
- `address`: verified conference location; leave blank for non-conference records.
- `article_number`: eLocator or article number.
- `Alternative official pages`: secondary official pagination, such as CVF acceptance-version pages.
- `Address verification`: `verified`, `corrected`, `not applicable`, or `unresolved`.
- `DOI`: only a verified title-matching DOI.
- `DOI title match`: `exact`, `no DOI found`, or `mismatch—not adopted`.
- `Verification status`: `verified`, `corrected`, `partially verified`, or `unresolved`.

### Step 10: Validate before delivery

Before returning the CSV:

1. Row count equals parsed entry count.
2. Sequence is unchanged.
3. Every `Title` equals the original input title.
4. No DOI marked as a mismatch appears in the `DOI` column.
5. Every filled DOI has a direct DOI URL.
6. Every corrected page range has an official source.
7. Article numbers are not mislabeled as page ranges.
8. Future or not-yet-published records are not presented as already published.
9. Missing DOI values remain blank.
10. Record unresolved and ambiguous cases honestly.
11. Every conference paper has a verified `address`, or has blank `address`, `Address verification = unresolved`, and `Needs review = YES`.
12. Every row with `journal` or `booktitle` has a `Venue ID`, and each `Venue ID` maps to exactly one entry kind and one byte-for-byte identical canonical venue name.

## Progress updates

For large files:

- report parsed record count;
- report early confirmed errors;
- report progress after meaningful batches;
- report DOI acceptance criteria;
- do not claim completion before generating and validating the CSV.

## Default user-facing result

State the total records processed, number with verified formal sources, number with accepted DOI values, number of page corrections, unresolved cases, confirmation that titles were unchanged, and provide a link to the CSV.


## Mandatory corrected BibTeX output

In addition to the verified CSV, generate a corrected `.bib` file by default.

### CSV-to-BibTeX rules

1. Use the verified CSV as the source of truth.
2. Preserve:
   - original row order;
   - BibTeX key;
   - complete author string;
   - exact input title.
3. Select the entry type from verified metadata:
   - non-empty `journal` → `@article`;
   - non-empty `booktitle` → `@inproceedings`;
   - otherwise retain a valid original type such as `@misc` or `@techreport`.
4. Write only applicable fields, in this order:
   - `author`;
   - `title`;
   - `journal` or `booktitle`;
   - `address` for conference papers;
   - `volume`;
   - `number`;
   - `pages`;
   - `year`;
   - `doi`;
   - `eprint`;
   - `archivePrefix`;
   - `url`;
   - `note` for nonstandard records when useful.
5. Copy `DOI` only from the verified CSV. Never add a rejected or unverified DOI.
6. Use `Official URL` as `url`; fall back to `DOI URL`.
7. For arXiv records, write:
   ```bibtex
   eprint        = {ARXIV_ID},
   archivePrefix = {arXiv},
   ```
8. Normalize only page-range punctuation to BibTeX `--`. Do not change title wording or capitalization.
9. Do not copy audit-only columns such as verification notes into normal academic entries.
10. Validate before delivery:
    - BibTeX entry count equals CSV row count;
    - key order is identical;
    - keys are unique;
    - every generated title is byte-for-byte identical to the CSV `Title`;
    - every generated DOI exists in the CSV and passed title matching.
    - every generated conference entry copies its verified `address` from the CSV.

Use `scripts/csv_to_bibtex.py` for deterministic conversion when available.
The converter must stop with an error when a conference row has no verified `address`; resolve or explicitly report the blocker instead of silently emitting an incomplete conference entry.
The converter must also stop when venue-name verification is unresolved, a `Venue ID` is missing, or a `Venue ID` maps to inconsistent journal or conference names.

### Default artifacts

Return all of the following:

1. verified UTF-8 BOM CSV;
2. corrected BibTeX file;
3. audit report when unresolved or corrected records exist.


## Uncertain-reference marking

CSV files cannot store cell background colors. Therefore, use a dual representation:

1. The verified CSV must always include:
   - `Needs review`: `YES` or `NO`;
   - `Review reason`: concise reason for manual review.
2. Generate an XLSX counterpart with the same rows and columns.
3. In the XLSX file, fill the entire row light yellow when `Needs review = YES`.
4. Use yellow fill `#FFF2CC`.
5. Preserve the CSV and BibTeX as the canonical machine-readable outputs.

Mark `Needs review = YES` when one or more of the following apply:

- `Verification status` is `partially verified` or contains `unresolved`;
- a DOI candidate is not confirmed or its registered title does not match;
- final pagination, article number, volume, issue, or publication metadata remains unconfirmed;
- a conference address remains unconfirmed;
- a venue identity or canonical venue name remains unresolved;
- publication status is only claimed rather than established by an official record.

Do not mark a reference uncertain merely because it legitimately has no DOI or no continuous pages. A verified arXiv-only paper, TMLR article, workshop paper, policy document, software guide, or non-paginated publication may still be fully verified.

## Default output artifacts

Return:

1. verified UTF-8 BOM CSV with review-marker columns;
2. corrected BibTeX file;
3. formatted XLSX with uncertain rows highlighted yellow;
4. audit report when corrections or unresolved records exist.


## Formal-venue claim continuation rule

Do not stop verification at an arXiv, OpenReview, project-page, or other
preprint record when the input entry already claims a formal journal or
conference venue.

When the input contains a non-preprint `journal` or `booktitle`, but the first
exact-title result is only a preprint:

1. Continue searching the exact title together with:
   - the claimed venue;
   - first author;
   - publication year;
   - `DOI`;
   - publisher domain.
2. Check the publisher, DOI registry metadata, author ORCID, and official
   proceedings before declaring the formal version unconfirmed.
3. Search common capitalization variants, but do not alter the stored title.
4. Treat differences caused only by capitalization, BibTeX braces, Unicode
   punctuation, or LaTeX formatting as non-semantic title matches.
5. A preprint may be retained as the final source only after the claimed formal
   venue has been explicitly checked and no matching formal record is found.
6. Record the formal-search sources checked in `Changes / notes` when the
   result remains unresolved.

This rule prevents a verified journal article from being incorrectly downgraded
to an arXiv-only record merely because the preprint ranks first in search.


## Review-highlighting precision rule

Yellow highlighting means genuine unresolved bibliographic identity or final
publisher metadata—not merely the absence of a DOI or continuous pages.

Do **not** mark a row for review when:

- an official ICLR, NeurIPS, RSS, TMLR, UAI, arXiv-only, policy, software, or
  workshop record is fully verified but legitimately has no DOI;
- an official venue record is verified but the venue does not expose
  continuous pagination;
- an exact-title early-access journal DOI is verified but final volume, issue,
  or pages have not yet been assigned.

Mark a row for review only when:

- final publisher identity remains unresolved;
- a claimed formal venue cannot be confirmed;
- a conference location cannot be confirmed from an official or primary source;
- a journal or conference identity cannot be mapped confidently to one canonical official name;
- final DOI or pages are expected but not yet available and the record is still
  provisional;
- a related formal version has a substantively different title or author list,
  so adopting it would violate title preservation.

## Second-pass source expansion

Before concluding that a DOI is unavailable:

1. For NeurIPS papers, check both the official NeurIPS paper page and the
   proceedings DOI record.
2. For ECCV papers, check the Springer chapter page for DOI, LNCS volume, and
   pages.
3. For IEEE/CVF papers, check CVF Open Access and IEEE/DBLP pagination; retain
   both official page systems when they differ.
4. For RSS papers, check the official roboticsproceedings.org paper page.
5. For a claimed formal journal record, check the publisher, DOI registry, and
   author ORCID before falling back to arXiv.
6. For a formal version with a substantively changed title, do not create a
   hybrid citation. Retain the exact-title preprint and report the related
   formal version separately.
