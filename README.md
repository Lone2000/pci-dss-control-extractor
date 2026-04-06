# PCI DSS v4.0 Control Extractor

Automated extraction of all PCI DSS v4.0.1 security controls from the official PDF standard into a structured CSV format — ready for import into GRC platforms, compliance tools, or security control databases.

## What This Does

Takes the PCI DSS v4.0.1 Requirements and Testing Procedures PDF (image-based/scanned) and extracts every control into a clean CSV with:

| Column | Description |
|---|---|
| Control ID | Sequential number |
| Control Description | Defined Approach Requirements text |
| Domain | Requirement heading (e.g., "Requirement 1: Install and Maintain Network Security Controls") |
| Framework (FK) | Framework foreign key (7 = PCI DSS v4.0) |
| Identifier | Control number (e.g., 1.1.1, 12.10.7, A1.2.3) |
| Implementation Guidance | Purpose + Good Practice sections from Guidance column |
| Is Active | Yes |

## Output

**328 controls** extracted across:
- Requirements 1–12 (289 controls)
- Appendix A1, A2, A3 (39 controls)

Output file: [`output/PCI_DSS_v4_Controls.csv`](output/PCI_DSS_v4_Controls.csv)

## Project Structure

```
.
├── output/                  # Final extracted CSV
│   └── PCI_DSS_v4_Controls.csv
├── scripts/                 # Extraction scripts
│   ├── extract_pci_full.py       # Full standalone extractor (all 296 pages)
│   ├── extract_remaining.py      # Batch extractor for remaining pages
│   ├── extract_appendix.py       # Appendix control extractor
│   └── archive/                  # Incremental build scripts (historical)
├── src/                     # Source PDFs and reference files
│   ├── feed-claude-pci.pdf       # PCI DSS v4.0.1 standard (main)
│   ├── Appendix-controls.pdf     # Appendix controls PDF
│   └── Dummy Sheet - Sheet1.csv  # Sample format reference
├── .gitignore
└── README.md
```

## How It Works

1. **PDF Rendering** — PyMuPDF renders each page of the scanned PDF to PNG
2. **Vision Extraction** — Claude Haiku (claude-haiku-4-5) reads each page image and extracts structured control data
3. **Parsing & Merging** — Controls spanning multiple pages are automatically merged; duplicates are deduplicated
4. **CSV Output** — Final sorted CSV with all controls in the confirmed format

## Tech Stack

- Python 3.14+
- [PyMuPDF](https://pymupdf.readthedocs.io/) — PDF to image rendering
- [Anthropic API](https://docs.anthropic.com/) — Claude Haiku vision model for OCR extraction
- Resumable processing with JSON checkpoints

## Usage

To re-run extraction (requires Anthropic API key):

```bash
pip install anthropic pymupdf pillow
set ANTHROPIC_API_KEY=sk-ant-...
python scripts/extract_pci_full.py
```

Estimated API cost: ~$0.40 for all pages.

## License

The extracted data is derived from the PCI DSS v4.0.1 standard published by the PCI Security Standards Council. This tooling is for educational and compliance purposes.
