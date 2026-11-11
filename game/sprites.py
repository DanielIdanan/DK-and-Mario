"""All game sprites: platforms, ladders, player, DK, barrels, fire, coins."""
import os, random
import pygame
from game.assets import SND_BARREL, SND_JUMP, load_sprite, palette_swap_luigi
from game.settings import BARREL_DIR, BLACK, COIN_IMG_PATH, CYAN, DK_DIR, FIRE_DIR, FLOOR_IMG_PATH, GAME_SETTINGS, HEART_IMG_PATH, HEIGHT, MARIO_DIR, ORANGE, PAULINE_DIR, PINK, PURPLE, RED, SILVER, WIDTH, YELLOW

# =============================================================
# CLASSES
# =============================================================

class Ladder(pygame.sprite.Sprite):
    def __init__(self, x, y, height):
        super().__init__()
        self.image = pygame.Surface((30, height))
        self.image.set_colorkey(BLACK) 
        self.rect = self.image.get_rect(topleft=(x, y))
        self.draw_ladder()

    def draw_ladder(self):
        pygame.draw.line(self.image, CYAN, (0, 0), (0, self.rect.height), 3)
        pygame.draw.line(self.image, CYAN, (28, 0), (28, self.rect.height), 3)
        for i in range(0, self.rect.height, 20):
            pygame.draw.line(self.image, CYAN, (0, i), (28, i), 2)

class Cage:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.active = True 

    def draw(self, surface):
        if self.active:
            pygame.draw.rect(surface, SILVER, self.rect, 5) 
            for i in range(self.rect.x + 10, self.rect.right, 15):
                pygame.draw.line(surface, SILVER, (i, self.rect.top), (i, self.rect.bottom), 3)
            pygame.draw.line(surface, SILVER, (self.rect.left, self.rect.centery), (self.rect.right, self.rect.centery), 3)

