from pathlib import Path
BASE = Path("data")

def raw_prices(ticker: str) -> Path:
    return BASE / "raw" / "prices" / f"{ticker}.parquet"

def features_tech(ticker: str) -> Path:
    return BASE / "features" / "tech" / f"{ticker}.parquet"
