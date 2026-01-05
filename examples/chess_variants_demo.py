from grandmasterism import GrandmasterismEngine

gm = GrandmasterismEngine()
print(gm.deliberate_chess_variant("standard", "e4"))
print(gm.deliberate_chess_variant("crazyhouse", "e4"))
print(gm.optimize_chess_timeline("crazyhouse"))
