from scoring import ScoringSystem

class GameEconomy:
    def __init__(self, map_reference, mode="arcade"):
        self.mode = mode
        self.map = map_reference
        self.score_system = ScoringSystem(map_reference)
        self.score = 0
        self.coins = 16 if mode == "arcade" else float('inf')

    def calculate_total_score(self):
        total = 0
        for pos, abbr in self.map.grid.items():
            total += self.score_system.scoring_main(pos, abbr)
        return total

    def place_building(self, pos, building_abbr):
        if self.mode == "arcade" and self.coins < 1:
            return False, "Not enough coins to place building."

        if self.mode == "arcade":
            self.coins -= 1

        # Place building on map grid here before scoring (if not done elsewhere)
        self.map.grid[(pos[1], pos[0])] = building_abbr  # if needed

        # Recalculate total score after placement
        self.score = self.calculate_total_score()

        return True, "Building placed."

    def generate_arcade_coins(self):
        coins = 0
        visited = set()

        for (y, x), abbr in self.map.grid.items():
            pos = (x, y)
            print(f"Checking tile at {pos}: {abbr}")
            if abbr in ["I", "C"] and pos not in visited:
                connected = self.score_system.get_connected_buildings(pos)
                count = sum(1 for _, b in connected if b == "R")
                coins += count
                visited.add(pos)

        return coins

    def calculate_freeplay_income(self):
        profit = 0
        upkeep = 0

        res_clusters = self.score_system._get_clusters("R")
        total_residential = sum(len(cluster) for cluster in res_clusters)
        profit += total_residential
        upkeep += len(res_clusters)

        industry_count = 0
        commercial_count = 0
        park_count = 0

        for abbr in self.map.grid.values():
            if abbr == "I":
                industry_count += 1
            elif abbr == "C":
                commercial_count += 1
            elif abbr == "O":
                park_count += 1

        profit += industry_count * 2
        upkeep += industry_count

        profit += commercial_count * 3
        upkeep += commercial_count * 2

        upkeep += park_count

        road_clusters = self.score_system._get_clusters("*")
        for cluster in road_clusters:
            if len(cluster) == 1:
                upkeep += 1

        return profit, upkeep

    def get_stats_arcade(self):
        coins = self.coins
        score = self.score
        return coins, score

    def get_stats_freeplay(self):
        profit, upkeep = self.calculate_freeplay_income()
        return profit, upkeep, self.score
