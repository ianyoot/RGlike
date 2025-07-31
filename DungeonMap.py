import numpy as np
import pygame

def generator(width=128, height=128):
    return np.random.choice([1, 2], size=(height, width), p=[0.45, 0.55])

def cellular_automata_step(map_data):
    new_map = np.copy(map_data)
    for y in range(1, map_data.shape[0] - 1):      # rows
        for x in range(1, map_data.shape[1] - 1):  # columns
            wall_count = np.sum(map_data[y - 1:y + 2, x - 1:x + 2] == 1)
            if wall_count > 4:
                new_map[y, x] = 1
            else:
                new_map[y, x] = 2
    return new_map

def flood_fill(map_data, y, x):
    if map_data[y, x] != 2:
        return
    visited = set()
    to_visit = [(y, x)]
    while to_visit:
        cy, cx = to_visit.pop()
        if (cy, cx) in visited:
            continue
        if not (0 <= cy < map_data.shape[0] and 0 <= cx < map_data.shape[1]):
            continue
        if map_data[cy, cx] == 2:
            visited.add((cy, cx))
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dy != 0 or dx != 0:
                        ny, nx = cy + dy, cx + dx
                        if (0 <= ny < map_data.shape[0] and 0 <= nx < map_data.shape[1]):
                            if (ny, nx) not in visited:
                                to_visit.append((ny, nx))

def draw_map(map_data, screen, offset_x=0, offset_y=0, tile_size=20):
    for y in range(map_data.shape[0]):
        for x in range(map_data.shape[1]):
            color = (100, 100, 100) if map_data[y, x] == 1 else (50, 50, 50)
            pygame.draw.rect(
                screen, color,
                pygame.Rect(x * tile_size + offset_x, y * tile_size + offset_y, tile_size, tile_size)
            )