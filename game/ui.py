"""Buttons and the HUD."""
import pygame
from game.assets import SND_CLICK
from game.settings import BROWN, DARKBROWN, FONT, GAME_SETTINGS, HUD_FONT, WHITE, WIDTH, YELLOW

class RPGButton:
    def __init__(self, text, x, y, w=450, h=70):
        self.text = text; self.rect = pygame.Rect(x, y, w, h)
    def draw(self, surf):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        color = DARKBROWN if hover else BROWN
        pygame.draw.rect(surf, color, self.rect, border_radius=10)
        pygame.draw.rect(surf, YELLOW, self.rect, 4, 10)
        label = FONT.render(self.text, True, WHITE)
        surf.blit(label, (self.rect.centerx - label.get_width()//2, self.rect.centery - label.get_height()//2))
    def clicked(self):
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
            if GAME_SETTINGS["sound"] and SND_CLICK: SND_CLICK.play()
            pygame.time.delay(200); return True
        return False


def draw_hud(surf, mode, p1_lives, p1_coins, p1_score=0, p2_lives=0, p2_coins=0):
    # --- CONSTANTS FOR EXACT LOOK ---
    MARGIN_X = 20
    MARGIN_Y = 20
    LINE_SPACING = 25  # Reduced spacing for smaller text
    TOTAL_COINS = 20

    # ==========================
    # PLAYER 1 (LEFT SIDE)
    # ==========================
    # 1. Score (White)
    score_surf = HUD_FONT.render(f"Score: {p1_score}", False, WHITE)
    surf.blit(score_surf, (MARGIN_X, MARGIN_Y))

    # 2. Lives (White)
    lives_surf = HUD_FONT.render(f"Lives: {p1_lives}", False, WHITE)
    surf.blit(lives_surf, (MARGIN_X, MARGIN_Y + LINE_SPACING))

    # 3. Coins (Yellow)
    # UPDATED: Checks for both VS AI and Race Mode now
    if mode in ["vs_ai", "race_mode"]:
        coins_text = f"Coins: {p1_coins}"
    else:
        coins_text = f"Coins: {p1_coins}/{TOTAL_COINS}"
        
    coins_surf = HUD_FONT.render(coins_text, False, YELLOW)
    surf.blit(coins_surf, (MARGIN_X, MARGIN_Y + LINE_SPACING * 2))

    # ==========================
    # PLAYER 2 / CPU (RIGHT SIDE)
    # ==========================
    if mode in ["vs_ai", "race_mode"]:
        p2_name = "CPU" if mode == "vs_ai" else "P2"
        
        # 1. P2/CPU Score (Calculated from coins for display)
        # We display a score for the second player so it looks distinct
        p2_display_score = p2_coins * 100
        p2_score_txt = f"{p2_name} Score: {p2_display_score}"
        p2_score_surf = HUD_FONT.render(p2_score_txt, False, WHITE)
        p2_score_x = WIDTH - p2_score_surf.get_width() - MARGIN_X
        surf.blit(p2_score_surf, (p2_score_x, MARGIN_Y))

        # 2. Lives (White)
        p2_lives_txt = f"{p2_name} Lives: {p2_lives}"
        p2_lives_surf = HUD_FONT.render(p2_lives_txt, False, WHITE)
        p2_lives_x = WIDTH - p2_lives_surf.get_width() - MARGIN_X
        surf.blit(p2_lives_surf, (p2_lives_x, MARGIN_Y + LINE_SPACING)) 

        # 3. Coins (Yellow)
        # UPDATED: Checks for both VS AI and Race Mode now
        if mode in ["vs_ai", "race_mode"]:
            p2_coins_txt = f"Coins: {p2_coins}" # Just raw coins
        else:
            p2_coins_txt = f"Coins: {p2_coins}/{TOTAL_COINS}"

        p2_coins_surf = HUD_FONT.render(p2_coins_txt, False, YELLOW)
        p2_coins_x = WIDTH - p2_coins_surf.get_width() - MARGIN_X
        surf.blit(p2_coins_surf, (p2_coins_x, MARGIN_Y + LINE_SPACING * 2))
