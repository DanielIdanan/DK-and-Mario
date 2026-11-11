"""Level loops and game modes."""
import asyncio, random, sys
import pygame
from game.assets import SND_COIN, SND_GAMEOVER, SND_WIN
from game.levels import generate_random_level
from game.pathfinder import BFS_Pathfinder
from game.screens import game_beaten_screen, level_complete_screen
from game.settings import BLACK, FPS, GAME_SETTINGS, GREEN_NEON, HEIGHT, HUD_FONT, RED, TITLE_FONT, WIDTH, clock
from game.sprites import Cage, Coin, DonkeyKong, Pauline, Player
from game.ui import draw_hud

async def run_level(level_num, current_score, current_lives, mode="singleplayer"):
    screen = pygame.display.get_surface()
    all_sprites = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    barrels = pygame.sprite.Group()
    fires = pygame.sprite.Group()
    
    platforms, ladders = generate_random_level()
    for p in platforms: all_sprites.add(p)
    for l in ladders: all_sprites.add(l)

    bfs_solver = BFS_Pathfinder(platforms, ladders)
    
    # Initialize Players
    player = Player(50, 600)
    
    bot_player = None
    if mode == "vs_ai":
        bot_player = Player(150, 600, is_luigi=True, is_bot=True, lives=3)
        bot_player.pathfinder = bfs_solver

    dk = DonkeyKong(WIDTH//2 - 45, 10) 
    pauline = None
    if level_num == 4:
        pauline = Pauline(dk.rect.x + 100, dk.rect.y + 10)
    
    target_rect = pauline.rect if pauline else dk.rect
    cage_rect = pygame.Rect(target_rect.x - 5, target_rect.y - 5, target_rect.width + 10, target_rect.height + 10)
    cage = Cage(cage_rect.x, cage_rect.y, cage_rect.width, cage_rect.height)

    score = current_score
    lives = current_lives
    
    coin_target = 20 
    
    # Coin Tracking Variables
    p1_coins_collected = 0
    bot_coins_collected = 0

    valid_platforms = [p for p in platforms if 150 < p.rect.y < 650]
    
    attempts = 0
    while len(coins) < coin_target and attempts < 200:
        target_plat = random.choice(valid_platforms)
        new_c = Coin(target_plat)
        if not pygame.sprite.spritecollideany(new_c, coins):
            coins.add(new_c); all_sprites.add(new_c)
        attempts += 1
    
    optimal_moves = bfs_solver.calculate_coin_path((50, 600), coins, target_rect.center)
    
    if mode != "singleplayer" and mode != "vs_ai":
        cage.active = False 
    elif mode == "singleplayer" and level_num < 4:
         pass

    game_state = "playing"
    winner_text = ""
    win_timer = 0
    win_sound_played = False
    
    running = True
    while running:
        clock.tick(FPS); await asyncio.sleep(0)
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: return "menu", 0, 0

        if game_state == "playing":
            keys = pygame.key.get_pressed()
            player.update(keys, platforms, ladders, target_rect, coins)
            
            if bot_player: 
                bot_target = target_rect if not cage.active else None
                bot_player.update(keys, platforms, ladders, bot_target, coins)
            
            if pauline: pauline.update()
            dk.update_ai(barrels, fires, level_num)
            fires.update(platforms)
            
            # --- COIN COLLECTION (UPDATED) ---
            collected_by_p1 = pygame.sprite.spritecollide(player, coins, True)
            if collected_by_p1:
                p1_coins_collected += len(collected_by_p1) # Track count
                if GAME_SETTINGS["sound"] and SND_COIN: SND_COIN.play()
                score += 100 * len(collected_by_p1)

            if bot_player:
                collected_by_bot = pygame.sprite.spritecollide(bot_player, coins, True)
                if collected_by_bot:
                    bot_coins_collected += len(collected_by_bot) # Track bot count
                    if GAME_SETTINGS["sound"] and SND_COIN: SND_COIN.play()

            # Cage Opening Logic
            if len(coins) == 0:
                cage.active = False

            # Win Check
            target_hit = False
            if not cage.active:
                if player.rect.colliderect(target_rect):
                    if pauline: pauline.is_saved = True
                    target_hit = True; winner_text = "PLAYER 1 WINS!"

            if bot_player and not cage.active:
                if bot_player.rect.colliderect(target_rect):
                    if pauline: pauline.is_saved = True
                    target_hit = True; winner_text = "COMPUTER WINS!"

            if target_hit:
                game_state = "victory_anim"
                dk.start_death()
                win_timer = pygame.time.get_ticks()
                if not win_sound_played:
                    if GAME_SETTINGS["sound"] and SND_WIN: SND_WIN.play()
                    win_sound_played = True

            # Hazards
            for b in barrels:
                b.update(platforms)
                if player.rect.colliderect(b.rect): 
                    lives -= 1; b.kill(); player.rect.topleft = (50, 600)
                if bot_player and bot_player.rect.colliderect(b.rect): 
                    bot_player.lives -= 1; b.kill(); bot_player.rect.topleft = (150, 600)

            for f in fires:
                if player.rect.colliderect(f.rect): 
                    lives -= 1; f.kill(); player.rect.topleft = (50, 600)
                if bot_player and bot_player.rect.colliderect(f.rect):
                    bot_player.lives -= 1; f.kill(); bot_player.rect.topleft = (150, 600)

            if lives <= 0:
                 game_state = "game_over"
                 if GAME_SETTINGS["sound"] and SND_GAMEOVER: SND_GAMEOVER.play()

            if bot_player and bot_player.lives <= 0:
                winner_text = "PLAYER 1 WINS!"
                game_state = "victory_anim"
                dk.start_death()
                win_timer = pygame.time.get_ticks()

        elif game_state == "victory_anim":
            dk.update_death_anim()
            if pauline: pauline.update()
            if pygame.time.get_ticks() - win_timer > 2000:
                if mode == "vs_ai" and winner_text == "COMPUTER WINS!": return "menu", score, lives 
                if level_num == 4: return "game_beaten", score, lives, optimal_moves
                return "won", score, lives, optimal_moves

        elif game_state == "game_over":
            over_txt = TITLE_FONT.render("GAME OVER", True, RED)
            screen.blit(over_txt, (WIDTH//2 - over_txt.get_width()//2, HEIGHT//2))
            pygame.display.update(); await asyncio.sleep(3); return "menu", 0, 0

        # Draw
        for p in platforms: p.draw(screen)
        for l in ladders: screen.blit(l.image, l.rect)
        dk.draw(screen)
        if pauline: pauline.draw(screen)
        cage.draw(screen)
        for b in barrels: b.draw(screen)
        for f in fires: f.draw(screen)
        for c in coins: screen.blit(c.image, c.rect)
        player.draw(screen)
        if bot_player: bot_player.draw(screen)
        
        # --- NEW UI CALL ---
        # This replaces the old messy text blocks
        bot_lives = bot_player.lives if bot_player else 0
        draw_hud(screen, mode, lives, p1_coins_collected, score, bot_lives, bot_coins_collected)

        # Status Text for Cage (MOVED TO BOTTOM)
        if not cage.active and game_state == "playing":
             txt_open = HUD_FONT.render(f"CAGE OPEN! GO TO TOP!", True, GREEN_NEON)
             # Position set to Bottom Middle (HEIGHT - 80)
             screen.blit(txt_open, (WIDTH//2 - txt_open.get_width()//2, HEIGHT - 80))

        if winner_text and game_state == "victory_anim":
            txt_win = TITLE_FONT.render(winner_text, True, GREEN_NEON)
            screen.blit(txt_win, (WIDTH//2 - txt_win.get_width()//2, HEIGHT//2))

        pygame.display.update()


async def single_player_campaign():
    lvl = 1; score = 0; lives = 3
    while lvl <= 4:
        res = await run_level(lvl, score, lives, mode="singleplayer")
        if len(res) == 4: status, score, lives, opt = res
        else: status, score, lives = res; opt=0

        if status == "menu": return "menu"
        if status == "game_beaten": await game_beaten_screen(score, lives, opt); return "menu"
        if status == "won":
            action = await level_complete_screen(lvl, score, lives, opt)
            if action == "menu": return "menu"
            lvl += 1
    return "menu"

async def vs_ai_mode():
    res = await run_level(1, 0, 3, mode="vs_ai")
    return "menu"


async def run_2p_race_level(level_num):
    screen = pygame.display.get_surface()
    # 1. GENERATE MAP & ASSETS
    platforms, ladders = generate_random_level()
    all_sprites = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    barrels = pygame.sprite.Group()
    fires = pygame.sprite.Group()
    
    for p in platforms: all_sprites.add(p)
    for l in ladders: all_sprites.add(l)

    # 2. INITIALIZE PLAYERS
    # Player 1 (Mario Style)
    p1 = Player(50, 600, is_luigi=False)
    # Player 2 (Luigi Style)
    p2 = Player(150, 600, is_luigi=True)
    
    p1_lives = 3
    p2_lives = 3
    
    # Track collected coins separately
    p1_coins_collected = 0
    p2_coins_collected = 0

    # 3. SETUP BOSS & OBJECTIVE
    dk = DonkeyKong(WIDTH//2 - 45, 10)
    pauline = Pauline(dk.rect.x + 100, dk.rect.y + 10)
    
    # CAGE SETUP
    cage_rect = pygame.Rect(pauline.rect.x - 5, pauline.rect.y - 5, pauline.rect.width + 10, pauline.rect.height + 10)
    cage = Cage(cage_rect.x, cage_rect.y, cage_rect.width, cage_rect.height)
    
    # SPAWN COINS
    valid_platforms = [p for p in platforms if 150 < p.rect.y < 650]
    while len(coins) < 20:
        if not valid_platforms: break 
        target_plat = random.choice(valid_platforms)
        new_c = Coin(target_plat)
        if not pygame.sprite.spritecollideany(new_c, coins):
            coins.add(new_c); all_sprites.add(new_c)

    winner = None
    dk_vanished = False
    
    # --- GAME LOOP ---
    while True:
        clock.tick(FPS); await asyncio.sleep(0)
        screen.fill(BLACK)
        
        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: return "menu"

        if not winner:
            keys = pygame.key.get_pressed()
            
            # UPDATE PLAYERS
            if p1_lives > 0: p1.update(keys, platforms, ladders)
            if p2_lives > 0: p2.update(keys, platforms, ladders)
            
            pauline.update()
            fires.update(platforms)
            
            # UPDATE DK
            if not dk_vanished:
                if dk.is_dying:
                    dk.update_death_anim()
                    if not dk.alive(): dk_vanished = True
                else:
                    dk.update_ai(barrels, fires, level_num)
                    dk.draw(screen)

            # --- COIN COLLECTION (SEPARATE TRACKING) ---
            if p1_lives > 0:
                hit_list = pygame.sprite.spritecollide(p1, coins, True)
                for c in hit_list:
                    p1_coins_collected += 1
                    if GAME_SETTINGS["sound"] and SND_COIN: SND_COIN.play()
            
            if p2_lives > 0:
                hit_list = pygame.sprite.spritecollide(p2, coins, True)
                for c in hit_list:
                    p2_coins_collected += 1
                    if GAME_SETTINGS["sound"] and SND_COIN: SND_COIN.play()

            # --- UNLOCK CAGE ---
            # Cage opens when ALL coins on the map are gone
            if len(coins) == 0 and cage.active:
                cage.active = False
                dk.start_death()
                if GAME_SETTINGS["sound"] and SND_WIN: SND_WIN.play()

            # --- WIN CONDITION ---
            if not cage.active:
                if p1_lives > 0 and p1.rect.colliderect(pauline.rect): 
                    winner = "PLAYER 1 WINS!"
                elif p2_lives > 0 and p2.rect.colliderect(pauline.rect): 
                    winner = "PLAYER 2 WINS!"
                
                if winner and GAME_SETTINGS["sound"] and SND_WIN: SND_WIN.play()

            # --- HAZARDS ---
            for b in barrels:
                b.update(platforms)
                # Player 1 Hit
                if p1_lives > 0 and b.rect.colliderect(p1.rect): 
                    p1_lives -= 1; b.kill(); p1.rect.topleft = (50, 600)
                # Player 2 Hit
                if p2_lives > 0 and b.rect.colliderect(p2.rect): 
                    p2_lives -= 1; b.kill(); p2.rect.topleft = (150, 600)
            
            for f in fires:
                # Player 1 Hit
                if p1_lives > 0 and f.rect.colliderect(p1.rect): 
                    p1_lives -= 1; f.kill(); p1.rect.topleft = (50, 600)
                # Player 2 Hit
                if p2_lives > 0 and f.rect.colliderect(p2.rect): 
                    p2_lives -= 1; f.kill(); p2.rect.topleft = (150, 600)

            # --- BOUNDS CHECK (Fell off map) ---
            if p1.rect.top > HEIGHT: p1.rect.topleft = (50, 600); p1_lives -= 1
            if p2.rect.top > HEIGHT: p2.rect.topleft = (150, 600); p2_lives -= 1
            
            # --- DOUBLE GAME OVER CHECK ---
            if p1_lives <= 0 and p2_lives <= 0:
                 winner = "GAME OVER (DRAW)"

        # --- DRAWING ---
        for p in platforms: p.draw(screen)
        for l in ladders: screen.blit(l.image, l.rect)
        if not dk_vanished: dk.draw(screen)
        pauline.draw(screen)
        cage.draw(screen)
        for b in barrels: b.draw(screen)
        for f in fires: f.draw(screen)
        for c in coins: screen.blit(c.image, c.rect)
        
        # Draw Players (only if alive)
        if p1_lives > 0: p1.draw(screen)
        if p2_lives > 0: p2.draw(screen)
        
        # --- UI DRAWING CALL ---
        draw_hud(screen, "race_mode", p1_lives, p1_coins_collected, 0, p2_lives, p2_coins_collected)

        # Handle Win/Loss Screen Overlay
        if winner:
            txt = TITLE_FONT.render(winner, True, GREEN_NEON)
            screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2))
            pygame.display.update()
            await asyncio.sleep(3)
            return "menu"

        pygame.display.update()
