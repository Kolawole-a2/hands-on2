# ---------- Imports ----------
import pandas as pd
import numpy as np
import h2o
from h2o.automl import H2OAutoML
from pathlib import Path

# ---------- Utilities ----------
def shannon_entropy(s: str) -> float:
    """Compute Shannon entropy of a string"""
    if not s:
        return 0.0
    from collections import Counter
    from math import log2
    counts = Counter(s)
    probs = [c / len(s) for c in counts.values()]
    return -sum(p * log2(p) for p in probs)

def synth_dga_like(n: int, min_len=12, max_len=28, tlds=None):
    tlds = tlds or [".com", ".net", ".org", ".info", ".xyz"]
    out = []
    for _ in range(n):
        length = np.random.randint(min_len, max_len + 1)
        core = "".join(np.random.choice(list("abcdefghijklmnopqrstuvwxyz0123456789"), length))
        tld = np.random.choice(tlds)
        out.append(core + tld)
    return out

def synth_legit_like(n: int, tlds=None):
    tlds = tlds or [".com", ".net", ".org"]
    tokens = ["home", "shop", "blog", "data", "news", "app"]
    out = []
    for _ in range(n):
        core = "".join(np.random.choice(tokens, size=3))
        tld = np.random.choice(tlds)
        out.append(core + tld)
    return out

def build_dataset(n_legit=250, n_dga=250) -> pd.DataFrame:
    legit = synth_legit_like(n_legit)
    dga = synth_dga_like(n_dga)
    df = pd.DataFrame({
        "domain": legit + dga,
        "label": ["legit"]*n_legit + ["dga"]*n_dga
    })
    df["length"] = df["domain"].apply(len)
    df["entropy"] = df["domain"].apply(shannon_entropy)
    return df

# ---------- Main ----------
if __name__ == "__main__":
    h2o.init()
    df = build_dataset()
    df.to_csv("dga_dataset_train.csv", index=False)

    h2o_df = h2o.H2OFrame(df)
    x = ["length", "entropy"]
    y = "label"

    aml = H2OAutoML(max_models=5, seed=42)
    aml.train(x=x, y=y, training_frame=h2o_df)

    model_dir = Path("model")
    model_dir.mkdir(exist_ok=True)
    aml.leader.download_mojo(path=model_dir, get_genmodel_jar=True)
    print(f"MOJO exported to {model_dir}")
    h2o.cluster().shutdown()
