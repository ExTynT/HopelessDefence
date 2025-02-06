import pygame

class Economy:
    """Trieda pre správu hernej ekonomiky"""
    def __init__(self, window, window_width):
        """Inicializácia ekonomiky"""
        self.window = window
        self.window_width = window_width
        self.coins = 150  # začiatočné množstvo peňazí (dosť na basic vežu)
        self.coin_generation_rate = 15  # 15 mincí za interval
        self.generation_interval = 45  # interval generovania mincí (45 framov)
        self.generation_timer = 0  # časovač pre generovanie mincí
    
    def update(self):
        """Aktualizácia ekonomiky a generovanie mincí"""
        self.generation_timer += 1
        if self.generation_timer >= self.generation_interval:
            self.coins += self.coin_generation_rate
            self.generation_timer = 0
    
    def can_afford(self, cost):
        """Kontrola, či je dostatok mincí na nákup"""
        return self.coins >= cost
    
    def spend_coins(self, amount):
        """Pokus o utratenie mincí, vráti True ak je úspešný"""
        if self.can_afford(amount):
            self.coins -= amount
            return True
        return False 