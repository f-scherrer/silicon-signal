import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator, MACD
from src.core.config import get_settings
from src.core.registry import raw_prices, features_tech
from src.core.io import save_parquet
from pathlib import Path
import logging

log = logging.getLogger(__name__)

def _compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values("ts")
    df["ema_20"] = EMAIndicator(df["close"], 20).ema_indicator()
    df["ema_50"] = EMAIndicator(df["close"], 50).ema_indicator()
    df["rsi_14"] = RSIIndicator(df["close"], 14).rsi()
    macd = MACD(df["close"])
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()
    df["macd_hist"] = macd.macd_diff()
    return df

def run():
    _, cfg = get_settings()
    universe = cfg["market"]["universe"]
    out_count = 0
    for t in universe:
        in_path = raw_prices(t)
        if not Path(in_path).exists():
            log.warning("Kein Raw-Preisfile gefunden: %s (skipping)", in_path)
            continue
        df = pd.read_parquet(in_path)
        df["ts"] = pd.to_datetime(df["ts"], utc=True)
        df = _compute_indicators(df)
        save_parquet(df, str(features_tech(t)))
        out_count += 1
    log.info("Baseline/Tech Features geschrieben für %d Ticker.", out_count)
    return True
