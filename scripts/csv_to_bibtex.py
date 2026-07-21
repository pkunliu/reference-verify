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


def choose_entry_type(row: dict[str, str]) -> str:
    if clean(row.get("journal")):
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
        journal = clean(row.get("journal"))
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


def convert_row(row: dict[str, str]) -> str:
    entry_type = choose_entry_type(row)
    lines = [f"@{entry_type}{{{clean(row['Key'])},"]

    add_field(lines, "author", clean(row.get("Authors")))
    add_field(lines, "title", clean(row.get("Title")))
    add_field(lines, "journal", clean(row.get("journal")))
    add_field(lines, "booktitle", clean(row.get("booktitle")))
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

    # The verifier only populates this field after DOI-title matching.
    add_field(lines, "doi", clean(row.get("DOI")))

    arxiv_id = re.sub(
        r"^arXiv\s*:\s*", "", clean(row.get("arXiv ID")), flags=re.I
    )
    if arxiv_id:
        add_field(lines, "eprint", arxiv_id)
        add_field(lines, "archivePrefix", "arXiv")

    add_field(
        lines,
        "url",
        clean(row.get("Official URL")) or clean(row.get("DOI URL")),
    )

    if entry_type in {"misc", "techreport"}:
        add_field(lines, "note", clean(row.get("Formal publication status")))

    lines.append("}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("bib_file", type=Path)
    args = parser.parse_args()

    with args.csv_file.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    if not rows:
        raise SystemExit("CSV contains no reference rows.")

    keys = [clean(row.get("Key")) for row in rows]
    if len(keys) != len(set(keys)):
        raise SystemExit("Duplicate BibTeX keys detected.")

    validate_venue_consistency(rows)

    entries = [convert_row(row) for row in rows]
    args.bib_file.write_text("\n\n".join(entries) + "\n", encoding="utf-8")

    output = args.bib_file.read_text(encoding="utf-8")
    generated_keys = re.findall(r"^@\w+\{([^,]+),", output, flags=re.M)
    if generated_keys != keys:
        raise SystemExit("Generated BibTeX order does not match CSV order.")

    for row, entry in zip(rows, entries):
        exact_title = f"title         = {{{row['Title']}}},"
        if exact_title not in entry:
            raise SystemExit(f"Title preservation failed for {row['Key']}.")

    print(f"Generated {len(entries)} BibTeX entries: {args.bib_file}")


if __name__ == "__main__":
    main()
