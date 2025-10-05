import logging.config, yaml
def setup_logging(path: str = "config/logging.yaml"):
    with open(path, "r") as f:
        cfg = yaml.safe_load(f)
    logging.config.dictConfig(cfg)
