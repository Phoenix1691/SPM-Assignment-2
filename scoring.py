# scoring.py - This file contains the scoring system for the city-building game.
class ScoringSystem:
    def __init__(self, map_reference):
        self.map = map_reference
        self.building_counts = {}

    def update_building_counts(self):
        self.building_counts = {}
        for pos, abbr in self.map.grid.items():
            if abbr:
                self.building_counts[abbr] = self.building_counts.get(abbr, 0) + 1

    def get_adjacent_buildings(self, pos):
        adjacent = []
        x, y = pos
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            abbr = self.map.grid.get((ny, nx))  # note row=y, col=x order in key
            if abbr:
                adjacent.append(((nx, ny), abbr))
        return adjacent

    def get_connected_buildings(self, start_pos, include_roads=False):
        visited = set()
        to_visit = [start_pos]
        connected = []

        while to_visit:
            pos = to_visit.pop()
            if pos in visited:
                continue
            visited.add(pos)

            x, y = pos
            abbr = self.map.grid.get((y, x))
            if not abbr:
                continue

            if abbr == "*":  
                if include_roads:
                    connected.append((pos, abbr))
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    new_pos = (x + dx, y + dy)
                    if new_pos not in visited:
                        to_visit.append(new_pos)
            else:
                connected.append((pos, abbr))
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    road_pos = (x + dx, y + dy)
                    if road_pos not in visited:
                        rx, ry = road_pos
                        road_abbr = self.map.grid.get((ry, rx))
                        if road_abbr == "*":
                            to_visit.append(road_pos)

        return connected

    def scoring_main(self, pos, building_abbr):
        self.update_building_counts()
        print(f"Scoring for {building_abbr} at {pos}")

        if building_abbr == "*":
            score = self.score_road(pos)
        elif building_abbr == "I":
            score = self.score_industry()
        elif building_abbr == "C":
            score = self.score_commercial(pos)
        elif building_abbr == "O":
            score = self.score_park(pos)
        elif building_abbr == "R":
            score = self.score_residential(pos)
        else:
            score = 0

        print(f"Score returned: {score}")
        return score


    def score_residential(self, pos):
        adj = self.get_adjacent_buildings(pos)
        if any(b == "I" for _, b in adj):
            return 1
        points = 0
        for _, b in adj:
            if b in ["R", "C"]:
                points += 1
            elif b == "O":
                points += 2
        return points

    def score_industry(self):
        return self.building_counts.get("I", 0)

    def score_commercial(self, pos):
        connected = self.get_connected_buildings(pos)
        return sum(1 for _, b in connected if b == "R")


    def score_park(self, pos):
        connected = self.get_connected_buildings(pos)
        return sum(1 for _, b in connected if b == "O")

    def score_road(self, pos):
        x, y = pos
        # Collect all tiles in the same row
        row_tiles = [self.map.grid.get((y, col)) for col in range(self.map.grid_size)] if hasattr(self.map, 'grid_size') else []
        return sum(1 for abbr in row_tiles if abbr == "*")

    def _get_clusters(self, building_abbr):
        visited = set()
        clusters = []

        for (y, x), abbr in self.map.grid.items():
            if abbr == building_abbr and (x, y) not in visited:
                cluster = self._dfs_cluster((x, y), building_abbr, visited)
                clusters.append(cluster)
        return clusters

    def _dfs_cluster(self, start_pos, building_abbr, visited):
        stack = [start_pos]
        cluster = []

        while stack:
            pos = stack.pop()
            if pos in visited:
                continue
            visited.add(pos)
            cluster.append(pos)

            x, y = pos
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                abbr = self.map.grid.get((ny, nx))
                if abbr == building_abbr and (nx, ny) not in visited:
                    stack.append((nx, ny))

        return cluster
