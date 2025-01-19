import pygame
from Enemy import Enemy

class Wave:
    def __init__(self, window, game_map):
        self.window = window
        self.game_map = game_map
        self.enemies = []  # list na uloženie nepriateľov
        
        # nastavenie vlastností vlny
        self.wave_size = 15  # počet nepriateľov vo vlne
        self.spawn_delay = 60  # počet framov medzi spawnmi
        self.spawn_timer = 0  # časovač pre spawn
        self.enemies_spawned = 0  # počet vytvorených nepriateľov
        self.wave_complete = False  # stav dokončenia vlny
        
    def update(self):
        # spawn nového nepriateľa ak je to možné
        if self.enemies_spawned < self.wave_size:
            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_delay:
                self.enemies.append(Enemy(self.window, self.game_map))
                self.enemies_spawned += 1
                self.spawn_timer = 0
        
        # odstránenie mŕtvych nepriateľov zo zoznamu
        self.enemies = [enemy for enemy in self.enemies if enemy.alive]
        
        # kontrola či je vlna dokončená
        if self.enemies_spawned == self.wave_size and len(self.enemies) == 0:
            self.wave_complete = True
            
    def draw(self):
        # vykreslenie všetkých nepriateľov
        for enemy in self.enemies:
            enemy.draw() 