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
        self.menu_music.set_volume(0.2)
        self.is_music_playing = False
        
        # načítanie zvukových efektov
        self.shop_music = pygame.mixer.Sound("music/shop_bg.mp3")
        self.shop_music.set_volume(0.2)
        self.game_over_sound = pygame.mixer.Sound("music/game_over.mp3")
        self.game_over_sound.set_volume(0.3)
        self.boss_victory_sound = pygame.mixer.Sound("music/boss_victory.mp3")
        self.boss_victory_sound.set_volume(0.3)
        
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
        if not self.is_music_playing:
            self.game_over_sound.play(-1)  # loop 
            self.is_music_playing = True
        
        self.window.fill((20, 20, 20))
        
        # Nadpis
        title = self.title_font.render("Game Over", True, (255, 0, 0))
        title_rect = title.get_rect(center=(self.window_width // 2, 200))
        self.window.blit(title, title_rect)
        
        # Tlačidlo
        menu_rect = self.draw_button("Main Menu", 400, self.is_mouse_over_button("Main Menu", 400, mouse_pos))
        
        return {"menu": menu_rect}
    
    def draw_boss_victory(self, mouse_pos, hp_multiplier, income_rate):
        # Play boss victory sound if not already playing
        if not self.is_music_playing:
            self.boss_victory_sound.play(-1)  # loop 
            self.is_music_playing = True
        
        # pozadie
        self.window.fill((30, 30, 30))
        
        # nadpis
        title = self.title_font.render("BOSS DEFEATED!", True, (255, 215, 0))
        title_rect = title.get_rect(centerx=self.window_width//2, y=80)  # posunuté vyššie
        self.window.blit(title, title_rect)
        
        # štatistiky
        stats_y = 150  # posunuté vyššie
        
        # Aktuálne hodnoty
        current_text = self.font.render("CURRENT:", True, (255, 255, 255))
        current_rect = current_text.get_rect(centerx=self.window_width//2, y=stats_y)
        self.window.blit(current_text, current_rect)
        
        hp_text = self.font.render(f"Enemy HP: +{int((hp_multiplier-1)*100)}%", True, (255, 255, 255))
        hp_rect = hp_text.get_rect(centerx=self.window_width//2, y=stats_y + 35)  # menší odstup
        self.window.blit(hp_text, hp_rect)
        
        income_text = self.font.render(f"Income Rate: {income_rate}", True, (255, 255, 255))
        income_rect = income_text.get_rect(centerx=self.window_width//2, y=stats_y + 65)  # menší odstup
        self.window.blit(income_text, income_rect)
        
        # Budúce hodnoty
        next_text = self.font.render("NEXT LEVEL:", True, (255, 0, 0))
        next_rect = next_text.get_rect(centerx=self.window_width//2, y=stats_y + 110)  # menší odstup
        self.window.blit(next_text, next_rect)
        
        next_hp = self.font.render(f"Enemy HP: +{int((hp_multiplier*1.25-1)*100)}%", True, (255, 0, 0))
        next_hp_rect = next_hp.get_rect(centerx=self.window_width//2, y=stats_y + 145)  # menší odstup
        self.window.blit(next_hp, next_hp_rect)
        
        next_income = self.font.render(f"Income Rate: {max(10, income_rate-1)}", True, (255, 0, 0))
        next_income_rect = next_income.get_rect(centerx=self.window_width//2, y=stats_y + 175)  # menší odstup
        self.window.blit(next_income, next_income_rect)
        
        # tlačidlá - posunuté vyššie
        button_width = 200
        button_height = 50
        button_margin = 20
        buttons_y = stats_y + 230  # posunuté vyššie
        
        # Continue tlačidlo
        continue_button = pygame.draw.rect(self.window, (50, 50, 50),
                                         (self.window_width//2 - button_width//2,
                                          buttons_y,
                                          button_width, button_height))
        
        # Shop tlačidlo
        shop_button = pygame.draw.rect(self.window, (50, 50, 50),
                                     (self.window_width//2 - button_width//2,
                                      buttons_y + button_height + button_margin,
                                      button_width, button_height))
        
        # Menu tlačidlo
        menu_button = pygame.draw.rect(self.window, (50, 50, 50),
                                     (self.window_width//2 - button_width//2,
                                      buttons_y + (button_height + button_margin) * 2,
                                      button_width, button_height))
        
        # hover efekt
        if continue_button.collidepoint(mouse_pos):
            pygame.draw.rect(self.window, (70, 70, 70), continue_button)
        if shop_button.collidepoint(mouse_pos):
            pygame.draw.rect(self.window, (70, 70, 70), shop_button)
        if menu_button.collidepoint(mouse_pos):
            pygame.draw.rect(self.window, (70, 70, 70), menu_button)
        
        # text na tlačidlách
        continue_text = self.font.render("CONTINUE", True, (255, 215, 0))
        shop_text = self.font.render("SHOP", True, (255, 215, 0))
        menu_text = self.font.render("MENU", True, (255, 215, 0))
        
        continue_text_rect = continue_text.get_rect(center=continue_button.center)
        shop_text_rect = shop_text.get_rect(center=shop_button.center)
        menu_text_rect = menu_text.get_rect(center=menu_button.center)
        
        self.window.blit(continue_text, continue_text_rect)
        self.window.blit(shop_text, shop_text_rect)
        self.window.blit(menu_text, menu_text_rect)
        
        return {
            "continue": continue_button,
            "shop": shop_button,
            "menu": menu_button
        }
    
    def is_mouse_over_button(self, text, y_position, mouse_pos, offset_x=0):
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.window_width // 2 + offset_x, y_position))
        # Presná detekcia kolízie s textom tlačidla
        button_rect = pygame.Rect(text_rect.x, text_rect.y,
                                text_rect.width, text_rect.height)
        return button_rect.collidepoint(mouse_pos)
    
    def stop_all_sounds(self):
        """Zastaví všetky zvuky"""
        self.menu_music.stop()
        self.game_over_sound.stop()
        self.boss_victory_sound.stop()
        self.is_music_playing = False

    def start_game_timer(self):
        # zastavenie menu hudby pri začatí hry
        self.stop_all_sounds()
        self.game_start_time = pygame.time.get_ticks() / 1000  # čas v sekundách
        
    def get_completion_time(self):
        current_time = pygame.time.get_ticks() / 1000
        return current_time - self.game_start_time 