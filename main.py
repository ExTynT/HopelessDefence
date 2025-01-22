import pygame
from Map import Map
from Tower import Tower
from Wave import Wave
from Economy import Economy
from Menus import Menus
from Shop import Shop

pygame.init()
pygame.mixer.init()

GAME_WIDTH = 600 
UI_WIDTH = 200    
WIDTH = GAME_WIDTH + UI_WIDTH
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Hopeless Defence")

fps = 60
timer = pygame.time.Clock()

# načítanie hernej hudby
current_music_track = 1
game_music = pygame.mixer.Sound(f"music/{current_music_track}_bg.mp3")
game_music.set_volume(0.2)  # nižšia hlasitosť pre hudbu v pozadí
is_game_music_playing = False

def change_background_music():
    global current_music_track, game_music, is_game_music_playing
    game_music.stop()
    current_music_track = current_music_track % 4 + 1  # cykluje od 1 do 4
    game_music = pygame.mixer.Sound(f"music/{current_music_track}_bg.mp3")
    game_music.set_volume(0.2)
    game_music.play(-1)  # -1 means loop indefinitely
    is_game_music_playing = True

def init_game():
    global player_hp, player_max_hp, game_map, economy, tower, wave, is_game_music_playing, game_music, current_music_track, shop
    player_max_hp = 100
    player_hp = player_max_hp
    game_map = Map(1,screen,GAME_WIDTH,HEIGHT)  # 1 je číslo mapy, nie levelu
    economy = Economy(screen, GAME_WIDTH)
    shop = Shop(screen, GAME_WIDTH, HEIGHT)
    tower = Tower(screen,GAME_WIDTH,HEIGHT,game_map,economy,shop)
    wave = Wave(screen, game_map)
    # načítanie a spustenie hernej hudby
    if not is_game_music_playing:
        current_music_track = 1
        game_music = pygame.mixer.Sound(f"music/{current_music_track}_bg.mp3")
        game_music.set_volume(0.2)
        game_music.play(-1)  # -1 means loop indefinitely
        is_game_music_playing = True
    # Reset menu music state
    menus.is_music_playing = False

