"""
HIPAA Control Extractor
=======================
Extracts HIPAA Security Rule and Privacy Rule controls into CSV.
Uses Claude Haiku to extract verbatim regulatory text from the CFR.
"""

import anthropic
import csv
import json
import os
import re
import sys
import time
import fitz

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STRUCTURE_PDF = os.path.join(BASE_DIR, "src", "HIPAA_Vectra_View_Framework_Structure.pdf")
REGULATION_PDF = os.path.join(BASE_DIR, "src", "hipaa-simplification-201303.pdf")
OUTPUT_CSV = os.path.join(BASE_DIR, "output", "HIPAA_Controls.csv")
PROGRESS = os.path.join(BASE_DIR, "temp", "progress_hipaa.json")

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
MODEL = "claude-haiku-4-5-20251001"
MAX_RETRIES = 5
PREVIEW_ONLY = "--preview" in sys.argv

# Section-to-page mapping in regulation PDF (approximate)
SECTION_PAGES = {
    "164.308": (63, 65),   # Administrative Safeguards
    "164.310": (65, 66),   # Physical Safeguards
    "164.312": (66, 67),   # Technical Safeguards
    "164.314": (67, 68),   # Organizational Requirements (Security)
    "164.316": (68, 69),   # Policies and Procedures
    "164.502": (77, 82),   # Uses and Disclosures General
    "164.504": (82, 86),   # Organizational Requirements (Privacy)
    "164.506": (86, 88),   # TPO
    "164.508": (88, 91),   # Authorizations
    "164.510": (91, 93),   # Facility Directories, Notification
    "164.512": (93, 101),  # Permitted Disclosures
    "164.514": (101, 106), # De-identification
    "164.520": (106, 109), # Notice
    "164.522": (109, 111), # Right to Restrict
    "164.524": (111, 114), # Right of Access
    "164.526": (114, 116), # Right to Amend
    "164.528": (116, 118), # Accounting of Disclosures
    "164.530": (118, 124), # Administrative Requirements
}


def parse_structure_pdf():
    """Parse the structure PDF to get all controls."""
    doc = fitz.open(STRUCTURE_PDF)
    controls = []
    current_domain = ""
    current_rule = ""

    for page_num in range(1, doc.page_count):  # Skip page 0
        text = doc[page_num].get_text()
        lines = [l.strip() for l in text.splitlines() if l.strip()]

        for line in lines:
            if "Part 1: Security Rule" in line:
                current_rule = "security"
            elif "Part 2: Privacy Rule" in line:
                current_rule = "privacy"

        # Track domain changes inline — assign domain to controls that follow
        # Build a list of (line_index, domain_name) for domain headers on this page
        domain_at_line = {}
        for li, line in enumerate(lines):
            dm = re.match(r"Domain \d+\s*[\u2013\u2014–—-]\s*(.+?)(?:\s*[|\u00a7]|\s*$)", line)
            if dm:
                domain_at_line[li] = dm.group(1).strip()

        i = 0
        while i < len(lines):
            line = lines[i]

            # Update domain if we pass a domain header
            if i in domain_at_line:
                current_domain = domain_at_line[i]
                i += 1
                continue

            if line in ("Identifier", "Standard", "Control", "R/A", "Summary") or \
               line.startswith("Domain") or line.startswith("Part") or \
               line.startswith("Note") or line.startswith("High-priority") or \
               ("controls" in line and ("Required" in line or "Addressable" in line or "|" in line)) or \
               line.startswith("Security Rule") or line.startswith("Privacy Rule") or \
               line.startswith("TOTAL") or line.startswith("HIPAA") or \
               line.startswith("The Privacy") or line.startswith("Source:"):
                i += 1
                continue

            if re.match(r"^164\.\d+", line):
                identifier = line
                j = i + 1
                collected = []
                while j < len(lines) and len(collected) < 3:
                    nl = lines[j]
                    if re.match(r"^164\.\d+", nl) or nl.startswith("Domain") or \
                       ("controls" in nl and ("Required" in nl or "Addressable" in nl)):
                        break
                    if nl not in ("Identifier", "Standard", "Control", "R/A"):
                        collected.append(nl)
                    j += 1

                data = [c for c in collected if c not in ("R", "A")]
                standard = data[0] if len(data) >= 1 else ""
                control_name = data[1] if len(data) >= 2 else standard
                fk = 9 if current_rule == "security" else 47

                controls.append({
                    "identifier": identifier,
                    "standard": standard,
                    "control_name": control_name,
                    "domain": current_domain,
                    "framework_fk": fk,
                    "rule": current_rule,
                })
            i += 1

    doc.close()
    return controls


