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
