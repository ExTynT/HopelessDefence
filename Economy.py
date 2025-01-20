import pygame

class Economy:
    def __init__(self, window, window_width):
        self.window = window
        self.window_width = window_width
        self.coins = 150  # začiatočné množstvo peňazí (dosť na basic vežu)
        self.coin_generation_rate = 15  # 15
        self.generation_interval = 45  # 45 - generovanie
        self.generation_timer = 0
    
    def update(self):
        self.generation_timer += 1
        if self.generation_timer >= self.generation_interval:
            self.coins += self.coin_generation_rate
            self.generation_timer = 0
    
    def can_afford(self, cost):
        return self.coins >= cost
    
    def spend_coins(self, amount):
        if self.can_afford(amount):
            self.coins -= amount
            return True
        return False 