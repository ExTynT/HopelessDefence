import pygame
from Map import Map
from Tower import Tower
from Wave import Wave

pygame.init()

GAME_WIDTH = 600 
UI_WIDTH = 200    
WIDTH = GAME_WIDTH + UI_WIDTH
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Tower Defense")

fps = 60
timer = pygame.time.Clock()

player_max_hp = 100
player_hp = player_max_hp
title_font = pygame.font.Font(None, 48)
font = pygame.font.Font(None, 36)

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
    
    # informácie o vlne
    pygame.draw.rect(screen, (60, 60, 60), (GAME_WIDTH + 15, 180, UI_WIDTH - 30, 100), border_radius=10)
    
    wave_text = font.render(f"WAVE {wave.current_wave}/4", True, (255, 215, 0))
    wave_rect = wave_text.get_rect(centerx=GAME_WIDTH + UI_WIDTH//2, y=190)
    screen.blit(wave_text, wave_rect)
    
    enemies_text = font.render("Enemies Left:", True, (255, 255, 255))
    enemies_rect = enemies_text.get_rect(centerx=GAME_WIDTH + UI_WIDTH//2, y=220)
    screen.blit(enemies_text, enemies_rect)
    
    count = wave.wave_size - wave.enemies_spawned + len(wave.enemies)
    count_text = title_font.render(f"{count}", True, (255, 215, 0))
    count_rect = count_text.get_rect(centerx=GAME_WIDTH + UI_WIDTH//2, y=250)
    screen.blit(count_text, count_rect)

# inicializácia herných objektov
game_map = Map(1,screen,GAME_WIDTH,HEIGHT)
tower = Tower(screen,GAME_WIDTH,HEIGHT,game_map)
wave = Wave(screen, game_map)

# hlavná herná slučka
run = True
while run:
    screen.fill('gray')
    timer.tick(fps)

    # spracovanie udalostí
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos_x,pos_y = pygame.mouse.get_pos()
            if pos_x < GAME_WIDTH:  # umiestňovanie veží len v hernej ploche
                if not tower.handle_menu_click(pos_x, pos_y):
                    tower.place_tower(pos_x,pos_y)

    # aktualizácia vlny a kontrola uniknutých nepriateľov
    wave.update()
    for enemy in wave.enemies[:]:  # použijeme kópiu zoznamu pre bezpečné odstránenie
        if enemy.alive and enemy.y > HEIGHT - enemy.cell_size:  # nepriateľ prešiel cez koniec mapy
            player_hp -= 10  # poškodenie za uniknutého nepriateľa
            enemy.alive = False  # označíme nepriateľa ako mŕtveho
            wave.enemies.remove(enemy)  # odstránime ho zo zoznamu

    # vykreslenie herných prvkov
    game_map.draw_level()
    game_map.draw_grass()
    game_map.draw_path()
    game_map.draw_booster()
    wave.draw()
    tower.draw_towers(wave.enemies)
    
    # vykreslenie UI
    draw_ui_panel()

    pygame.display.flip()

pygame.quit()
