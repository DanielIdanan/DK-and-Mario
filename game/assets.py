"""Sounds, sprite loading and the animated menu background."""
import os
import pygame
from game.settings import BG_DIR, HEIGHT, SND_DIR, WIDTH

def load_snd(filename):
    path = os.path.join(SND_DIR, filename)
    if os.path.exists(path): return pygame.mixer.Sound(path)
    return None

SND_BG = os.path.join(SND_DIR, "bg.ogg")
SND_CLICK = load_snd("click.ogg")
SND_JUMP = load_snd("jump.ogg")
SND_COIN = load_snd("coin.ogg")
SND_WIN = load_snd("win.ogg")
SND_GAMEOVER = load_snd("gameover.ogg")
SND_BARREL = load_snd("barrel_roll.ogg")

if os.path.exists(SND_BG):
    pygame.mixer.music.load(SND_BG)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

_SPRITE_CACHE = {}
def load_sprite(path, w, h, fallback_color):
    key = (path, w, h)
    if key in _SPRITE_CACHE: return _SPRITE_CACHE[key]
    s = _load_sprite(path, w, h, fallback_color)
    _SPRITE_CACHE[key] = s
    return s

def _load_sprite(path, w, h, fallback_color):
    try:
        img = pygame.image.load(path).convert()
        img.set_colorkey((0,0,0))
        if "floor" in path: img.set_colorkey((255, 255, 255))
        return pygame.transform.scale(img, (w, h))
    except:
        surf = pygame.Surface((w, h))
        surf.fill(fallback_color)
        return surf

def palette_swap_luigi(surface):
    width, height = surface.get_size()
    new_surf = surface.copy()
    pixels = pygame.PixelArray(new_surf)
    for x in range(width):
        for y in range(height):
            c = new_surf.unmap_rgb(pixels[x, y])
            if c.r > 100 and c.g < 80 and c.b < 80:
                pixels[x, y] = (c.g, c.r, c.b, c.a)
    pixels.close()
    return new_surf

def load_bg_frames(folder):
    frames = []
    try:
        for name in sorted(os.listdir(folder)):
            if name.lower().endswith((".jpg", ".png")):
                frames.append(pygame.image.load(os.path.join(folder, name)).convert())
    except Exception:
        pass
    return frames or [pygame.Surface((WIDTH, HEIGHT))]

BG_FRAMES = load_bg_frames(BG_DIR)
bg_frame_index = 0
bg_anim_timer = 0
bg_scaled = pygame.transform.scale(BG_FRAMES[0], (WIDTH, HEIGHT))

def draw_dynamic_background(surf):
    global bg_anim_timer, bg_frame_index, bg_scaled
    current_time = pygame.time.get_ticks()
    if len(BG_FRAMES) > 1:
        if current_time - bg_anim_timer > 100:
            bg_frame_index = (bg_frame_index + 1) % len(BG_FRAMES)
            bg_anim_timer = current_time
            bg_scaled = pygame.transform.scale(BG_FRAMES[bg_frame_index], (WIDTH, HEIGHT))
        surf.blit(bg_scaled, (0,0))
    else:
        surf.fill((30, 20, 10))
