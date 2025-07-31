import pygame
import random
import numpy as np
from DungeonMap import generator, cellular_automata_step, flood_fill, draw_map
from Player import Player, Arrow
from Enemy import Enemy, Bullet
import math
from main_menu import main_menu
class PowerUp:
    def __init__(self, x, y, kind):
        self.x = x
        self.y = y
        self.width = tile_size // 2
        self.height = tile_size // 2
        self.kind = kind
        self.color = {
            "bounce": (0, 255, 255),
            "speed": (0, 255, 0),
            "range": (255, 255, 0)
        }[kind]

    def draw(self, surface, offset_x=0, offset_y=0):
        pygame.draw.rect(
            surface, self.color,
            pygame.Rect(self.x + offset_x, self.y + offset_y, self.width, self.height)
        )
class Particle:
    def __init__(self, x, y, color, lifetime=30):
        self.x = x
        self.y = y
        self.dx = random.uniform(-3, 3)
        self.dy = random.uniform(-3, 3)
        self.color = color
        self.lifetime = lifetime
        self.age = 0

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.dy += 0.1  # gravity effect
        self.age += 1

    def draw(self, surface, offset_x=0, offset_y=0):
        if self.age < self.lifetime:
            pygame.draw.circle(surface, self.color, (int(self.x + offset_x), int(self.y + offset_y)), 3)
# 遊戲設定
map_width, map_height = 128, 128
tile_size = 20
screen_width, screen_height = map_width * tile_size, map_height * tile_size

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('Fight till We Die')
clock = pygame.time.Clock()
CAMERA_WIDTH, CAMERA_HEIGHT = 1280, 720
camera_surface = pygame.Surface((CAMERA_WIDTH, CAMERA_HEIGHT))
pygame.font.init()
font = pygame.font.SysFont(None, 28)

