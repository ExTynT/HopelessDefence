import pygame

class Map:
    def __init__(self,level,window,window_width,window_height):
        
        self.level = level
        self.window = window
        self.window_width = window_width
        self.window_height = window_height

        self.grass = pygame.image.load("sprites/map/grass.png")
        self.stone = pygame.image.load("sprites/map/stone.jpeg")
       
    
        self.cell_size = 60                         # velkost policka - 35x35px
        grid_col = window_width // self.cell_size    # pocet stplcov
        grid_row = window_height // self.cell_size   # pocet riadkov

        # transformacie obrazkov, aby sa vošli do políčka
        self.grass_obrazok = pygame.transform.scale(self.grass, (self.cell_size, self.cell_size))
        self.stone_obrazok = pygame.transform.scale(self.stone, (self.cell_size, self.cell_size))

        # schéma mapy
        self.map_1 = [
            [2,1,0,0,0,0,0,0,0,0],
            [0,1,0,0,1,1,1,1,1,0],
            [0,1,1,1,1,0,0,0,1,0],
            [0,0,0,0,0,0,1,1,1,0],
            [0,1,1,1,1,1,1,0,0,0],
            [0,1,0,0,0,0,0,0,0,0],
            [0,1,1,1,1,1,1,1,1,0],
            [0,0,0,0,0,0,0,0,1,0],
            [0,1,1,1,1,1,1,1,1,0],
            [0,2,0,0,0,0,0,0,0,0]
        ]
    
    # kreslenie políčok
    def draw_level(self):
        for x in range(0,self.window_width,self.cell_size):
            pygame.draw.line(self.window,"black",(x,0),(x,self.window_height))
        for y in range(0,self.window_height,self.cell_size):
            pygame.draw.line(self.window,"black",(0,y),(self.window_width,y))

    # kreslenie trávy
    def draw_grass(self):
        for y, row in enumerate(self.map_1):
            for x, cell_value in enumerate(row):
                if cell_value == 0:
                    pos_x = x * self.cell_size
                    pos_y = y * self.cell_size
                    self.window.blit(self.grass_obrazok, (pos_x, pos_y))

    # kreslenie cestičky
    def draw_path(self):
        for y,row in enumerate(self.map_1):
            for x,cell_value in enumerate(row):
                if cell_value == 1 or cell_value == 2:
                    pos_x = x * self.cell_size
                    pos_y = y * self.cell_size
                    self.window.blit(self.stone_obrazok, (pos_x,pos_y))

        


        



                





        

