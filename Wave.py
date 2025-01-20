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
                self.enemies.append(Enemy(self.window, self.game_map, enemy_type))
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