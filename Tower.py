import pygame
import math

class Tower():
    def __init__(self,window,window_width,window_height,game_map,economy,shop):
        self.window = window
        self.window_width = window_width
        self.window_height = window_height
        self.cell_size = 60
        self.tower_positions = []  # list na uloženie pozície veží a ich typov [(x, y, typ), ...]
        self.tower_upgrades = {}  # slovník na sledovanie upgradov pre jednotlivé veže {(x, y): "upgrade_type"}
        self.game_map = game_map
        self.economy = economy  # pridanie ekonomiky
        self.shop = shop  # pridanie shopu
        self.menu_state = None  # None, "placement", "upgrade", "sell"
        self.selected_cell = None  # pozícia bunky pre menu výberu
        self.projectiles = []  # list aktívnych projektilov
        self.font = pygame.font.Font("fonts/joystix monospace.otf", 16)  # font pre ceny
        self.sell_tower_pos = None  # pozícia veže pre predaj
        self.upgrade_tower_pos = None  # pozícia veže pre upgrade
        self.show_stats = False  # nový flag pre zobrazenie štatistík
        self.firing_towers = {}  # sledovanie stavu streľby pre každú vežu {(x,y): timer}
        self.firing_animation_duration = 10  # trvanie firing animácie v snímkach
        
        # Vytvorenie stats ikony
        self.stats_icon = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.rect(self.stats_icon, (200, 200, 200), (2, 2, 16, 4))  # horný riadok
        pygame.draw.rect(self.stats_icon, (200, 200, 200), (2, 8, 12, 4))  # stredný riadok
        pygame.draw.rect(self.stats_icon, (200, 200, 200), (2, 14, 8, 4))  # spodný riadok
        
        # načítanie zvukového efektu pre laser
        self.laser_sound = pygame.mixer.Sound("music/towers/laser.mp3")
        self.laser_sound.set_volume(0.1)  # extrémne nízka hlasitosť
        
        # načítanie zvukového efektu pre basic vežu
        self.basic_sound = pygame.mixer.Sound("music/towers/basic.mp3")
        self.basic_sound.set_volume(0.15)  # extrémne nízka hlasitosť
        
        # načítanie zvukového efektu pre cannon
        self.cannon_sound = pygame.mixer.Sound("music/towers/cannon.mp3")
        self.cannon_sound.set_volume(0.15)  # extrémne nízka hlasitosť
    
        # načítanie a transformácia obrázkov
        self.tower_1 = pygame.image.load("sprites/towers/tower_1_laser.png")
        self.tower_1 = pygame.transform.scale(self.tower_1, (self.cell_size, self.cell_size))
        
        # načítanie firing spritov pre laser vežu
        self.tower_1_firing = pygame.image.load("sprites/towers/tower_1_laser_s.png")  # sprite pre strieľanie základnej veže
        self.tower_1_firing = pygame.transform.scale(self.tower_1_firing, (self.cell_size, self.cell_size))
        
        self.tower_1_piercing_firing = pygame.image.load("sprites/towers/tower_1_laser_1_s.png")  # sprite pre strieľanie piercing upgradu
        self.tower_1_piercing_firing = pygame.transform.scale(self.tower_1_piercing_firing, (self.cell_size, self.cell_size))
        
        self.tower_1_overcharge_firing = pygame.image.load("sprites/towers/tower_1_laser_2_s.png")  # sprite pre strieľanie overcharge upgradu
        self.tower_1_overcharge_firing = pygame.transform.scale(self.tower_1_overcharge_firing, (self.cell_size, self.cell_size))
        
        # načítanie upgrade spritov pre laser vežu
        self.tower_1_piercing = pygame.image.load("sprites/towers/tower_1_laser_1.png")
        self.tower_1_piercing = pygame.transform.scale(self.tower_1_piercing, (self.cell_size, self.cell_size))
        
        self.tower_1_overcharge = pygame.image.load("sprites/towers/tower_1_laser_2.png")
        self.tower_1_overcharge = pygame.transform.scale(self.tower_1_overcharge, (self.cell_size, self.cell_size))
        
        self.tower_1_overcharge_active = pygame.image.load("sprites/towers/tower_1_laser_2_o.png")
        self.tower_1_overcharge_active = pygame.transform.scale(self.tower_1_overcharge_active, (self.cell_size, self.cell_size))
        
        self.tower_2 = pygame.image.load("sprites/towers/tower_2_cannon.png")
        self.tower_2 = pygame.transform.scale(self.tower_2, (self.cell_size, self.cell_size))
        
        # načítanie firing sprite pre cannon
        self.tower_2_firing = pygame.image.load("sprites/towers/tower_2_cannon_fire.png")
        self.tower_2_firing = pygame.transform.scale(self.tower_2_firing, (self.cell_size, self.cell_size))
        
        # načítanie upgrade spritov pre cannon
        self.tower_2_heavy = pygame.image.load("sprites/towers/tower_2_cannon_1.png")
        self.tower_2_heavy = pygame.transform.scale(self.tower_2_heavy, (self.cell_size, self.cell_size))
        self.tower_2_heavy_firing = pygame.image.load("sprites/towers/tower_2_cannon_1_r.png")
        self.tower_2_heavy_firing = pygame.transform.scale(self.tower_2_heavy_firing, (self.cell_size, self.cell_size))
        
        self.tower_2_cluster = pygame.image.load("sprites/towers/tower_2_cannon_2.png")
        self.tower_2_cluster = pygame.transform.scale(self.tower_2_cluster, (self.cell_size, self.cell_size))
        self.tower_2_cluster_firing = pygame.image.load("sprites/towers/tower_2_cannon_2_r.png")
        self.tower_2_cluster_firing = pygame.transform.scale(self.tower_2_cluster_firing, (self.cell_size, self.cell_size))
        
        self.tower_3 = pygame.image.load("sprites/towers/tower_3_basic.png")
        self.tower_3 = pygame.transform.scale(self.tower_3, (self.cell_size, self.cell_size))
        
        # načítanie firing spritov pre basic vežu
        self.tower_3_firing = pygame.image.load("sprites/towers/tower_3_basic_s.png")  # sprite pre strieľanie základnej veže
        self.tower_3_firing = pygame.transform.scale(self.tower_3_firing, (self.cell_size, self.cell_size))
        
        # načítanie upgrade spritov pre basic vežu
        self.tower_3_rapid = pygame.image.load("sprites/towers/tower_3_basic_1.png")
        self.tower_3_rapid = pygame.transform.scale(self.tower_3_rapid, (self.cell_size, self.cell_size))
        self.tower_3_rapid_firing = pygame.image.load("sprites/towers/tower_3_basic_1_s.png")  # sprite pre strieľanie rapid fire upgradu
        self.tower_3_rapid_firing = pygame.transform.scale(self.tower_3_rapid_firing, (self.cell_size, self.cell_size))
        
        self.tower_3_double = pygame.image.load("sprites/towers/tower_3_basic_2.png")
        self.tower_3_double = pygame.transform.scale(self.tower_3_double, (self.cell_size, self.cell_size))
        self.tower_3_double_firing = pygame.image.load("sprites/towers/tower_3_basic_2_s.png")  # sprite pre strieľanie double shot upgradu
        self.tower_3_double_firing = pygame.transform.scale(self.tower_3_double_firing, (self.cell_size, self.cell_size))
        
        self.tower_4 = pygame.image.load("sprites/towers/tower_4_boosting.png")
        self.tower_4 = pygame.transform.scale(self.tower_4, (self.cell_size, self.cell_size))
        
        # načítanie upgrade spritov pre boosting vežu
        self.tower_4_dmg = pygame.image.load("sprites/towers/tower_4_boosting_1.png")
        self.tower_4_dmg = pygame.transform.scale(self.tower_4_dmg, (self.cell_size, self.cell_size))
        
        self.tower_4_spd = pygame.image.load("sprites/towers/tower_4_boosting_2.png")
        self.tower_4_spd = pygame.transform.scale(self.tower_4_spd, (self.cell_size, self.cell_size))
        
        # načítanie unboosted sprite pre boosting vežu
        self.tower_4_unboosted = pygame.image.load("sprites/towers/tower_4_boosting_u.png")
        self.tower_4_unboosted = pygame.transform.scale(self.tower_4_unboosted, (self.cell_size, self.cell_size))
        
        # načítanie boost symbolu
        self.boost_icon = pygame.image.load("sprites/towers/status/red_symbol.png")
        self.boost_icon = pygame.transform.scale(self.boost_icon, (15, 15))
        
        # načítanie boost upgrade symbolov
        self.dmg_boost_icon = pygame.image.load("sprites/towers/status/boosting_tower_upgrade_1.png")
        self.dmg_boost_icon = pygame.transform.scale(self.dmg_boost_icon, (15, 15))
        
        self.spd_boost_icon = pygame.image.load("sprites/towers/status/boosting_tower_upgrade_2.png")
        self.spd_boost_icon = pygame.transform.scale(self.spd_boost_icon, (15, 15))
        
        # projektily
        self.cannonball = pygame.image.load("sprites/towers/projectile/cannonball.png")
        self.cannonball = pygame.transform.scale(self.cannonball, (20, 20))
        
        self.bullet = pygame.image.load("sprites/towers/projectile/bullet.png")
        self.bullet = pygame.transform.scale(self.bullet, (12, 12))
        
        # načítanie upgrade symbolov pre laser vežu
        self.piercing_beam_icon = pygame.image.load("sprites/towers/status/laser_tower_upgrade_1.png")
        self.piercing_beam_icon = pygame.transform.scale(self.piercing_beam_icon, (15, 15))
        
        self.overcharge_icon = pygame.image.load("sprites/towers/status/laser_tower_upgrade_2.png")
        self.overcharge_icon = pygame.transform.scale(self.overcharge_icon, (15, 15))
        
        # načítanie upgrade symbolov pre cannon vežu
        self.heavy_shells_icon = pygame.image.load("sprites/towers/status/cannon_tower_upgrade_1.png")
        self.heavy_shells_icon = pygame.transform.scale(self.heavy_shells_icon, (15, 15))
        
        self.cluster_bombs_icon = pygame.image.load("sprites/towers/status/cannon_tower_upgrade_2.png")
        self.cluster_bombs_icon = pygame.transform.scale(self.cluster_bombs_icon, (15, 15))
        
        # nastavenie vlastností veží
        self.tower_types = {
            1: {"damage": 1, "range": self.cell_size * 2, "cooldown": 0, "cost": 200},  # laser
            2: {"damage": 24, "range": self.cell_size * 2.5, "cooldown": 45, "cost": 350},  # cannon
            3: {"damage": 12, "range": self.cell_size * 2.2, "cooldown": 20, "cost": 150},  # basic
            4: {"range": self.cell_size * 1.5, "cost": 300}  # boosting tower
        }
        
        # nastavenie upgradov
        self.upgrades = {
            "rapid_fire": {
                "name": "Rapid Fire",
                "cost": 100,
                "description": "Basic Tower\nFaster shooting\nDMG: 15 (+25%)\nCD: -25%",
                "effects": {
                    "cooldown": 15,
                    "damage": 15
                }
            },
            "double_shot": {
                "name": "Double Shot",
                "cost": 150,
                "description": "Basic Tower\n2 projectiles\nDMG: 9 each\nFaster shots",
                "effects": {
                    "projectiles": 2,
                    "damage": 9
                }
            },
            "piercing_beam": {
                "name": "Piercing Beam",
                "cost": 175,
                "description": "Laser Tower\nPierces enemies\n1st: 100% DMG\n2nd: 50% DMG",
                "effects": {
                    "pierce": True,
                    "second_damage": 0.5
                }
            },
            "overcharge": {
                "name": "Overcharge",
                "cost": 200,
                "description": "Laser Tower\n2x DMG boost\nActive: 5s\nCooldown: 3s",
                "effects": {
                    "damage": 2,
                    "active_time": 300,  # 5 sekúnd (60 FPS * 5)
                    "cooldown_time": 180  # 3 sekundy (60 FPS * 3)
                }
            },
            "heavy_shells": {
                "name": "Heavy Shells",
                "cost": 200,
                "description": "Cannon Tower\nSingle target\nDMG: 84 (+350%)\nLonger CD",
                "effects": {
                    "damage": 84,
                    "cooldown": 90  # dlhší cooldown pre balance
                }
            },
            "cluster_bombs": {
                "name": "Cluster Bombs",
                "cost": 250,
                "description": "Cannon Tower\n3 projectiles\nCenter: 54 DMG\nSides: 30 DMG",
                "effects": {
                    "center_damage": 54,  # 150% z pôvodných 36 (1.5x24)
                    "side_damage": 30,    # 80% z pôvodných 36 (1.5x24)
                    "cooldown": 60        # dlhší cooldown pre balance
                }
            },
            "damage_boost": {
                "name": "DMG Boost",
                "cost": 350,
                "description": "Boost Tower\n+50% DMG boost\nRange: 1 cell\nFor nearby towers",
                "effects": {
                    "damage_boost": 1.5  # Zvýšené na 50%
                }
            },
            "speed_boost": {
                "name": "SPD Boost",
                "cost": 350,
                "description": "Boost Tower\n+25% ATK SPD\nRange: 1 cell\nFor nearby towers",
                "effects": {
                    "speed_boost": 1.25
                }
            }
        }
        
        self.tower_cooldowns = {}  # sledovanie cooldownu pre každú vežu
        self.overcharge_states = {}  # sledovanie stavu overcharge pre každú vežu {(x,y): {"active": bool, "timer": int}}
        self.show_upgrade_menu = False  # či sa má zobraziť upgrade menu

        # načítanie upgrade symbolov pre basic vežu
        self.rapid_fire_icon = pygame.image.load("sprites/towers/status/basic_tower_upgrade_1.png")
        self.rapid_fire_icon = pygame.transform.scale(self.rapid_fire_icon, (15, 15))
        
        self.double_shot_icon = pygame.image.load("sprites/towers/status/basic_tower_upgrade_2.png")
        self.double_shot_icon = pygame.transform.scale(self.double_shot_icon, (15, 15))

        # sledovanie spomalených nepriateľov
        self.slowed_enemies = {}  # {enemy: remaining_slow_time}

    def draw_selection_menu(self):
        if self.selected_cell:
            x, y = self.selected_cell
            menu_width = 240
            menu_height = 80
            
            menu_x = min(x * self.cell_size, self.window_width - menu_width)
            menu_y = y * self.cell_size - menu_height
            
            if menu_y < 0:
                menu_y = y * self.cell_size + self.cell_size
                
            pygame.draw.rect(self.window, (50, 50, 50), 
                           (menu_x, menu_y, menu_width, menu_height))
            
            # kontrola či je políčko zlaté pre vyššiu cenu
            is_gold_tile = self.game_map.map_1[y][x] == 3
            
            small_size = 40
            # laser
            small_laser = pygame.transform.scale(self.tower_1, (small_size, small_size))
            self.window.blit(small_laser, (menu_x + 10, menu_y + 10))
            tower_cost = self.tower_types[1]['cost']
            if is_gold_tile:
                tower_cost = int(tower_cost * 1.5)
            cost_text = self.font.render(f"${tower_cost}", True, 
                                       (255, 255, 0) if self.economy.can_afford(tower_cost) else (255, 0, 0))
            self.window.blit(cost_text, (menu_x + 10, menu_y + 55))
            
            # cannon
            small_cannon = pygame.transform.scale(self.tower_2, (small_size, small_size))
            self.window.blit(small_cannon, (menu_x + 70, menu_y + 10))
            tower_cost = self.tower_types[2]['cost']
            if is_gold_tile:
                tower_cost = int(tower_cost * 1.5)
            cost_text = self.font.render(f"${tower_cost}", True,
                                       (255, 255, 0) if self.economy.can_afford(tower_cost) else (255, 0, 0))
            self.window.blit(cost_text, (menu_x + 70, menu_y + 55))
            
            # basic
            small_basic = pygame.transform.scale(self.tower_3, (small_size, small_size))
            self.window.blit(small_basic, (menu_x + 130, menu_y + 10))
            tower_cost = self.tower_types[3]['cost']
            if is_gold_tile:
                tower_cost = int(tower_cost * 1.5)
            cost_text = self.font.render(f"${tower_cost}", True,
                                       (255, 255, 0) if self.economy.can_afford(tower_cost) else (255, 0, 0))
            self.window.blit(cost_text, (menu_x + 130, menu_y + 55))
            
            # boosting
            small_boost = pygame.transform.scale(self.tower_4, (small_size, small_size))
            self.window.blit(small_boost, (menu_x + 190, menu_y + 10))
            tower_cost = self.tower_types[4]['cost']
            if is_gold_tile:
                tower_cost = int(tower_cost * 1.5)
            cost_text = self.font.render(f"${tower_cost}", True,
                                       (255, 255, 0) if self.economy.can_afford(tower_cost) else (255, 0, 0))
            self.window.blit(cost_text, (menu_x + 190, menu_y + 55))

    def handle_menu_click(self, pos_x, pos_y):
        if self.selected_cell and self.menu_state == "placement":
            grid_x, grid_y = self.selected_cell
            menu_x = min(grid_x * self.cell_size, self.window_width - 240)
            menu_y = grid_y * self.cell_size - 80
            
            if menu_y < 0:
                menu_y = grid_y * self.cell_size + self.cell_size
                
            if menu_y <= pos_y <= menu_y + 80:
                selected_tower = None
                if menu_x + 10 <= pos_x <= menu_x + 50:  # laser
                    selected_tower = 1
                elif menu_x + 70 <= pos_x <= menu_x + 110:  # cannon
                    selected_tower = 2
                elif menu_x + 130 <= pos_x <= menu_x + 170:  # basic
                    selected_tower = 3
                elif menu_x + 190 <= pos_x <= menu_x + 230:  # boosting
                    selected_tower = 4
                
                if selected_tower:
                    # kontrola či je políčko zlaté pre vyššiu cenu
                    is_gold_tile = self.game_map.map_1[grid_y][grid_x] == 3
                    tower_cost = self.tower_types[selected_tower]['cost']
                    if is_gold_tile:
                        tower_cost = int(tower_cost * 1.5)  # 50% navýšenie ceny na zlatom políčku
                    
                    if self.economy.can_afford(tower_cost):
                        self.economy.spend_coins(tower_cost)
                        self.tower_positions.append((grid_x, grid_y, selected_tower))
                        self.selected_cell = None
                        self.menu_state = None
                        return True
        return False

    def get_distance(self, tower_x, tower_y, enemy):
        # výpočet stredu veže
        tower_center_x = tower_x * self.cell_size + self.cell_size // 2
        tower_center_y = tower_y * self.cell_size + self.cell_size // 2
        
        # ak je enemy None (pre boosting tower), vrátime 0
        if enemy is None:
            return 0
            
        # výpočet stredu nepriateľa
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

    def add_projectile(self, start_x, start_y, enemies, damage, tower_type, upgrade_type=None):
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
            
            if tower_type == 2 and upgrade_type == "cluster_bombs":
                # stredný projektil (150% damage)
                self.projectiles.append({
                    'x': start_x,
                    'y': start_y,
                    'target_x': end_x,
                    'target_y': end_y,
                    'velocity_x': velocity_x,
                    'velocity_y': velocity_y,
                    'enemies': enemies[:3],
                    'damage': self.upgrades["cluster_bombs"]["effects"]["center_damage"],
                    'hit': False,
                    'type': tower_type,
                    'upgrade': upgrade_type
                })
                
                # bočné projektily (80% damage)
                angle = math.pi / 6  # 30 stupňov
                for direction in [-1, 1]:  # -1 pre ľavý, 1 pre pravý projektil
                    cos_angle = math.cos(angle)
                    sin_angle = math.sin(angle)
                    rotated_vx = velocity_x * cos_angle - velocity_y * sin_angle * direction
                    rotated_vy = velocity_x * sin_angle * direction + velocity_y * cos_angle
                    
                    self.projectiles.append({
                        'x': start_x,
                        'y': start_y,
                        'target_x': start_x + rotated_vx * (distance/speed),
                        'target_y': start_y + rotated_vy * (distance/speed),
                        'velocity_x': rotated_vx,
                        'velocity_y': rotated_vy,
                        'enemies': enemies[:3],
                        'damage': self.upgrades["cluster_bombs"]["effects"]["side_damage"],
                        'hit': False,
                        'type': tower_type,
                        'upgrade': upgrade_type
                    })
            elif tower_type == 3 and self.tower_types[tower_type].get("projectiles", 1) == 2:
                # prvý projektil mierne vľavo
                self.projectiles.append({
                    'x': start_x - 5,
                    'y': start_y,
                    'target_x': end_x,
                    'target_y': end_y,
                    'velocity_x': velocity_x,
                    'velocity_y': velocity_y,
                    'enemies': [enemy],
                    'damage': damage,
                    'hit': False,
                    'type': tower_type,
                    'upgrade': upgrade_type
                })
                # druhý projektil mierne vpravo
                self.projectiles.append({
                    'x': start_x + 5,
                    'y': start_y,
                    'target_x': end_x,
                    'target_y': end_y,
                    'velocity_x': velocity_x,
                    'velocity_y': velocity_y,
                    'enemies': [enemy],
                    'damage': damage,
                    'hit': False,
                    'type': tower_type,
                    'upgrade': upgrade_type
                })
            else:
                self.projectiles.append({
                    'x': start_x,
                    'y': start_y,
                    'target_x': end_x,
                    'target_y': end_y,
                    'velocity_x': velocity_x,
                    'velocity_y': velocity_y,
                    'enemies': enemies[:3] if tower_type == 2 else [enemy],
                    'damage': damage,
                    'hit': False,
                    'type': tower_type,
                    'upgrade': upgrade_type
                })

    def update_projectiles(self, enemies):
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
                
                if proj['type'] == 2:  # cannon
                    if proj.get('upgrade') == "heavy_shells":
                        # poškodenie len prvého nepriateľa
                        if proj['enemies'] and proj['enemies'][0].alive:
                            enemy = proj['enemies'][0]
                            enemy.take_damage(proj['damage'])
                            if not enemy.alive:
                                self.economy.coins += enemy.reward
                    elif proj.get('upgrade') == "cluster_bombs":
                        # vytvorenie 3 menších výbuchov
                        cluster_damage = proj['damage']
                        angles = [0, 120, 240]  # rozdelenie do trojuholníka
                        for angle in angles:
                            rad_angle = math.radians(angle)
                            offset_x = math.cos(rad_angle) * 30  # 30 pixelov od centra
                            offset_y = math.sin(rad_angle) * 30
                            
                            # nájdenie nepriateľov v dosahu clusteru
                            cluster_enemies = []
                            cluster_center_x = proj['target_x'] + offset_x
                            cluster_center_y = proj['target_y'] + offset_y
                            
                            for enemy in enemies:
                                if enemy.alive:
                                    dx = (enemy.x + enemy.cell_size // 4) - cluster_center_x
                                    dy = (enemy.y + enemy.cell_size // 4) - cluster_center_y
                                    if math.sqrt(dx * dx + dy * dy) < 30:  # 30 pixelov dosah clusteru
                                        cluster_enemies.append(enemy)
                            
                            # poškodenie nepriateľov v dosahu clusteru
                            for enemy in cluster_enemies:
                                enemy.take_damage(cluster_damage)
                                if not enemy.alive:
                                    self.economy.coins += enemy.reward
                    else:
                        # normálny cannon útok
                        for enemy in proj['enemies']:
                            if enemy.alive:
                                enemy.take_damage(proj['damage'])
                                if not enemy.alive:
                                    self.economy.coins += enemy.reward
                else:
                    # basic tower útok
                    for enemy in proj['enemies']:
                        if enemy.alive:
                            enemy.take_damage(proj['damage'])
                            if not enemy.alive:
                                self.economy.coins += enemy.reward
                
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
                # kontrola či je boosting tower na golden tile
                is_on_gold = self.game_map.map_1[boost_y][boost_x] == 3
                max_range = 2 if is_on_gold else 1  # dvojnásobný rozsah na golden tile
                
                dx = abs(x - boost_x)
                dy = abs(y - boost_y)
                if dx <= max_range and dy <= max_range:  # v dosahu podľa typu políčka
                    return True
        return False

    def draw_boost_indicators(self):
        # vykreslenie boost indikátorov pre všetky veže v dosahu boosting tower
        for x, y, tower_type in self.tower_positions:
            if tower_type != 4 and self.is_boosted_by_tower(x, y):
                indicator_x = x * self.cell_size + self.cell_size - 20
                indicator_y = y * self.cell_size + self.cell_size - 20  # Zmenené na pravý dolný roh
                self.window.blit(self.boost_icon, (indicator_x, indicator_y))

    def attack(self, enemies):
        for x, y, tower_type in self.tower_positions:
            # Preskočiť boosting tower, ktorá neútočí
            if tower_type == 4:
                continue
                
            # Kontrola cooldownu
            tower_pos = (x, y)
            if tower_pos in self.tower_cooldowns and self.tower_cooldowns[tower_pos] > 0:
                self.tower_cooldowns[tower_pos] -= 1
                continue
            
            # Nájdenie najbližšieho nepriateľa v dosahu
            valid_enemies = [enemy for enemy in enemies 
                           if self.is_in_range(x, y, enemy, tower_type) and 
                           not (hasattr(enemy, 'is_dying_animation') and enemy.is_dying_animation())]
            
            if not valid_enemies:
                continue
                
            target = min(valid_enemies, 
                        key=lambda enemy: self.get_distance(x, y, enemy))
            
            # Získanie upgrade typu pre vežu
            upgrade_type = self.tower_upgrades.get((x, y))
            
            # Nastavenie cooldownu podľa typu veže a upgradu
            if tower_type == 1:  # laser
                cooldown = 0
            elif tower_type == 2:  # cannon
                if upgrade_type == "heavy_shells":
                    cooldown = self.upgrades["heavy_shells"]["effects"]["cooldown"]
                elif upgrade_type == "cluster_bombs":
                    cooldown = self.upgrades["cluster_bombs"]["effects"]["cooldown"]
                else:
                    cooldown = self.tower_types[2]["cooldown"]
            else:  # basic
                if upgrade_type == "rapid_fire":
                    cooldown = self.upgrades["rapid_fire"]["effects"]["cooldown"]
                else:
                    cooldown = self.tower_types[3]["cooldown"]
            
            # Aplikácia speed boost efektu ak je v dosahu boosting tower
            if self.is_boosted_by_tower(x, y):
                boost_type = None
                for bx, by, bt in self.tower_positions:
                    if bt == 4 and self.is_in_range(bx, by, None, bt):
                        boost_type = self.tower_upgrades.get((bx, by))
                        if boost_type == "speed_boost":
                            cooldown = int(cooldown / self.upgrades["speed_boost"]["effects"]["speed_boost"])
                            break
            
            self.tower_cooldowns[tower_pos] = cooldown
            
            # Streľba podľa typu veže
            self.shoot((x, y, tower_type), valid_enemies)

    def place_tower(self, pos_x, pos_y, is_right_click):
        # najprv skontrolujeme či neklikáme mimo menu
        if self.menu_state is not None:
            if self.handle_outside_click(pos_x, pos_y):
                return
        
        grid_x = pos_x // self.cell_size
        grid_y = pos_y // self.cell_size
        
        # kontrola či je políčko prázdne a či je to cesta
        if 0 <= grid_x < self.window_width // self.cell_size and 0 <= grid_y < self.window_height // self.cell_size:
            if self.game_map.map_1[grid_y][grid_x] in [0, 3]:  # 0 = tráva, 3 = zlaté políčko
                # kontrola či na políčku už nie je veža
                tower_exists = False
                for x, y, _ in self.tower_positions:
                    if x == grid_x and y == grid_y:
                        tower_exists = True
                        if is_right_click:
                            # zobrazenie sell menu
                            if self.menu_state is None:
                                self.menu_state = "sell"
                                self.sell_tower_pos = (grid_x, grid_y)
                        else:
                            # zobrazenie upgrade menu
                            if self.menu_state is None:
                                self.menu_state = "upgrade"
                                self.upgrade_tower_pos = (grid_x, grid_y)
                        break
                
                # ak nie je veža a nie je pravý klik, otvoríme menu pre výber veže
                if not tower_exists and not is_right_click:
                    if self.menu_state is None:
                        self.selected_cell = (grid_x, grid_y)
                        self.menu_state = "placement"

    def show_sell_confirmation(self, grid_x, grid_y, sell_price):
        # vykreslenie pozadia pre sell menu
        menu_width = 200
        menu_height = 100
        menu_x = grid_x * self.cell_size
        menu_y = grid_y * self.cell_size - menu_height
        
        if menu_y < 0:
            menu_y = grid_y * self.cell_size + self.cell_size
            
        if menu_x + menu_width > self.window_width:
            menu_x = self.window_width - menu_width
        
        pygame.draw.rect(self.window, (50, 50, 50), 
                        (menu_x, menu_y, menu_width, menu_height))
        
        # text pre predajnú cenu
        price_text = self.font.render(f"Sell for ${sell_price}?", True, (255, 215, 0))
        text_rect = price_text.get_rect(centerx=menu_x + menu_width//2, y=menu_y + 20)
        self.window.blit(price_text, text_rect)
        
        # tlačidlá Yes/No
        yes_button = pygame.draw.rect(self.window, (0, 200, 0),
                                    (menu_x + 20, menu_y + 60, 70, 30))
        no_button = pygame.draw.rect(self.window, (200, 0, 0),
                                   (menu_x + 110, menu_y + 60, 70, 30))
        
        yes_text = self.font.render("Yes", True, (255, 255, 255))
        no_text = self.font.render("No", True, (255, 255, 255))
        
        yes_rect = yes_text.get_rect(center=yes_button.center)
        no_rect = no_text.get_rect(center=no_button.center)
        
        self.window.blit(yes_text, yes_rect)
        self.window.blit(no_text, no_rect)
        
        return {"yes": yes_button, "no": no_button}

    def handle_sell_click(self, pos_x, pos_y):
        if not (self.menu_state == "sell" and self.sell_tower_pos):
            return False
            
        grid_x, grid_y = self.sell_tower_pos
        
        # nájdenie indexu a typu veže
        tower_index = None
        tower_type = None
        for i, (x, y, t) in enumerate(self.tower_positions):
            if x == grid_x and y == grid_y:
                tower_index = i
                tower_type = t
                break
        
        if tower_index is None:
            return False
            
        # výpočet predajnej ceny
        base_cost = self.tower_types[tower_type]['cost']
        if self.game_map.map_1[grid_y][grid_x] == 3:
            base_cost = int(base_cost * 2.5)  # 2.5x cena na zlatom políčku
        sell_price = int(base_cost * 0.75)
        
        # získanie tlačidiel z menu
        buttons = self.show_sell_confirmation(grid_x, grid_y, sell_price)
        
        if buttons["yes"].collidepoint(pos_x, pos_y):
            # predaj veže
            self.economy.coins += sell_price
            # vymazanie upgradu pre túto pozíciu
            if (grid_x, grid_y) in self.tower_upgrades:
                del self.tower_upgrades[(grid_x, grid_y)]
            self.tower_positions.pop(tower_index)
            self.menu_state = None
            self.sell_tower_pos = None
            return True
            
        if buttons["no"].collidepoint(pos_x, pos_y):
            self.menu_state = None
            self.sell_tower_pos = None
            return True
            
        return False

    def draw_tower_stats(self, tower_type, grid_x, grid_y, menu_x, menu_y, menu_width):
        """Vykreslí štatistiky veže"""
        stats = self.get_tower_stats(tower_type, grid_x, grid_y)
        
        # Základné štatistiky
        base_stats = self.tower_types[tower_type].copy()
        
        # Pozadie menu
        pygame.draw.rect(self.window, (50, 50, 50), (menu_x, menu_y, menu_width, 140))
        
        # Nadpis
        title = self.font.render("TOWER STATS", True, (255, 215, 0))
        title_rect = title.get_rect(centerx=menu_x + menu_width//2, y=menu_y + 10)
        self.window.blit(title, title_rect)
        
        # Menší font pre štatistiky
        stats_font = pygame.font.Font("fonts/joystix monospace.otf", 12)
        
        # Aktuálne hodnoty
        y_offset = menu_y + 40
        
        if "damage" in stats and tower_type != 4:  # pre všetky veže okrem boosting
            base_dmg = base_stats["damage"]
            current_dmg = stats["damage"]
            boost_text = " *" if stats.get("has_dmg_boost", False) else ""
            dmg_text = stats_font.render(f"DMG: {current_dmg:.1f} (Base: {base_dmg}){boost_text}", True, (255, 255, 255))
            dmg_rect = dmg_text.get_rect(centerx=menu_x + menu_width//2, y=y_offset)
            self.window.blit(dmg_text, dmg_rect)
            y_offset += 20
        
        if "cooldown" in stats and tower_type != 4:
            base_cd = base_stats["cooldown"]
            current_cd = stats["cooldown"]
            boost_text = " *" if stats.get("has_spd_boost", False) else ""
            cd_text = stats_font.render(f"CD: {current_cd:.1f} (Base: {base_cd}){boost_text}", True, (255, 255, 255))
            cd_rect = cd_text.get_rect(centerx=menu_x + menu_width//2, y=y_offset)
            self.window.blit(cd_text, cd_rect)
            y_offset += 20
        
        if "boost_type" in stats:  # pre boosting tower
            boost_type = stats["boost_type"]
            boost_value = stats["boost_value"]
            boost_range = stats["range"]
            
            type_text = stats_font.render(f"Type: {boost_type.upper()}", True, (255, 255, 255))
            type_rect = type_text.get_rect(centerx=menu_x + menu_width//2, y=y_offset)
            self.window.blit(type_text, type_rect)
            y_offset += 20
            
            value_text = stats_font.render(f"Boost: {boost_value}", True, (255, 255, 255))
            value_rect = value_text.get_rect(centerx=menu_x + menu_width//2, y=y_offset)
            self.window.blit(value_text, value_rect)
            y_offset += 20
            
            range_text = stats_font.render(f"Range: {boost_range}", True, (255, 255, 255))
            range_rect = range_text.get_rect(centerx=menu_x + menu_width//2, y=y_offset)
            self.window.blit(range_text, range_rect)
            y_offset += 20
        
        # ikona pre prepnutie späť - v pravom hornom rohu
        stats_button = pygame.draw.rect(self.window, (40, 40, 40), 
                                      (menu_x + menu_width - 30, menu_y + 5, 25, 25))
        self.window.blit(self.stats_icon, (menu_x + menu_width - 27, menu_y + 7))
        
        return {"stats": stats_button}

    def draw_upgrade_menu(self):
        """Vykreslí menu pre vylepšenie veže"""
        if not self.upgrade_tower_pos:
            return None
            
        grid_x, grid_y = self.upgrade_tower_pos
        tower_type = None
        
        # nájdenie typu veže na danej pozícii
        for x, y, t in self.tower_positions:
            if x == grid_x and y == grid_y:
                tower_type = t
                break
        
        if tower_type is None:
            return None
        
        # pozícia menu
        menu_x = grid_x * self.cell_size
        menu_y = grid_y * self.cell_size - 200
        menu_width = 240
        menu_height = 200
        button_height = 50
        
        if menu_y < 0:
            menu_y = grid_y * self.cell_size + self.cell_size
            
        if menu_x + menu_width > self.window_width:
            menu_x = self.window_width - menu_width
            
        # pozadie menu
        pygame.draw.rect(self.window, (50, 50, 50), (menu_x, menu_y, menu_width, menu_height))
        
        # ikona pre prepnutie na štatistiky - v pravom hornom rohu
        stats_button = pygame.draw.rect(self.window, (40, 40, 40), 
                                      (menu_x + menu_width - 30, menu_y + 5, 25, 25))
        self.window.blit(self.stats_icon, (menu_x + menu_width - 27, menu_y + 7))
        
        # Ak je veža upgradnutá alebo je zapnuté zobrazenie štatistík
        if (grid_x, grid_y) in self.tower_upgrades or self.show_stats:
            return self.draw_tower_stats(tower_type, grid_x, grid_y, menu_x, menu_y, menu_width)
        
        # nadpis
        title_text = self.font.render("UPGRADES", True, (255, 215, 0))
        title_rect = title_text.get_rect(centerx=menu_x + menu_width//2, y=menu_y + 10)
        self.window.blit(title_text, title_rect)
        
        # kontrola či je na zlatom políčku
        is_gold_tile = self.game_map.map_1[grid_y][grid_x] == 3
        
        upgrade_rects = {}
        button_y = menu_y + 40
        
        if tower_type == 3:  # basic veža
            # rapid fire upgrade
            rapid_fire = pygame.draw.rect(self.window, (40, 40, 40),
                                        (menu_x + 10, button_y, menu_width//2 - 15, button_height))
            
            name_text = self.font.render("Rapid", True, 
                                       (255, 255, 0) if self.economy.can_afford(self.upgrades["rapid_fire"]["cost"] * (2 if is_gold_tile else 1)) 
                                       else (255, 0, 0))
            
            name_rect = name_text.get_rect(centerx=rapid_fire.centerx, y=button_y + 5)
            cost_text = self.font.render(f"${self.upgrades['rapid_fire']['cost'] * (2 if is_gold_tile else 1)}", True, 
                                       (255, 255, 0) if self.economy.can_afford(self.upgrades["rapid_fire"]["cost"] * (2 if is_gold_tile else 1)) 
                                       else (255, 0, 0))
            
            cost_rect = cost_text.get_rect(centerx=rapid_fire.centerx, y=button_y + 25)
            
            self.window.blit(name_text, name_rect)
            self.window.blit(cost_text, cost_rect)
            
            upgrade_rects["rapid_fire"] = rapid_fire
            
            # double shot upgrade
            double_shot = pygame.draw.rect(self.window, (40, 40, 40),
                                         (menu_x + menu_width//2 + 5, button_y, menu_width//2 - 15, button_height))
            
            name_text = self.font.render("Double", True, 
                                       (255, 255, 0) if self.economy.can_afford(self.upgrades["double_shot"]["cost"] * (2 if is_gold_tile else 1)) 
                                       else (255, 0, 0))
            cost_text = self.font.render(f"${self.upgrades['double_shot']['cost'] * (2 if is_gold_tile else 1)}", True, 
                                       (255, 255, 0) if self.economy.can_afford(self.upgrades["double_shot"]["cost"] * (2 if is_gold_tile else 1)) 
                                       else (255, 0, 0))
            
            double_name_rect = name_text.get_rect(centerx=double_shot.centerx, y=button_y + 5)
            cost_rect = cost_text.get_rect(centerx=double_shot.centerx, y=button_y + 25)
            
            self.window.blit(name_text, double_name_rect)
            self.window.blit(cost_text, cost_rect)
            
            upgrade_rects["double_shot"] = double_shot
            
            # popis upgradov
            description_y = button_y + button_height + 10
            if rapid_fire.collidepoint(pygame.mouse.get_pos()):
                description_lines = self.upgrades["rapid_fire"]["description"].split('\n')
            elif double_shot.collidepoint(pygame.mouse.get_pos()):
                description_lines = self.upgrades["double_shot"]["description"].split('\n')
            else:
                description_lines = ["Hover over upgrade", "to see details"]
            
            for line in description_lines:
                desc_text = self.font.render(line, True, (255, 255, 255))
                desc_rect = desc_text.get_rect(centerx=menu_x + menu_width//2, y=description_y)
                self.window.blit(desc_text, desc_rect)
                description_y += 20
        
        elif tower_type == 1:  # laser veža
            # piercing beam upgrade
            piercing = pygame.draw.rect(self.window, (40, 40, 40),
                                      (menu_x + 10, button_y, menu_width//2 - 15, button_height))
            
            name_text = self.font.render("Pierce", True, 
                                       (255, 255, 0) if self.economy.can_afford(self.upgrades["piercing_beam"]["cost"] * (2 if is_gold_tile else 1)) 
                                       else (255, 0, 0))
            cost_text = self.font.render(f"${self.upgrades['piercing_beam']['cost'] * (2 if is_gold_tile else 1)}", True,
                                       (255, 255, 0) if self.economy.can_afford(self.upgrades["piercing_beam"]["cost"] * (2 if is_gold_tile else 1))
                                       else (255, 0, 0))
            
            name_rect = name_text.get_rect(centerx=piercing.centerx, y=button_y + 5)
            cost_rect = cost_text.get_rect(centerx=piercing.centerx, y=button_y + 25)
            
            self.window.blit(name_text, name_rect)
            self.window.blit(cost_text, cost_rect)
            
            upgrade_rects["piercing_beam"] = piercing
            
            # overcharge upgrade
            overcharge = pygame.draw.rect(self.window, (40, 40, 40),
                                        (menu_x + menu_width//2 + 5, button_y, menu_width//2 - 15, button_height))
            
            name_text = self.font.render("Charge", True, 
                                       (255, 255, 0) if self.economy.can_afford(self.upgrades["overcharge"]["cost"] * (2 if is_gold_tile else 1)) 
                                       else (255, 0, 0))
            cost_text = self.font.render(f"${self.upgrades['overcharge']['cost'] * (2 if is_gold_tile else 1)}", True,
                                       (255, 255, 0) if self.economy.can_afford(self.upgrades["overcharge"]["cost"] * (2 if is_gold_tile else 1))
                                       else (255, 0, 0))
            
            overcharge_name_rect = name_text.get_rect(centerx=overcharge.centerx, y=button_y + 5)
            cost_rect = cost_text.get_rect(centerx=overcharge.centerx, y=button_y + 25)
            
            self.window.blit(name_text, overcharge_name_rect)
            self.window.blit(cost_text, cost_rect)
            
            upgrade_rects["overcharge"] = overcharge
            
            # popis upgradov
            description_y = button_y + button_height + 10
            if piercing.collidepoint(pygame.mouse.get_pos()):
                description_lines = self.upgrades["piercing_beam"]["description"].split('\n')
            elif overcharge.collidepoint(pygame.mouse.get_pos()):
                description_lines = self.upgrades["overcharge"]["description"].split('\n')
            else:
                description_lines = ["Hover over upgrade", "to see details"]
            
            for line in description_lines:
                desc_text = self.font.render(line, True, (255, 255, 255))
                desc_rect = desc_text.get_rect(centerx=menu_x + menu_width//2, y=description_y)
                self.window.blit(desc_text, desc_rect)
                description_y += 20
                
        elif tower_type == 2:  # cannon veža
            # heavy shells upgrade
            heavy = pygame.draw.rect(self.window, (40, 40, 40),
                                   (menu_x + 10, button_y, menu_width//2 - 15, button_height))
            
            name_text = self.font.render("Heavy", True, 
                                       (255, 255, 0) if self.economy.can_afford(self.upgrades["heavy_shells"]["cost"] * (2 if is_gold_tile else 1)) 
                                       else (255, 0, 0))
            cost_text = self.font.render(f"${self.upgrades['heavy_shells']['cost'] * (2 if is_gold_tile else 1)}", True,
                                       (255, 255, 0) if self.economy.can_afford(self.upgrades["heavy_shells"]["cost"] * (2 if is_gold_tile else 1))
                                       else (255, 0, 0))
            
            name_rect = name_text.get_rect(centerx=heavy.centerx, y=button_y + 5)
            cost_rect = cost_text.get_rect(centerx=heavy.centerx, y=button_y + 25)
            
            self.window.blit(name_text, name_rect)
            self.window.blit(cost_text, cost_rect)
            
            upgrade_rects["heavy_shells"] = heavy
            
            # cluster bombs upgrade
            cluster = pygame.draw.rect(self.window, (40, 40, 40),
                                     (menu_x + menu_width//2 + 5, button_y, menu_width//2 - 15, button_height))
            
            name_text = self.font.render("Cluster", True, 
                                       (255, 255, 0) if self.economy.can_afford(self.upgrades["cluster_bombs"]["cost"] * (2 if is_gold_tile else 1)) 
                                       else (255, 0, 0))
            cost_text = self.font.render(f"${self.upgrades['cluster_bombs']['cost'] * (2 if is_gold_tile else 1)}", True,
                                       (255, 255, 0) if self.economy.can_afford(self.upgrades["cluster_bombs"]["cost"] * (2 if is_gold_tile else 1))
                                       else (255, 0, 0))
            
            cluster_name_rect = name_text.get_rect(centerx=cluster.centerx, y=button_y + 5)
            cost_rect = cost_text.get_rect(centerx=cluster.centerx, y=button_y + 25)
            
            self.window.blit(name_text, cluster_name_rect)
            self.window.blit(cost_text, cost_rect)
            
            upgrade_rects["cluster_bombs"] = cluster
            
            # popis upgradov
            description_y = button_y + button_height + 10
            if heavy.collidepoint(pygame.mouse.get_pos()):
                description_lines = self.upgrades["heavy_shells"]["description"].split('\n')
            elif cluster.collidepoint(pygame.mouse.get_pos()):
                description_lines = self.upgrades["cluster_bombs"]["description"].split('\n')
            else:
                description_lines = ["Hover over upgrade", "to see details"]
            
            for line in description_lines:
                desc_text = self.font.render(line, True, (255, 255, 255))
                desc_rect = desc_text.get_rect(centerx=menu_x + menu_width//2, y=description_y)
                self.window.blit(desc_text, desc_rect)
                description_y += 20
                
        elif tower_type == 4:  # boosting tower
            # damage boost upgrade
            damage = pygame.draw.rect(self.window, (40, 40, 40),
                                   (menu_x + 10, button_y, menu_width//2 - 15, button_height))
            
            name_text = self.font.render("DMG", True, 
                                       (255, 255, 0) if self.economy.can_afford(self.upgrades["damage_boost"]["cost"] * (2 if is_gold_tile else 1)) 
                                       else (255, 0, 0))
            
            name_rect = name_text.get_rect(centerx=damage.centerx, y=button_y + 5)
            cost_text = self.font.render(f"${self.upgrades['damage_boost']['cost'] * (2 if is_gold_tile else 1)}", True,
                                       (255, 255, 0) if self.economy.can_afford(self.upgrades["damage_boost"]["cost"] * (2 if is_gold_tile else 1))
                                       else (255, 0, 0))
            
            cost_rect = cost_text.get_rect(centerx=damage.centerx, y=button_y + 25)
            
            self.window.blit(name_text, name_rect)
            self.window.blit(cost_text, cost_rect)
            
            upgrade_rects["damage_boost"] = damage
            
            # speed boost upgrade
            speed = pygame.draw.rect(self.window, (40, 40, 40),
                                     (menu_x + menu_width//2 + 5, button_y, menu_width//2 - 15, button_height))
            
            name_text = self.font.render("SPD", True, 
                                       (255, 255, 0) if self.economy.can_afford(self.upgrades["speed_boost"]["cost"] * (2 if is_gold_tile else 1)) 
                                       else (255, 0, 0))
            cost_text = self.font.render(f"${self.upgrades['speed_boost']['cost'] * (2 if is_gold_tile else 1)}", True,
                                       (255, 255, 0) if self.economy.can_afford(self.upgrades["speed_boost"]["cost"] * (2 if is_gold_tile else 1))
                                       else (255, 0, 0))
            
            speed_name_rect = name_text.get_rect(centerx=speed.centerx, y=button_y + 5)
            cost_rect = cost_text.get_rect(centerx=speed.centerx, y=button_y + 25)
            
            self.window.blit(name_text, speed_name_rect)
            self.window.blit(cost_text, cost_rect)
            
            upgrade_rects["speed_boost"] = speed
            
            # popis upgradov
            description_y = button_y + button_height + 10
            if damage.collidepoint(pygame.mouse.get_pos()):
                description_lines = self.upgrades["damage_boost"]["description"].split('\n')
            elif speed.collidepoint(pygame.mouse.get_pos()):
                description_lines = self.upgrades["speed_boost"]["description"].split('\n')
            else:
                description_lines = ["Hover over upgrade", "to see details"]
            
            for line in description_lines:
                desc_text = self.font.render(line, True, (255, 255, 255))
                desc_rect = desc_text.get_rect(centerx=menu_x + menu_width//2, y=description_y)
                self.window.blit(desc_text, desc_rect)
                description_y += 20
        
        return {"stats": stats_button, **upgrade_rects}

    def handle_upgrade_click(self, pos_x, pos_y):
        """Spracuje kliknutie v upgrade menu"""
        if not self.upgrade_tower_pos:
            return False
            
        buttons = self.draw_upgrade_menu()
        if not buttons:
            return False
            
        # Kontrola kliknutia na stats tlačidlo
        if "stats" in buttons and buttons["stats"].collidepoint(pos_x, pos_y):
            self.show_stats = not self.show_stats
            return True
                    
        grid_x, grid_y = self.upgrade_tower_pos
        
        # kontrola či je na zlatom políčku
        is_gold_tile = self.game_map.map_1[grid_y][grid_x] == 3
        
        # Kontrola kliknutia na upgrade tlačidlá
        for upgrade_type, button in buttons.items():
            if upgrade_type != "stats" and button.collidepoint(pos_x, pos_y):
                cost = self.upgrades[upgrade_type]["cost"] * (2.5 if is_gold_tile else 1)
                if self.economy.can_afford(cost):
                    self.economy.spend_coins(cost)
                    self.tower_upgrades[(grid_x, grid_y)] = upgrade_type
                    self.menu_state = None
                    self.upgrade_tower_pos = None
                    return True
        
        return False

    def draw_towers(self, enemies, is_paused=False):
        # vykreslenie všetkých veží
        for grid_x, grid_y, tower_type in self.tower_positions:
            pixel_x = grid_x * self.cell_size
            pixel_y = grid_y * self.cell_size
            if 0 <= grid_x < len(self.game_map.map_1[0]) and 0 <= grid_y < len(self.game_map.map_1):
                if tower_type == 1:  # laser tower
                    # Kontrola či je veža v stave streľby
                    if (grid_x, grid_y) in self.firing_towers:
                        if (grid_x, grid_y) in self.tower_upgrades:
                            upgrade_type = self.tower_upgrades[(grid_x, grid_y)]
                            if upgrade_type == "piercing_beam":
                                tower_img = self.tower_1_piercing_firing
                            elif upgrade_type == "overcharge":
                                tower_img = self.tower_1_overcharge_firing
                            else:
                                tower_img = self.tower_1_firing
                        else:
                            tower_img = self.tower_1_firing
                        self.firing_towers[(grid_x, grid_y)] -= 1
                        if self.firing_towers[(grid_x, grid_y)] <= 0:
                            del self.firing_towers[(grid_x, grid_y)]
                    else:
                        if (grid_x, grid_y) in self.tower_upgrades:
                            upgrade_type = self.tower_upgrades[(grid_x, grid_y)]
                            if upgrade_type == "piercing_beam":
                                tower_img = self.tower_1_piercing
                            elif upgrade_type == "overcharge":
                                tower_img = self.tower_1_overcharge
                            else:
                                tower_img = self.tower_1
                        else:
                            tower_img = self.tower_1
                elif tower_type == 2:
                    # Kontrola či je veža v stave streľby
                    if (grid_x, grid_y) in self.firing_towers:
                        if (grid_x, grid_y) in self.tower_upgrades:
                            upgrade_type = self.tower_upgrades[(grid_x, grid_y)]
                            if upgrade_type == "heavy_shells":
                                tower_img = self.tower_2_heavy_firing
                            elif upgrade_type == "cluster_bombs":
                                tower_img = self.tower_2_cluster_firing
                            else:
                                tower_img = self.tower_2_firing
                        else:
                            tower_img = self.tower_2_firing
                        self.firing_towers[(grid_x, grid_y)] -= 1
                        if self.firing_towers[(grid_x, grid_y)] <= 0:
                            del self.firing_towers[(grid_x, grid_y)]
                    else:
                        if (grid_x, grid_y) in self.tower_upgrades:
                            upgrade_type = self.tower_upgrades[(grid_x, grid_y)]
                            if upgrade_type == "heavy_shells":
                                tower_img = self.tower_2_heavy
                            elif upgrade_type == "cluster_bombs":
                                tower_img = self.tower_2_cluster
                            else:
                                tower_img = self.tower_2
                        else:
                            tower_img = self.tower_2
                elif tower_type == 3:  # basic tower
                    # Kontrola či je veža v stave streľby
                    if (grid_x, grid_y) in self.firing_towers:
                        if (grid_x, grid_y) in self.tower_upgrades:
                            upgrade_type = self.tower_upgrades[(grid_x, grid_y)]
                            if upgrade_type == "rapid_fire":
                                tower_img = self.tower_3_rapid_firing  # sprite pre strieľanie rapid fire upgradu
                            elif upgrade_type == "double_shot":
                                tower_img = self.tower_3_double_firing  # sprite pre strieľanie double shot upgradu
                            else:
                                tower_img = self.tower_3_firing  # sprite pre strieľanie základnej veže
                        else:
                            tower_img = self.tower_3_firing  # sprite pre strieľanie základnej veže
                        self.firing_towers[(grid_x, grid_y)] -= 1
                        if self.firing_towers[(grid_x, grid_y)] <= 0:
                            del self.firing_towers[(grid_x, grid_y)]
                    else:
                        if (grid_x, grid_y) in self.tower_upgrades:
                            upgrade_type = self.tower_upgrades[(grid_x, grid_y)]
                            if upgrade_type == "rapid_fire":
                                tower_img = self.tower_3_rapid
                            elif upgrade_type == "double_shot":
                                tower_img = self.tower_3_double
                            else:
                                tower_img = self.tower_3
                        else:
                            tower_img = self.tower_3
                else:  # boosting tower
                    # Kontrola či veža aktívne boostuje
                    is_boosting = self.is_boosting_any_tower(grid_x, grid_y)
                    
                    if not is_boosting:
                        tower_img = self.tower_4_unboosted
                    elif (grid_x, grid_y) in self.tower_upgrades:
                        upgrade_type = self.tower_upgrades[(grid_x, grid_y)]
                        if upgrade_type == "damage_boost":
                            tower_img = self.tower_4_dmg
                        elif upgrade_type == "speed_boost":
                            tower_img = self.tower_4_spd
                        else:
                            tower_img = self.tower_4
                    else:
                        tower_img = self.tower_4
                self.window.blit(tower_img, (pixel_x, pixel_y))
                
                # zobrazenie upgrade ikon
                if (grid_x, grid_y) in self.tower_upgrades:
                    upgrade_type = self.tower_upgrades[(grid_x, grid_y)]
                    if tower_type == 1:  # laser tower
                        if upgrade_type == "piercing_beam":
                            self.window.blit(self.piercing_beam_icon, (pixel_x + self.cell_size - 20, pixel_y + 5))
                        elif upgrade_type == "overcharge":
                            self.window.blit(self.overcharge_icon, (pixel_x + self.cell_size - 20, pixel_y + 5))
                    elif tower_type == 2:  # cannon tower
                        if upgrade_type == "heavy_shells":
                            self.window.blit(self.heavy_shells_icon, (pixel_x + self.cell_size - 20, pixel_y + 5))
                        elif upgrade_type == "cluster_bombs":
                            self.window.blit(self.cluster_bombs_icon, (pixel_x + self.cell_size - 20, pixel_y + 5))
                    elif tower_type == 3:  # basic tower
                        if upgrade_type == "rapid_fire":
                            self.window.blit(self.rapid_fire_icon, (pixel_x + self.cell_size - 20, pixel_y + 5))
                        elif upgrade_type == "double_shot":
                            self.window.blit(self.double_shot_icon, (pixel_x + self.cell_size - 20, pixel_y + 5))
                    elif tower_type == 4:  # boosting tower
                        if upgrade_type == "damage_boost":
                            self.window.blit(self.dmg_boost_icon, (pixel_x + self.cell_size - 20, pixel_y + 5))
                        elif upgrade_type == "speed_boost":
                            self.window.blit(self.spd_boost_icon, (pixel_x + self.cell_size - 20, pixel_y + 5))
        
        if not is_paused:
            self.attack(enemies)
            self.update_projectiles(enemies)
        
        self.draw_projectiles()
        self.draw_boost_indicators()
        self.draw_selection_menu()
        self.draw_upgrade_menu()
        
        # vykreslenie sell menu ak je aktívne
        if self.menu_state == "sell" and self.sell_tower_pos:
            grid_x, grid_y = self.sell_tower_pos
            # nájdenie indexu a typu veže
            tower_index = None
            tower_type = None
            for i, (x, y, t) in enumerate(self.tower_positions):
                if x == grid_x and y == grid_y:
                    tower_index = i
                    tower_type = t
                    break
            
            if tower_index is not None:
                # výpočet predajnej ceny
                base_cost = self.tower_types[tower_type]['cost']
                if self.game_map.map_1[grid_y][grid_x] == 3:
                    base_cost = int(base_cost * 2.5)  # 2.5x cena na zlatom políčku
                sell_price = int(base_cost * 0.75)
                self.show_sell_confirmation(grid_x, grid_y, sell_price)

    def update_game_map(self, new_map):
        """Aktualizácia mapy pre nový level"""
        self.game_map = new_map
        self.selected_cell = None  # reset výberu pri zmene mapy
        self.tower_upgrades.clear()  # reset upgradov pri zmene levelu
        self.tower_cooldowns.clear()  # reset cooldownov
        self.overcharge_states.clear()  # reset overcharge stavov

    def close_all_menus(self):
        """Zatvorenie všetkých otvorených menu"""
        self.selected_cell = None
        self.upgrade_tower_pos = None
        self.sell_tower_pos = None
        self.menu_state = None

    def handle_outside_click(self, pos_x, pos_y):
        """Spracovanie kliknutia mimo menu"""
        if self.menu_state == "placement":  # menu pre výber veže
            grid_x, grid_y = self.selected_cell
            menu_x = min(grid_x * self.cell_size, self.window_width - 240)
            menu_y = grid_y * self.cell_size - 80
            
            if menu_y < 0:  # ak je menu príliš hore, posunie sa dole
                menu_y = grid_y * self.cell_size + self.cell_size
                
            menu_rect = pygame.Rect(menu_x, menu_y, 240, 80)
            if not menu_rect.collidepoint(pos_x, pos_y):
                self.close_all_menus()
                return True
                
        elif self.menu_state == "upgrade":  # menu pre upgrade veže
            grid_x, grid_y = self.upgrade_tower_pos
            menu_x = grid_x * self.cell_size
            menu_y = grid_y * self.cell_size - 200
            
            if menu_y < 0:  # ak je menu príliš hore, posunie sa dole
                menu_y = grid_y * self.cell_size + self.cell_size
                
            if menu_x + 240 > self.window_width:  # ak je menu príliš vpravo, posunie sa doľava
                menu_x = self.window_width - 240
                
            menu_rect = pygame.Rect(menu_x, menu_y, 240, 200)
            if not menu_rect.collidepoint(pos_x, pos_y):
                self.close_all_menus()
                return True
                
        elif self.menu_state == "sell":  # menu pre predaj veže
            grid_x, grid_y = self.sell_tower_pos
            menu_x = grid_x * self.cell_size
            menu_y = grid_y * self.cell_size - 100
            
            if menu_y < 0:  # ak je menu príliš hore, posunie sa dole
                menu_y = grid_y * self.cell_size + self.cell_size
                
            if menu_x + 200 > self.window_width:  # ak je menu príliš vpravo, posunie sa doľava
                menu_x = self.window_width - 200
                
            menu_rect = pygame.Rect(menu_x, menu_y, 200, 100)
            if not menu_rect.collidepoint(pos_x, pos_y):
                self.close_all_menus()
                return True
                
        return False

    def get_tower_stats(self, tower_type, grid_x, grid_y):
        """Vráti finálne štatistiky veže po aplikovaní všetkých bonusov"""
        base_stats = self.tower_types[tower_type].copy()
        
        # Aplikovanie bonusov zo shopu
        shop_damage_mult, shop_speed_mult = self.shop.get_tower_multipliers(tower_type)
        
        # Nájdenie boostov z boosting veží
        dmg_boost = 1.0
        spd_boost = 1.0
        for boost_x, boost_y, t in self.tower_positions:
            if t == 4:  # boosting tower
                # kontrola či je v dosahu
                max_range = 2 if self.game_map.map_1[boost_y][boost_x] == 3 else 1
                dx = abs(grid_x - boost_x)
                dy = abs(grid_y - boost_y)
                if dx <= max_range and dy <= max_range:
                    # zistenie typu boostu
                    if (boost_x, boost_y) in self.tower_upgrades:
                        if self.tower_upgrades[(boost_x, boost_y)] == "damage_boost":
                            dmg_boost = max(dmg_boost, 1.5)  # 50% boost
                        elif self.tower_upgrades[(boost_x, boost_y)] == "speed_boost":
                            spd_boost = max(spd_boost, 1.25)  # 25% boost
                    else:
                        dmg_boost = max(dmg_boost, 1.25)  # základný 25% boost
        
        # Aplikovanie upgrade bonusov
        if (grid_x, grid_y) in self.tower_upgrades:
            upgrade_type = self.tower_upgrades[(grid_x, grid_y)]
            upgrade_effects = self.upgrades[upgrade_type]["effects"]
            
            if tower_type == 4:  # boosting tower
                if upgrade_type == "damage_boost":
                    base_stats["boost_type"] = "damage"
                    base_stats["boost_value"] = "50%"
                elif upgrade_type == "speed_boost":
                    base_stats["boost_type"] = "speed"
                    base_stats["boost_value"] = "25%"
                base_stats["range"] = "1 cell"
                if self.game_map.map_1[grid_y][grid_x] == 3:
                    base_stats["range"] = "2 cells"
            else:
                if "damage" in upgrade_effects:
                    base_stats["damage"] = upgrade_effects["damage"]
                if "cooldown" in upgrade_effects:
                    base_stats["cooldown"] = upgrade_effects["cooldown"]
        elif tower_type == 4:  # základné štatistiky pre boosting tower
            base_stats["boost_type"] = "none"
            base_stats["boost_value"] = "25%"
            base_stats["range"] = "1 cell"
            if self.game_map.map_1[grid_y][grid_x] == 3:
                base_stats["range"] = "2 cells"
        
        # Aplikovanie shop multiplikátorov a boostov na finálne hodnoty
        if "damage" in base_stats:
            base_stats["damage"] *= shop_damage_mult * dmg_boost
        if "cooldown" in base_stats:
            base_stats["cooldown"] /= (shop_speed_mult * spd_boost)  # delenie pre cooldown
            
        # Uloženie informácie o boostoch pre zobrazenie
        if tower_type != 4:  # len pre nebootsovacie veže
            base_stats["has_dmg_boost"] = dmg_boost > 1.0
            base_stats["has_spd_boost"] = spd_boost > 1.0
            base_stats["dmg_boost_value"] = int((dmg_boost - 1.0) * 100)
            base_stats["spd_boost_value"] = int((spd_boost - 1.0) * 100)
            
        return base_stats

    def shoot(self, tower_pos, valid_enemies):
        if not valid_enemies:
            return
            
        x, y, tower_type = tower_pos
        start_x = x * self.cell_size + self.cell_size // 2
        start_y = y * self.cell_size + self.cell_size // 2
        
        # Získanie damage multiplikátora
        damage_multiplier = 1.0
        if self.game_map.map_1[y][x] == 3:  # zlaté políčko
            damage_multiplier *= 1.25
        if self.is_boosted_by_tower(x, y):  # boost od veže
            damage_multiplier *= 1.25
            
        # Získanie shop multiplikátorov
        shop_damage_mult, shop_speed_mult = self.shop.get_tower_multipliers(tower_type)
        damage_multiplier *= shop_damage_mult
        
        upgrade_type = self.tower_upgrades.get((x, y))
        
        if tower_type == 1:  # laser
            # Nastavenie firing stavu pre laser vežu
            self.firing_towers[(x, y)] = self.firing_animation_duration
            
            enemy = valid_enemies[0]
            end_x = enemy.x + enemy.cell_size // 4
            end_y = enemy.y + enemy.cell_size // 4
            
            # Overcharge efekt
            if upgrade_type == "overcharge":
                tower_pos = (x, y)
                if tower_pos not in self.overcharge_states:
                    # Inicializácia overcharge stavu
                    self.overcharge_states[tower_pos] = {
                        "active": True,
                        "timer": self.upgrades["overcharge"]["effects"]["active_time"],
                        "cooldown_timer": 0
                    }
                
                overcharge_state = self.overcharge_states[tower_pos]
                if overcharge_state["active"]:
                    damage_multiplier *= self.upgrades["overcharge"]["effects"]["damage"]
                    overcharge_state["timer"] -= 1
                    
                    # Keď vyprší active time
                    if overcharge_state["timer"] <= 0:
                        overcharge_state["active"] = False
                        overcharge_state["cooldown_timer"] = self.upgrades["overcharge"]["effects"]["cooldown_time"]
                else:  # Počas cooldownu nestrieľa
                    if overcharge_state["cooldown_timer"] > 0:
                        overcharge_state["cooldown_timer"] -= 1
                        # Po vypršaní cooldownu
                        if overcharge_state["cooldown_timer"] <= 0:
                            overcharge_state["active"] = True
                            overcharge_state["timer"] = self.upgrades["overcharge"]["effects"]["active_time"]
                        return  # Nestrieľa počas cooldownu
            
            # Kreslenie a damage pre prvý cieľ
            pygame.draw.line(self.window, (255,0,0), (start_x, start_y), (end_x, end_y), 2)
            self.laser_sound.play()
            enemy.take_damage(self.tower_types[1]["damage"] * damage_multiplier)
            if not enemy.alive and not (hasattr(enemy, 'is_dying_animation') and enemy.is_dying_animation()):
                self.economy.coins += enemy.reward
            
            # Piercing beam logika
            if upgrade_type == "piercing_beam" and len(valid_enemies) > 1:
                second_enemy = valid_enemies[1]
                second_end_x = second_enemy.x + second_enemy.cell_size // 4
                second_end_y = second_enemy.y + second_enemy.cell_size // 4
                
                pygame.draw.line(self.window, (255,0,0), (end_x, end_y), (second_end_x, second_end_y), 2)
                second_enemy.take_damage(self.tower_types[1]["damage"] * damage_multiplier * 
                                      self.upgrades["piercing_beam"]["effects"]["second_damage"])
                if not second_enemy.alive and not (hasattr(second_enemy, 'is_dying_animation') and second_enemy.is_dying_animation()):
                    self.economy.coins += second_enemy.reward
                    
        else:  # cannon alebo basic
            tower_damage = self.tower_types[tower_type]["damage"]
            
            if tower_type == 2:  # cannon
                # Nastavenie firing stavu pre cannon
                self.firing_towers[(x, y)] = self.firing_animation_duration
                
                if upgrade_type == "heavy_shells":
                    valid_enemies = valid_enemies[:1]  # len prvý nepriateľ
                    tower_damage = self.upgrades["heavy_shells"]["effects"]["damage"]
                elif upgrade_type == "cluster_bombs":
                    tower_damage = self.upgrades["cluster_bombs"]["effects"]["center_damage"]
                self.add_projectile(start_x, start_y, valid_enemies, tower_damage * damage_multiplier, 
                                  tower_type, upgrade_type)
                self.cannon_sound.play()
                
            else:  # basic tower
                # Nastavenie firing stavu pre basic vežu
                self.firing_towers[(x, y)] = self.firing_animation_duration  # nastavenie stavu strieľania
                
                if upgrade_type == "rapid_fire":
                    tower_damage = self.upgrades["rapid_fire"]["effects"]["damage"]
                elif upgrade_type == "double_shot":
                    tower_damage = self.upgrades["double_shot"]["effects"]["damage"]
                    # dva projektily
                    self.add_projectile(start_x - 5, start_y, valid_enemies, tower_damage * damage_multiplier, 
                                      tower_type)
                    self.add_projectile(start_x + 5, start_y, valid_enemies, tower_damage * damage_multiplier, 
                                      tower_type)
                    self.basic_sound.play()
                    return
                
                self.add_projectile(start_x, start_y, valid_enemies, tower_damage * damage_multiplier, 
                                  tower_type)
                self.basic_sound.play()

    def is_boosting_any_tower(self, boost_x, boost_y):
        """Kontroluje či boosting veža aktívne boostuje nejaké veže"""
        # kontrola či je boosting tower na golden tile
        is_on_gold = self.game_map.map_1[boost_y][boost_x] == 3
        max_range = 2 if is_on_gold else 1  # dvojnásobný rozsah na golden tile
        
        # kontrola všetkých veží
        for x, y, tower_type in self.tower_positions:
            if tower_type != 4:  # ignorujeme iné boosting veže
                dx = abs(x - boost_x)
                dy = abs(y - boost_y)
                if dx <= max_range and dy <= max_range:  # v dosahu podľa typu políčka
                    return True
        return False


