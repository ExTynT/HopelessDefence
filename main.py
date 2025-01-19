import pygame
from Map import Map
pygame.init()

WIDTH = 600
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])

fps = 60
timer = pygame.time.Clock()

run = True

while run:

    screen.fill('gray')
    timer.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    game_map = Map(1,screen,WIDTH,HEIGHT)
    game_map.draw_level()
    game_map.draw_grass()
    game_map.draw_path()



    pygame.display.flip()

pygame.quit()
