#!/usr/bin/env python3
"""Convert a Strict Reference Verifier CSV into corrected BibTeX.

The converter preserves row order, BibTeX keys, author strings, and titles.
It uses only verified metadata columns and never invents a DOI.
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


def clean(value: str | None) -> str:
    return (value or "").strip()


def normalize_pages(value: str) -> str:
    value = clean(value).replace("–", "--").replace("—", "--")
    value = re.sub(r"(?<=\d)-(?=\d)", "--", value)
    return re.sub(r"-{3,}", "--", value)


def normalize_arxiv_id(value: str | None) -> str:
    value = clean(value)
    value = re.sub(r"^https?://arxiv\.org/(?:abs|pdf)/", "", value, flags=re.I)
    value = re.sub(r"\.pdf$", "", value, flags=re.I)
    return re.sub(r"^arXiv\s*:\s*", "", value, flags=re.I)


def is_arxiv_journal(value: str) -> bool:
    normalized = value.replace(r"ar\relax Xiv", "arXiv")
    return bool(re.match(r"^arXiv(?:\s+preprint)?(?:\s+arXiv\s*:.*)?$", normalized, re.I))


def effective_arxiv_id(row: dict[str, str]) -> str:
    arxiv_id = normalize_arxiv_id(row.get("arXiv ID"))
    if arxiv_id:
        return arxiv_id
    journal = clean(row.get("journal")).replace(r"ar\relax Xiv", "arXiv")
    match = re.match(r"^arXiv(?:\s+preprint)?\s+arXiv\s*:\s*(\S+)\s*$", journal, re.I)
    return normalize_arxiv_id(match.group(1)) if match else ""


def effective_journal(row: dict[str, str]) -> str:
    journal = clean(row.get("journal"))
    booktitle = clean(row.get("booktitle"))
    arxiv_id = effective_arxiv_id(row)

    if arxiv_id and not booktitle and (not journal or is_arxiv_journal(journal)):
        return f"arXiv preprint arXiv:{arxiv_id}"
    return journal


def choose_entry_type(row: dict[str, str]) -> str:
    if effective_journal(row):
        return "article"
    if clean(row.get("booktitle")):
        return "inproceedings"
    original = clean(row.get("Entry type")).lower()
    return original if original in {
        "article", "inproceedings", "misc", "techreport", "book", "incollection"
    } else "misc"


def add_field(lines: list[str], name: str, value: str) -> None:
    if value:
        lines.append(f"  {name:<13} = {{{value}}},")


def validate_venue_consistency(rows: list[dict[str, str]]) -> None:
    venues: dict[str, tuple[str, str]] = {}

    for row in rows:
        key = clean(row.get("Key"))
        journal = effective_journal(row)
        booktitle = clean(row.get("booktitle"))

        if journal and booktitle:
            raise SystemExit(
                f"Entry {key!r} has both journal and booktitle; venue kind is ambiguous."
            )
        if not journal and not booktitle:
            continue

        venue_id = clean(row.get("Venue ID"))
        if not venue_id:
            raise SystemExit(f"Entry {key!r} has no Venue ID.")
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", venue_id):
            raise SystemExit(
                f"Entry {key!r} has invalid Venue ID {venue_id!r}; "
                "use lowercase letters, digits, and hyphens."
            )

        verification = clean(row.get("Venue name verification")).lower()
        if verification not in {"verified", "corrected"}:
            raise SystemExit(
                f"Entry {key!r} has unresolved venue-name verification."
            )

        venue = ("journal", journal) if journal else ("booktitle", booktitle)
        previous = venues.get(venue_id)
        if previous is not None and previous != venue:
            raise SystemExit(
                f"Venue ID {venue_id!r} maps to inconsistent names or kinds: "
                f"{previous!r} versus {venue!r}."
            )
        venues[venue_id] = venue


def convert_row(row: dict[str, str], include_doi_url: bool) -> str:
    entry_type = choose_entry_type(row)
    lines = [f"@{entry_type}{{{clean(row['Key'])},"]

    add_field(lines, "author", clean(row.get("Authors")))
    add_field(lines, "title", clean(row.get("Title")))
    journal = effective_journal(row)
    booktitle = clean(row.get("booktitle"))
    add_field(lines, "journal", journal)
    add_field(lines, "booktitle", booktitle)
    address = clean(row.get("address"))
    if entry_type == "inproceedings" and not address:
        raise SystemExit(
            f"Conference entry {clean(row.get('Key'))!r} has no verified address."
        )
    if entry_type == "inproceedings":
        add_field(lines, "address", address)
    add_field(lines, "volume", clean(row.get("volume")))
    add_field(lines, "number", clean(row.get("number")))
    add_field(lines, "pages", normalize_pages(row.get("pages", "")))
    add_field(lines, "year", clean(row.get("year")) or clean(row.get("Original year")))

    arxiv_id = effective_arxiv_id(row)
    if arxiv_id and not booktitle and is_arxiv_journal(journal):
        add_field(lines, "eprint", arxiv_id)
        add_field(lines, "archivePrefix", "arXiv")

    if include_doi_url:
        # The verifier only populates this field after DOI-title matching.
        add_field(lines, "doi", clean(row.get("DOI")))
        add_field(
            lines,
            "url",
            clean(row.get("Official URL")) or clean(row.get("DOI URL")),
        )

    if entry_type in {"misc", "techreport"}:
        add_field(lines, "note", clean(row.get("Formal publication status")))

    lines.append("}")
    return "\n".join(lines)


def validate_output(
    output: str,
    entries: list[str],
    rows: list[dict[str, str]],
    keys: list[str],
    include_doi_url: bool,
) -> None:
    if not include_doi_url and re.search(
        r"^\s*(?:doi|url)\s*=", output, flags=re.I | re.M
    ):
        raise SystemExit("DOI/URL-free BibTeX contains a doi or url field.")

    generated_keys = re.findall(r"^@\w+\{([^,]+),", output, flags=re.M)
    if generated_keys != keys:
        raise SystemExit("Generated BibTeX order does not match CSV order.")

    for row, entry in zip(rows, entries):
        exact_title = f"title         = {{{row['Title']}}},"
        if exact_title not in entry:
            raise SystemExit(f"Title preservation failed for {row['Key']}.")
        journal = effective_journal(row)
        booktitle = clean(row.get("booktitle"))
        arxiv_id = effective_arxiv_id(row)
        is_pure_arxiv = bool(
            arxiv_id and not booktitle and is_arxiv_journal(journal)
        )
        if is_pure_arxiv:
            if f"eprint        = {{{arxiv_id}}}," not in entry:
                raise SystemExit(f"Missing or mismatched eprint for {row['Key']}.")
            if "archivePrefix = {arXiv}," not in entry:
                raise SystemExit(f"Missing archivePrefix for {row['Key']}.")
        elif re.search(r"^\s*(?:eprint|archiveprefix)\s*=", entry, flags=re.I | re.M):
            raise SystemExit(
                f"Formally published entry {row['Key']} contains arXiv export fields."
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("bib_with_doi_url", type=Path)
    parser.add_argument("bib_without_doi_url", type=Path)
    args = parser.parse_args()

    with args.csv_file.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    if not rows:
        raise SystemExit("CSV contains no reference rows.")

    keys = [clean(row.get("Key")) for row in rows]
    if len(keys) != len(set(keys)):
        raise SystemExit("Duplicate BibTeX keys detected.")

    validate_venue_consistency(rows)

    entries_with = [convert_row(row, include_doi_url=True) for row in rows]
    entries_without = [convert_row(row, include_doi_url=False) for row in rows]
    output_with = "\n\n".join(entries_with) + "\n"
    output_without = "\n\n".join(entries_without) + "\n"

    validate_output(output_with, entries_with, rows, keys, include_doi_url=True)
    validate_output(
        output_without, entries_without, rows, keys, include_doi_url=False
    )

    expected_without = re.sub(
        r"^[ \t]*(?:doi|url)[ \t]*=[ \t]*\{.*\},[ \t]*(?:\n|$)",
        "",
        output_with,
        flags=re.I | re.M,
    )
    if expected_without != output_without:
        raise SystemExit("The two BibTeX variants differ beyond doi/url fields.")

    args.bib_with_doi_url.write_text(output_with, encoding="utf-8")
    args.bib_without_doi_url.write_text(output_without, encoding="utf-8")
    print(
        f"Generated {len(rows)} entries in each BibTeX variant: "
        f"{args.bib_with_doi_url} and {args.bib_without_doi_url}"
    )


if __name__ == "__main__":
    main()
