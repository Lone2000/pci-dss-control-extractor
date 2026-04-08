"""
NIS2 Control Extractor
======================
Extracts NIS2 controls from the ENISA Technical Implementation Guidance PDF.
Uses PyMuPDF for text extraction (free) and Claude Sonnet for condensing long texts.
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
PDF_PATH = os.path.join(BASE_DIR, "src", "[FID_45] ENISA_Technical_implementation_guidance_on_cybersecurity_risk_management_measures_version_1.0.pdf")
OUTPUT_CSV = os.path.join(BASE_DIR, "output", "NIS_Controls.csv")
PROGRESS = os.path.join(BASE_DIR, "temp", "progress_nis.json")

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
SONNET_MODEL = "claude-sonnet-4-6"
HAIKU_MODEL = "claude-haiku-4-5-20251001"
CONDENSE_THRESHOLD = 800       # Only condense texts longer than this
SONNET_THRESHOLD = 1500        # Use Sonnet for very long texts, Haiku for moderately long
MAX_RETRIES = 5
PREVIEW_ONLY = "--preview" in sys.argv

# Chapter number -> Domain name mapping
CHAPTER_DOMAINS = {
    "1": "POLICY ON THE SECURITY OF NETWORK AND INFORMATION SYSTEMS",
    "2": "RISK MANAGEMENT POLICY",
    "3": "INCIDENT HANDLING",
    "4": "BUSINESS CONTINUITY AND CRISIS MANAGEMENT",
    "5": "SUPPLY CHAIN SECURITY",
    "6": "SECURITY IN NETWORK AND INFORMATION SYSTEMS ACQUISITION, DEVELOPMENT AND MAINTENANCE",
    "7": "CYBERSECURITY RISK MANAGEMENT MEASURES EFFECTIVENESS ASSESSMENT",
    "8": "BASIC CYBER HYGIENE PRACTICES AND SECURITY TRAINING",
    "9": "CRYPTOGRAPHY",
    "10": "HUMAN RESOURCES SECURITY",
    "11": "ACCESS CONTROL",
    "12": "ASSET MANAGEMENT",
    "13": "ENVIRONMENTAL AND PHYSICAL SECURITY",
}

# Section number -> Control (section heading) mapping
# Will be built dynamically from PDF text


def extract_controls_from_pdf():
    """Parse the PDF and extract all controls with their text."""
    doc = fitz.open(PDF_PATH)
    full_text = ""
    for page in doc:
        full_text += page.get_text() + "\n"
    doc.close()

    # Build section heading map: X.Y -> heading name
    section_headings = {}
    for m in re.finditer(r'\n(\d+\.\d+)\s+([A-Z][A-Z\s,\-\/\(\)]+)\n', full_text):
        key = m.group(1)
        val = m.group(2).strip()
        if key not in section_headings and len(val) > 5 and "TECHNICAL" not in val:
            section_headings[key] = val

    # Find all controls: X.Y.Z. followed by text
    controls = []
    # Pattern: "X.Y.Z." at start of line or after newline, followed by text
    control_pattern = re.compile(
        r'(\d+\.\d+\.\d+)\.\s+(.*?)(?=\d+\.\d+\.\d+\.\s|\Z)',
        re.DOTALL
    )

    for m in control_pattern.finditer(full_text):
        identifier = m.group(1)
        body = m.group(2).strip()

        # Skip if this is a cross-reference or very short
        if len(body) < 50:
            continue

        # Split body into Description (before GUIDANCE) and Guidance (after GUIDANCE)
        guidance_split = re.split(r'\nGUIDANCE\s*\n', body, maxsplit=1)

        description = guidance_split[0].strip()
        guidance = ""

        if len(guidance_split) > 1:
            guidance_text = guidance_split[1]
            # Cut guidance at "EXAMPLES OF EVIDENCE" or next chapter marker
            evidence_split = re.split(r'\nEXAMPLES OF EVIDENCE\s*\n', guidance_text, maxsplit=1)
            guidance = evidence_split[0].strip()

        # Clean up: remove page headers/footers
        description = re.sub(r'TECHNICAL IMPLEMENTATION GUIDANCE\s*\n\s*June 2025, version 1\.0\s*\n\s*\d+\s*\n', ' ', description)
        guidance = re.sub(r'TECHNICAL IMPLEMENTATION GUIDANCE\s*\n\s*June 2025, version 1\.0\s*\n\s*\d+\s*\n', ' ', guidance)

        # Remove bullet markers and convert to flowing text
        for text_ref in ['description', 'guidance']:
            val = description if text_ref == 'description' else guidance
            # Replace bullet markers with sentence separators
            val = re.sub(r'\s*[•�]\s*', '. ', val)
            val = re.sub(r'\s*o\s{2,}', '. ', val)  # sub-bullets "o  text"
            val = re.sub(r'\s*[–—-]\s{2,}', '. ', val)  # dash bullets
            # Clean up double periods and leading periods
            val = re.sub(r'\.\.+', '.', val)
            val = re.sub(r'^\.\s*', '', val)
            if text_ref == 'description':
                description = val
            else:
                guidance = val

        # Collapse whitespace to single line
        description = " ".join(description.split())
        guidance = " ".join(guidance.split())

        # Determine chapter and section
        parts = identifier.split(".")
        chapter_num = parts[0]
        section_num = f"{parts[0]}.{parts[1]}"

        domain = CHAPTER_DOMAINS.get(chapter_num, "")
        control_name = section_headings.get(section_num, domain)

        controls.append({
            "identifier": identifier,
            "control": control_name,
            "description": description,
            "domain": domain,
            "guidance": guidance,
            "framework_fk": 45,
        })

    return controls


def call_api(client, prompt, model=SONNET_MODEL):
    """Call API with retries."""
    wait = 5
    for attempt in range(MAX_RETRIES):
        try:
            resp = client.messages.create(
                model=model,
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}],
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


def condense_texts(client, controls):
    """Use Sonnet to condense long Control Descriptions and Implementation Guidance."""
    to_condense = []
    for i, c in enumerate(controls):
        needs_desc = len(c["description"]) > CONDENSE_THRESHOLD
        needs_guide = len(c["guidance"]) > CONDENSE_THRESHOLD
        if needs_desc or needs_guide:
            # Determine max text length to pick model
            max_len = max(
                len(c["description"]) if needs_desc else 0,
                len(c["guidance"]) if needs_guide else 0
            )
            # Use Haiku for all — Sonnet has server issues currently
            use_sonnet = False  # max_len > SONNET_THRESHOLD
            to_condense.append((i, needs_desc, needs_guide, use_sonnet))

    if not to_condense:
        print("  No texts exceed threshold — skipping condensation")
        return controls

    haiku_count = sum(1 for _, _, _, s in to_condense if not s)
    sonnet_count = sum(1 for _, _, _, s in to_condense if s)
    print(f"  {len(to_condense)} controls need condensation: {haiku_count} via Haiku, {sonnet_count} via Sonnet")

    # Group by model, then process in batches of 5
    for use_sonnet in [False, True]:
        group = [(i, nd, ng, s) for i, nd, ng, s in to_condense if s == use_sonnet]
        if not group:
            continue
        model = SONNET_MODEL if use_sonnet else HAIKU_MODEL
        model_name = "Sonnet" if use_sonnet else "Haiku"

        batch_size = 5
        for batch_start in range(0, len(group), batch_size):
            batch = group[batch_start:batch_start + batch_size]
            print(f"  [{model_name}] Batch {batch_start//batch_size + 1}/{(len(group)-1)//batch_size + 1} ({len(batch)} controls)... ", end="", flush=True)

            # Build prompt with all texts in batch
            items = []
            for idx, needs_desc, needs_guide, _ in batch:
                c = controls[idx]
                item_parts = [f"CONTROL {c['identifier']}:"]
                if needs_desc:
                    item_parts.append(f"DESCRIPTION: {c['description']}")
                if needs_guide:
                    item_parts.append(f"GUIDANCE: {c['guidance']}")
                items.append("\n".join(item_parts))

            texts_block = "\n\n---\n\n".join(items)

            prompt = f"""You are condensing regulatory and guidance text for a compliance control library.