class Pauline(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = []
        for i in range(1, 5):
            p_path = os.path.join(PAULINE_DIR, f"pauline_{i}.png")
            self.frames.append(load_sprite(p_path, 40, 60, PINK))
        if not self.frames: 
            s = pygame.Surface((40,60)); s.fill(PINK); self.frames=[s]

        try: self.heart_img = load_sprite(HEART_IMG_PATH, 40, 40, RED)
        except: self.heart_img = pygame.Surface((40,40)); self.heart_img.fill(RED)

        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.frame_index = 0
        self.is_saved = False

    def update(self):
        if not self.is_saved:
            self.frame_index += 0.1
            if self.frame_index >= len(self.frames): self.frame_index = 0
            self.image = self.frames[int(self.frame_index)]

    def draw(self, surf):
        surf.blit(self.image, self.rect)
        if self.is_saved:
            h_rect = self.heart_img.get_rect(centerx=self.rect.centerx, bottom=self.rect.top - 10)
            surf.blit(self.heart_img, h_rect)

class Fire(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = []
        for i in range(1, 5):
            f_path = os.path.join(FIRE_DIR, f"fire_{i}.png")
            self.frames.append(load_sprite(f_path, 30, 30, RED))
        if not self.frames: s = pygame.Surface((30,30)); s.fill(RED); self.frames=[s]

        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.frame_index = 0
        self.vel_y = 0
        self.vel_x = random.choice([-3, 3])
        self.gravity = 0.4

    def update(self, platforms):
        self.frame_index += 0.2
        if self.frame_index >= len(self.frames): self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        
        self.vel_y += self.gravity
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        for plat in platforms:
            if self.rect.colliderect(plat.rect):
                if self.vel_y > 0:
                    self.rect.bottom = plat.rect.top
                    self.vel_y = -5 
        
        if self.rect.right > WIDTH: self.vel_x *= -1
        if self.rect.left < 0: self.vel_x *= -1
        if self.rect.y > 600: self.kill()
        if self.rect.top > HEIGHT: self.kill()

    def draw(self, surf):
        surf.blit(self.image, self.rect)

class Coin(pygame.sprite.Sprite):
    def __init__(self, target_plat):
        super().__init__()
        try: self.image = load_sprite(COIN_IMG_PATH, 30, 30, YELLOW)
        except: self.image = pygame.Surface((30,30)); self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = target_plat.rect.top - 5
        
        safe_left = target_plat.rect.left + 60
        safe_right = target_plat.rect.right - self.rect.width - 60
        if safe_right > safe_left:
            self.rect.x = random.randint(safe_left, safe_right)
        else:
            self.rect.centerx = target_plat.rect.centerx

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        try:
            tile_img = pygame.image.load(FLOOR_IMG_PATH).convert()
            tile_img.set_colorkey((255, 255, 255)) 
            tile_w = tile_img.get_width()
        except:
            tile_img = pygame.Surface((40, 40)); tile_img.fill(RED); tile_w = 40

        self.image = pygame.Surface((w, h))
        self.image.set_colorkey((0,0,0))
        for x_pos in range(0, w, tile_w):
            self.image.blit(tile_img, (x_pos, 0))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surf):
        surf.blit(self.image, self.rect)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, is_luigi=False, is_bot=False, lives=3):
        super().__init__()
        # --- AI FAILSAFE VARIABLES ---
        self.last_pos = (x, y)
        self.stuck_timer = 0
        
        self.is_luigi = is_luigi
        self.is_bot = is_bot
        self.lives = lives
        self.animations = { "idle_r": [], "idle_l": [], "run_r": [], "run_l": [], "jump_r": [], "jump_l": [], "dead_r": [], "dead_l": [], "climb": [] }
        
        def get_frame(name): 
            img = load_sprite(os.path.join(MARIO_DIR, name), 40, 40, (50, 100, 255))
            if self.is_luigi: img = palette_swap_luigi(img)
            return img

        self.animations["idle_r"] = [get_frame("idle_r.png")]
        self.animations["idle_l"] = [get_frame("idle_l.png")]
        self.animations["run_r"] = [get_frame("run_r.png"), get_frame("idle_r.png")]
        self.animations["run_l"] = [get_frame("run_l.png"), get_frame("idle_l.png")]
        self.animations["jump_r"] = [get_frame("jump_r.png")]
        self.animations["jump_l"] = [get_frame("jump_l.png")]
        self.animations["dead_r"] = [get_frame("dead_r.png")]
        self.animations["dead_l"] = [get_frame("dead_l.png")]
        self.animations["climb"] = [get_frame("climb_1.png"), get_frame("climb_2.png")]

        self.state = "idle_r"
        self.frame_index = 0
        self.anim_speed = 0.15
        self.facing_right = True
        self.image = self.animations["idle_r"][0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y = 0; self.speed = 5; self.jump_power = -16
        self.gravity = 0.8; self.on_ground = False; self.climbing = False
        self.pathfinder = None 

        self.last_x = x
        self.climb_direction = 0 

        if self.is_luigi:
            self.key_L = pygame.K_LEFT; self.key_R = pygame.K_RIGHT
            self.key_U = pygame.K_UP; self.key_D = pygame.K_DOWN
            self.key_J = pygame.K_RSHIFT
        else:
            self.key_L = pygame.K_a; self.key_R = pygame.K_d
            self.key_U = pygame.K_w; self.key_D = pygame.K_s
            self.key_J = pygame.K_SPACE

    def animate(self):
        key = self.state
        if self.climbing: key = "climb"
        elif "dead" not in key:
            action = key.split('_')[0] 
            key = f"{action}_{'r' if self.facing_right else 'l'}"
        if key not in self.animations: key = "idle_r"
        self.frame_index += self.anim_speed
        if self.frame_index >= len(frames := self.animations[key]): self.frame_index = 0
        self.image = frames[int(self.frame_index)]

    def update(self, keys, platforms, ladders, target_obj=None, coins_group=None):
        dx = 0; dy = 0; moving = False
        jump_pressed = False
        up_pressed = False
        down_pressed = False
        
        if self.is_bot and self.pathfinder:
            # --- AI BRAIN ---
            action, x_target = self.pathfinder.get_next_move_for_bot(self.rect, coins_group, target_obj, self.climbing, self.climb_direction)
            
            # --- FAILSAFE CHEAT: DETECT IF STUCK ---
            if abs(self.rect.x - self.last_pos[0]) < 2 and abs(self.rect.y - self.last_pos[1]) < 2:
                self.stuck_timer += 1
            else:
                self.stuck_timer = 0
                self.last_pos = self.rect.center

            if self.stuck_timer > 120:
                self.stuck_timer = 0
                if coins_group and len(coins_group) > 0:
                     # Cheat: Teleport to the nearest coin if stuck too long
                    target = coins_group.sprites()[0]
                    self.rect.center = target.rect.center
                else:
                    self.rect.y -= 100 

            if action == "run_to_goal" or action == "run_to_ladder":
                dist_x = x_target - self.rect.centerx
                # SNAP LOGIC
                if abs(dist_x) <= self.speed:
                    self.rect.centerx = x_target
                    dx = 0
                elif dist_x > 0: dx = self.speed; self.facing_right = True; moving = True
                elif dist_x < 0: dx = -self.speed; self.facing_right = False; moving = True
                
                # =================================================
                # SMART JUMP LOGIC (ENHANCED)
                # =================================================
                if moving and self.on_ground:
                    # 1. VERTICAL JUMP: Is the target physically above us?
                    if target_obj:
                         # If target is within horizontal range (100px) but significantly above
                        if abs(target_obj.centerx - self.rect.centerx) < 100 and target_obj.bottom < self.rect.top:
                            jump_pressed = True

                    # 2. EDGE JUMP (IMPOSSIBLE JUMPS): 
                    # Only jump at the very last moment.
                    # We check a very small distance ahead (velocity + 5px)
                    look_ahead = (self.speed + 5) if self.facing_right else -(self.speed + 5)
                    
                    feet_check_x = self.rect.centerx + look_ahead
                    feet_check_y = self.rect.bottom + 5
                    
                    has_floor = False
                    for p in platforms:
                        if p.rect.collidepoint(feet_check_x, feet_check_y): 
                            has_floor = True
                            break
                    
                    if not has_floor:
                        jump_pressed = True

            elif action == "climb_up":
                self.rect.centerx = x_target 
                up_pressed = True; self.climb_direction = -1

            elif action == "climb_down":
                self.rect.centerx = x_target
                down_pressed = True; self.climb_direction = 1

        else:
            # --- HUMAN INPUT ---
            if keys[self.key_L]: dx = -self.speed; self.facing_right = False; moving = True
            if keys[self.key_R]: dx = self.speed; self.facing_right = True; moving = True
            if not self.climbing:
                if keys[self.key_J]: jump_pressed = True
            if keys[self.key_U]: up_pressed = True
            if keys[self.key_D]: down_pressed = True

        # CLIMBING LOGIC
        on_ladder_now = False
        hit_ladders = pygame.sprite.spritecollide(self, ladders, False)
        
        if not hit_ladders and down_pressed and not self.climbing:
            for l in ladders:
                if l.rect.collidepoint(self.rect.centerx, self.rect.bottom + 5):
                      hit_ladders = [l]; break

        if hit_ladders:
            ladder = hit_ladders[0]
            ladder_center = ladder.rect.centerx
            
            if up_pressed:
                if not self.climbing:
                    if abs(self.rect.centerx - ladder_center) < 20:
                        self.rect.centerx = ladder_center; self.climbing = True; on_ladder_now = True; dy = -3
                else: self.climbing = True; on_ladder_now = True; dy = -3
                    
            elif down_pressed:
                if not self.climbing:
                      if abs(self.rect.centerx - ladder_center) < 20:
                        self.rect.centerx = ladder_center; self.climbing = True; on_ladder_now = True; dy = 3
                else: self.climbing = True; on_ladder_now = True; dy = 3
            elif self.climbing:
                on_ladder_now = True; dy = 0

        if not on_ladder_now: 
            self.climbing = False; self.climb_direction = 0

        if self.climbing: self.state = "climb"
        elif not self.on_ground: self.state = "jump"
        elif moving: self.state = "run"
        else: self.state = "idle"

        self.animate()
        
        self.rect.x += dx
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > WIDTH: self.rect.right = WIDTH
        
        if not self.climbing:
            for plat in platforms:
                 if self.rect.colliderect(plat.rect):
                    if dx > 0 and self.rect.right - dx <= plat.rect.left + 5: self.rect.right = plat.rect.left
                    elif dx < 0 and self.rect.left - dx >= plat.rect.right - 5: self.rect.left = plat.rect.right

        if not self.climbing: self.vel_y += self.gravity; dy += self.vel_y
        else: self.vel_y = 0

        self.rect.y += dy
        self.on_ground = False 
        
        if not self.climbing:
            for plat in platforms:
                if self.rect.colliderect(plat.rect):
                    if dy > 0: self.rect.bottom = plat.rect.top; self.vel_y = 0; self.on_ground = True
                    elif dy < 0: self.rect.top = plat.rect.bottom; self.vel_y = 0

        if jump_pressed and self.on_ground and not self.climbing:
            self.vel_y = self.jump_power
            if GAME_SETTINGS["sound"] and SND_JUMP: SND_JUMP.play()

    def draw(self, surf):
        visual_rect = self.rect.copy()
        visual_rect.y += 5
        surf.blit(self.image, visual_rect)


class Barrel(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = []
        for i in range(1, 5):
            path = os.path.join(BARREL_DIR, f"roll_{i}.png")
            self.frames.append(load_sprite(path, 30, 30, ORANGE))
        if not self.frames: 
            # Fallback if images are missing
            s = pygame.Surface((30,30))
            s.fill(ORANGE)
            self.frames = [s]

        self.frame_index = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y = 0; self.vel_x = 0; self.gravity = 0.5; self.dragging = False
        self.scored = False 

    def update(self, platforms):
        self.frame_index += 0.2
        if self.frame_index >= len(self.frames): self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

        if self.dragging:
            mx, my = pygame.mouse.get_pos()
            self.rect.center = (mx, my)
            self.vel_y = 0 
        else:
            self.vel_y += self.gravity
            self.rect.x += self.vel_x 
            self.rect.y += self.vel_y
            
            for plat in platforms:
                if self.rect.colliderect(plat.rect):
                    if self.vel_y > 0: 
                        self.rect.bottom = plat.rect.top
                        self.vel_y = 0

            if self.rect.y > 600:
                 if self.rect.right < 0 or self.rect.left > WIDTH: self.kill()
            else:
                if self.rect.right > WIDTH: self.rect.right = WIDTH; self.vel_x *= -1 
                elif self.rect.left < 0: self.rect.left = 0; self.vel_x *= -1 

            if self.rect.top > HEIGHT: self.kill()

    def draw(self, surf):
        surf.blit(self.image, self.rect)

class DonkeyKong(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprites = {}
        states = ["idle", "hold", "beat_l", "beat_r", "roll_l", "roll_r"]
        for s in states:
            self.sprites[s] = load_sprite(os.path.join(DK_DIR, f"{s}.png"), 90, 90, PURPLE)
        
        self.death_anim = []
        for i in range(1, 6):
            self.death_anim.append(load_sprite(os.path.join(DK_DIR, f"dead_{i}.png"), 90, 90, PURPLE))

        self.state = "idle"
        self.image = self.sprites["idle"]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 8; self.facing_right = False
        self.barrels_thrown = 0; self.last_throw_dir = -1
        self.is_dying = False; self.death_frame = 0; self.death_timer = 0
        self.last_fire_time = 0

    def start_death(self):
        if not self.is_dying:
            self.is_dying = True; self.death_frame = 0; self.death_timer = pygame.time.get_ticks()

    def update_ai(self, barrels_group, fires_group, current_level):
        if self.is_dying: return # Stop attacking if dying
        
        curr_time = pygame.time.get_ticks()
        loop_time = (curr_time / 1000) % 15 
        
        if 3 <= loop_time < 7:
            beat_phase = (curr_time // 500) % 2
            self.image = self.sprites["beat_l"] if beat_phase == 0 else self.sprites["beat_r"]
            if current_level == 4:
                if curr_time - self.last_fire_time > 800:
                    f = Fire(self.rect.centerx, self.rect.bottom)
                    fires_group.add(f)
                    self.last_fire_time = curr_time
        elif 0 <= loop_time < 3:
            self.image = self.sprites["idle"]
            self.barrels_thrown = 0
        elif 7 <= loop_time < 9:
            self.image = self.sprites["hold"]
        elif 9 <= loop_time < 15:
            throw_slot = int((loop_time - 9) / 2) 
            if self.barrels_thrown <= throw_slot:
                self.barrels_thrown += 1
                throw_dir = random.choice([-1, 1])
                self.last_throw_dir = throw_dir
                new_barrel = Barrel(self.rect.centerx, self.rect.bottom - 35)
                new_barrel.vel_x = throw_dir * 4 
                barrels_group.add(new_barrel)
                if GAME_SETTINGS["sound"] and SND_BARREL: SND_BARREL.play()
            
            if self.last_throw_dir == 1: self.image = self.sprites["roll_r"]
            else: self.image = self.sprites["roll_l"]

    def update(self, keys): 
        if keys[pygame.K_LEFT]: self.rect.x -= self.speed; self.facing_right = False
        if keys[pygame.K_RIGHT]: self.rect.x += self.speed; self.facing_right = True
        self.image = self.sprites["roll_r"] if self.facing_right else self.sprites["roll_l"]

    def update_death_anim(self):
        # Handles playing the animation then deleting the sprite
        curr_time = pygame.time.get_ticks()
        if curr_time - self.death_timer > 150:
            self.death_frame += 1
            self.death_timer = curr_time
        
        if self.death_frame < len(self.death_anim):
            self.image = self.death_anim[self.death_frame]
        else:
            self.kill() # VANISH LOGIC: Removes DK from all groups

    def draw(self, surf):
        # Only draw if he hasn't vanished (alive or mid-animation)
        if not self.is_dying or (self.is_dying and self.death_frame < len(self.death_anim)):
             surf.blit(self.image, self.rect)
