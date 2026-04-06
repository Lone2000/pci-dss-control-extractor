"""
PCI DSS PDF Extractor — Standalone Script
==========================================
Extracts all controls from the PCI DSS v4.0 PDF (pre-rendered as PNG pages)
into a CSV matching the confirmed output format.

Requirements:
  pip install anthropic pymupdf pillow

Usage:
  set ANTHROPIC_API_KEY=sk-ant-...
  python extract_pci_full.py

Or the script will prompt you for the key if not set.

Features:
  - Resumable: saves progress to progress.json after every page
  - Rate limit safe: automatic retry with exponential backoff
  - Tracks Requirement domain across pages
  - Merges multi-page controls (continuations)
  - Sorted final output: 1.1.1 -> 12.x.x
"""

import anthropic
import base64
import csv
import json
import os
import re
import sys
import time

# ─── CONFIG ──────────────────────────────────────────────────────────────────

BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES_DIR   = os.path.join(BASE_DIR, "temp", "pdf_pages")
PROGRESS    = os.path.join(BASE_DIR, "temp", "progress.json")
OUTPUT_CSV  = os.path.join(BASE_DIR, "output", "PCI_DSS_v4_Controls.csv")

MODEL       = "claude-haiku-4-5-20251001"   # cheapest vision model
DELAY_SEC   = 0.6                           # pause between pages (avoid bursting)
MAX_RETRIES = 5                             # retries on rate-limit / server errors

# ─── PROMPT ──────────────────────────────────────────────────────────────────

PROMPT = """You are extracting structured data from a PCI DSS v4.0 standard page image.

Layout: 2-column landscape page.
  LEFT column  "Requirements and Testing Procedures" — contains the control identifier and requirement text.
  RIGHT column "Guidance" — contains Purpose, Good Practice, Examples, Definitions.

TASK: For every X.Y.Z control visible on this page output exactly one line per control:

  CONTROL|<identifier>|<domain>|<description>|<guidance>

Rules:
- identifier : the X.Y.Z number only  (e.g. 1.2.3)
- domain     : the Requirement heading in full  (e.g. "Requirement 1: Install and Maintain Network Security Controls")
               Infer from any section header visible on the page or from context.
- description: ONLY the "Defined Approach Requirements" text.
               Do NOT include testing procedures (lines like "1.2.3.a Examine…").
               Join all bullet points into ONE single line — no newlines.
- guidance   : ALL text from Purpose section + ALL text from Good Practice section, combined.
               Join into ONE single line — no newlines, no section labels.
               Do NOT include Examples, Definitions, Further Information, or Applicability Notes.
- If a control is continued from a previous page, still output a CONTROL line with whatever
  description/guidance text is visible on THIS page (it will be merged automatically).
- If the page is a cover, overview, table of contents, appendix, or contains no X.Y.Z controls:
  output the single word SKIP.

Output ONLY lines starting with "CONTROL|" or the word "SKIP". Nothing else whatsoever."""

# ─── HELPERS ─────────────────────────────────────────────────────────────────

def encode_png(path: str) -> str:
    with open(path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode()


def sort_key(identifier: str):
    """Sort 1.2.3 numerically; A1.2.3 after 12.x.x."""
    parts = re.split(r"[.\s]+", identifier.strip())
    result = []
    for p in parts:
        # leading letter (e.g. A1 -> sort after 12)
        m = re.match(r"([A-Za-z]*)(\d+)", p)
        if m:
            result.append((1 if m.group(1) else 0, int(m.group(2))))
        else:
            result.append((0, 0))
    return result


def call_api(client: anthropic.Anthropic, img_b64: str) -> str:
    """Call the API with retries on rate-limit / server errors."""
    wait = 5
    for attempt in range(MAX_RETRIES):
        try:
            resp = client.messages.create(
                model=MODEL,
                max_tokens=2048,
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": img_b64,
                            },
                        },
                        {"type": "text", "text": PROMPT},
                    ],
                }],
            )
            return resp.content[0].text.strip()
        except anthropic.RateLimitError:
            print(f"    [rate limit] waiting {wait}s …")
            time.sleep(wait)
            wait = min(wait * 2, 120)
        except anthropic.APIStatusError as e:
            if e.status_code >= 500:
                print(f"    [server error {e.status_code}] waiting {wait}s …")
                time.sleep(wait)
                wait = min(wait * 2, 120)
            else:
                raise
    raise RuntimeError(f"Failed after {MAX_RETRIES} retries")


