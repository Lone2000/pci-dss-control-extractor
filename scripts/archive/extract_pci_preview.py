import anthropic
import base64
import csv
import os
import re

client = anthropic.Anthropic()

PAGE_DIR = r"c:\Users\PC\Desktop\Control Outputs\pdf_pages"
OUTPUT_CSV = r"c:\Users\PC\Desktop\Control Outputs\PCI_Controls_Preview.csv"

PROMPT = """You are extracting structured data from a PCI DSS v4.0 standard document page image.

This page has a 2-column layout (landscape orientation):
- LEFT column "Requirements and Testing Procedures": control identifier + "Defined Approach Requirements" text + testing procedures
- RIGHT column "Guidance": Purpose, Good Practice, Examples, Definitions

Extract the following. If the page is an intro/overview/section-divider/appendix with no X.Y.Z control, respond with SKIP.

For EACH X.Y.Z control on this page, respond with one line in this exact format:
CONTROL|<identifier>|<domain>|<description>|<guidance>

Rules:
- identifier: the X.Y.Z number (e.g. 1.2.3)
- domain: the Requirement name (e.g. "Requirement 1: Install and Maintain Network Security Controls") — infer from context
- description: ONLY the "Defined Approach Requirements" text (not testing procedures). Join all bullet points into ONE single line, no newlines.
- guidance: ALL text from the right Guidance column (Purpose + Good Practice + Examples + Definitions). Join into ONE single line, no newlines.
- If a control continues from the previous page, still output it as a new CONTROL line with whatever text is visible.
- Do NOT include testing procedures (lines starting with the identifier + a/b/c) in the description.

Output ONLY lines starting with CONTROL| or the word SKIP. Nothing else."""


def encode_image(path):
    with open(path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")


def extract_page(page_num):
    path = os.path.join(PAGE_DIR, f"page_{page_num:04d}.png")
    if not os.path.exists(path):
        return []

    img_data = encode_image(path)
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2000,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": img_data,
                        },
                    },
                    {"type": "text", "text": PROMPT},
                ],
            }
        ],
    )

    text = response.content[0].text.strip()
    controls = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("CONTROL|"):
            parts = line.split("|", 4)
            if len(parts) == 5:
                controls.append(
                    {
                        "identifier": parts[1].strip(),
                        "domain": parts[2].strip(),
                        "description": parts[3].strip(),
                        "guidance": parts[4].strip(),
                    }
                )
    return controls


def main():
    all_controls = []
    seen_identifiers = set()

    for page_num in range(15):  # pages 0-14
        print(f"Processing page {page_num}...")
        controls = extract_page(page_num)
        for c in controls:
            ident = c["identifier"]
            if ident not in seen_identifiers:
                seen_identifiers.add(ident)
                all_controls.append(c)
                print(f"  Found: {ident}")
            else:
                # Merge guidance if it's a continuation
                for existing in all_controls:
                    if existing["identifier"] == ident:
                        existing["guidance"] = (existing["guidance"] + " " + c["guidance"]).strip()
                        existing["description"] = (existing["description"] + " " + c["description"]).strip()
                        print(f"  Merged continuation: {ident}")
                        break

    # Sort by identifier
    def sort_key(c):
        parts = re.split(r"[.\s]", c["identifier"])
        nums = []
        for p in parts:
            try:
                nums.append(int(p))
            except ValueError:
                nums.append(0)
        return nums

    all_controls.sort(key=sort_key)

    # Write CSV
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Control ID", "Control", "Control Description", "Criticality",
            "Domain", "Framework (FK)", "Identifier", "Implementation Guidance",
            "Is Active", "Mapped Controls", "Type", "Weight"
        ])
        for i, c in enumerate(all_controls, start=1):
            writer.writerow([
                i, "", c["description"], "", c["domain"],
                7, c["identifier"], c["guidance"],
                "Yes", "", "", ""
            ])

    print(f"\nDone! {len(all_controls)} controls written to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
