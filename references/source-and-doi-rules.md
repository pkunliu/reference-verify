# Source and DOI rules

## Preferred official sources

- CVPR / ICCV / WACV: CVF Open Access and IEEE Xplore.
- NeurIPS: NeurIPS Proceedings.
- ICLR: ICLR Proceedings and OpenReview.
- ICML / CoRL: PMLR.
- ECCV and Springer conference chapters: SpringerLink.
- IEEE journals / ICRA / IROS / ICASSP / 3DV: IEEE Xplore.
- ACM journals / SIGGRAPH: ACM Digital Library.
- Elsevier journals: ScienceDirect.
- Wiley journals: Wiley Online Library.
- AAAI: AAAI Proceedings.
- TMLR: OpenReview/TMLR.
- RSS: official Robotics: Science and Systems proceedings.
- arXiv: only for the preprint record or when no formal publication exists.

## DOI rejection conditions

Reject a DOI when:

- the publisher title contains substantive words not present in the supplied title;
- the DOI is for a survey, supplement, dataset, erratum, or related work rather than the supplied paper;
- the DOI resolves to a different publication without evidence that it is the same version;
- the DOI was inferred from page numbers or neighboring records;
- the DOI appears only in an unverified secondary database and not in an official record.

## Page rules

- A one-number field may be an article number, eLocator, or page.
- Confirm its semantics from the official publisher.
- Do not convert article number `111447` into a page range.
- For ACM article-style pagination, retain the article number separately.
- For records with no formal pagination, leave `pages` blank.

## Conference address rules

- Verify the event location from the official conference site, official proceedings front matter, publisher record, or official program.
- Write physical locations as `City, Country` when the official source supports that form.
- Use `Online` only for an officially fully online event.
- Preserve official wording for hybrid or multi-site events and explain it in the audit notes.
- Do not use publisher addresses, organizer headquarters, author affiliations, or another edition's location.
- If no official or primary source confirms the location, leave `address` blank and require manual review.

## Canonical venue-name rules

- Assign one stable lowercase `Venue ID` to each verified journal or conference identity.
- Use one official unabbreviated `journal` or `booktitle` string for every row sharing that `Venue ID`.
- Do not mix abbreviations, acronyms, parenthetical aliases, capitalization variants, or optional `Proceedings of` forms.
- Keep year, edition, address, volume, and publisher series in their dedicated fields when possible.
- Keep workshops, main conferences, journals, and materially renamed venue eras as distinct identities.
- Mark ambiguous venue identity for review instead of forcing a merge.