def parse_response(text: str, fallback_domain: str) -> list[dict]:
    """Parse CONTROL| lines from a model response."""
    controls = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("CONTROL|"):
            continue
        parts = line.split("|", 4)
        if len(parts) != 5:
            continue
        _, ident, domain, desc, guidance = parts
        ident    = ident.strip()
        domain   = domain.strip() or fallback_domain
        desc     = " ".join(desc.split())     # collapse whitespace
        guidance = " ".join(guidance.split())
        if ident:
            controls.append({
                "identifier": ident,
                "domain":     domain,
                "description": desc,
                "guidance":   guidance,
            })
    return controls


def load_progress() -> dict:
    if os.path.exists(PROGRESS):
        with open(PROGRESS, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"last_page": -1, "domain": "", "controls": {}}


def save_progress(state: dict):
    with open(PROGRESS, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def write_csv(controls_map: dict):
    """Sort controls and write final CSV."""
    rows = sorted(controls_map.values(), key=lambda c: sort_key(c["identifier"]))
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Control ID", "Control", "Control Description", "Criticality",
            "Domain", "Framework (FK)", "Identifier", "Implementation Guidance",
            "Is Active", "Mapped Controls", "Type", "Weight",
        ])
        for i, c in enumerate(rows, start=1):
            writer.writerow([
                i, "", c["description"], "", c["domain"],
                7, c["identifier"], c["guidance"],
                "Yes", "", "", "",
            ])
    return len(rows)


# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    # API key
    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        api_key = input("Enter your Anthropic API key: ").strip()
    if not api_key:
        sys.exit("ERROR: No API key provided.")

    client = anthropic.Anthropic(api_key=api_key)

    # Collect page files
    pages = sorted(
        f for f in os.listdir(PAGES_DIR) if f.startswith("page_") and f.endswith(".png")
    )
    total = len(pages)
    print(f"Found {total} pages in {PAGES_DIR}")

    # Load prior progress
    state = load_progress()
    last_done = state.get("last_page", -1)
    domain    = state.get("domain", "")
    controls  = state.get("controls", {})   # keyed by identifier

    if last_done >= 0:
        print(f"Resuming from page {last_done + 1} ({len(controls)} controls so far)\n")

    # Process pages
    for idx, fname in enumerate(pages):
        page_num = int(re.search(r"\d+", fname).group())

        if page_num <= last_done:
            continue  # already done

        path = os.path.join(PAGES_DIR, fname)
        print(f"[{page_num:03d}/{total-1}] {fname} … ", end="", flush=True)

        img_b64 = encode_png(path)
        response_text = call_api(client, img_b64)

        if response_text.strip().upper() == "SKIP":
            print("skip")
        else:
            found = parse_response(response_text, domain)
            for c in found:
                ident = c["identifier"]
                # Update domain tracker if model returned one
                if c["domain"]:
                    domain = c["domain"]
                    c["domain"] = domain

                if ident in controls:
                    # Merge continuation: append any new text not already present
                    existing = controls[ident]
                    if c["description"] and c["description"] not in existing["description"]:
                        existing["description"] = (existing["description"] + " " + c["description"]).strip()
                    if c["guidance"] and c["guidance"] not in existing["guidance"]:
                        existing["guidance"] = (existing["guidance"] + " " + c["guidance"]).strip()
                else:
                    controls[ident] = c

            print(f"{len(found)} control(s) → total {len(controls)}")

        # Save checkpoint
        state["last_page"] = page_num
        state["domain"]    = domain
        state["controls"]  = controls
        save_progress(state)

        time.sleep(DELAY_SEC)

    # Write final CSV
    print(f"\nWriting CSV …")
    count = write_csv(controls)
    print(f"Done! {count} controls written to:\n  {OUTPUT_CSV}")
    print(f"\nTo start over: delete progress.json and re-run.")


if __name__ == "__main__":
    main()
