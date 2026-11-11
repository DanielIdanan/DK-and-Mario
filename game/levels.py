"""Random level generator."""
import random
import pygame
from game.settings import WIDTH
from game.sprites import Ladder, Platform

# =============================================================
# RANDOM MAP GENERATOR (OVERLAP FIX & LOWER HEIGHTS)
# =============================================================

def generate_random_level():
    platforms = pygame.sprite.Group()
    ladders = pygame.sprite.Group()
    
    platforms.add(Platform(0, 680, 1280, 40))
    # NEW HEIGHTS: Moved everything down so top is visible
    heights = [560, 440, 320, 200] 
    
    for h in heights:
        num_segs = random.randint(2, 3)
        current_floor_segments = [] 
        for _ in range(num_segs):
            width = random.randint(300, 500)
            attempts = 0
            while attempts < 10:
                x_pos = random.randint(0, WIDTH - width)
                new_rect = pygame.Rect(x_pos, h, width, 30)
                overlap = False
                for seg in current_floor_segments:
                    # Overlap Check
                    if new_rect.colliderect(seg.inflate(50, 0)):
                        overlap = True; break
                if not overlap:
                    platforms.add(Platform(x_pos, h, width, 30))
                    current_floor_segments.append(new_rect)
                    break
                attempts += 1
        
        # Ensure Ladders
        if current_floor_segments:
            chosen_rect = random.choice(current_floor_segments)
            # Center ladder on platform
            ladder_x = chosen_rect.centerx 
            ladders.add(Ladder(ladder_x, h, 130))
        
    # GOAL PLATFORM (LOWERED TO Y=100)
    platforms.add(Platform(WIDTH//2 - 200, 100, 400, 30))
    ladders.add(Ladder(WIDTH//2, 100, 110)) 

    return platforms, ladders

def load_level_data(level_num):
    return generate_random_level()
