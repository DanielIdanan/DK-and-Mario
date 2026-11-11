"""Menus and static screens."""
import asyncio, sys
import pygame
from game.assets import draw_dynamic_background
from game.settings import BLACK, CYAN, FONT, FPS, GAME_SETTINGS, GREEN_NEON, HEIGHT, SMALL, SUBTITLE_FONT, TITLE_FONT, WHITE, WIDTH, YELLOW, clock
from game.ui import RPGButton

# =============================================================
# SCREENS & LOOPS
# =============================================================

async def level_complete_screen(level, score, lives, optimal_moves=0):
    screen = pygame.display.get_surface()
    cont_btn = RPGButton("CONTINUE" if level < 4 else "MAIN MENU", WIDTH//2 - 225, 450)
    exit_btn = RPGButton("EXIT GAME", WIDTH//2 - 225, 550)
    
    while True:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        
        t = TITLE_FONT.render("LEVEL COMPLETE!", True, GREEN_NEON)
        s = FONT.render(f"Final Score: {score}", True, WHITE)
        l = FONT.render(f"Lives Left: {lives}", True, WHITE)
        opt_txt = SMALL.render(f"BFS Analysis (TSP Estimate): {optimal_moves} Moves", True, CYAN)

        screen.blit(t, (WIDTH//2 - t.get_width()//2, 80))
        screen.blit(s, (WIDTH//2 - s.get_width()//2, 180))
        screen.blit(l, (WIDTH//2 - l.get_width()//2, 230))
        screen.blit(opt_txt, (WIDTH//2 - opt_txt.get_width()//2, 280))

        cont_btn.draw(screen); exit_btn.draw(screen)
        
        if cont_btn.clicked(): return "next"
        if exit_btn.clicked(): return "menu"
        pygame.display.update(); clock.tick(FPS); await asyncio.sleep(0)

async def game_beaten_screen(score, lives, optimal_moves=0):
    screen = pygame.display.get_surface()
    btn = RPGButton("MAIN MENU", WIDTH//2 - 225, 500)
    while True:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            
        t1 = TITLE_FONT.render("GAME BEATEN!", True, YELLOW)
        t2 = FONT.render("Congratulations! You saved Pauline.", True, WHITE)
        t3 = FONT.render(f"Total Score: {score}", True, WHITE)
        opt_txt = SMALL.render(f"BFS Analysis (TSP Estimate): {optimal_moves} Moves", True, CYAN)

        screen.blit(t1, (WIDTH//2 - t1.get_width()//2, 100))
        screen.blit(t2, (WIDTH//2 - t2.get_width()//2, 200))
        screen.blit(t3, (WIDTH//2 - t3.get_width()//2, 300))
        screen.blit(opt_txt, (WIDTH//2 - opt_txt.get_width()//2, 360))

        btn.draw(screen)
        if btn.clicked(): return "menu"
        pygame.display.update(); clock.tick(FPS); await asyncio.sleep(0)

async def how_to_play_screen():
    screen = pygame.display.get_surface()
    back_btn = RPGButton("BACK", WIDTH//2 - 225, 580)
    while True:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        
        title = TITLE_FONT.render("HOW TO PLAY", True, YELLOW)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        instr = [
            "MODES:",
            "1 PLAYER: Standard Campaign.",
            "VS AI: Race against the computer!",
            "2 PLAYER: Race your friend to the top!",
            "",
            "OBJECTIVE: Collect Coins -> Open Cage!",
            "(Level 4: Save Pauline at the top)",
            "",
            "PLAYER 1 (MARIO): WASD | SPACE",
            "PLAYER 2 (LUIGI): ARROWS | R-SHIFT"
        ]
        for i, line in enumerate(instr):
            txt = FONT.render(line, True, WHITE)
            screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 120 + i * 40))
        back_btn.draw(screen)
        if back_btn.clicked(): return
        pygame.display.update(); clock.tick(FPS); await asyncio.sleep(0)

async def credits_screen():
    screen = pygame.display.get_surface()
    back_btn = RPGButton("BACK", WIDTH//2 - 225, 580)
    while True:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        
        title = TITLE_FONT.render("CREDITS", True, YELLOW)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        lines = [
            "DEVELOPED BY:", "BSIT 2C GROUP-1", "",
            "ASSETS & ART:", "DANIEL IDANAN", "JULIAN JAY DE GUZMAN", "",
            "SPECIAL THANKS:", "PROF. JOHNIEL MENDOZA", "Gordon College CCS", "",
            "ALL RIGHTS RESERVED © 2025"
        ]
        for i, line in enumerate(lines):
            col = YELLOW if i == len(lines)-1 else WHITE
            txt = FONT.render(line, True, col)
            screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 150 + i * 35))
        back_btn.draw(screen)
        if back_btn.clicked(): return
        pygame.display.update(); clock.tick(FPS); await asyncio.sleep(0)


async def settings_menu():
    screen = pygame.display.get_surface()
    while True:
        txt_fs = "FULLSCREEN: F11 (BROWSER)" if sys.platform == "emscripten" else f"FULLSCREEN: {'ON' if GAME_SETTINGS['fullscreen'] else 'OFF'}"
        txt_snd = f"SOUND: {'ON' if GAME_SETTINGS['sound'] else 'OFF'}"
        
        fs_btn = RPGButton(txt_fs, WIDTH//2 - 225, 200)
        snd_btn = RPGButton(txt_snd, WIDTH//2 - 225, 290)
        htp_btn = RPGButton("HOW TO PLAY", WIDTH//2 - 225, 380)
        crd_btn = RPGButton("CREDITS", WIDTH//2 - 225, 470)
        back_btn = RPGButton("BACK", WIDTH//2 - 225, 560)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        draw_dynamic_background(screen)
        title = TITLE_FONT.render("SETTINGS", True, YELLOW)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))
        
        fs_btn.draw(screen); snd_btn.draw(screen)
        htp_btn.draw(screen); crd_btn.draw(screen); back_btn.draw(screen)

        if back_btn.clicked(): return "menu"
        if htp_btn.clicked(): await how_to_play_screen()
        if crd_btn.clicked(): await credits_screen()
        if fs_btn.clicked():
            if sys.platform != "emscripten":
                GAME_SETTINGS["fullscreen"] = not GAME_SETTINGS["fullscreen"]
                if GAME_SETTINGS["fullscreen"]: screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                else: screen = pygame.display.set_mode((WIDTH, HEIGHT))
        if snd_btn.clicked():
            GAME_SETTINGS["sound"] = not GAME_SETTINGS["sound"]
            if GAME_SETTINGS["sound"]: pygame.mixer.music.unpause()
            else: pygame.mixer.music.pause()
        pygame.display.update(); clock.tick(FPS); await asyncio.sleep(0)

async def mode_select():
    screen = pygame.display.get_surface()
    sp_btn = RPGButton("1 PLAYER", WIDTH//2 - 225, 250)
    ai_btn = RPGButton("VS COMPUTER (AI)", WIDTH//2 - 225, 340)
    tp_btn = RPGButton("2 PLAYER (RACE)", WIDTH//2 - 225, 430)
    back_btn = RPGButton("BACK", WIDTH//2 - 225, 520)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        draw_dynamic_background(screen); title = TITLE_FONT.render("SELECT MODE", True, YELLOW)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))
        
        sp_btn.draw(screen); ai_btn.draw(screen)
        tp_btn.draw(screen); back_btn.draw(screen)
        
        if sp_btn.clicked(): return "singleplayer"
        if ai_btn.clicked(): return "vs_ai"
        if tp_btn.clicked(): return "race_mode"
        if back_btn.clicked(): return "menu"
        pygame.display.update(); clock.tick(FPS); await asyncio.sleep(0)

async def main_menu():
    screen = pygame.display.get_surface()
    play_btn = RPGButton("PLAY GAME", WIDTH//2 - 225, 350); set_btn = RPGButton("SETTINGS", WIDTH//2 - 225, 440); quit_btn = RPGButton("QUIT", WIDTH//2 - 225, 530)
    y_off = 0; direction = 0.5
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        draw_dynamic_background(screen); y_off += direction
        if y_off > 10 or y_off < -10: direction *= -1
        t1 = TITLE_FONT.render("DONKEY KONG", True, YELLOW); t2 = SUBTITLE_FONT.render("(DSA Edition)", True, WHITE)
        screen.blit(t1, (WIDTH//2 - t1.get_width()//2, 120 + y_off)); screen.blit(t2, (WIDTH//2 - t2.get_width()//2, 200 + y_off))
        play_btn.draw(screen); set_btn.draw(screen); quit_btn.draw(screen)
        if play_btn.clicked(): return "mode_select"
        if set_btn.clicked(): return "settings"
        if quit_btn.clicked(): pygame.quit(); sys.exit()
        pygame.display.update(); clock.tick(FPS); await asyncio.sleep(0)