For each control below, condense the DESCRIPTION and/or GUIDANCE to roughly half their length.

Rules:
- Preserve ALL key requirements, obligations, and actionable items
- Do NOT lose any specific action, condition, or compliance obligation
- Remove only verbose preamble, redundant cross-references, repeated phrases, and filler
- Convert any bullet points into flowing sentences — NO bullet markers in output
- Keep the text as a single paragraph on one line — no linebreaks
- Retain at least 80% of the original meaning and specificity
- Do NOT add interpretation — only condense what is there

Output format — one section per control:
CONDENSED|<identifier>|DESCRIPTION|<condensed description text>
CONDENSED|<identifier>|GUIDANCE|<condensed guidance text>

Only output lines for the fields that need condensing. If only DESCRIPTION was provided, only output the DESCRIPTION line.

{texts_block}"""

            try:
                response = call_api(client, prompt, model=model)
            except RuntimeError:
                print(f"FAILED — keeping original text")
                continue

            # Parse response
            count = 0
            for line in response.splitlines():
                line = line.strip()
                if line.startswith("CONDENSED|"):
                    parts = line.split("|", 3)
                    if len(parts) == 4:
                        ident = parts[1].strip()
                        field = parts[2].strip()
                        text = " ".join(parts[3].split())

                        # Find the control and update
                        for idx, needs_desc, needs_guide, _ in batch:
                            if controls[idx]["identifier"] == ident:
                                if field == "DESCRIPTION":
                                    controls[idx]["description"] = text
                                elif field == "GUIDANCE":
                                    controls[idx]["guidance"] = text
                                count += 1
                                break

            print(f"{count} condensed")
            time.sleep(1.5 if use_sonnet else 0.8)

    return controls


def main():
    api_key = API_KEY
    if not api_key:
        api_key = input("Enter your Anthropic API key: ").strip()
    if not api_key:
        sys.exit("ERROR: No API key provided.")

    client = anthropic.Anthropic(api_key=api_key)

    # Step 1: Extract controls from PDF
    print("Extracting controls from PDF...")
    controls = extract_controls_from_pdf()
    print(f"Found {len(controls)} controls")

    if PREVIEW_ONLY:
        controls = controls[:8]
        print(f"Preview mode: first {len(controls)} only\n")

    # Show first few
    for c in controls[:3]:
        print(f"  {c['identifier']} | {c['control'][:40]} | desc={len(c['description'])}ch | guide={len(c['guidance'])}ch")
    print()

    # Step 2: Condense long texts with Sonnet
    print("Condensing long texts with Sonnet...")
    controls = condense_texts(client, controls)

    # Step 3: Write CSV
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
            writer.writerow([
                i, c["control"], c["description"], "",
                c["domain"], c["framework_fk"], c["identifier"],
                c["guidance"], "Yes", "", "", "",
            ])

    print(f"Done! {len(controls)} controls written to {OUTPUT_CSV}")

    # Save progress
    os.makedirs(os.path.join(BASE_DIR, "temp"), exist_ok=True)
    with open(PROGRESS, "w", encoding="utf-8") as f:
        json.dump({"controls": len(controls), "preview": PREVIEW_ONLY}, f, indent=2)


if __name__ == "__main__":
    main()
