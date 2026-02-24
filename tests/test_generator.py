from src.generators.synthetic_fintech import generate, SynthParams

def test_generate_shapes():
    dfs = generate(SynthParams(n_applications=200, days=14, seed=7))
    assert set(dfs.keys()) == {"applications", "payments", "marketing_events"}
    assert len(dfs["applications"]) == 200
    assert len(dfs["marketing_events"]) > 0
