from arcade_mode import ArcadeGame, get_building_class
from buildings.residential import residential
from buildings.industry import industry
from buildings.commercial import commercial
from buildings.park import park
from buildings.road import road

def test_building_scores_arcade():
    print("\n=== Running Arcade Mode Score Tests ===")

    # Grid with building type identifiers
    test_grid = {
        (0, 0): 'R',
        (0, 1): 'I',
        (0, 2): 'C',
        (1, 0): 'O',
        (1, 1): '*',
    }

    # Convert to building instances
    grid_instances = {}
    for pos, btype in test_grid.items():
        cls = get_building_class(btype)
        if cls is None:
            print(f"Unknown building type {btype} at {pos}")
            continue
        grid_instances[pos] = cls()

    # Expected scores per building type (manually calculated)
    expected_scores = {
    (0, 0): 0,  # Residential
    (0, 1): 1,  # Industry
    (0, 2): 0,  # Commercial
    (1, 0): 0,  # Park
    (1, 1): 0,  # Road
    }


    all_passed = True

    for pos, building in grid_instances.items():
        row, col = pos
        try:
            score = building.score(grid_instances, row, col, mode="arcade")
            if isinstance(score, tuple):
                score = score[0]  # Take profit only for arcade scoring
        except Exception as e:
            print(f"Error scoring building {building.type_identifier} at {pos}: {e}")
            all_passed = False
            continue

        expected = expected_scores.get(pos)
        print(f"Score of {building.type_identifier} at {pos} = {score} (expected {expected})")
        if expected is not None and score != expected:
            print(f"Mismatch at {pos}: expected {expected}, got {score}")
            all_passed = False

    if all_passed:
        print("✅ All arcade mode score tests passed!")
    else:
        print("❌ Some arcade mode score tests failed.")

def make_grid(building_positions):
    grid = {}
    for (row, col), building_class in building_positions.items():
        b = building_class()
        grid[(row, col)] = b
    return grid

def test_freeplay_profit_upkeep():
    print("\n=== Running Freeplay Mode Profit/Upkeep Tests ===")

    tests = [
        {
            "desc": "Single Residential (should be 1 profit, 1 upkeep)",
            "grid": {(0, 0): residential},
            "expected": (1, 1),
        },
        {
            "desc": "Two connected Residential (should be 2 profit, 1 upkeep)",
            "grid": {(0, 0): residential, (0, 1): residential},
            "expected": (2, 1),
        },
        {
            "desc": "Two disconnected Residential (should be 2 profit, 2 upkeep)",
            "grid": {(0, 0): residential, (2, 2): residential},
            "expected": (2, 2),
        },
        {
            "desc": "One Industry (2 profit, 1 upkeep)",
            "grid": {(1, 1): industry},
            "expected": (2, 1),
        },
        {
            "desc": "One Commercial (3 profit, 2 upkeep)",
            "grid": {(1, 1): commercial},
            "expected": (3, 2),
        },
        {
            "desc": "One Park (0 profit, 1 upkeep)",
            "grid": {(1, 1): park},
            "expected": (0, 1),
        },
        {
            "desc": "Unconnected Road (0 profit, 1 upkeep)",
            "grid": {(1, 1): road},
            "expected": (0, 1),
        },
        {
            "desc": "Connected Road (0 profit, 0 upkeep)",
            "grid": {(1, 1): road, (1, 2): residential},
            "expected": (1, 1),  # Road is connected, upkeep 0; R = 1 profit, 1 upkeep
        },
    ]

    for test in tests:
        grid = make_grid(test["grid"])
        profit = 0
        upkeep = 0
        visited = set()  # shared visited set for cluster tracking

        for (r, c), b in grid.items():
            print(f"Calculating profit/upkeep for building at ({r},{c}) of type {type(b).__name__}")
            if hasattr(b, 'type_identifier') and b.type_identifier == 'R':
                p, u = b.calculate_profit_and_upkeep(grid, r, c, mode="freeplay", visited=visited)
            else:
                p, u = b.calculate_profit_and_upkeep(grid, r, c, mode="freeplay")
            profit += p
            upkeep += u

        print(f"{test['desc']}: Profit = {profit}, Upkeep = {upkeep}, Expected = {test['expected']}")
        assert (profit, upkeep) == test["expected"], f"FAILED: {test['desc']}"

    print("✅ All freeplay profit/upkeep tests passed!")

if __name__ == "__main__":
    test_building_scores_arcade()
    test_freeplay_profit_upkeep()
