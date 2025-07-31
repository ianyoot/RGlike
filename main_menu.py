import pygame
import sys
import random
is_fullscreen = True
screen = None  # <-- Add this line

def main_menu(scr):
    global is_fullscreen, screen
    screen = scr  # always use the global screen
    # ...rest of your code...
    pygame.font.init()
    font = pygame.font.SysFont(None, 48)
    title_font = pygame.font.SysFont(None, 72)

    clock = pygame.time.Clock()
    screen_width, screen_height = screen.get_size()

    button_width, button_height = 250, 60
    spacing = 20  # 按鈕間距

    # 按鈕設定（會自動水平置中）
    buttons = [
        {
            "text": "Start",
            "rect": pygame.Rect(
                (screen_width - button_width) // 2,
                screen_height // 2 - button_height - spacing // 2,
                button_width,
                button_height
            )
        },
        {
            "text": "Leave",
            "rect": pygame.Rect(
                (screen_width - button_width) // 2,
                screen_height // 2 + spacing // 2,
                button_width,
                button_height
            )
        },
    ]

    # --- Animated shapes setup ---
    shapes = []
    shape_timer = 0
    player_falling = False

    def spawn_shape(kind=None):
        if kind is None:
            kind = random.choice(["enemy_melee", "enemy_ranged"])
        x = random.randint(0, screen_width - 40)
        y = -40
        if kind == "enemy_melee":
            color = (255, 0, 0)
            size = 40
            speed = random.uniform(1.2, 2.2)
        elif kind == "enemy_ranged":
            color = (255, 165, 0)
            size = 40
            speed = random.uniform(1.0, 1.8)
        else:  # player
            color = (0, 255, 255)
            size = 40
            speed = random.uniform(0.8, 1.2)
        angle = random.uniform(0, 360)
        rotate_speed = random.uniform(0.2, 0.7) * random.choice([-1, 1])
        shapes.append({
            "kind": kind, "x": x, "y": y, "color": color, "size": size,
            "speed": speed, "angle": angle, "rotate_speed": rotate_speed
        })

    while True:
        screen.fill((0, 0, 0))

        shape_timer += 1

        # Enemies fall frequently
        if shape_timer % 10 == 0:
            spawn_shape("enemy_melee" if random.random() < 0.5 else "enemy_ranged")

        # Only one player at a time, spawn rarely if none present
        if not any(s["kind"] == "player" for s in shapes):
            if random.randint(0, 240) == 0:  # ~once every 4 seconds at 60fps
                spawn_shape("player")

        # Animate and draw shapes
        for shape in shapes[:]:
            shape["y"] += shape["speed"]
            shape["angle"] += shape["rotate_speed"]
            # Draw rotated rect
            surf = pygame.Surface((shape["size"], shape["size"]), pygame.SRCALPHA)
            pygame.draw.rect(surf, shape["color"], (0, 0, shape["size"], shape["size"]))
            rotated = pygame.transform.rotate(surf, shape["angle"])
            rect = rotated.get_rect(center=(shape["x"] + shape["size"] // 2, int(shape["y"]) + shape["size"] // 2))
            screen.blit(rotated, rect.topleft)
            if shape["y"] > screen_height:
                shapes.remove(shape)

        # 畫標題（置中）
        title_surface = title_font.render("Fight till We Die", True, (255, 255, 255))
        screen.blit(
            title_surface,
            ((screen_width - title_surface.get_width()) // 2, 100)
        )

        # 畫按鈕
        mouse_pos = pygame.mouse.get_pos()
        for btn in buttons:
            color = (100, 100, 255) if btn["rect"].collidepoint(mouse_pos) else (100, 100, 100)
            pygame.draw.rect(screen, color, btn["rect"])

            text_surface = font.render(btn["text"], True, (255, 255, 255))
            screen.blit(
                text_surface,
                (
                    btn["rect"].x + (btn["rect"].width - text_surface.get_width()) // 2,
                    btn["rect"].y + (btn["rect"].height - text_surface.get_height()) // 2,
                )
            )

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    is_fullscreen = not is_fullscreen
                    if is_fullscreen:
                        screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((screen_width, screen_height))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0]["rect"].collidepoint(pygame.mouse.get_pos()):
                    return  # Start game
                elif buttons[1]["rect"].collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()