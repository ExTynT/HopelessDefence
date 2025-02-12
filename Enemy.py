import pygame
import random

class Enemy:
    def __init__(self, window, game_map, enemy_type=1, hp_multiplier=1):
        self.window = window
        self.game_map = game_map
        self.cell_size = 60
        self.enemy_type = enemy_type
        
        # základné vlastnosti
        self.max_health = 100 * hp_multiplier  # základné HP pre všetky typy
        self.health = self.max_health
        self.speed = 2  # základná rýchlosť
        self.base_speed = self.speed  # uloženie základnej rýchlosti pre efekty spomalenia
        self.reward = 15  # základná odmena
        
        # nájdenie štartovacej pozície (hodnota 2 v mape)
        for y, row in enumerate(game_map.map_1):
            for x, value in enumerate(row):
                if value == 2:
                    self.x = x * self.cell_size + self.cell_size // 4
                    self.y = y * self.cell_size + self.cell_size // 4
                    # Počiatočný smer pohybu - pre bossa doprava, pre ostatných dole
                    self.last_move = (1, 0) if enemy_type == 4 else (0, 1)
                    break
        
        self.alive = True

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = False

    def draw_health_bar(self):
        bar_width = self.cell_size // 2
        bar_height = 5
        health_width = (self.health / self.max_health) * bar_width
        
        # pozadie health baru (červené)
        pygame.draw.rect(self.window, (255,0,0), 
                        (self.x, self.y - 10, bar_width, bar_height))
        # health bar (zelený)
        pygame.draw.rect(self.window, (0,255,0), 
                        (self.x, self.y - 10, health_width, bar_height))

    def move(self):
        # výpočet aktuálnej pozície v mriežke
        grid_x = int(self.x // self.cell_size)
        grid_y = int(self.y // self.cell_size)
        
        # výpočet stredu bunky
        cell_center_x = grid_x * self.cell_size + self.cell_size // 4
        cell_center_y = grid_y * self.cell_size + self.cell_size // 4
        
        # pohyb k ďalšiemu stredu bunky
        if (abs(self.x - cell_center_x) < self.speed and 
            abs(self.y - cell_center_y) < self.speed):
            
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for dx, dy in directions:
                next_x = grid_x + dx
                next_y = grid_y + dy
                if (0 <= next_x < len(self.game_map.map_1[0]) and 
                    0 <= next_y < len(self.game_map.map_1)):
                    next_value = self.game_map.map_1[next_y][next_x]
                    if next_value in [1, 4] and (dx, dy) != (-self.last_move[0], -self.last_move[1]) if self.last_move else True:
                        # Ak sa mení smer, aktualizujeme last_direction
                        if hasattr(self, 'last_direction'):
                            if dx < 0:
                                self.last_direction = "left"
                            elif dx > 0:
                                self.last_direction = "right"
                            elif dy < 0:
                                self.last_direction = "up"
                            elif dy > 0:
                                self.last_direction = "down"
                        self.last_move = (dx, dy)
                        break
        
        if self.last_move:
            self.x += self.last_move[0] * self.speed
            self.y += self.last_move[1] * self.speed
            
        # kontrola či nepriateľ neopustil mapu
        if 0 <= grid_x < len(self.game_map.map_1[0]) and 0 <= grid_y < len(self.game_map.map_1):
            # ak je na políčku s hodnotou 4 (koniec cesty), označíme ho ako mŕtveho
            if self.game_map.map_1[grid_y][grid_x] == 4:
                self.alive = False
        else:
            # ak je mimo mapy, tiež ho označíme ako mŕtveho
            self.alive = False

    def draw(self):
        if self.alive:
            self.window.blit(self.image, (self.x, self.y))
            self.draw_health_bar()
            self.move()

    def update_path(self):
        # nájdenie štartovacej pozície (hodnota 2 v mape)
        for y, row in enumerate(self.game_map.map_1):
            for x, value in enumerate(row):
                if value == 2:
                    self.x = x * self.cell_size + self.cell_size // 4
                    self.y = y * self.cell_size + self.cell_size // 4
                    # Počiatočný smer pohybu - pre bossa doprava, pre ostatných dole
                    self.last_move = (1, 0) if self.enemy_type == 4 else (0, 1)
                    break
