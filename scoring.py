class ScoringSystem:
    def __init__(self, map_reference):
        self.map = map_reference
        self.building_counts = {}

    def update_building_counts(self):
        self.building_counts = {}
        for row in self.map.grid:
            for tile in row:
                if tile and tile.building:
                    abbr = tile.building.abbreviation
                    self.building_counts[abbr] = self.building_counts.get(abbr, 0) + 1

    def get_adjacent_buildings(self, pos):
        adjacent = []
        x, y = pos
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= ny < len(self.map.grid) and 0 <= nx < len(self.map.grid[0]):
                tile = self.map.grid[ny][nx]
                if tile and tile.building:
                    adjacent.append(((nx, ny), tile.building))
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
            if not (0 <= y < len(self.map.grid) and 0 <= x < len(self.map.grid[0])):
                continue

            tile = self.map.grid[y][x]
            if not tile or not tile.building:
                continue

            abbr = tile.building.abbreviation

            if abbr == "*":  
                if include_roads:
                    connected.append((pos, tile.building))
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    new_pos = (x + dx, y + dy)
                    if new_pos not in visited:
                        to_visit.append(new_pos)
            else:
                connected.append((pos, tile.building))
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    road_pos = (x + dx, y + dy)
                    if road_pos not in visited:
                        rx, ry = road_pos
                        if 0 <= ry < len(self.map.grid) and 0 <= rx < len(self.map.grid[0]):
                            road_tile = self.map.grid[ry][rx]
                            if road_tile and road_tile.building and road_tile.building.abbreviation == "*":
                                to_visit.append(road_pos)

        return connected

    def scoring_main(self, pos, building_abbr):
        self.update_building_counts()

        if building_abbr == "*":
            return self.score_road(pos)
        elif building_abbr == "I":
            return self.score_industry()
        elif building_abbr == "C":
            return self.score_commercial(pos)
        elif building_abbr == "O":
            return self.score_park(pos)
        elif building_abbr == "R":
            return self.score_residential(pos)
        else:
            return 0

    def score_residential(self, pos):
        adj = self.get_adjacent_buildings(pos)
        if any(b.abbreviation == "I" for _, b in adj):
            return 1
        points = 0
        for _, b in adj:
            if b.abbreviation in ["R", "C"]:
                points += 1
            elif b.abbreviation == "O":
                points += 2
        return points

    def score_industry(self):
        return self.building_counts.get("I", 0)

    def score_commercial(self, pos):
        connected = self.get_connected_buildings(pos)
        return sum(1 for _, b in connected if b.abbreviation == "C")

    def score_park(self, pos):
        connected = self.get_connected_buildings(pos)
        return sum(1 for _, b in connected if b.abbreviation == "O")

    def score_road(self, pos):
        x, y = pos
        if not (0 <= y < len(self.map.grid)):
            return 0
        row = self.map.grid[y]
        return sum(1 for tile in row if tile and tile.building and tile.building.abbreviation == "*")

    def calculate_profit_and_upkeep(self):
        profit = 0
        upkeep = 0

        res_clusters = self._get_clusters("R")
        total_residential = sum(len(cluster) for cluster in res_clusters)
        profit += total_residential
        upkeep += len(res_clusters)

        industry_buildings = [b for row in self.map.grid for tile in row if tile and tile.building and (b:=tile.building).abbreviation == "I"]
        profit += len(industry_buildings) * 2
        upkeep += len(industry_buildings) * 1

        commercial_buildings = [b for row in self.map.grid for tile in row if tile and tile.building and (b:=tile.building).abbreviation == "C"]
        profit += len(commercial_buildings) * 3
        upkeep += len(commercial_buildings) * 2

        park_buildings = [b for row in self.map.grid for tile in row if tile and tile.building and (b:=tile.building).abbreviation == "O"]
        upkeep += len(park_buildings)

        road_clusters = self._get_clusters("*")
        for cluster in road_clusters:
            if len(cluster) == 1:
                upkeep += 1

        return profit, upkeep

    def _get_clusters(self, building_abbr):
        visited = set()
        clusters = []

        for y, row in enumerate(self.map.grid):
            for x, tile in enumerate(row):
                if tile and tile.building and tile.building.abbreviation == building_abbr and (x, y) not in visited:
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
                if 0 <= ny < len(self.map.grid) and 0 <= nx < len(self.map.grid[0]):
                    tile = self.map.grid[ny][nx]
                    if tile and tile.building and tile.building.abbreviation == building_abbr and (nx, ny) not in visited:
                        stack.append((nx, ny))

        return cluster

    def coin_gen_arcade(self):
        coins = 0
        visited = set()

        for y, row in enumerate(self.map.grid):
            for x, tile in enumerate(row):
                pos = (x, y)
                if tile and tile.building and tile.building.abbreviation in ["I", "C"] and pos not in visited:
                    connected = self.get_connected_buildings(pos)
                    count = sum(1 for _, b in connected if b.abbreviation == "R")
                    coins += count
                    visited.add(pos)

        return coins