def draw_ui_panel():
    # vykreslenie pozadia UI
    pygame.draw.rect(screen, (40, 40, 40), (GAME_WIDTH, 0, UI_WIDTH, HEIGHT))
    
    # nadpis
    title = title_font.render("STATS", True, (255, 215, 0))
    title_rect = title.get_rect(centerx=GAME_WIDTH + UI_WIDTH//2, y=20)
    screen.blit(title, title_rect)
    
    # oddeľovacia čiara
    pygame.draw.line(screen, (255, 215, 0), 
                    (GAME_WIDTH + 20, 60), 
                    (WIDTH - 20, 60), 3)
    
    # vykreslenie HP baru
    hp_text = font.render("HP:", True, (255, 255, 255))
    screen.blit(hp_text, (GAME_WIDTH + 20, 80))
    
    hp_bar_width = UI_WIDTH - 40
    hp_bar_height = 20
    # pozadie HP baru (červené)
    pygame.draw.rect(screen, (200, 0, 0), 
                    (GAME_WIDTH + 20, 110, hp_bar_width, hp_bar_height))
    # HP bar (zelený)
    hp_percentage = player_hp / player_max_hp
    pygame.draw.rect(screen, (0, 200, 0), 
                    (GAME_WIDTH + 20, 110, hp_bar_width * hp_percentage, hp_bar_height))
    
    hp_value = font.render(f"{player_hp}/{player_max_hp}", True, (255, 255, 255))
    hp_value_rect = hp_value.get_rect(centerx=GAME_WIDTH + UI_WIDTH//2, y=140)
    screen.blit(hp_value, hp_value_rect)
    
    # vykreslenie levelu
    # box pre level
    level_box = pygame.draw.rect(screen, (60, 60, 60), 
                              (GAME_WIDTH + 15, 165, UI_WIDTH - 30, 85), 
                              border_radius=10)
    
    level_text = font.render("LEVEL:", True, (255, 215, 0))
    level_rect = level_text.get_rect(centerx=GAME_WIDTH + UI_WIDTH//2, y=175)
    screen.blit(level_text, level_rect)
    
    level_value = title_font.render(str(game_map.level), True, (255, 215, 0))
    level_value_rect = level_value.get_rect(centerx=GAME_WIDTH + UI_WIDTH//2, y=205)
    screen.blit(level_value, level_value_rect)
    
    # vykreslenie coinov
    coins_text = font.render("COINS:", True, (255, 215, 0))
    coins_rect = coins_text.get_rect(x=GAME_WIDTH + 20, y=260)
    screen.blit(coins_text, coins_rect)
    
    coins_value = title_font.render(str(economy.coins), True, (255, 215, 0))
    coins_value_rect = coins_value.get_rect(centerx=GAME_WIDTH + UI_WIDTH//2, y=290)
    screen.blit(coins_value, coins_value_rect)
    
    # informácie o vlne
    pygame.draw.rect(screen, (60, 60, 60), (GAME_WIDTH + 15, 330, UI_WIDTH - 30, 120), border_radius=10)

    wave_text = font.render(f"WAVE {wave.current_wave}/4", True, (255, 215, 0))
    wave_rect = wave_text.get_rect(centerx=GAME_WIDTH + UI_WIDTH//2, y=340)
    screen.blit(wave_text, wave_rect)
    
    enemies_text = font.render("ENEMIES", True, (255, 255, 255))
    enemies_rect = enemies_text.get_rect(centerx=GAME_WIDTH + UI_WIDTH//2, y=380)
    screen.blit(enemies_text, enemies_rect)
    
    count = wave.wave_size - wave.enemies_spawned + len(wave.enemies)
    count_text = title_font.render(f"{count}", True, (255, 215, 0))
    count_rect = count_text.get_rect(centerx=GAME_WIDTH + UI_WIDTH//2, y=405)
    screen.blit(count_text, count_rect)
    
    # tlačidlo pre návrat do menu
    menu_button = pygame.draw.rect(screen, (40, 40, 40),
                                 (GAME_WIDTH + 20, HEIGHT - 60, UI_WIDTH - 40, 40))
    menu_text = font.render("Menu", True, (255, 215, 0))
    menu_rect = menu_text.get_rect(center=menu_button.center)
    screen.blit(menu_text, menu_rect)
    
    return menu_button  # vrátime rect tlačidla pre detekciu kliknutia

def draw_game_screen():
    # vykreslenie herných prvkov
    game_map.draw_level()
    game_map.draw_grass()
    game_map.draw_path()
    game_map.draw_booster()
    wave.draw()
    tower.draw_towers(wave.enemies)
    return draw_ui_panel()  # vrátime rect menu tlačidla

title_font = pygame.font.Font("fonts/joystix monospace.otf", 32)
font = pygame.font.Font("fonts/joystix monospace.otf", 20)

# inicializácia menu
menus = Menus(screen, WIDTH, HEIGHT)
shop = Shop(screen, GAME_WIDTH, HEIGHT)  # pridanie globálnej inštancie shopu

# hlavná herná slučka
run = True
game_state = "menu"  # menu, game, pause, win, game_over, boss_victory
completion_time = 0  # čas dokončenia hry

def update_game():
    global game_state, player_hp, game_map, is_game_music_playing
    # aktualizácia vlny a kontrola uniknutých nepriateľov
    wave.update()
    for enemy in wave.enemies[:]:
        # výpočet pozície v mriežke
        grid_x = int(enemy.x // enemy.cell_size)
        grid_y = int(enemy.y // enemy.cell_size)
        
        # kontrola či je nepriateľ na konci cesty (hodnota 4)
        if enemy.alive and 0 <= grid_x < len(game_map.map_1[0]) and 0 <= grid_y < len(game_map.map_1):
            if game_map.map_1[grid_y][grid_x] == 4:
                if enemy.enemy_type == 4:  # ak je to boss
                    player_hp -= 80
                else:
                    player_hp -= 10
                enemy.alive = False
                wave.enemies.remove(enemy)
                if player_hp <= 0:
                    game_music.stop()  # zastavenie hernej hudby pri game over
                    is_game_music_playing = False
                    menus.is_music_playing = False  # Reset menu music state
                    game_state = "game_over"
    
    # kontrola výhry v leveli
    if wave.current_wave == 4 and wave.wave_complete and len(wave.enemies) == 0:
        game_music.stop()  # zastavenie hernej hudby pri boss victory
        is_game_music_playing = False
        game_state = "boss_victory"
        return

    # aktualizácia ekonomiky
    economy.update()

while run:
    screen.fill('gray')
    timer.tick(fps)
    mouse_pos = pygame.mouse.get_pos()

    # spracovanie udalostí
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "menu":
                buttons = menus.draw_main_menu(mouse_pos)
                if buttons["play"].collidepoint(mouse_pos):
                    game_state = "game"
                    init_game()
                    menus.start_game_timer()
                elif buttons["exit"].collidepoint(mouse_pos):
                    run = False
                    
            elif game_state in ["win", "game_over", "boss_victory"]:
                if game_state == "boss_victory":
                    buttons = menus.draw_boss_victory(mouse_pos, wave.hp_multiplier, economy.coin_generation_rate)
                    if buttons["continue"].collidepoint(mouse_pos):
                        # Zastavenie boss victory hudby
                        menus.stop_all_sounds()
                        # Zmena hudby na ďalšiu skladbu
                        change_background_music()
                        
                        # Predaj všetkých veží
                        for tower_pos in tower.tower_positions[:]:
                            x, y, tower_type = tower_pos
                            base_cost = tower.tower_types[tower_type]['cost']
                            if game_map.map_1[y][x] == 3:  # ak je na zlatom políčku
                                base_cost = int(base_cost * 1.5)
                            sell_price = int(base_cost * 0.75)
                            economy.coins += sell_price
                        tower.tower_positions.clear()  # Odstránenie všetkých veží
                        
                        # Reset peňazí a zníženie income
                        economy.coins = 150  # Reset na základnú hodnotu
                        economy.coin_generation_rate = max(10, economy.coin_generation_rate - 1)  # Zníženie o 1, minimum 10
                        
                        # Prechod na ďalší level
                        next_level = wave.reset()  # Získanie náhodného ďalšieho levelu
                        current_level = game_map.level + 1  # Zachovanie a zvýšenie čísla levelu
                        game_map = Map(next_level, screen, GAME_WIDTH, HEIGHT)
                        game_map.level = current_level  # Nastavenie správneho čísla levelu
                        wave.update_game_map(game_map)  # Aktualizácia mapy vo Wave class
                        tower.update_game_map(game_map)  # Aktualizácia mapy v Tower class
                        game_state = "game"
                    elif buttons["menu"].collidepoint(mouse_pos):
                        menus.stop_all_sounds()
                        game_music.stop()
                        is_game_music_playing = False
                        game_state = "menu"
                    elif buttons["shop"].collidepoint(mouse_pos):  # nové tlačidlo pre shop
                        menus.stop_all_sounds()  # zastavenie boss victory hudby
                        game_music.stop()  # zastavenie hernej hudby pri vstupe do shopu
                        is_game_music_playing = False
                        shop.add_level_credits(economy.coins)  # konvertovanie mincí na kredity
                        economy.coins = 0
                        game_state = "shop"
                else:
                    buttons = menus.draw_win_screen(mouse_pos, completion_time) if game_state == "win" else menus.draw_game_over(mouse_pos)
                    if buttons["menu"].collidepoint(mouse_pos):
                        menus.stop_all_sounds()
                        game_music.stop()  # zastavenie hernej hudby pri návrate do menu
                        is_game_music_playing = False
                        game_state = "menu"
                    
            elif game_state == "game":
                menu_button = draw_game_screen()
                if menu_button.collidepoint(mouse_pos):
                    game_music.stop()  # zastavenie hernej hudby pri návrate do menu
                    is_game_music_playing = False
                    game_state = "menu"
                elif mouse_pos[0] < GAME_WIDTH:  # umiestňovanie veží len v hernej ploche
                    if event.button == 3:  # pravé tlačidlo
                        tower.place_tower(mouse_pos[0], mouse_pos[1], True)
                    elif event.button == 1:  # ľavé tlačidlo
                        if not tower.handle_menu_click(mouse_pos[0], mouse_pos[1]):
                            if not tower.handle_upgrade_click(mouse_pos[0], mouse_pos[1]):
                                if not tower.handle_sell_click(mouse_pos[0], mouse_pos[1]):
                                    tower.place_tower(mouse_pos[0], mouse_pos[1], False)

            elif game_state == "shop":
                buttons = shop.draw(mouse_pos)
                if buttons["return"].collidepoint(mouse_pos):
                    shop.stop_music()  # zastavenie shop hudby
                    game_state = "boss_victory"  # návrat na boss victory screen
                elif buttons["switch"].collidepoint(mouse_pos):
                    shop.current_page = "stats" if shop.current_page == "upgrades" else "upgrades"
                else:
                    # Spracovanie kliknutí na upgrady
                    shop.handle_click(mouse_pos[0], mouse_pos[1])

    # aktualizácia a vykreslenie podľa herného stavu
    if game_state == "menu":
        menus.draw_main_menu(mouse_pos)
        
    elif game_state == "game":
        update_game()
        draw_game_screen()
        
    elif game_state == "win":
        menus.draw_win_screen(mouse_pos, completion_time)
        
    elif game_state == "game_over":
        menus.draw_game_over(mouse_pos)

    elif game_state == "boss_victory":
        menus.draw_boss_victory(mouse_pos, wave.hp_multiplier, economy.coin_generation_rate)

    elif game_state == "shop":
        shop.draw(mouse_pos)

    pygame.display.flip()

pygame.quit()
