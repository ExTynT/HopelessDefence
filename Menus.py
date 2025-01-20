import pygame

class Menus:
    def __init__(self, window, window_width, window_height):
        self.window = window
        self.window_width = window_width
        self.window_height = window_height
        # načítanie pixelového písma
        self.title_font = pygame.font.Font("fonts/joystix monospace.otf", 48)
        self.font = pygame.font.Font("fonts/joystix monospace.otf", 24)
        self.current_menu = "main"  # main, pause, win, game_over
        self.game_start_time = 0
        
        # inicializácia menu hudby
        pygame.mixer.init()
        self.menu_music = pygame.mixer.Sound("music/Pixel_Dream_menu.mp3")
        self.menu_music.set_volume(0.5)  # nastavenie hlasitosti na 50%
        self.is_music_playing = False
        
        # načítanie pozadia menu
        self.menu_background = pygame.image.load("sprites/menu/background.png")
        self.menu_background = pygame.transform.scale(self.menu_background, (window_width, window_height))
        
    def draw_button(self, text, y_position, selected=False, offset_x=0):
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.window_width // 2 + offset_x, y_position))
        self.window.blit(text_surface, text_rect)
        return text_rect
        
    def draw_main_menu(self, mouse_pos):
        # spustenie hudby ak ešte nehrá
        if not self.is_music_playing:
            self.menu_music.play(-1)  # -1 znamená nekonečné opakovanie
            self.is_music_playing = True

        # vykreslenie pozadia
        self.window.blit(self.menu_background, (0, 0))
        
        # Vykreslenie tieňa pre hrubší efekt
        title_shadow = self.title_font.render("Hopeless    Defence", True, (0, 0, 0))
        title_rect = title_shadow.get_rect(center=(self.window_width // 2, 100))
        # Vykreslenie textu viackrát s malým posunom pre hrubší efekt
        for offset in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
            shadow_rect = title_rect.copy()
            shadow_rect.x += offset[0]
            shadow_rect.y += offset[1]
            self.window.blit(title_shadow, shadow_rect)
        # Hlavný text
        self.window.blit(title_shadow, title_rect)
        
        # Tmavý pruh na spodku
        bottom_bar_height = 60
        bottom_bar = pygame.Surface((self.window_width, bottom_bar_height))
        bottom_bar.fill((20, 20, 20))
        bottom_bar.set_alpha(230)  # mierne priehľadný
        self.window.blit(bottom_bar, (0, self.window_height - bottom_bar_height))
        
        # Tlačidlá
        button_y = self.window_height - bottom_bar_height//2
        play_rect = self.draw_button("Play", button_y, self.is_mouse_over_button("Play", button_y, mouse_pos), offset_x=-100)
        exit_rect = self.draw_button("Exit", button_y, self.is_mouse_over_button("Exit", button_y, mouse_pos), offset_x=100)
        
        # Oddeľovač medzi tlačidlami
        separator_height = 20
        pygame.draw.line(self.window, (255, 255, 255),
                        (self.window_width//2, self.window_height - bottom_bar_height + (bottom_bar_height-separator_height)//2),
                        (self.window_width//2, self.window_height - bottom_bar_height + (bottom_bar_height+separator_height)//2),
                        2)
        
        return {"play": play_rect, "exit": exit_rect}
        
    def draw_pause_menu(self, mouse_pos):
        # Polopriehľadné pozadie
        overlay = pygame.Surface((self.window_width, self.window_height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.window.blit(overlay, (0, 0))
        
        # Nadpis
        title = self.title_font.render("Paused", True, (255, 215, 0))
        title_rect = title.get_rect(center=(self.window_width // 2, 200))
        self.window.blit(title, title_rect)
        
        # Tlačidlá
        continue_rect = self.draw_button("Continue", 350, self.is_mouse_over_button("Continue", 350, mouse_pos))
        menu_rect = self.draw_button("Main Menu", 450, self.is_mouse_over_button("Main Menu", 450, mouse_pos))
        
        return {"continue": continue_rect, "menu": menu_rect}
        
    def draw_win_screen(self, mouse_pos, completion_time):
        self.window.fill((20, 20, 20))
        
        # Nadpis
        title = self.title_font.render("Victory!", True, (255, 215, 0))
        title_rect = title.get_rect(center=(self.window_width // 2, 150))
        self.window.blit(title, title_rect)
        
        # Čas dokončenia
        minutes = int(completion_time // 60)
        seconds = int(completion_time % 60)
        time_text = self.font.render(f"Completion Time: {minutes}:{seconds:02d}", True, (255, 255, 255))
        time_rect = time_text.get_rect(center=(self.window_width // 2, 250))
        self.window.blit(time_text, time_rect)
        
        # Tlačidlo
        menu_rect = self.draw_button("Main Menu", 400, self.is_mouse_over_button("Main Menu", 400, mouse_pos))
        
        return {"menu": menu_rect}
        
    def draw_game_over(self, mouse_pos):
        self.window.fill((20, 20, 20))
        
        # Nadpis
        title = self.title_font.render("Game Over", True, (255, 0, 0))
        title_rect = title.get_rect(center=(self.window_width // 2, 200))
        self.window.blit(title, title_rect)
        
        # Tlačidlo
        menu_rect = self.draw_button("Main Menu", 400, self.is_mouse_over_button("Main Menu", 400, mouse_pos))
        
        return {"menu": menu_rect}
    
    def draw_boss_victory(self, mouse_pos, hp_multiplier, income_rate):
        # vykreslenie pozadia
        self.window.fill((40, 40, 40))
        
        # nadpis
        title = self.title_font.render("BOSS DEFEATED!", True, (255, 215, 0))
        title_rect = title.get_rect(center=(self.window_width // 2, 100))
        self.window.blit(title, title_rect)
        
        # vykreslenie modifierov
        modifiers_text = self.font.render("CURRENT MODIFIERS:", True, (255, 255, 255))
        modifiers_rect = modifiers_text.get_rect(center=(self.window_width // 2, 200))
        self.window.blit(modifiers_text, modifiers_rect)
        
        # HP modifier
        hp_text = self.font.render(f"Enemy HP: +{int((hp_multiplier - 1) * 100)}%", True, (255, 100, 100))
        hp_rect = hp_text.get_rect(center=(self.window_width // 2, 250))
        self.window.blit(hp_text, hp_rect)
        
        # Income modifier
        income_text = self.font.render(f"Income Rate: {income_rate}/s", True, (255, 215, 0))
        income_rect = income_text.get_rect(center=(self.window_width // 2, 300))
        self.window.blit(income_text, income_rect)
        
        # Next level info
        next_info = self.font.render("Next Level:", True, (255, 255, 255))
        next_info_rect = next_info.get_rect(center=(self.window_width // 2, 350))
        self.window.blit(next_info, next_info_rect)
        
        # HP increase info
        hp_increase_text = self.font.render("- Enemy HP +25%", True, (255, 100, 100))
        hp_increase_rect = hp_increase_text.get_rect(center=(self.window_width // 2, 380))
        self.window.blit(hp_increase_text, hp_increase_rect)
        
        changes_text = self.font.render("- Income -1/s", True, (255, 100, 100))
        changes_rect = changes_text.get_rect(center=(self.window_width // 2, 410))
        self.window.blit(changes_text, changes_rect)
        
        coins_text = self.font.render("- Coins reset to 150", True, (255, 100, 100))
        coins_rect = coins_text.get_rect(center=(self.window_width // 2, 440))
        self.window.blit(coins_text, coins_rect)
        
        # tlačidlá
        continue_text = self.font.render("Continue", True, (255, 215, 0))
        continue_rect = continue_text.get_rect(center=(self.window_width // 2 - 100, 500))
        self.window.blit(continue_text, continue_rect)
        
        menu_text = self.font.render("Menu", True, (255, 215, 0))
        menu_rect = menu_text.get_rect(center=(self.window_width // 2 + 100, 500))
        self.window.blit(menu_text, menu_rect)
        
        # zvýraznenie tlačidiel pri hover
        if self.is_mouse_over_button("Continue", 500, mouse_pos, -100):
            pygame.draw.rect(self.window, (255, 215, 0), continue_rect, 2)
        if self.is_mouse_over_button("Menu", 500, mouse_pos, 100):
            pygame.draw.rect(self.window, (255, 215, 0), menu_rect, 2)
        
        return {
            "continue": continue_rect,
            "menu": menu_rect
        }
    
    def is_mouse_over_button(self, text, y_position, mouse_pos, offset_x=0):
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.window_width // 2 + offset_x, y_position))
        # Presná detekcia kolízie s textom tlačidla
        button_rect = pygame.Rect(text_rect.x, text_rect.y,
                                text_rect.width, text_rect.height)
        return button_rect.collidepoint(mouse_pos)
    
    def start_game_timer(self):
        # zastavenie menu hudby pri začatí hry
        self.menu_music.stop()
        self.is_music_playing = False
        self.game_start_time = pygame.time.get_ticks() / 1000  # čas v sekundách
        
    def get_completion_time(self):
        current_time = pygame.time.get_ticks() / 1000
        return current_time - self.game_start_time 