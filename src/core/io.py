import pandas as pd
from pathlib import Path

def ensure_dir(path):
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p

def save_parquet(df: pd.DataFrame, path: str):
    ensure_dir(Path(path).parent)
    df.to_parquet(path, index=False)

def load_parquet(path: str) -> pd.DataFrame:
    return pd.read_parquet(path)
