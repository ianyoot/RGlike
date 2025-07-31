import random
import math
import pygame

class Enemy:
    def __init__(self, x, y, enemy_type="melee", tile_size=20):
        self.x = x
        self.y = y
        self.width = tile_size
        self.height = tile_size
        self.color = (255, 0, 0) if enemy_type == "melee" else (255, 165, 0)
        self.hp = 30 if enemy_type == "melee" else 20
        self.speed = 2 if enemy_type == "melee" else 1
        self.enemy_type = enemy_type
        self.attack_range = 40 if enemy_type == "melee" else 200
        self.attack_cooldown = 1000
        self.last_attack_time = 0

        # Wandering state
        self.state = "wandering"  # or "chasing"
        self.wander_dir = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
        self.wander_timer = random.randint(30, 90)  # frames

    def can_see_player(self, player, map_data, tile_size=20, vision_range=200):
        # Simple distance check (replace with line-of-sight for more realism)
        dx = (player.x + player.width // 2) - (self.x + self.width // 2)
        dy = (player.y + player.height // 2) - (self.y + self.height // 2)
        distance = math.hypot(dx, dy)
        if distance > vision_range:
            return False
        # Optionally, add line-of-sight check here
        return True
    def attack_player(self, player, bullets, current_time):
        # Calculate center positions for accurate targeting
        enemy_cx = self.x + self.width // 2
        enemy_cy = self.y + self.height // 2
        player_cx = player.x + player.width // 2
        player_cy = player.y + player.height // 2

        dx = player_cx - enemy_cx
        dy = player_cy - enemy_cy
        distance = math.hypot(dx, dy)

        if distance <= self.attack_range and current_time - self.last_attack_time >= self.attack_cooldown:
            self.last_attack_time = current_time
            if self.enemy_type == "melee":
                player.take_damage(10)
            else:
                if distance != 0:
                    dx /= distance
                    dy /= distance
                bullets.append(Bullet(enemy_cx, enemy_cy, dx, dy))
    def move_towards(self, player, map_data, tile_size=20):
        if self.state == "wandering":
            dx, dy = self.wander_dir
            new_x = self.x + dx * self.speed
            new_y = self.y + dy * self.speed
            corners = [
                (new_x, new_y),
                (new_x + self.width - 1, new_y),
                (new_x, new_y + self.height - 1),
                (new_x + self.width - 1, new_y + self.height - 1)
            ]
            can_move = True
            for cx, cy in corners:
                tile_x = int(cx) // tile_size
                tile_y = int(cy) // tile_size
                # FIXED: correct bounds and indexing!
                if not (0 <= tile_y < map_data.shape[0] and 0 <= tile_x < map_data.shape[1]) or map_data[tile_y, tile_x] != 2:
                    can_move = False
                    break
            if can_move:
                self.x = new_x
                self.y = new_y
            # Change direction occasionally
            self.wander_timer -= 1
            if self.wander_timer <= 0 or not can_move:
                self.wander_dir = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
                self.wander_timer = random.randint(30, 90)
        elif self.state == "chasing":
            # Move toward player
            dx = player.x - self.x
            dy = player.y - self.y
            dist = math.hypot(dx, dy)
            if dist > 0:
                dx /= dist
                dy /= dist
                new_x = self.x + dx * self.speed
                new_y = self.y + dy * self.speed
                corners = [
                    (new_x, new_y),
                    (new_x + self.width - 1, new_y),
                    (new_x, new_y + self.height - 1),
                    (new_x + self.width - 1, new_y + self.height - 1)
                ]
                can_move = True
                for cx, cy in corners:
                    tile_x = int(cx) // tile_size
                    tile_y = int(cy) // tile_size
                    # Correct bounds and indexing!
                    if not (0 <= tile_y < map_data.shape[0] and 0 <= tile_x < map_data.shape[1]) or map_data[tile_y, tile_x] != 2:
                        can_move = False
                        break
                if can_move:
                    self.x = new_x
                    self.y = new_y
    def draw(self, screen, offset_x=0, offset_y=0):
        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(self.x + offset_x, self.y + offset_y, self.width, self.height)
        )
    def take_damage(self, amount):
        self.hp -= amount
class Bullet:
    def __init__(self, x, y, dx, dy, speed=5, damage=10):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = speed
        self.width = 5
        self.height = 5
        self.color = (255, 255, 0)
        self.damage = damage

    def move(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

    def draw(self, screen, offset_x=0, offset_y=0):
        pygame.draw.rect(
            screen, 
            self.color, 
            pygame.Rect(self.x + offset_x, self.y + offset_y, self.width, self.height))



    def collides_with(self, target):
        return pygame.Rect(self.x, self.y, self.width, self.height).colliderect(
            pygame.Rect(target.x, target.y, target.width, target.height))
