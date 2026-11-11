"""BFS pathfinder used by the AI player."""
import math
import pygame

# =============================================================
# ROBUST GRAPH PATHFINDER (Fixed AttributeError)
# =============================================================
class BFS_Pathfinder:
    def __init__(self, platforms, ladders):
        self.platforms = list(platforms)
        self.ladders = list(ladders)
        self.levels = [] # Stores unique Y-heights of floors
        self.graph = {}  # { floor_y: [ (connected_floor_y, ladder_obj), ... ] }
        
        self.analyze_levels()
        self.build_graph()

    def analyze_levels(self):
        # 1. Identify all unique floor heights from platforms
        raw_heights = [p.rect.top for p in self.platforms]
        raw_heights.sort()
        
        self.levels = []
        if raw_heights:
            current_level = raw_heights[0]
            count = 1
            total = current_level
            
            for h in raw_heights[1:]:
                if h - current_level < 20: # Group close platforms
                    count += 1
                    total += h
                    current_level = h
                else:
                    self.levels.append(int(total / count))
                    current_level = h
                    total = h
                    count = 1
            self.levels.append(int(total / count))

    def get_closest_level(self, y_pos):
        if not self.levels: return y_pos
        return min(self.levels, key=lambda lvl: abs(lvl - y_pos))

    def build_graph(self):
        self.graph = {}
        for lvl in self.levels: self.graph[lvl] = []

        for lad in self.ladders:
            top_node = self.get_closest_level(lad.rect.top)
            bottom_node = self.get_closest_level(lad.rect.bottom)
            
            if top_node != bottom_node:
                self.graph[top_node].append((bottom_node, lad))
                self.graph[bottom_node].append((top_node, lad))

    def find_path(self, start_y, target_y):
        start_node = self.get_closest_level(start_y)
        target_node = self.get_closest_level(target_y)

        if start_node == target_node: return []

        queue = [[start_node]]
        visited = {start_node}

        while queue:
            path = queue.pop(0)
            node = path[-1]

            if node == target_node:
                return path

            if node in self.graph:
                for neighbor, ladder in self.graph[node]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        new_path = list(path)
                        new_path.append(neighbor)
                        queue.append(new_path)
        return []

    # --- THIS WAS THE MISSING FUNCTION CAUSING THE CRASH ---
    def calculate_coin_path(self, start_pos, coins_group, goal_pos):
        # Returns a rough estimate of moves to collect coins
        # This prevents the game loop from crashing when calculating stats
        return len(coins_group) * 15 + 10 
    # -------------------------------------------------------

    def get_next_move_for_bot(self, player_rect, coins_group, final_goal_rect, is_climbing, climb_dir):
        # 1. COMMITMENT
        if is_climbing:
            if climb_dir == -1: return "climb_up", player_rect.centerx
            if climb_dir == 1: return "climb_down", player_rect.centerx

        # 2. TARGET SELECTION
        target_rect = final_goal_rect
        if coins_group and len(coins_group) > 0:
            closest_coin = min(coins_group, key=lambda c: math.hypot(c.rect.x - player_rect.x, c.rect.y - player_rect.y))
            target_rect = closest_coin.rect

        # 3. PATHFINDING
        start_level = self.get_closest_level(player_rect.bottom)
        target_level = self.get_closest_level(target_rect.bottom)

        if start_level == target_level:
            return "run_to_goal", target_rect.centerx

        path = self.find_path(start_level, target_level)
        
        if not path or len(path) < 2:
            return "run_to_goal", target_rect.centerx

        next_level = path[1]
        
        best_ladder = None
        min_dist = 9999
        
        for neighbor, ladder in self.graph.get(start_level, []):
            if neighbor == next_level:
                dist = abs(player_rect.centerx - ladder.rect.centerx)
                if dist < min_dist:
                    min_dist = dist
                    best_ladder = ladder
        
        if best_ladder:
            if abs(player_rect.centerx - best_ladder.rect.centerx) < 15:
                if next_level < start_level: return "climb_up", best_ladder.rect.centerx
                else: return "climb_down", best_ladder.rect.centerx
            else:
                return "run_to_ladder", best_ladder.rect.centerx

        return "wait", 0
