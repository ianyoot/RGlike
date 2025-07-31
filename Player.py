import pygame
import math

class Player:
    def __init__(self, x, y, speed=5, tile_size=20):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = tile_size
        self.height = tile_size
        self.color = (0, 255, 255) 
        self.attack_damage = 10
        self.attack_range = 50
        self.hp = 100
        self.max_hp = 100

        # 藥水屬性
        self.potions = 3
        self.heal_amount = 30
        self.last_potion_time = 0
        self.potion_cooldown = 5000  # 毫秒

    def move(self, dx, dy, map_data, tile_size=20):
        new_x = self.x + dx
        new_y = self.y + dy
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
            # Use correct bounds and indexing
            if not (0 <= tile_x < map_data.shape[1] and 0 <= tile_y < map_data.shape[0]) or map_data[tile_y, tile_x] != 2:
                can_move = False
                break
        if can_move:
            self.x = new_x
            self.y = new_y
    def attack(self, enemies):
        for enemy in enemies:
            if abs(self.x - enemy.x) < 50 and abs(self.y - enemy.y) < 50:
                enemy.take_damage(self.attack_damage)

    def take_damage(self, amount):
        self.hp -= amount

    def draw(self, screen, offset_x=0, offset_y=0):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x + offset_x, self.y + offset_y, self.width, self.height))

    def draw_health_bar(self, surface, offset_x=0, offset_y=0):
        bar_width = self.width * 4  # Make the bar twice as long as the player
        bar_height = 10             # Make the bar taller
        x = self.x + offset_x - (bar_width - self.width) // 2  # Center above player
        y = self.y + offset_y - bar_height - 6  # 6 pixels above the player
        fill = int((self.hp / self.max_hp) * bar_width)
        # Draw background (red)
        pygame.draw.rect(surface, (255, 0, 0), (x, y, bar_width, bar_height))
        # Draw fill (green)
        pygame.draw.rect(surface, (0, 255, 0), (x, y, fill, bar_height))

    def shoot_arrow(self, target_x, target_y):
        start_x = self.x + self.width // 2
        start_y = self.y + self.height // 2
        dx = target_x - start_x
        dy = target_y - start_y
        dist = math.hypot(dx, dy)
        if dist < 1e-3:  # Allow very small distances
            dx, dy = 1, 0  # Default direction (right)
        else:
            dx /= dist
            dy /= dist
        return Arrow(start_x, start_y, dx, dy)

    def use_potion(self):
        current_time = pygame.time.get_ticks()
        if (
                self.hp < self.max_hp and
                self.potions > 0 and
                current_time - self.last_potion_time >= self.potion_cooldown
        ):
            self.hp += self.heal_amount
            self.hp = min(self.hp, self.max_hp)
            self.potions -= 1
            self.last_potion_time = current_time

class Arrow:
    def __init__(self, x, y, dx, dy, speed=10, damage=10):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = speed
        self.width = 5
        self.height = 5
        self.color = (0, 0, 255)
        self.damage = damage
        self.ricocheted = False  # Track if ricocheted

    def move(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

    def ricochet(self, hit_x, hit_y):
        if hit_x:
            self.dx *= -1
        if hit_y:
            self.dy *= -1
        self.ricocheted = True

    def draw(self, screen, offset_x=0, offset_y=0):
        pygame.draw.rect(
            screen, 
            self.color, 
            pygame.Rect(self.x + offset_x, self.y + offset_y, self.width, self.height))
    def collides_with(self, target):
        return pygame.Rect(self.x, self.y, self.width, self.height).colliderect(
            pygame.Rect(target.x, target.y, target.width, target.height))