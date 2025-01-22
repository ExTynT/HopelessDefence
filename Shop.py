import pygame

class Shop:
    def __init__(self, window, window_width, window_height):
        self.window = window
        self.window_width = window_width
        self.window_height = window_height
        self.credits = 0
        self.current_page = "upgrades"  # or "stats"
        self.right_aligned = False  # New alignment state
        self.font = pygame.font.Font("fonts/joystix monospace.otf", 16)
        
        # Načítanie obrázkov veží pre shop
        self.tower_images = {
            "laser": pygame.transform.scale(pygame.image.load("sprites/towers/tower_1_laser.png"), (60, 60)),
            "cannon": pygame.transform.scale(pygame.image.load("sprites/towers/tower_2_cannon.png"), (60, 60)),
            "basic": pygame.transform.scale(pygame.image.load("sprites/towers/tower_3_basic.png"), (60, 60))
        }
        
        # Sledovanie upgradov pre každú vežu
        self.tower_upgrades = {
            "laser": {"damage": 0, "speed": 0},
            "cannon": {"damage": 0, "speed": 0},
            "basic": {"damage": 0, "speed": 0}
        }
        
        # Ceny upgradov
        self.base_upgrade_cost = 500  # základná cena za 10% upgrade
        self.upgrade_cost_increase = 50  # zvýšenie ceny po každom upgrade
        
        # Pozície sliderov
        self.sliders = {
            "laser_damage": {"x": 150, "y": 100, "width": 200, "height": 20, "value": 0},
            "laser_speed": {"x": 150, "y": 140, "width": 200, "height": 20, "value": 0},
            "cannon_damage": {"x": 150, "y": 220, "width": 200, "height": 20, "value": 0},
            "cannon_speed": {"x": 150, "y": 260, "width": 200, "height": 20, "value": 0},
            "basic_damage": {"x": 150, "y": 340, "width": 200, "height": 20, "value": 0},
            "basic_speed": {"x": 150, "y": 380, "width": 200, "height": 20, "value": 0}
        }
        
        # Aktívny slider (ten, ktorý práve ťaháme)
        self.active_slider = None
        
        # Načítanie shop hudby
        self.shop_music = pygame.mixer.Sound("music/shop_bg.mp3")
        self.shop_music.set_volume(0.2)
        self.is_music_playing = False

    def add_level_credits(self, coins):
        """Konvertuje zostávajúce mince z levelu na kredity"""
        self.credits += coins

    def get_upgrade_cost(self, tower_type, upgrade_type):
        """Vypočíta aktuálnu cenu upgradu"""
        current_level = self.tower_upgrades[tower_type][upgrade_type]
        return self.base_upgrade_cost + (current_level * self.upgrade_cost_increase)

    def can_afford_upgrade(self, cost):
        return self.credits >= cost

    def apply_upgrade(self, tower_type, upgrade_type):
        """Aplikuje upgrade na vežu"""
        if self.tower_upgrades[tower_type][upgrade_type] >= 10:
            return False  # Max level
        
        cost = self.get_upgrade_cost(tower_type, upgrade_type)
        if not self.can_afford_upgrade(cost):
            return False
            
        self.credits -= cost
        self.tower_upgrades[tower_type][upgrade_type] += 1
        return True

    def remove_upgrade(self, tower_type, upgrade_type):
        """Odstráni upgrade z veže a vráti kredity"""
        if self.tower_upgrades[tower_type][upgrade_type] > 0:
            self.tower_upgrades[tower_type][upgrade_type] -= 1
            cost = self.get_upgrade_cost(tower_type, upgrade_type)  # plná hodnota
            self.credits += cost  # vrátenie plnej hodnoty

    def draw_slider(self, x, y, width, height, value, max_value=10):
        """Vykreslí slider pre upgrade"""
        # Pozadie slideru
        pygame.draw.rect(self.window, (100, 100, 100), (x, y, width, height))
        
        # Aktívna časť slideru
        active_width = (width * value) / max_value
        pygame.draw.rect(self.window, (200, 200, 0), (x, y, active_width, height))
        
        # Ohraničenie slideru
        pygame.draw.rect(self.window, (255, 255, 255), (x, y, width, height), 2)

    def draw_upgrades_page(self):
        """Vykreslí stránku s upgradmi"""
        # Nadpis
        title = self.font.render("TOWER UPGRADES", True, (255, 215, 0))
        self.window.blit(title, (self.window_width//2 - title.get_width()//2, 80))
        
        # Vykreslenie pre každú vežu
        # Calculate x position based on alignment
        base_x = 50 if not self.right_aligned else self.window_width - 650
        towers = ["laser", "cannon", "basic"]
        y_offset = 150
        spacing = 140  # menší priestor medzi vežami
        
        for tower in towers:
            # Obrázok veže
            self.window.blit(self.tower_images[tower], (50, y_offset))
            
            # Názov veže
            name = tower.capitalize() + " Tower"
            name_text = self.font.render(name, True, (255, 255, 255))
            name_x = base_x + 100 if not self.right_aligned else base_x - 100
            self.window.blit(name_text, (name_x, y_offset))
            
            # Damage upgrade - positions adjusted for alignment
            dmg_x = base_x + 100 if not self.right_aligned else base_x - 100
            dmg_text = self.font.render(f"Damage +{self.tower_upgrades[tower]['damage']*10}%", True, (255, 255, 255))
            self.window.blit(dmg_text, (dmg_x, y_offset + 40))
            slider_x = base_x + 250 if not self.right_aligned else self.window_width - 450
            self.draw_slider(slider_x, y_offset + 40, 250, 20, self.tower_upgrades[tower]['damage'])
            
            # Cost pre damage upgrade - posunuté doprava
            cost = self.get_upgrade_cost(tower, "damage")
            cost_color = (255, 255, 0) if self.can_afford_upgrade(cost) else (255, 0, 0)
            cost_text = self.font.render(f"${cost}", True, cost_color)
            self.window.blit(cost_text, (570, y_offset + 40))
            
            # + a - tlačidlá pre damage - posunuté ďalej
            pygame.draw.rect(self.window, (0, 200, 0), (630, y_offset + 40, 30, 20))
            pygame.draw.rect(self.window, (200, 0, 0), (670, y_offset + 40, 30, 20))
            plus = self.font.render("+", True, (255, 255, 255))
            minus = self.font.render("-", True, (255, 255, 255))
            self.window.blit(plus, (638, y_offset + 40))
            self.window.blit(minus, (680, y_offset + 40))
            
            # Speed upgrade - väčší odstup
            speed_text = self.font.render(f"Speed +{self.tower_upgrades[tower]['speed']*10}%", True, (255, 255, 255))
            self.window.blit(speed_text, (150, y_offset + 80))
            self.draw_slider(300, y_offset + 80, 250, 20, self.tower_upgrades[tower]['speed'])
            
            # Cost pre speed upgrade - posunuté doprava
            cost = self.get_upgrade_cost(tower, "speed")
            cost_color = (255, 255, 0) if self.can_afford_upgrade(cost) else (255, 0, 0)
            cost_text = self.font.render(f"${cost}", True, cost_color)
            self.window.blit(cost_text, (570, y_offset + 80))
            
            # + a - tlačidlá pre speed - posunuté ďalej
            pygame.draw.rect(self.window, (0, 200, 0), (630, y_offset + 80, 30, 20))
            pygame.draw.rect(self.window, (200, 0, 0), (670, y_offset + 80, 30, 20))
            self.window.blit(plus, (638, y_offset + 80))
            self.window.blit(minus, (680, y_offset + 80))
            
            y_offset += spacing

    def draw_stats_page(self):
        """Vykreslí stránku so štatistikami"""
        # Nadpis
        title = self.font.render("TOWER STATS", True, (255, 215, 0))
        self.window.blit(title, (self.window_width//2 - title.get_width()//2, 80))
        
        # Calculate x position based on alignment
        base_x = 50 if not self.right_aligned else self.window_width - 650
        
        # Základné hodnoty veží
        base_stats = {
            "laser": {"damage": 1, "cooldown": 0},
            "cannon": {"damage": 12, "cooldown": 45},
            "basic": {"damage": 12, "cooldown": 20}
        }
        
        # Vykreslenie pre každú vežu
        towers = ["laser", "cannon", "basic"]
        y_offset = 150
        spacing = 140  # menší priestor medzi vežami
        
        for tower in towers:
            # Obrázok veže
            self.window.blit(self.tower_images[tower], (base_x, y_offset))
            
            # Názov veže
            name = tower.capitalize() + " Tower"
            name_text = self.font.render(name, True, (255, 255, 255))
            name_x = base_x + 100 if not self.right_aligned else base_x - 100
            self.window.blit(name_text, (name_x, y_offset))
            
            # Základné hodnoty - posunuté doprava
            base_dmg = base_stats[tower]["damage"]
            base_cd = base_stats[tower]["cooldown"]
            base_text = self.font.render(f"Base DMG: {base_dmg}  |  Base CD: {base_cd}", True, (180, 180, 180))
            self.window.blit(base_text, (300, y_offset + 30))
            
            # Damage stat s bonusom - posunuté doprava
            dmg_bonus = self.tower_upgrades[tower]['damage'] * 10
            total_dmg = base_dmg * (1 + dmg_bonus/100)
            dmg_text = self.font.render(f"Total DMG: {total_dmg:.1f} (+{dmg_bonus}%)", True, (255, 255, 255))
            self.window.blit(dmg_text, (300, y_offset + 60))
            
            # Speed stat s bonusom - posunuté doprava
            speed_bonus = self.tower_upgrades[tower]['speed'] * 10
            total_cd = base_cd / (1 + speed_bonus/100)
            speed_text = self.font.render(f"Final CD: {total_cd:.1f} (-{speed_bonus}%)", True, (255, 255, 255))
            self.window.blit(speed_text, (300, y_offset + 90))
            
            y_offset += spacing

    def draw(self, mouse_pos):
        """Vykreslí aktuálnu stránku shopu"""
        # Spustenie hudby ak ešte nehrá
        if not self.is_music_playing:
            self.shop_music.play(-1)  # -1 znamená nekonečné opakovanie
            self.is_music_playing = True
            
        # Pozadie na celé okno
        self.window.fill((30, 30, 30))
        
        # Return tlačidlo
        return_button = pygame.draw.rect(self.window, (50, 50, 50), (20, 20, 130, 40))
        return_text = self.font.render("RETURN", True, (255, 255, 255))
        self.window.blit(return_text, (35, 30))
        
        # Kredity - posunuté ďalej doľava
        credits_text = self.font.render(f"Credits: ${self.credits}", True, (255, 255, 255))
        self.window.blit(credits_text, (self.window_width - 400, 30))
        
        # Prepínacie tlačidlo - úplne na pravom okraji
        switch_button = pygame.draw.rect(self.window, (50, 50, 50), (self.window_width - 100, 20, 80, 40))
        switch_text = self.font.render("SWITCH", True, (255, 255, 255))
        self.window.blit(switch_text, (self.window_width - 95, 30))
        
        if self.current_page == "upgrades":
            self.draw_upgrades_page()
        else:
            self.draw_stats_page()
            
        return {"return": return_button, "switch": switch_button}

    def handle_click(self, pos_x, pos_y):
        """Spracuje kliknutie v shope"""
        # Kontrola return tlačidla
        return_button = pygame.Rect(20, 20, 130, 40)
        if return_button.collidepoint(pos_x, pos_y):
            self.shop_music.stop()  # zastavenie hudby pri odchode zo shopu
            self.is_music_playing = False
            return True
            
        # Kontrola prepínacieho tlačidla - nová pozícia
        if self.window_width - 100 <= pos_x <= self.window_width - 20 and 20 <= pos_y <= 60:
            self.current_page = "stats" if self.current_page == "upgrades" else "upgrades"
            return False
            
        if self.current_page == "upgrades":
            # Kontrola upgrade tlačidiel
            towers = ["laser", "cannon", "basic"]
            y_offset = 150
            spacing = 140
            
            for tower in towers:
                # Damage + button
                if 630 <= pos_x <= 660 and y_offset + 40 <= pos_y <= y_offset + 60:
                    if self.tower_upgrades[tower]["damage"] < 10:
                        cost = self.get_upgrade_cost(tower, "damage")
                        if self.apply_upgrade(tower, "damage"):
                            pass
                        else:
                            pass
                
                # Damage - button
                elif 670 <= pos_x <= 700 and y_offset + 40 <= pos_y <= y_offset + 60:
                    if self.tower_upgrades[tower]["damage"] > 0:
                        self.remove_upgrade(tower, "damage")
                        pass
                
                # Speed + button
                elif 630 <= pos_x <= 660 and y_offset + 80 <= pos_y <= y_offset + 100:
                    if self.tower_upgrades[tower]["speed"] < 10:
                        cost = self.get_upgrade_cost(tower, "speed")
                        if self.apply_upgrade(tower, "speed"):
                            pass
                        else:
                            pass
                
                # Speed - button
                elif 670 <= pos_x <= 700 and y_offset + 80 <= pos_y <= y_offset + 100:
                    if self.tower_upgrades[tower]["speed"] > 0:
                        self.remove_upgrade(tower, "speed")
                        pass
                
                y_offset += spacing
                
        return False

    def get_tower_multipliers(self, tower_type):
        """Vráti aktuálne damage a speed multiplikátory pre danú vežu"""
        if tower_type == 1:
            tower = "laser"
        elif tower_type == 2:
            tower = "cannon"
        elif tower_type == 3:
            tower = "basic"
        else:
            return 1.0, 1.0  # pre boosting tower
            
        damage_mult = 1.0 + (self.tower_upgrades[tower]["damage"] * 0.1)  # každý level je +10%
        speed_mult = 1.0 + (self.tower_upgrades[tower]["speed"] * 0.1)   # každý level je +10%
        
        return damage_mult, speed_mult 

    def stop_music(self):
        if self.is_music_playing:
            self.shop_music.stop()
            self.is_music_playing = False 