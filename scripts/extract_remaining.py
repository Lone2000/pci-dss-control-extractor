import anthropic
import base64
import csv
import json
import os
import re
import time

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR  = os.path.join(BASE_DIR, "pdf_pages")
PROGRESS   = os.path.join(BASE_DIR, "progress_remaining.json")
OUTPUT_CSV = os.path.join(BASE_DIR, "PCI_Controls_Preview.csv")

API_KEY    = os.environ.get("ANTHROPIC_API_KEY", "")
MODEL      = "claude-haiku-4-5-20251001"
DELAY_SEC  = 0.6
MAX_RETRIES = 5
START_PAGE = 214
END_PAGE   = 295

PROMPT = """You are extracting structured data from a PCI DSS v4.0 standard page image.

Layout: 2-column landscape page.
  LEFT column  "Requirements and Testing Procedures" — contains the control identifier and requirement text.
  RIGHT column "Guidance" — contains Purpose, Good Practice, Examples, Definitions.

TASK: For every X.Y.Z control visible on this page output exactly one line per control:

  CONTROL|<identifier>|<domain>|<description>|<guidance>

Rules:
- identifier : the X.Y.Z number only  (e.g. 10.5.1)
- domain     : the Requirement heading in full  (e.g. "Requirement 10: Log and Monitor All Access to System Components and Cardholder Data")
               Infer from any section header visible on the page or from context.
- description: ONLY the "Defined Approach Requirements" text.
               Do NOT include testing procedures (lines like "10.5.1.a Examine…").
               Join all bullet points into ONE single line — no newlines.
               Transcribe the FULL EXACT text as written — do NOT paraphrase or shorten.
- guidance   : ALL text from Purpose section + ALL text from Good Practice section, combined.
               Join into ONE single line — no newlines, no section labels like "Purpose" or "Good Practice".
               Transcribe the FULL EXACT text as written — do NOT paraphrase, summarize, or shorten.
               Do NOT include Examples, Definitions, Further Information, or Applicability Notes.
- If a control is continued from a previous page, still output a CONTROL line with whatever
  description/guidance text is visible on THIS page (it will be merged automatically).
- If the page is a cover, overview, table of contents, appendix with no X.Y.Z controls,
  or a continuation page with ONLY testing procedures and no new requirement text:
  output the single word SKIP.

Output ONLY lines starting with "CONTROL|" or the word "SKIP". Nothing else whatsoever."""


def encode_png(path):
    with open(path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode()


def call_api(client, img_b64):
    wait = 5
    for attempt in range(MAX_RETRIES):
        try:
            resp = client.messages.create(
                model=MODEL,
                max_tokens=4096,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": img_b64}},
                        {"type": "text", "text": PROMPT},
                    ],
                }],
            )
            return resp.content[0].text.strip()
        except anthropic.RateLimitError:
            print(f"    [rate limit] waiting {wait}s...")
            time.sleep(wait)
            wait = min(wait * 2, 120)
        except anthropic.APIStatusError as e:
            if e.status_code >= 500:
                print(f"    [server error {e.status_code}] waiting {wait}s...")
                time.sleep(wait)
                wait = min(wait * 2, 120)
            else:
                raise
    raise RuntimeError(f"Failed after {MAX_RETRIES} retries")


def parse_response(text, fallback_domain):
    controls = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("CONTROL|"):
            continue
        parts = line.split("|", 4)
        if len(parts) != 5:
            continue
        _, ident, domain, desc, guidance = parts
        ident = ident.strip()
        domain = domain.strip() or fallback_domain
        desc = " ".join(desc.split())
        guidance = " ".join(guidance.split())
        if ident:
            controls.append({"identifier": ident, "domain": domain, "description": desc, "guidance": guidance})
    return controls


def load_progress():
    if os.path.exists(PROGRESS):
        with open(PROGRESS, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"last_page": START_PAGE - 1, "domain": "Requirement 10: Log and Monitor All Access to System Components and Cardholder Data", "controls": {}}


def save_progress(state):
    with open(PROGRESS, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def main():
    client = anthropic.Anthropic(api_key=API_KEY)

    # Count existing rows
    existing_count = 0
    if os.path.exists(OUTPUT_CSV):
        with open(OUTPUT_CSV, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            for row in reader:
                if row and row[0]:
                    existing_count += 1
    print(f"Existing CSV has {existing_count} rows")

    state = load_progress()
    last_done = state["last_page"]
    domain = state["domain"]
    controls = state["controls"]

    if last_done >= START_PAGE:
        print(f"Resuming from page {last_done + 1} ({len(controls)} controls extracted so far)")

    for page_num in range(START_PAGE, END_PAGE + 1):
        if page_num <= last_done:
            continue

        fname = f"page_{page_num:04d}.png"
        path = os.path.join(PAGES_DIR, fname)
        if not os.path.exists(path):
            continue

        print(f"[{page_num:03d}/{END_PAGE}] {fname} ... ", end="", flush=True)

        img_b64 = encode_png(path)
        response_text = call_api(client, img_b64)

        if response_text.strip().upper() == "SKIP":
            print("skip")
        else:
            found = parse_response(response_text, domain)
            for c in found:
                ident = c["identifier"]
                if c["domain"]:
                    domain = c["domain"]
                    c["domain"] = domain
                if ident in controls:
                    existing = controls[ident]
                    if c["description"] and c["description"] not in existing["description"]:
                        existing["description"] = (existing["description"] + " " + c["description"]).strip()
                    if c["guidance"] and c["guidance"] not in existing["guidance"]:
                        existing["guidance"] = (existing["guidance"] + " " + c["guidance"]).strip()
                else:
                    controls[ident] = c
            print(f"{len(found)} control(s) -> total {len(controls)}")

        state["last_page"] = page_num
        state["domain"] = domain
        state["controls"] = controls
        save_progress(state)
        time.sleep(DELAY_SEC)

    # Sort and append to CSV
    def sort_key(identifier):
        parts = re.split(r"[.\s]+", identifier.strip())
        result = []
        for p in parts:
            m = re.match(r"([A-Za-z]*)(\d+)", p)
            if m:
                result.append((1 if m.group(1) else 0, int(m.group(2))))
            else:
                result.append((0, 0))
        return result

    sorted_controls = sorted(controls.values(), key=lambda c: sort_key(c["identifier"]))

    with open(OUTPUT_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for i, c in enumerate(sorted_controls, start=existing_count + 1):
            writer.writerow([
                i, "", c["description"], "", c["domain"],
                7, c["identifier"], c["guidance"],
                "Yes", "", "", "",
            ])

    print(f"\nAppended {len(sorted_controls)} controls (IDs {existing_count+1}-{existing_count+len(sorted_controls)})")
    print(f"Total rows now: {existing_count + len(sorted_controls)}")


if __name__ == "__main__":
    main()
