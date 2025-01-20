import pygame
import random

class Enemy:
    def __init__(self, window, game_map, enemy_type=1):
        self.window = window
        self.game_map = game_map
        self.cell_size = 60
        self.enemy_type = enemy_type
        
        # nastavenie vlastností podľa typu nepriateľa
        if enemy_type == 1:  # základný orb
            self.image = pygame.image.load("sprites/enemies/orb_1.png")
            self.max_health = 100
            self.speed = 2
        elif enemy_type == 2:  # rýchly orb
            self.image = pygame.image.load("sprites/enemies/orb_2_speed.png")
            self.max_health = 100  # rovnaké HP ako základný orb
            self.speed = 2  # rovnaká základná rýchlosť
            self.is_speed_orb = True  # príznak pre rýchly orb
        elif enemy_type == 3:  # odolný orb
            self.image = pygame.image.load("sprites/enemies/orb_3_tough.png")
            self.max_health = 400
            self.speed = 1.5
        elif enemy_type == 4:  # boss
            self.image = pygame.image.load("sprites/enemies/orb_4_boss.png")
            self.max_health = 1000
            self.speed = 2.5
        
        # transformácia obrázku podľa typu
        size_multiplier = 1.5 if enemy_type == 4 else 1
        self.image = pygame.transform.scale(self.image, 
            (int(self.cell_size//2 * size_multiplier), 
             int(self.cell_size//2 * size_multiplier)))
        
        self.health = self.max_health
        
        # nájdenie štartovacej pozície (hodnota 2 v mape)
        for y, row in enumerate(game_map.map_1):
            for x, value in enumerate(row):
                if value == 2:
                    self.x = x * self.cell_size + self.cell_size // 4
                    self.y = y * self.cell_size + self.cell_size // 4
                    self.last_move = (0, 1)  # počiatočný smer pohybu (dole)
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
        
        # špeciálna logika pre modré orby
        if hasattr(self, 'is_speed_orb'):
            # ak sme v strede bunky, hľadáme nový smer
            if (abs(self.x - cell_center_x) < 2 and abs(self.y - cell_center_y) < 2):
                self.x = cell_center_x
                self.y = cell_center_y
                
                # kontrola možných smerov pohybu
                directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                for dx, dy in directions:
                    next_x = grid_x + dx
                    next_y = grid_y + dy
                    if (0 <= next_x < len(self.game_map.map_1[0]) and 
                        0 <= next_y < len(self.game_map.map_1)):
                        next_value = self.game_map.map_1[next_y][next_x]
                        if next_value in [1, 4] and (dx, dy) != (-self.last_move[0], -self.last_move[1]) if self.last_move else True:
                            self.last_move = (dx, dy)
                            break
            
            # pohyb k ďalšiemu stredu bunky
            if self.last_move:
                self.x += self.last_move[0] * self.speed * 1.4
                self.y += self.last_move[1] * self.speed * 1.4
        else:
            # pôvodná logika pre ostatné orby
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
                            self.last_move = (dx, dy)
                            break
            
            if self.last_move:
                self.x += self.last_move[0] * self.speed
                self.y += self.last_move[1] * self.speed
            
        # kontrola či nepriateľ neopustil mapu
        if self.x < -self.cell_size or self.x > self.game_map.window_width or \
           self.y < -self.cell_size or self.y > self.game_map.window_height:
            self.alive = False

    def draw(self):
        if self.alive:
            self.window.blit(self.image, (self.x, self.y))
            self.draw_health_bar()
            self.move()
