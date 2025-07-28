    grid = make_grid(test["grid"])
        profit = 0
        upkeep = 0
        visited = set()  # shared visited set for cluster tracking

        for (r, c), b in grid.items():
            # Pass visited only for residential to avoid issues:
            if hasattr(b, 'type_identifier') and b.type_identifier == 'R':
                p, u = b.calculate_profit_and_upkeep(grid, r, c, mode="freeplay", visited=visited)
            else:
                p, u = b.calculate_profit_and_upkeep(grid, r, c, mode="freeplay")
            profit += p
            upkeep += u

        print(f"{test['desc']}: Profit = {profit}, Upkeep = {upkeep}, Expected = {test['expected']}")
        assert (profit, upkeep) == test["expected"], f"FAILED: {test['desc']}"
