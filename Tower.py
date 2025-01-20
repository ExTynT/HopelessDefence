import pygame
import math

class Tower():
    def __init__(self,window,window_width,window_height,game_map):
        self.window = window
        self.window_width = window_width
        self.window_height = window_height
        self.cell_size = 60
        self.tower_positions = []  # list na uloženie pozície veží a ich typov [(x, y, typ), ...]
        self.game_map = game_map
        self.selected_cell = None  # pozícia bunky pre menu výberu
        self.projectiles = []  # list aktívnych projektilov
    
        # načítanie a transformácia obrázkov
        self.tower_1 = pygame.image.load("sprites/towers/tower_1_laser.png")
        self.tower_1 = pygame.transform.scale(self.tower_1, (self.cell_size, self.cell_size))
        
        self.tower_2 = pygame.image.load("sprites/towers/tower_2_cannon.png")
        self.tower_2 = pygame.transform.scale(self.tower_2, (self.cell_size, self.cell_size))
        
        self.tower_3 = pygame.image.load("sprites/towers/tower_3_basic.png")
        self.tower_3 = pygame.transform.scale(self.tower_3, (self.cell_size, self.cell_size))
        
        self.tower_4 = pygame.image.load("sprites/towers/tower_4_boosting.png")
        self.tower_4 = pygame.transform.scale(self.tower_4, (self.cell_size, self.cell_size))
        
        # načítanie boost symbolu
        self.boost_icon = pygame.image.load("sprites/towers/status/red_symbol.png")
        self.boost_icon = pygame.transform.scale(self.boost_icon, (15, 15))
        
        # projektily
        self.cannonball = pygame.image.load("sprites/towers/projectile/cannonball.png")
        self.cannonball = pygame.transform.scale(self.cannonball, (20, 20))
        
        self.bullet = pygame.image.load("sprites/towers/projectile/bullet.png")
        self.bullet = pygame.transform.scale(self.bullet, (12, 12))
        
        # nastavenie vlastností veží
        self.tower_types = {
            1: {"damage": 1, "range": self.cell_size * 2, "cooldown": 0},  # laser - stály damage
            2: {"damage": 12, "range": self.cell_size * 2.5, "cooldown": 45},  # cannon - silnejší ale pomalší
            3: {"damage": 12, "range": self.cell_size * 2.2, "cooldown": 20},  # basic - rýchle strely s vysokým damage
            4: {"range": self.cell_size * 1.5}  # boosting tower - zvyšuje damage okolitých veží
        }
        self.tower_cooldowns = {}  # sledovanie cooldownu pre každú vežu

    def draw_selection_menu(self):
        if self.selected_cell:
            x, y = self.selected_cell
            # pozadie menu
            menu_width = 240  # rozšírené pre štyri veže
            menu_height = 60
            menu_x = x * self.cell_size
            menu_y = y * self.cell_size - menu_height
            
            # ak by menu presiahlo hornú hranicu, zobraz ho pod bunkou
            if menu_y < 0:
                menu_y = y * self.cell_size + self.cell_size
                
            pygame.draw.rect(self.window, (50, 50, 50), 
                           (menu_x, menu_y, menu_width, menu_height))
            
            # miniatúry veží
            small_size = 40
            # laser
            small_laser = pygame.transform.scale(self.tower_1, (small_size, small_size))
            self.window.blit(small_laser, (menu_x + 10, menu_y + 10))
            # cannon
            small_cannon = pygame.transform.scale(self.tower_2, (small_size, small_size))
            self.window.blit(small_cannon, (menu_x + 70, menu_y + 10))
            # basic
            small_basic = pygame.transform.scale(self.tower_3, (small_size, small_size))
            self.window.blit(small_basic, (menu_x + 130, menu_y + 10))
            # boosting
            small_boost = pygame.transform.scale(self.tower_4, (small_size, small_size))
            self.window.blit(small_boost, (menu_x + 190, menu_y + 10))

    def handle_menu_click(self, pos_x, pos_y):
        if self.selected_cell:
            grid_x, grid_y = self.selected_cell
            menu_x = grid_x * self.cell_size
            menu_y = grid_y * self.cell_size - 60
            
            # ak je menu pod bunkou
            if menu_y < 0:
                menu_y = grid_y * self.cell_size + self.cell_size
                
            # kontrola kliknutia na miniatúry
            if menu_y <= pos_y <= menu_y + 60:
                if menu_x + 10 <= pos_x <= menu_x + 50:  # laser
                    self.tower_positions.append((grid_x, grid_y, 1))
                    self.selected_cell = None
                    return True
                elif menu_x + 70 <= pos_x <= menu_x + 110:  # cannon
                    self.tower_positions.append((grid_x, grid_y, 2))
                    self.selected_cell = None
                    return True
                elif menu_x + 130 <= pos_x <= menu_x + 170:  # basic
                    self.tower_positions.append((grid_x, grid_y, 3))
                    self.selected_cell = None
                    return True
                elif menu_x + 190 <= pos_x <= menu_x + 230:  # boosting
                    self.tower_positions.append((grid_x, grid_y, 4))
                    self.selected_cell = None
                    return True
        return False

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

    def is_in_range(self, tower_x, tower_y, enemy, tower_type):
        # kontrola či je nepriateľ v dosahu veže
        distance = self.get_distance(tower_x, tower_y, enemy)
        return distance <= self.tower_types[tower_type]["range"]

    def add_projectile(self, start_x, start_y, enemies, damage, tower_type):
        if not enemies:
            return
            
        # mieri len na prvého nepriateľa
        enemy = enemies[0]
        end_x = enemy.x + enemy.cell_size // 4
        end_y = enemy.y + enemy.cell_size // 4
        
        # výpočet smeru a rýchlosti
        dx = end_x - start_x
        dy = end_y - start_y
        distance = math.sqrt(dx * dx + dy * dy)
        if distance > 0:
            speed = 8 if tower_type == 2 else 15  # rýchlejšie pre basic vežu
            velocity_x = (dx / distance) * speed
            velocity_y = (dy / distance) * speed
            
            self.projectiles.append({
                'x': start_x,
                'y': start_y,
                'target_x': end_x,
                'target_y': end_y,
                'velocity_x': velocity_x,
                'velocity_y': velocity_y,
                'enemies': enemies[:3] if tower_type == 2 else [enemy],  # AOE len pre cannon
                'damage': damage,
                'hit': False,
                'type': tower_type  # pre rozlíšenie typu projektilu
            })

    def update_projectiles(self):
        # aktualizácia pozícií projektilov
        for proj in self.projectiles[:]:  # kópia listu pre bezpečné odstránenie
            proj['x'] += proj['velocity_x']
            proj['y'] += proj['velocity_y']
            
            # kontrola zásahu
            dx = proj['target_x'] - proj['x']
            dy = proj['target_y'] - proj['y']
            distance = math.sqrt(dx * dx + dy * dy)
            
            if distance < 10 and not proj['hit']:  # projektil zasiahol cieľ a ešte nespôsobil poškodenie
                proj['hit'] = True
                # aplikácia AOE poškodenia na všetkých nepriateľov v dosahu
                for enemy in proj['enemies']:
                    if enemy.alive:
                        enemy.take_damage(proj['damage'])
                self.projectiles.remove(proj)
            elif not any(enemy.alive for enemy in proj['enemies']):  # všetky ciele sú mŕtve
                self.projectiles.remove(proj)

    def draw_projectiles(self):
        # vykreslenie všetkých projektilov
        for proj in self.projectiles:
            if proj['type'] == 2:  # cannon
                self.window.blit(self.cannonball, (int(proj['x'] - 10), int(proj['y'] - 10)))
            else:  # basic
                self.window.blit(self.bullet, (int(proj['x'] - 6), int(proj['y'] - 6)))

    def is_boosted_by_tower(self, x, y):
        # kontrola či je veža v dosahu boosting tower
        for boost_x, boost_y, tower_type in self.tower_positions:
            if tower_type == 4:  # boosting tower
                dx = abs(x - boost_x)
                dy = abs(y - boost_y)
                if dx <= 1 and dy <= 1:  # v dosahu 1 políčka
                    return True
        return False

    def draw_boost_indicators(self):
        # vykreslenie boost indikátorov pre všetky veže v dosahu boosting tower
        for x, y, tower_type in self.tower_positions:
            if tower_type != 4 and self.is_boosted_by_tower(x, y):
                indicator_x = x * self.cell_size + self.cell_size - 20
                indicator_y = y * self.cell_size + 5
                self.window.blit(self.boost_icon, (indicator_x, indicator_y))

    def attack(self, enemies):
        if not enemies:
            return
            
        for grid_x, grid_y, tower_type in self.tower_positions:
            tower_key = (grid_x, grid_y)
            
            # aktualizácia cooldownu
            if tower_key in self.tower_cooldowns:
                self.tower_cooldowns[tower_key] = max(0, self.tower_cooldowns[tower_key] - 1)
            else:
                self.tower_cooldowns[tower_key] = 0
                
            # hľadanie nepriateľov v dosahu
            enemies_in_range = []
            
            for enemy in enemies:
                if enemy.alive and self.is_in_range(grid_x, grid_y, enemy, tower_type):
                    distance = self.get_distance(grid_x, grid_y, enemy)
                    enemies_in_range.append((enemy, distance))
            
            # zoradenie nepriateľov podľa vzdialenosti
            enemies_in_range.sort(key=lambda x: x[1])
            
            # kontrola či je veža na zlatom políčku (3) pre boost a či je v dosahu boosting tower
            is_boosted = self.game_map.map_1[grid_y][grid_x] == 3
            is_tower_boosted = self.is_boosted_by_tower(grid_x, grid_y)
            damage_multiplier = 1
            if is_boosted:
                damage_multiplier *= 1.25
            if is_tower_boosted:
                damage_multiplier *= 1.25
            
            if enemies_in_range and tower_type != 4:  # boosting tower neútočí
                start_x = grid_x * self.cell_size + self.cell_size // 2
                start_y = grid_y * self.cell_size + self.cell_size // 2
                
                if tower_type == 1:  # laser
                    enemy = enemies_in_range[0][0]
                    # kreslenie laseru
                    end_x = enemy.x + enemy.cell_size // 4
                    end_y = enemy.y + enemy.cell_size // 4
                    pygame.draw.line(self.window, (255,0,0), 
                                   (start_x, start_y), (end_x, end_y), 2)
                    # aplikácia poškodenia
                    enemy.take_damage(self.tower_types[1]["damage"] * damage_multiplier)
                
                elif (tower_type in [2, 3]) and self.tower_cooldowns[tower_key] == 0:  # cannon alebo basic
                    # vytvorenie nového projektilu
                    targets = [e[0] for e in enemies_in_range[:3]]
                    self.add_projectile(start_x, start_y, targets, 
                                      self.tower_types[tower_type]["damage"] * damage_multiplier,
                                      tower_type)
                    # reset cooldownu
                    self.tower_cooldowns[tower_key] = self.tower_types[tower_type]["cooldown"]

    def place_tower(self,pos_x,pos_y):
        # prevod pozície myši na pozíciu v mriežke
        grid_x = pos_x // self.cell_size
        grid_y = pos_y // self.cell_size
        
        # kontrola či je pozícia v mape a či je to tráva alebo zlaté políčko
        if 0 <= grid_x < len(self.game_map.map_1[0]) and 0 <= grid_y < len(self.game_map.map_1):
            if self.game_map.map_1[grid_y][grid_x] in [0, 3]:
                # kontrola či už tam nie je veža
                if not any(x == grid_x and y == grid_y for x, y, _ in self.tower_positions):
                    self.selected_cell = (grid_x, grid_y)

    def draw_towers(self, enemies):
        # vykreslenie všetkých veží
        for grid_x, grid_y, tower_type in self.tower_positions:
            pixel_x = grid_x * self.cell_size
            pixel_y = grid_y * self.cell_size
            if 0 <= grid_x < len(self.game_map.map_1[0]) and 0 <= grid_y < len(self.game_map.map_1):
                if tower_type == 1:
                    tower_img = self.tower_1
                elif tower_type == 2:
                    tower_img = self.tower_2
                elif tower_type == 3:
                    tower_img = self.tower_3
                else:
                    tower_img = self.tower_4
                self.window.blit(tower_img, (pixel_x, pixel_y))
        
        self.attack(enemies)
        self.update_projectiles()
        self.draw_projectiles()
        self.draw_boost_indicators()  # vykreslenie boost indikátorov
        self.draw_selection_menu()
        
        

