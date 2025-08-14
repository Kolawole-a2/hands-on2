# ---------- Imports ----------
import os
from pathlib import Path
import numpy as np
import pandas as pd
import h2o
from h2o.estimators import H2OEstimator

# Optional GenAI
try:
    import openai as genai
except ImportError:
    genai = None

# ---------- Utilities ----------
def shannon_entropy(s: str) -> float:
    if not s:
        return 0.0
    from collections import Counter
    from math import log2
    counts = Counter(s)
    probs = [c / len(s) for c in counts.values()]
    return -sum(p * log2(p) for p in probs)

def featurize(domain: str) -> pd.DataFrame:
    core = domain.split(".", 1)[0].replace("-", "")
    return pd.DataFrame([{
        "domain": domain,
        "length": len(core),
        "entropy": shannon_entropy(core)
    }])

def generate_playbook(xai_findings: str) -> str:
    api_key = os.getenv("GOOGLE_API_KEY", "").strip()
    if api_key and genai is not None:
        # Call GenAI here (mock example)
        return f"Generated playbook based on AI: {xai_findings}"
    return f"Local fallback playbook: {xai_findings}"

# ---------- Model Loading ----------
def load_model(model_dir: Path):
    mojo_files = list(model_dir.glob("*.zip"))
    if not mojo_files:
        raise FileNotFoundError("No MOJO found in model directory")
    model = h2o.import_mojo(str(mojo_files[0]))
    return model

# ---------- SHAP Wrapper ----------
def predict_proba_for_shap(model: H2OEstimator, X_df: pd.DataFrame) -> np.ndarray:
    pred_df = h2o.H2OFrame(X_df)
    pred = model.predict(pred_df).as_data_frame()
    return pred[["dga", "legit"]].to_numpy()

# ---------- Main ----------
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", required=True)
    args = parser.parse_args()
    domain = args.domain

    h2o.init()
    model = load_model(Path("model"))
    X = featurize(domain)
    pred_df = h2o.H2OFrame(X)
    pred = model.predict(pred_df).as_data_frame()
    
    label = pred["predict"][0]
    confidence = pred["dga"][0] if "dga" in pred.columns else max(pred.iloc[0])
    
    print("\n[Prediction]")
    print(pred)
    print(f"\n[Result] Domain: {domain} -> {label} (confidence ~ {confidence})")

    if label == "dga":
        xai_findings = f"- Alert: Potential DGA domain detected. - Domain: '{domain}' - Confidence: {confidence}"
        playbook = generate_playbook(xai_findings)
        print("\n[Prescriptive Playbook]")
        print(playbook)
    else:
        print("\n[Info] Prediction is 'legit' — no prescriptive playbook generated.")

    h2o.cluster().shutdown()
