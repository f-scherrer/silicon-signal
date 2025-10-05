from src.modules.01_baseline_features.run import run
def test_smoke_run():
    assert run() in (True, False)
