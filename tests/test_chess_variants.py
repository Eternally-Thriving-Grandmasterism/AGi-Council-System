from grandmasterism.modules.chess_engine_variants import ChessEngineVariants

def test_variant_move():
    engine = ChessEngineVariants()
    result = engine.simulate_variant_move("standard", "e4")
    assert "fen" in result
    assert result["eval_score"] == 0
