import pygame

class Enemy:
    def __init__(self, window, game_map):
        self.window = window
        self.game_map = game_map
        self.cell_size = 60
        
        # načítanie a transformácia obrázku nepriateľa
        self.image = pygame.image.load("sprites/enemies/orb_1.png")
        self.image = pygame.transform.scale(self.image, (self.cell_size // 2, self.cell_size // 2))
        
        # systém životov
        self.max_health = 100
        self.health = self.max_health
        
        # nájdenie štartovacej pozície (hodnota 2 v mape)
        for y, row in enumerate(game_map.map_1):
            for x, value in enumerate(row):
                if value == 2:
                    self.x = x * self.cell_size + self.cell_size // 4
                    self.y = y * self.cell_size + self.cell_size // 4
                    self.last_move = (0, 1)  # počiatočný smer pohybu (dole)
                    break
        
        self.speed = 2
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
        
        # kontrola či sme blízko stredu bunky pre zmenu smeru
        if (abs(self.x - cell_center_x) < self.speed and 
            abs(self.y - cell_center_y) < self.speed):
            
            # kontrola možných smerov pohybu
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # dole, hore, vpravo, vľavo
            for dx, dy in directions:
                next_x = grid_x + dx
                next_y = grid_y + dy
                
                # kontrola či je ďalšia pozícia v rámci mapy
                if (0 <= next_x < len(self.game_map.map_1[0]) and 
                    0 <= next_y < len(self.game_map.map_1)):
                    next_value = self.game_map.map_1[next_y][next_x]
                    
                    # kontrola či je ďalšia pozícia cesta a či nejdeme späť
                    if next_value in [1, 4] and (dx, dy) != (-self.last_move[0], -self.last_move[1]) if self.last_move else True:
                        self.last_move = (dx, dy)
                        break
        
        # pohyb v aktuálnom smere
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
