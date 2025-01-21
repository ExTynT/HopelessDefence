import pygame
import random
from Enemy import Enemy

class Wave:
    def __init__(self, window, game_map):
        self.window = window
        self.game_map = game_map
        self.enemies = []  # list na uloženie nepriateľov
        
        # nastavenie vlastností vĺn
        self.current_wave = 1
        self.wave_size = 15  # počet nepriateľov vo vlne
        self.spawn_delay = 60  # počet framov medzi spawnmi
        self.spawn_timer = 0  # časovač pre spawn
        self.enemies_spawned = 0  # počet vytvorených nepriateľov
        self.wave_complete = False  # stav dokončenia vlny
        self.available_levels = list(range(1, 5))  # dostupné levely 1-4
        self.hp_multiplier = 1.0  # násobiteľ HP nepriateľov
        
    def update_game_map(self, new_map):
        """Aktualizácia mapy pre nový level"""
        self.game_map = new_map
        # Aktualizácia pathfindingu pre existujúcich nepriateľov
        for enemy in self.enemies:
            enemy.game_map = new_map
            enemy.update_path()
        
    def get_enemy_type(self):
        if self.current_wave == 1:
            return 1
        elif self.current_wave == 2:
            return 1 if random.random() < 0.5 else 2
        elif self.current_wave == 3:
            chance = random.random()
            if chance < 0.2:
                return 1
            elif chance < 0.5:
                return 2
            else:
                return 3
        else:  # wave 4
            if self.enemies_spawned == self.wave_size - 1:  # posledný nepriateľ
                return 4
            chance = random.random()
            if chance < 0.2:
                return 1
            elif chance < 0.5:
                return 2
            else:
                return 3
    
    def start_next_wave(self):
        self.current_wave += 1
        self.enemies_spawned = 0
        self.wave_complete = False
        self.spawn_timer = 0
        
    def update(self):
        # spawn nového nepriateľa ak je to možné
        if self.enemies_spawned < self.wave_size and not self.wave_complete:
            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_delay:
                enemy_type = self.get_enemy_type()
                new_enemy = Enemy(self.window, self.game_map, enemy_type)
                new_enemy.max_health *= self.hp_multiplier  # aplikácia HP multiplikátora
                new_enemy.health = new_enemy.max_health  # nastavenie aktuálneho HP
                self.enemies.append(new_enemy)
                self.enemies_spawned += 1
                self.spawn_timer = 0
        
        # odstránenie mŕtvych nepriateľov zo zoznamu
        self.enemies = [enemy for enemy in self.enemies if enemy.alive]
        
        # kontrola či je vlna dokončená
        if self.enemies_spawned == self.wave_size and len(self.enemies) == 0:
            self.wave_complete = True
            if self.current_wave < 4:  # automaticky začať ďalšiu vlnu
                self.start_next_wave()
            
    def draw(self):
        # vykreslenie všetkých nepriateľov
        for enemy in self.enemies:
            enemy.draw()
            
    def reset(self):
        """Reset waves for new level and get random next level"""
        self.current_wave = 1
        self.wave_complete = False
        self.enemies = []
        self.enemies_spawned = 0
        self.spawn_timer = 0
        self.wave_size = 15  # Reset na prvú vlnu
        self.hp_multiplier *= 1.25  # zvýšenie HP o 25%
        
        # Náhodný výber ďalšieho levelu
        if not self.available_levels:  # ak sú všetky levely použité
            self.available_levels = list(range(1, 5))  # reset dostupných levelov (1-4)
        
        # Získanie aktuálneho levelu z game_map
        current_map = self.game_map.map_level
        
        # Ak je v available_levels len jeden level a je to ten istý ako aktuálny,
        # resetujeme available_levels
        if len(self.available_levels) == 1 and self.available_levels[0] == current_map:
            self.available_levels = list(range(1, 5))
            self.available_levels.remove(current_map)
        
        # Odstránenie aktuálneho levelu z možností, ak tam je
        if current_map in self.available_levels:
            self.available_levels.remove(current_map)
            
        next_level = random.choice(self.available_levels)
        self.available_levels.remove(next_level)  # odstránenie použitého levelu
        return next_level 