def spawn_enemy():
    global enemy_spawned_count
    if enemy_spawned_count >= enemy_spawn_limit:
        return
    cam_left = int(cam_x // tile_size)
    cam_top = int(cam_y // tile_size)
    cam_right = int((cam_x + CAMERA_WIDTH) // tile_size)
    cam_bottom = int((cam_y + CAMERA_HEIGHT) // tile_size)
    for _ in range(100):
        edge = random.choice(['top', 'bottom', 'left', 'right'])
        if edge == 'top':
            sy = random.randint(0, max(0, cam_top - 1))
            sx = random.randint(0, map_width - 1)
        elif edge == 'bottom':
            sy = random.randint(min(map_height - 1, cam_bottom + 1), map_height - 1)
            sx = random.randint(0, map_width - 1)
        elif edge == 'left':
            sx = random.randint(0, max(0, cam_left - 1))
            sy = random.randint(0, map_height - 1)
        else:
            sx = random.randint(min(map_width - 1, cam_right + 1), map_width - 1)
            sy = random.randint(0, map_height - 1)
        if 0 <= sx < map_width and 0 <= sy < map_height and map_data[sy, sx] == 2:
            enemy_type = random.choice(["melee", "ranged"])
            enemies.append(Enemy(sx * tile_size, sy * tile_size, enemy_type, tile_size=tile_size))
            enemy_spawned_count += 1
            break

def run_game():
    
    global screen, is_fullscreen, CAMERA_WIDTH, CAMERA_HEIGHT, camera_surface
    # ...rest of your code...
    # ...rest of your code...
    # ...rest of your code...
    particles = []
    global map_data, player, enemies, bullets, arrows, enemy_kill_count, max_enemies, enemy_spawn_limit, enemy_spawned_count, exit_tile, current_level, cam_x, cam_y

    current_level = 1
    max_levels = 3
    map_data = generator()
    for _ in range(5):
        map_data = cellular_automata_step(map_data)
    flood_fill(map_data, random.randint(0, map_width - 1), random.randint(0, map_height - 1))

    while True:
        px = random.randint(0, map_width - 1)
        py = random.randint(0, map_height - 1)
        if map_data[py, px] == 2:
            break
    player = Player(px * tile_size, py * tile_size, tile_size=tile_size)
    enemies, bullets, arrows = [], [], []
    enemy_kill_count = 0
    max_enemies = 30 + enemy_kill_count//5
    enemy_spawn_limit = max_enemies
    enemy_spawned_count = 0
    exit_tile = None
    powerups = []
    for _ in range(20):  # spawn 20 powerups
        while True:
            px = random.randint(0, map_width - 1)
            py = random.randint(0, map_height - 1)
            if map_data[py, px] == 2:
                kind = random.choice(["bounce", "speed", "range"])
                powerups.append(PowerUp(px * tile_size + tile_size//4, py * tile_size + tile_size//4, kind))
                break
    running = True
    while running:
        draw_map(map_data, camera_surface)
        player.draw(camera_surface)
        player.draw_health_bar(camera_surface)
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    player.attack(enemies)
                elif event.button == 3:  
                    mx, my = pygame.mouse.get_pos()
                    center_x = (WINDOW_WIDTH - CAMERA_WIDTH) // 2
                    center_y = (WINDOW_HEIGHT - CAMERA_HEIGHT) // 2
                    mx_world = mx - center_x + cam_x
                    my_world = my - center_y + cam_y
                    arrow = player.shoot_arrow(mx_world, my_world)
                    if arrow:
                        arrows.append(arrow)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    is_fullscreen = not is_fullscreen
                    if is_fullscreen:
                        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                    CAMERA_WIDTH, CAMERA_HEIGHT = WINDOW_WIDTH, WINDOW_HEIGHT
                    camera_surface = pygame.Surface((CAMERA_WIDTH, CAMERA_HEIGHT))
                    # Update center_x and center_y after resizing
                    center_x = (WINDOW_WIDTH - CAMERA_WIDTH) // 2
                    center_y = (WINDOW_HEIGHT - CAMERA_HEIGHT) // 2
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_a]: dx = -player.speed
        if keys[pygame.K_d]: dx = player.speed
        if keys[pygame.K_w]: dy = -player.speed
        if keys[pygame.K_s]: dy = player.speed
        if keys[pygame.K_x]: player.use_potion()
        
        player.move(dx, dy, map_data, tile_size=tile_size)
        for powerup in powerups[:]:
            powerup_rect = pygame.Rect(powerup.x, powerup.y, powerup.width, powerup.height)
            player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
            if player_rect.colliderect(powerup_rect):
                if powerup.kind == "bounce":
                    player.extra_bounce = getattr(player, "extra_bounce", 0) + 1
                elif powerup.kind == "speed":
                    player.speed += 2
                elif powerup.kind == "range":
                    player.attack_range += 20
                powerups.remove(powerup)
        if len(enemies) < max_enemies and random.random() < 0.08:
            spawn_enemy()
        # If your camera_surface depends on screen size, recreate it:
        CAMERA_WIDTH, CAMERA_HEIGHT = WINDOW_WIDTH, WINDOW_HEIGHT
        camera_surface = pygame.Surface((CAMERA_WIDTH, CAMERA_HEIGHT))
            # ...existing event handling...
        for enemy in enemies:
            if enemy.can_see_player(player, map_data, tile_size=tile_size, vision_range=200):
                enemy.state = "chasing"
            else:
                enemy.state = "wandering"
            enemy.move_towards(player, map_data, tile_size=tile_size)
            enemy.attack_player(player, bullets, current_time)
        
        for bullet in bullets[:]:
            bullet.move()
            bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)
            tile_x = int(bullet.x) // tile_size
            tile_y = int(bullet.y) // tile_size
            if not (0 <= tile_x < map_width and 0 <= tile_y < map_height) or map_data[tile_y, tile_x] == 1:
                bullets.remove(bullet)
            elif bullet_rect.colliderect(pygame.Rect(player.x, player.y, player.width, player.height)):
                player.take_damage(bullet.damage)
                bullets.remove(bullet)

        for arrow in arrows[:]:
            arrow.move()
            arrow_rect = pygame.Rect(arrow.x, arrow.y, arrow.width, arrow.height)
            tile_x = int(arrow.x) // tile_size
            tile_y = int(arrow.y) // tile_size

            out_x = not (0 <= tile_x < map_width)
            out_y = not (0 <= tile_y < map_height)

            hit_x = False
            hit_y = False

            if out_x or (0 <= tile_y < map_height and map_data[tile_y, tile_x] == 1 and abs(arrow.dx) > abs(arrow.dy)):
                hit_x = True
            if out_y or (0 <= tile_x < map_width and map_data[tile_y, tile_x] == 1 and abs(arrow.dy) >= abs(arrow.dx)):
                hit_y = True

            if hit_x or hit_y:
                if not arrow.ricocheted:
                    arrow.ricochet(hit_x, hit_y)
                    continue
                else:
                    arrows.remove(arrow)
                    continue

            for enemy in enemies:
                enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                if arrow_rect.colliderect(enemy_rect):
                    enemy.take_damage(arrow.damage)
                    arrows.remove(arrow)
                    break
        dead_enemies = []
        for enemy in enemies:
            if enemy.hp <= 0:
                # Spawn particles for enemy death (smaller, orange color)
                for _ in range(15):  # fewer particles than player
                    particles.append(Particle(
                        enemy.x + enemy.width // 2,
                        enemy.y + enemy.height // 2,
                        (255, 128, 0),  # orange color for enemies
                        lifetime=20     # shorter lifetime
                    ))
                dead_enemies.append(enemy)
        for enemy in dead_enemies:
            enemies.remove(enemy)
        # Count kills
        enemy_kill_count += enemy_spawned_count - len(enemies)
        enemy_spawned_count = len(enemies)> 0

        # 敵人清除完畢後開啟出口
        if not enemies and enemy_spawned_count >= enemy_spawn_limit and not exit_tile:
            for _ in range(100):
                x = random.randint(0, map_width - 1)
                y = random.randint(0, map_height - 1)
                if map_data[x, y] == 2:
                    exit_tile = (x, y)
                    break

        if exit_tile:
            exit_rect = pygame.Rect(exit_tile[0] * tile_size, exit_tile[1] * tile_size, tile_size, tile_size)
            if pygame.Rect(player.x, player.y, player.width, player.height).colliderect(exit_rect):
                if current_level < max_levels:
                    current_level += 1
                    map_data = generator()
                    for _ in range(5):
                        map_data = cellular_automata_step(map_data)
                    flood_fill(map_data, random.randint(0, map_width - 1), random.randint(0, map_height - 1))
                    player.x, player.y = screen_width // 2, screen_height // 2
                    enemies.clear()
                    bullets.clear()
                    arrows.clear()
                    enemy_spawned_count = 0
                    exit_tile = None
                else:
                    print("通關成功！")
                    running = False

        if player.hp <= 0:
            # Spawn particles for player death (larger, cyan color)
            for _ in range(60):
                particles.append(Particle(
                    player.x + player.width // 2,
                    player.y + player.height // 2,
                    (0, 255, 255),  # cyan color for player
                    lifetime=30     # longer lifetime
                ))
            death_animation_time = pygame.time.get_ticks()
            while pygame.time.get_ticks() - death_animation_time < 1200:  # 1.2 seconds
                camera_surface.fill((0, 0, 0))
                draw_map(map_data, camera_surface, offset_x=-cam_x, offset_y=-cam_y, tile_size=tile_size)
                for p in particles:
                    p.update()
                    p.draw(camera_surface, offset_x=-cam_x, offset_y=-cam_y)
                screen.fill((0, 0, 0))
                center_x = (WINDOW_WIDTH - CAMERA_WIDTH) // 2
                center_y = (WINDOW_HEIGHT - CAMERA_HEIGHT) // 2
                screen.blit(camera_surface, (center_x, center_y))
                pygame.display.flip()
                clock.tick(60)
            print("你死了！")
            main_menu(screen)
            run_game()
            return

        cam_x = int(player.x + player.width // 2 - CAMERA_WIDTH // 2)
        cam_y = int(player.y + player.height // 2 - CAMERA_HEIGHT // 2)
        cam_x = max(0, min(cam_x, screen_width - CAMERA_WIDTH))
        cam_y = max(0, min(cam_y, screen_height - CAMERA_HEIGHT))
        camera_surface.fill((0, 0, 0))
        draw_map(map_data, camera_surface, offset_x=-cam_x, offset_y=-cam_y, tile_size=tile_size)

        if exit_tile:
            pygame.draw.rect(
                camera_surface, (0, 255, 255),
                pygame.Rect(exit_tile[0]*tile_size - cam_x, exit_tile[1]*tile_size - cam_y, tile_size, tile_size)
            )
        
        for p in particles[:]:
            p.update()
            p.draw(camera_surface, offset_x=-cam_x, offset_y=-cam_y)
            if p.age >= p.lifetime:
                particles.remove(p)

        player.draw(camera_surface,offset_x=-cam_x,offset_y=-cam_y )
        player.draw_health_bar(camera_surface, offset_x=-cam_x, offset_y=-cam_y)
        for enemy in enemies:
            enemy.draw(camera_surface, offset_x=-cam_x, offset_y=-cam_y)
        for bullet in bullets:
            bullet.draw(camera_surface, offset_x=-cam_x, offset_y=-cam_y)
        for arrow in arrows:
            arrow.draw(camera_surface, offset_x=-cam_x, offset_y=-cam_y)
        for powerup in powerups:
            powerup.draw(camera_surface, offset_x=-cam_x, offset_y=-cam_y)
        screen.fill((0, 0, 0))
        center_x = (WINDOW_WIDTH - CAMERA_WIDTH) // 2
        center_y = (WINDOW_HEIGHT - CAMERA_HEIGHT) // 2
        screen.blit(camera_surface, (center_x, center_y))

        potion_text = font.render(f"potion: {player.potions}", True, (255, 255, 255))
        center_x = (WINDOW_WIDTH - CAMERA_WIDTH) // 2
        center_y = (WINDOW_HEIGHT - CAMERA_HEIGHT) // 2
        screen.blit(potion_text, (center_x + 10, center_y + CAMERA_HEIGHT - 60))

        cooldown_left = max(0, (player.potion_cooldown - (current_time - player.last_potion_time)) // 1000)
        if cooldown_left > 0:
            cooldown_text = font.render(f"charging: {cooldown_left}s", True, (255, 100, 100))
            center_x = (WINDOW_WIDTH - CAMERA_WIDTH) // 2
            center_y = (WINDOW_HEIGHT - CAMERA_HEIGHT) // 2
            screen.blit(cooldown_text, (center_x + 10, center_y + CAMERA_HEIGHT - 30))

        pygame.display.flip()
        clock.tick(60)

main_menu(screen)
run_game()