def extract_section_text(section_num):
    """Extract text for a given section from the regulation PDF."""
    doc = fitz.open(REGULATION_PDF)

    # Strategy: find the page where "§ {section_num}" body text starts,
    # then grab that page + next few pages until we hit the next section
    full_text = ""
    for page in doc:
        full_text += page.get_text() + "\n"
    doc.close()

    # Find the section body text (not TOC or subpart header references)
    marker = f"\u00a7 {section_num}"

    # Find ALL occurrences
    positions = []
    start = 0
    while True:
        idx = full_text.find(marker, start)
        if idx < 0:
            break
        positions.append(idx)
        start = idx + 10

    # Score each occurrence to find the body text (not TOC or cross-references)
    best_idx = -1
    best_score = -999
    for pos in positions:
        chunk = full_text[pos:pos + 1000]
        before = full_text[max(0, pos - 30):pos]
        score = 0

        # Positive: regulatory body indicators
        if "Standard:" in chunk: score += 5
        if "Implementation" in chunk: score += 3
        if "Implement " in chunk: score += 3
        if "covered entity" in chunk: score += 2
        if "(a)(1)" in chunk: score += 2
        if "(ii)" in chunk: score += 2
        if "must" in chunk.lower(): score += 1
        if "shall" in chunk.lower(): score += 1

        # Positive: section definition pattern (§ 164.xxx   Title.\n)
        after_marker = full_text[pos + len(marker):pos + len(marker) + 60]
        if re.match(r"\s{2,}[A-Z]", after_marker): score += 4

        # Negative: TOC
        if "....." in chunk: score -= 10
        # Negative: cross-reference (preceded by "under", "in", comma, "or")
        before_stripped = before.strip()
        if before_stripped.endswith((",", "under", "in", "or", "and", "of")): score -= 5
        # Negative: multiple section refs nearby (subpart header listing)
        if chunk.count("\u00a7 164.") > 4: score -= 4

        if score > best_score:
            best_score = score
            best_idx = pos

    if best_idx >= 0:
        return full_text[best_idx:best_idx + 15000]

    return ""


def call_api(client, prompt_text):
    wait = 5
    for attempt in range(MAX_RETRIES):
        try:
            resp = client.messages.create(
                model=MODEL,
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt_text}],
            )
            return resp.content[0].text.strip()
        except anthropic.RateLimitError:
            print(f"    [rate limit] waiting {wait}s...")
            time.sleep(wait)
            wait = min(wait * 2, 120)
        except anthropic.APIStatusError as e:
            if e.status_code >= 500:
                print(f"    [server error] waiting {wait}s...")
                time.sleep(wait)
                wait = min(wait * 2, 120)
            else:
                raise
    raise RuntimeError(f"Failed after {MAX_RETRIES} retries")


