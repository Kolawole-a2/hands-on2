# Prescriptive DGA Detector

An end-to-end, **detection → explanation → prescription** pipeline:

1. **AutoML (H2O)** rapidly trains a DGA detector.
2. **XAI (SHAP)** explains *why* a specific domain was classified as DGA.
3. **GenAI (Google Generative AI)** turns those explanations into a **context-aware incident response playbook**.

## Tech Stack
- Python, H2O AutoML
- SHAP (local explanation)
- Google Generative AI (`google-generativeai`)
- Command-line interface

> **Java requirement:** H2O uses Java. Install Java 11+ and ensure `java -version` works.

## Setup

```bash
cd "my cursor projects/hands-on"
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt


Optional (for GenAI playbooks):

# Powershell
$env:GOOGLE_API_KEY="YOUR_KEY_HERE"
# bash
export GOOGLE_API_KEY="YOUR_KEY_HERE"

Train the model
python 1_train_and_export.py


Outputs:

dga_dataset_train.csv in repo root

model/ contains:

Native model (always)

DGA_Leader.zip (MOJO) if export supported

Analyze a domain
python 2_analyze_domain.py --domain google.com
python 2_analyze_domain.py --domain kq3v9z7j1x5f8g2h.info


Behavior:

Loads MOJO if available; otherwise loads native model.

Computes features (length, entropy), predicts class & confidence.

If dga, generates a local SHAP explanation and passes a structured summary to Gemini to produce a prescriptive IR playbook (or a local fallback if no API key).

Three-Stage Architecture

AutoML Training (H2O)

Synthesized training set (legit-like vs DGA-like) with features (length, entropy).

AutoML identifies the best model. MOJO exported to model/DGA_Leader.zip when supported.

Explainability (SHAP)

For a single prediction, SHAP KernelExplainer computes per-feature contributions toward dga probability.

Prescription (GenAI)

Programmatically summarizes SHAP results → xai_findings.

generate_playbook() prompts Gemini to emit an incident playbook with validation, containment, and escalation steps.

Notes

MOJO import uses h2o.import_mojo. If unavailable, we fall back to h2o.load_model (native).

SHAP uses a tiny background (median point) to stay fast.


---

# Prescriptive DGA Detector

An end-to-end, **detection → explanation → prescription** pipeline:

1. **AutoML (H2O)** rapidly trains a DGA detector.
2. **XAI (SHAP)** explains *why* a specific domain was classified as DGA.
3. **GenAI (Google Generative AI)** turns those explanations into a **context-aware incident response playbook**.

## Tech Stack
- Python, H2O AutoML
- SHAP (local explanation)
- Google Generative AI (`google-generativeai`)
- Command-line interface

> **Java requirement:** H2O uses Java. Install Java 11+ and ensure `java -version` works.

## Setup

```bash
cd "my cursor projects/hands-on"
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt


Optional (for GenAI playbooks):

# Powershell
$env:GOOGLE_API_KEY="YOUR_KEY_HERE"
# bash
export GOOGLE_API_KEY="YOUR_KEY_HERE"

Train the model
python 1_train_and_export.py


Outputs:

dga_dataset_train.csv in repo root

model/ contains:

Native model (always)

DGA_Leader.zip (MOJO) if export supported

Analyze a domain
python 2_analyze_domain.py --domain google.com
python 2_analyze_domain.py --domain kq3v9z7j1x5f8g2h.info


Behavior:

Loads MOJO if available; otherwise loads native model.

Computes features (length, entropy), predicts class & confidence.

If dga, generates a local SHAP explanation and passes a structured summary to Gemini to produce a prescriptive IR playbook (or a local fallback if no API key).

Three-Stage Architecture

AutoML Training (H2O)

Synthesized training set (legit-like vs DGA-like) with features (length, entropy).

AutoML identifies the best model. MOJO exported to model/DGA_Leader.zip when supported.

Explainability (SHAP)

For a single prediction, SHAP KernelExplainer computes per-feature contributions toward dga probability.

Prescription (GenAI)

Programmatically summarizes SHAP results → xai_findings.

generate_playbook() prompts Gemini to emit an incident playbook with validation, containment, and escalation steps.

Notes

MOJO import uses h2o.import_mojo. If unavailable, we fall back to h2o.load_model (native).

SHAP uses a tiny background (median point) to stay fast.


---

### File: `my cursor projects/hands-on/TESTING.md`
```markdown
# TESTING

## Prereqs
- `pip install -r requirements.txt`
- `python 1_train_and_export.py` (creates `/model` artifacts)
- (Optional) `GOOGLE_API_KEY` set for prescriptive playbooks.

## Test 1: Legitimate Domain

**Command**
```bash
python 2_analyze_domain.py --domain google.com


Expected

Output shows prediction legit (confidence varies).

No GenAI playbook printed (by design, only for dga).

Test 2: DGA-Like Domain

Command

python 2_analyze_domain.py --domain kq3v9z7j1x5f8g2h.info


Expected

Prediction likely dga with high confidence.

SHAP summary printed (feature impacts).

A prescriptive playbook is printed:

Validation steps (DNS logs, WHOIS, passive DNS)

Containment (egress block / DNS sinkhole)

Escalation criteria

Monitoring

Confidence and SHAP values will differ run-to-run due to synthesized data and AutoML randomness, but should qualitatively match the above behavior.


---

### File: `my cursor projects/hands-on/.github/workflows/lint.yml`
```yaml
name: Lint

on:
  push:
  pull_request:

jobs:
  ruff:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install ruff
        run: pip install ruff
      - name: Ruff check
        run: ruff check .
