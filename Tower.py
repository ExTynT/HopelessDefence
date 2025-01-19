import pygame

class Tower():
    def __init__(self,window,window_width,window_height,game_map):
        self.window = window
        self.window_width = window_width
        self.window_height = window_height
        self.cell_size = 60
        self.tower_positions = []  # list na uloženie pozície veží
        self.game_map = game_map
    
        # načítanie a transformácia obrázku veže
        self.tower_1 = pygame.image.load("sprites/towers/tower_1_laser.png")
        self.tower_1 = pygame.transform.scale(self.tower_1, (self.cell_size, self.cell_size))
        
        # nastavenie vlastností veže
        self.damage = 0.5  # základné poškodenie za frame
        self.range = self.cell_size * 2  # dosah veže (2 políčka)

    def get_distance(self, tower_x, tower_y, enemy):
        # výpočet stredu veže a nepriateľa
        tower_center_x = tower_x * self.cell_size + self.cell_size // 2
        tower_center_y = tower_y * self.cell_size + self.cell_size // 2
        enemy_center_x = enemy.x + enemy.cell_size // 4
        enemy_center_y = enemy.y + enemy.cell_size // 4
        
        # výpočet vzdialenosti pomocou Pytagorovej vety
        dx = tower_center_x - enemy_center_x
        dy = tower_center_y - enemy_center_y
        return (dx * dx + dy * dy) ** 0.5

    def is_in_range(self, tower_x, tower_y, enemy):
        # kontrola či je nepriateľ v dosahu veže
        distance = self.get_distance(tower_x, tower_y, enemy)
        return distance <= self.range

    def attack(self, enemies):
        if not enemies:
            return
            
        for grid_x, grid_y in self.tower_positions:
            # hľadanie najbližšieho nepriateľa v dosahu
            closest_enemy = None
            min_distance = float('inf')
            
            for enemy in enemies:
                if enemy.alive and self.is_in_range(grid_x, grid_y, enemy):
                    distance = self.get_distance(grid_x, grid_y, enemy)
                    if distance < min_distance:
                        min_distance = distance
                        closest_enemy = enemy
            
            if closest_enemy:
                # kontrola či je veža na zlatom políčku (3) pre boost
                is_boosted = self.game_map.map_1[grid_y][grid_x] == 3
                damage_multiplier = 1.25 if is_boosted else 1
                
                # kreslenie laseru
                start_x = grid_x * self.cell_size + self.cell_size // 2
                start_y = grid_y * self.cell_size + self.cell_size // 2
                end_x = closest_enemy.x + closest_enemy.cell_size // 4
                end_y = closest_enemy.y + closest_enemy.cell_size // 4
                pygame.draw.line(self.window, (255,0,0), (start_x, start_y), (end_x, end_y), 2)
                
                # aplikácia poškodenia
                closest_enemy.take_damage(self.damage * damage_multiplier)

    def place_tower(self,pos_x,pos_y):
        # prevod pozície myši na pozíciu v mriežke
        grid_x = pos_x // self.cell_size
        grid_y = pos_y // self.cell_size
        
        # kontrola či je pozícia v mape a či je to tráva alebo zlaté políčko
        if 0 <= grid_x < len(self.game_map.map_1[0]) and 0 <= grid_y < len(self.game_map.map_1):
            if self.game_map.map_1[grid_y][grid_x] == 0 or self.game_map.map_1[grid_y][grid_x] == 3:
                self.tower_positions.append((grid_x, grid_y))

    def draw_towers(self, enemies):
        # vykreslenie všetkých veží
        for grid_x, grid_y in self.tower_positions:
            pixel_x = grid_x * self.cell_size
            pixel_y = grid_y * self.cell_size
            if 0 <= grid_x < len(self.game_map.map_1[0]) and 0 <= grid_y < len(self.game_map.map_1):
                self.window.blit(self.tower_1, (pixel_x, pixel_y))
        
        self.attack(enemies)
        
        