def extract_reg_text_for_batch(client, controls_batch, section_text):
    """Send a batch of controls + their section text to Haiku."""
    identifiers_list = "\n".join(
        f"- {c['identifier']} — {c['control_name']}"
        for c in controls_batch
    )

    prompt = f"""You are a regulatory text extraction tool. You MUST output ONLY pipe-delimited RESULT lines — no explanations, no commentary, no markdown, no apologies, no extra text. If you cannot find exact text for a control, use the closest matching text from the provided regulation.

For each control below, find and copy the EXACT verbatim text from the regulation.

DESCRIPTION = the implementation specification or standard text (what must be done).
GUIDANCE = the parent standard text or surrounding regulatory context.

Rules:
- One line per control, no exceptions
- Format: RESULT|<identifier>|<description>|<guidance>
- All text on a single line — no linebreaks within fields
- Copy exact wording from the regulation — do not paraphrase
- You MUST output one RESULT line for EVERY control listed below

Controls:
{identifiers_list}

Regulation text:
{section_text[:12000]}"""

    response = call_api(client, prompt)
    results = {}
    for line in response.splitlines():
        line = line.strip()
        if line.startswith("RESULT|"):
            parts = line.split("|", 3)
            if len(parts) == 4:
                ident = parts[1].strip()
                desc = " ".join(parts[2].split())
                guidance = " ".join(parts[3].split())
                results[ident] = {"description": desc, "guidance": guidance}
    return results


def main():
    api_key = API_KEY
    if not api_key:
        api_key = input("Enter your Anthropic API key: ").strip()
    if not api_key:
        sys.exit("ERROR: No API key provided.")

    client = anthropic.Anthropic(api_key=api_key)

    # Step 1: Parse structure
    print("Parsing structure PDF...")
    controls = parse_structure_pdf()
    print(f"Found {len(controls)} controls")

    if PREVIEW_ONLY:
        controls = controls[:5]
        print(f"Preview mode: first {len(controls)} only\n")

    # Step 2: Group controls by base section for efficient API calls
    section_groups = {}
    for c in controls:
        base = re.match(r"(164\.\d+)", c["identifier"])
        if base:
            section = base.group(1)
            section_groups.setdefault(section, []).append(c)

    # Step 3: Extract regulation text per section and call Haiku
    print("Extracting regulatory text via Haiku API...")
    all_results = {}

    for section, group in section_groups.items():
        section_text = extract_section_text(section)
        if not section_text:
            print(f"  § {section}: no regulation text found, skipping {len(group)} controls")
            continue

        # Process in batches of 15 within each section
        for batch_start in range(0, len(group), 15):
            batch = group[batch_start:batch_start + 15]
            print(f"  § {section} batch {batch_start//15 + 1} ({len(batch)} controls)... ", end="", flush=True)
            results = extract_reg_text_for_batch(client, batch, section_text)
            all_results.update(results)
            print(f"{len(results)} results")
            time.sleep(0.6)

    # Step 4: Write CSV
    print(f"\nWriting CSV to {OUTPUT_CSV}...")
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Control ID", "Control", "Control Description", "Criticality",
            "Domain", "Framework (FK)", "Identifier", "Implementation Guidance",
            "Is Active", "Mapped Controls", "Type", "Weight",
        ])
        for i, c in enumerate(controls, start=1):
            if c["standard"] != c["control_name"]:
                control_label = f"{c['standard']} - {c['control_name']}"
            else:
                control_label = c["control_name"]

            reg = all_results.get(c["identifier"], {})
            desc = reg.get("description", "")
            guidance = reg.get("guidance", "")

            writer.writerow([
                i, control_label, desc, "",
                c["domain"], c["framework_fk"], c["identifier"],
                guidance, "Yes", "", "", "",
            ])

    print(f"Done! {len(controls)} controls written to {OUTPUT_CSV}")

    # Save progress
    os.makedirs(os.path.join(BASE_DIR, "temp"), exist_ok=True)
    with open(PROGRESS, "w", encoding="utf-8") as f:
        json.dump({"controls": len(controls), "results": len(all_results), "preview": PREVIEW_ONLY}, f, indent=2)


if __name__ == "__main__":
    main()
