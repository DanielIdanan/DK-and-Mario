"""Window, constants, paths, colors and fonts."""
import os
import pygame

# =============================================================
# INITIALIZATION & CONSTANTS
# =============================================================
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1280, 720
FPS = 60

GAME_SETTINGS = {
    "fullscreen": False,
    "sound": True
}

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Donkey Kong: DSA Edition")
clock = pygame.time.Clock()

# =============================================================
# ASSETS & PATHS
# =============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

FONT_DIR = os.path.join(ASSETS_DIR, "fonts")
IMG_DIR = os.path.join(ASSETS_DIR, "images")
SND_DIR = os.path.join(ASSETS_DIR, "sounds")
SPRITE_DIR = os.path.join(ASSETS_DIR, "sprites")

MARIO_DIR = os.path.join(SPRITE_DIR, "mario")
DK_DIR = os.path.join(SPRITE_DIR, "dk")
BARREL_DIR = os.path.join(SPRITE_DIR, "barrel")
PLATFORM_DIR = os.path.join(SPRITE_DIR, "platforms")
FIRE_DIR = os.path.join(SPRITE_DIR, "fire")
PAULINE_DIR = os.path.join(SPRITE_DIR, "pauline")

FONT_PATH = os.path.join(FONT_DIR, "RPG.ttf")
BG_DIR = os.path.join(IMG_DIR, "bg")
FLOOR_IMG_PATH = os.path.join(PLATFORM_DIR, "floor.png")
COIN_IMG_PATH = os.path.join(PLATFORM_DIR, "coin.png")
HEART_IMG_PATH = os.path.join(PAULINE_DIR, "heart.png") 

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 80, 80)
YELLOW = (255, 220, 120)
BROWN = (120, 70, 20)
DARKBROWN = (70, 40, 10)
GREEN_NEON = (50, 255, 50) 
PURPLE = (150, 50, 200)
ORANGE = (255, 165, 0)
SILVER = (192, 192, 192)
CYAN = (0, 255, 255)
PINK = (255, 105, 180) 

try:
    TITLE_FONT = pygame.font.Font(FONT_PATH, 60)
    SUBTITLE_FONT = pygame.font.Font(FONT_PATH, 30)
    FONT = pygame.font.Font(FONT_PATH, 35) 
    SMALL = pygame.font.Font(FONT_PATH, 20)
    HUD_FONT = pygame.font.Font(FONT_PATH, 24)
except:
    TITLE_FONT = pygame.font.Font(None, 60)
    SUBTITLE_FONT = pygame.font.Font(None, 30)
    FONT = pygame.font.Font(None, 35)
    SMALL = pygame.font.Font(None, 20)
    HUD_FONT = pygame.font.Font(None, 24)
