# Copyright (c) 2025 Florian Scherrer
# Licensed under the Business Source License 1.1 (BUSL-1.1).
# See the LICENSE file for the full text, including Change Date and Change License.

import importlib, argparse
from src.core.logging_config import setup_logging
from src.pipelines import dag_minimal

def _call(target: str):
    mod, func = target.split(":")
    m = importlib.import_module(mod)
    return getattr(m, func)()

def main():
    setup_logging()
    parser = argparse.ArgumentParser()
    parser.add_argument("--pipeline", choices=["minimal"], default="minimal")
    args = parser.parse_args()
    for name, target in dag_minimal():
        print(f"?? {name}")
        _call(target)

if __name__ == "__main__":
    main()
