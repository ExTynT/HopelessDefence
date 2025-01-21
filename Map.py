import pygame

class Map:
    def __init__(self,level,window,window_width,window_height):
        
        self.level = 1  # Začíname od levelu 1
        self.map_level = level  # Číslo mapy (1-4)
        self.window = window
        self.window_width = window_width
        self.window_height = window_height

        self.grass = pygame.image.load("sprites/map/grass.png")
        self.stone = pygame.image.load("sprites/map/stone.jpeg")
        self.gold = pygame.image.load("sprites/map/gold.png")
       
    
        self.cell_size = 60                         # velkost policka - 60x60px
        grid_col = window_width // self.cell_size    # pocet stlpcov
        grid_row = window_height // self.cell_size   # pocet riadkov

        # transformacie obrazkov, aby sa vošli do políčka
        self.grass_obrazok = pygame.transform.scale(self.grass, (self.cell_size, self.cell_size))
        self.stone_obrazok = pygame.transform.scale(self.stone, (self.cell_size, self.cell_size))
        self.gold = pygame.transform.scale(self.gold, (self.cell_size, self.cell_size))

        # schémy máp (10 levelov)
        self.maps = {
            1: [ # Pôvodná mapa
                [2,1,0,0,0,0,0,0,0,0],
                [0,1,0,0,1,1,1,1,1,0],
                [0,1,1,1,1,3,0,0,1,0],
                [0,0,0,0,0,0,1,1,1,0],
                [0,1,1,1,1,1,1,0,0,0],
                [0,1,0,0,0,0,0,0,0,0],
                [0,1,1,1,1,1,1,1,1,0],
                [0,0,0,0,0,0,0,3,1,0],
                [0,1,1,1,1,1,1,1,1,0],
                [0,4,0,0,0,0,0,0,0,0]
            ],
            2: [ 
                [2,1,0,0,0,0,0,0,3,0],
                [0,1,0,1,1,1,1,1,1,0],
                [0,1,0,1,0,0,0,0,1,0],
                [0,1,0,1,0,1,1,1,1,0],
                [0,1,0,1,0,1,3,0,0,0],
                [0,1,0,1,0,1,1,1,1,0],
                [0,1,0,1,0,0,0,0,1,0],
                [0,1,3,1,0,4,0,0,1,0],
                [0,1,1,1,0,1,1,1,1,0],
                [0,0,0,0,0,0,0,0,0,0]
            ],
            3: [ 
                [2,1,0,1,1,1,1,1,0,0],
                [0,1,0,1,0,0,0,1,0,0],
                [0,1,0,1,0,0,0,1,0,0],
                [0,1,0,1,0,0,3,1,0,0],
                [0,1,0,1,0,0,0,1,0,0],
                [0,1,0,1,0,1,1,1,0,0],
                [0,1,0,1,0,1,0,0,0,0],
                [0,1,3,1,0,1,1,1,1,0],
                [0,1,1,1,0,0,0,3,1,0],
                [0,0,0,0,0,0,0,0,4,0]
            ],
            4: [ 
                [0,0,0,0,2,0,0,0,0,0],
                [1,1,1,0,1,0,1,1,1,0],
                [1,0,1,0,1,0,1,3,1,0],
                [1,0,1,0,1,0,1,0,1,0],
                [1,0,1,0,1,1,1,0,1,0],
                [1,0,1,3,0,0,0,0,1,0],
                [1,0,1,1,1,1,1,1,1,0],
                [1,0,0,0,3,0,0,0,0,0],
                [1,1,1,1,1,1,1,1,1,4],
                [0,0,0,0,0,0,0,0,0,0]
            ]
        }

        # nastavenie aktuálnej mapy podľa levelu
        self.map_1 = self.maps[level]
    
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
                if cell_value == 1 or cell_value == 2 or cell_value == 4:
                    pos_x = x * self.cell_size
                    pos_y = y * self.cell_size
                    self.window.blit(self.stone_obrazok, (pos_x,pos_y))

    # kreslenie boosterov
    def draw_booster(self):
        for y,row in enumerate(self.map_1):
            for x,cell_value in enumerate(row):
                if cell_value == 3:
                    pos_x = x * self.cell_size
                    pos_y = y * self.cell_size
                    self.window.blit(self.gold,(pos_x,pos_y)) 

        


        



                





        

