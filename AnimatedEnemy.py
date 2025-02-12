import pygame
from Enemy import Enemy

class AnimatedEnemy(Enemy):
    def __init__(self, window, game_map, enemy_type=1, hp_multiplier=1):
        super().__init__(window, game_map, enemy_type, hp_multiplier)
        
        # Základné nastavenia pre všetky typy
        self.target_size = (int(self.cell_size * 0.8), int(self.cell_size * 0.8))  # 80% veľkosti bunky
        if enemy_type == 4:  # menšia veľkosť pre bossa
            self.target_size = (int(self.cell_size * 0.7), int(self.cell_size * 0.7))  # 70% veľkosti bunky
        # Offsety pre centrovanie v bunke
        self.sprite_offset_x = (self.cell_size - self.target_size[0]) // 2  # horizontálne centrovanie
        # Posunutie sprite vyššie od spodku bunky 
        self.sprite_offset_y = ((self.cell_size - self.target_size[1]) // 2) - 20
        self.frame = 0
        self.animation_speed = 0.2
        self.animation_timer = 0
        self.is_taking_damage = False
        self.damage_animation_timer = 0
        self.damage_animation_duration = 100  # 100 millisekúnd
        self.last_laser_hit_time = 0
        self.is_dying = False
        self.death_frame = 0
        self.death_animation_timer = 0
        self.death_animation_speed = 0.3  # Spomalenie death animácie 
        self.death_position = None
        self.last_direction = "down"  # Nastavenie počiatočného smeru na dole
        self.rotation = 0  # Pridanie rotácie
        self.flip_x = False  # Pridanie flip pre horizontálne otočenie
        
        if enemy_type == 1:
            try:
                # Načítanie len jedného spritesheetu pre všetky smery
                self.sprite = pygame.image.load("sprites/enemies/1/crow_walk.png").convert_alpha()
                self.damage_sprite = pygame.image.load("sprites/enemies/1/crow_damage.png").convert_alpha()
                self.frame_count = 4
                self.death_frame_count = 4
                
                # Získanie rozmerov spritesheetu
                sheet_width = self.sprite.get_width()
                self.frame_width = sheet_width // self.frame_count
                self.frame_height = self.sprite.get_height()
                
                # Načítanie damage framu (len prvý frame)
                damage_frame_surface = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
                damage_frame_surface.blit(self.damage_sprite, (0, 0), 
                                       (0, 0, self.frame_width, self.frame_height))
                self.damage_frame = pygame.transform.scale(damage_frame_surface, self.target_size)
                
                # Načítanie death framov zo samostatných súborov
                self.death_frames = []
                try:
                    # Načítanie death spritesheetu
                    death_spritesheet = pygame.image.load("sprites/enemies/1/crow_death2.png").convert_alpha()
                    
                    # Presné rozmery pre každý frám
                    frame_width = 64  # presná šírka jedného framu
                    frame_height = 64  # presná výška jedného framu
                    
                    # Rozdelenie na 4 framy s presnými pozíciami
                    frame_positions = [
                        (0, 0),       # prvý 
                        (64, 0),      # druhý 
                        (128, 0),     # tretí 
                        (192, 0)      # štvrtý 
                    ]
                    
                    for x_pos, y_pos in frame_positions:
                        # Vytvorenie nového surface s alpha kanálom
                        frame_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                        
                        # Vyrezanie framu s presnými rozmermi
                        frame_rect = (x_pos, y_pos, frame_width, frame_height)
                        frame_surface.blit(death_spritesheet, (0, 0), frame_rect)
                        
                        # Škálovanie na cieľovú veľkosť
                        scaled_frame = pygame.transform.scale(frame_surface, self.target_size)
                        self.death_frames.append(scaled_frame)
                        
                except Exception as e:
                    print(f"Error loading death spritesheet: {e}")
                
                # Načítanie prvého framu
                self.current_frame = self.get_frame(0)
                
            except Exception as e:
                print(f"Error loading enemy sprites: {e}")
                self.sprite = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
                self.frame_count = 1
                self.current_frame = self.sprite
            
            self.reward = 15
        elif enemy_type == 2:  # Worm
            try:
                # Načítanie spritesheetov pre worm-a
                self.sprite = pygame.image.load("sprites/enemies/2/Walk.png").convert_alpha()
                self.damage_sprite = pygame.image.load("sprites/enemies/2/Get Hit.png").convert_alpha()
                self.death_sprite = pygame.image.load("sprites/enemies/2/Death.png").convert_alpha()
                self.frame_count = 9  # počet fremov v walk animácii
                self.death_frame_count = 4  # posledné 4 framy z Death.png
                self.animation_speed = 0.1  # rýchlosť walk animácie
                self.death_animation_speed = 0.1  # rýchlosť death animácie
                
                # Získanie rozmerov spritesheetu
                sheet_width = self.sprite.get_width()
                self.frame_width = sheet_width // self.frame_count  # šírka jedného framu
                self.frame_height = self.sprite.get_height()  # výška framu
                
                # Načítanie damage framu (druhý frame z Get Hit animácie)
                damage_frame_surface = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
                damage_frame_surface.blit(self.damage_sprite, (0, 0), 
                                       (self.frame_width, 0, self.frame_width, self.frame_height))  # druhý frame
                self.damage_frame = pygame.transform.scale(damage_frame_surface, self.target_size)
                
                # Načítanie death framov (posledné 4 framy z Death.png)
                self.death_frames = []
                try:
                    death_sheet_width = self.death_sprite.get_width()
                    total_death_frames = death_sheet_width // self.frame_width
                    
                    # Načítanie posledných 4 framov
                    for i in range(total_death_frames - 4, total_death_frames):
                        frame_surface = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
                        frame_rect = (i * self.frame_width, 0, self.frame_width, self.frame_height)
                        frame_surface.blit(self.death_sprite, (0, 0), frame_rect)
                        scaled_frame = pygame.transform.scale(frame_surface, self.target_size)
                        self.death_frames.append(scaled_frame)
                        
                except Exception as e:
                    print(f"Error loading worm death animation: {e}")
                
                # Načítanie prvého framu
                self.current_frame = self.get_frame(0)
                
            except Exception as e:
                print(f"Error loading worm sprites: {e}")
                self.sprite = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
                self.frame_count = 1
                self.current_frame = self.sprite
            
            self.reward = 25
            self.speed = 2.5  # rýchlosť pohybu
        elif enemy_type == 3:  # Golem
            try:
                # Načítanie spritesheetov pre golem-a
                self.sprite = pygame.image.load("sprites/enemies/3/Golem_Armor_Run.png").convert_alpha()
                self.damage_sprite = pygame.image.load("sprites/enemies/3/Golem_Armor_Hit.png").convert_alpha()
                self.frame_count = 4  # počet framov v run animácii
                self.death_frame_count = 3  # počet framov v armor break animácii
                self.animation_speed = 0.2
                self.death_animation_speed = 0.2
                
                # Získanie rozmerov spritesheetu
                sheet_width = self.sprite.get_width()
                self.frame_width = sheet_width // self.frame_count  # šírka jedného framu
                self.frame_height = self.sprite.get_height()  # výška framu
                
                # Načítanie damage framu (prvé dva framy z Hit animácie)
                damage_frame_surface = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
                damage_frame_surface.blit(self.damage_sprite, (0, 0), 
                                       (0, 0, self.frame_width, self.frame_height))
                self.damage_frame = pygame.transform.scale(damage_frame_surface, self.target_size)
                
                # Načítanie death framov (posledné 3 framy z ArmorBreak)
                self.death_frames = []
                try:
                    death_spritesheet = pygame.image.load("sprites/enemies/3/Golem_Armor_ArmorBreak.png").convert_alpha()
                    death_sheet_width = death_spritesheet.get_width()
                    death_frame_width = self.frame_width  # rovnaká šírka ako pre walk animáciu
                    
                    # Načítanie posledných 3 framov z armor break animácie
                    total_frames = death_sheet_width // death_frame_width
                    start_frame = total_frames - 3  # začiatok od tretieho framu od konca
                    
                    for i in range(start_frame, total_frames):
                        frame_surface = pygame.Surface((death_frame_width, self.frame_height), pygame.SRCALPHA)
                        frame_rect = (i * death_frame_width, 0, death_frame_width, self.frame_height)
                        frame_surface.blit(death_spritesheet, (0, 0), frame_rect)
                        scaled_frame = pygame.transform.scale(frame_surface, self.target_size)
                        self.death_frames.append(scaled_frame)
                        
                except Exception as e:
                    print(f"Error loading golem death animation: {e}")
                
                # Načítanie prvého framu
                self.current_frame = self.get_frame(0)
                
            except Exception as e:
                print(f"Error loading golem sprites: {e}")
                self.sprite = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
                self.frame_count = 1
                self.current_frame = self.sprite
            
            self.reward = 40  # väčšia odmena za odolného nepriateľa
            self.speed = 1.5  # pomalší ako základný nepriateľ
        elif enemy_type == 4:  # Final Boss
            try:
                # Načítanie spritesheetov pre bossa -  len jeden základný sprite
                self.sprite = pygame.image.load("sprites/enemies/4/spr_enemy_finalboss_normal_strip6_r.png").convert_alpha()
                self.hurt_sprite = pygame.image.load("sprites/enemies/4/spr_enemy_finalboss_hurt_strip2.png").convert_alpha()
                
                self.frame_count = 6  # počet framov v animácii
                self.death_frame_count = 1  # len jeden frame pre smrť
                self.animation_speed = 0.2
                self.death_animation_speed = 0.2
                
                # Získanie rozmerov spritesheetu
                sheet_width = self.sprite.get_width()
                self.frame_width = sheet_width // self.frame_count  # šírka jedného framu
                self.frame_height = self.sprite.get_height()  # výška framu
                
                # Načítanie death framu (prvý frame z hurt animácie)
                damage_frame_surface = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
                damage_frame_surface.blit(self.hurt_sprite, (0, 0), 
                                       (0, 0, self.frame_width, self.frame_height))
                self.damage_frame = pygame.transform.scale(damage_frame_surface, self.target_size)
                
                # Death frame je ten istý ako damage frame
                self.death_frames = [self.damage_frame]
                
                # Načítanie prvého framu
                self.current_frame = self.get_frame(0)
                
            except Exception as e:
                print(f"Error loading boss sprites: {e}")
                self.sprite = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
                self.frame_count = 1
                self.current_frame = self.sprite
            
            self.reward = 100  # najväčšia odmena za bossa
            self.speed = 2  # štandardná rýchlosť
            self.max_health = 1000 * hp_multiplier  # 10x viac HP ako základný nepriateľ
            self.health = self.max_health
            self.last_move = (1, 0)  # počiatočný smer pohybu (doprava)
            self.last_direction = "right"  # počiatočný smer

    def get_frame(self, frame_number):
        # Vyreže jeden frame zo spritesheetu
        frame_surface = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
        frame_surface.blit(self.sprite, (0, 0), 
                         (frame_number * self.frame_width, 0, 
                          self.frame_width, self.frame_height))
        return pygame.transform.scale(frame_surface, self.target_size)

    def get_death_frame(self, frame_number):
        return self.death_frames[frame_number]

    def take_damage(self, damage):
        if self.is_dying:
            return
            
        current_time = pygame.time.get_ticks()
        # Pre laserový útok kontrolujeme čas od posledného zásahu
        is_laser_hit = damage == 1  # Laser má damage 1
        if not is_laser_hit or (current_time - self.last_laser_hit_time > 500):  # 500ms cooldown pre laser
            # Boss zobrazí damage animáciu len keď umiera
            if self.enemy_type == 4:
                self.is_taking_damage = self.health - damage <= 0
            else:
                self.is_taking_damage = True
            
            self.damage_animation_timer = current_time
            if is_laser_hit:
                self.last_laser_hit_time = current_time
        
        self.health -= damage
        if self.health <= 0 and not self.is_dying:
            self.is_dying = True
            self.death_frame = 0
            self.death_animation_timer = 0
            # Uloženie pozície kde enemy zomrel
            self.death_position = (self.x, self.y)

    def update_animation(self, delta_time=1/60):
        if self.is_dying:
            self.death_animation_timer += delta_time
            if self.death_animation_timer >= self.death_animation_speed:
                self.death_animation_timer = 0
                if self.death_frame < self.death_frame_count - 1:
                    self.death_frame += 1
                # Predanie kontroly pre posledný frame alebo bossa
                if self.death_frame == self.death_frame_count - 1 or (self.enemy_type == 4 and self.death_animation_timer >= self.death_animation_speed):
                    self.alive = False
        elif self.is_taking_damage:
            current_time = pygame.time.get_ticks()
            if current_time - self.damage_animation_timer >= self.damage_animation_duration:
                self.is_taking_damage = False
        else:
            self.animation_timer += delta_time
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                if self.enemy_type in [1, 2, 3, 4]:  # pre všetky animované typy
                    self.frame = (self.frame + 1) % self.frame_count
                    
                    # Špeciálna logika pre bossa (typ 4)
                    if self.enemy_type == 4:
                        # presne rovnaký systém ako pre ostatných nepriateľov
                        if self.last_move[0] < 0:  # doľava
                            if self.last_direction == "up":  # ak ide po hornej ceste
                                self.rotation = 180
                            else:  # ak ide po spodnej ceste
                                self.rotation = 0
                            self.flip_x = True
                        elif self.last_move[0] > 0:  # doprava
                            if self.last_direction == "up":  # ak ide po hornej ceste
                                self.rotation = 180
                            else:  # ak ide po spodnej ceste
                                self.rotation = 0
                            self.flip_x = False
                        elif self.last_move[1] < 0:  # hore
                            if self.last_direction == "right":  # ak ide z pravej strany
                                self.rotation = 270
                            else:  # ak ide z ľavej strany
                                self.rotation = 90
                            self.flip_x = False
                        elif self.last_move[1] > 0:  # dole
                            if self.last_direction == "right":  # ak ide z pravej strany
                                self.rotation = 270
                            else:  # ak ide z ľavej strany
                                self.rotation = 90
                            self.flip_x = True  # pridáme horizontálne otočenie pri pohybe dole
                        
                        # Aktualizácia posledného smeru len pri horizontálnom pohybe
                        if self.last_move[0] != 0:  # len pri pohybe doľava/doprava
                            if self.last_move[0] < 0:
                                self.last_direction = "left"
                            else:
                                self.last_direction = "right"
                        
                        self.current_frame = self.get_frame(self.frame)
                    # Špeciálna logika pre crow (typ 1)
                    elif self.enemy_type == 1 and self.last_move:
                        # Určenie rotácie podľa smeru pohybu - zostáva prilepený k ceste
                        if self.last_move[0] < 0:  # doľava
                            if self.last_direction == "up":  # ak ide po hornej ceste
                                self.rotation = 180
                            else:  # ak ide po spodnej ceste
                                self.rotation = 0
                            self.flip_x = True
                        elif self.last_move[0] > 0:  # doprava
                            if self.last_direction == "up":  # ak ide po hornej ceste
                                self.rotation = 180
                            else:  # ak ide po spodnej ceste
                                self.rotation = 0
                            self.flip_x = False
                        elif self.last_move[1] < 0:  # hore
                            if self.last_direction == "right":  # ak ide z pravej strany
                                self.rotation = 270
                            else:  # ak ide z ľavej strany
                                self.rotation = 90
                            self.flip_x = False
                        elif self.last_move[1] > 0:  # dole
                            if self.last_direction == "right":  # ak ide z pravej strany
                                self.rotation = 270
                            else:  # ak ide z ľavej strany
                                self.rotation = 90
                            self.flip_x = True  # horizontálne otočenie pri pohybe dole
                        
                        # Aktualizácia posledného smeru len pri horizontálnom pohybe
                        if self.last_move[0] != 0:  # len pri pohybe doľava/doprava
                            if self.last_move[0] < 0:
                                self.last_direction = "left"
                            else:
                                self.last_direction = "right"
                        
                        self.current_frame = self.get_frame(self.frame)
                    # Špeciálna logika pre worm (typ 2)
                    elif self.enemy_type == 2:  # worm
                        # Použijeme rovnaký systém ako pre crow
                        if self.last_move[0] < 0:  # doľava
                            if self.last_direction == "up":  # ak ide po hornej ceste
                                self.rotation = 180
                            else:  # ak ide po spodnej ceste
                                self.rotation = 0
                            self.flip_x = True
                        elif self.last_move[0] > 0:  # doprava
                            if self.last_direction == "up":  # ak ide po hornej ceste
                                self.rotation = 180
                            else:  # ak ide po spodnej ceste
                                self.rotation = 0
                            self.flip_x = False
                        elif self.last_move[1] < 0:  # hore
                            if self.last_direction == "right":  # ak ide z pravej strany
                                self.rotation = 270
                            else:  # ak ide z ľavej strany
                                self.rotation = 90
                            self.flip_x = False
                        elif self.last_move[1] > 0:  # dole
                            if self.last_direction == "right":  # ak ide z pravej strany
                                self.rotation = 270
                            else:  # ak ide z ľavej strany
                                self.rotation = 90
                            self.flip_x = True  # pridáme horizontálne otočenie pri pohybe dole
                        
                        # Aktualizácia posledného smeru len pri horizontálnom pohybe
                        if self.last_move[0] != 0:  # len pri pohybe doľava/doprava
                            if self.last_move[0] < 0:
                                self.last_direction = "left"
                            else:
                                self.last_direction = "right"
                        
                        self.current_frame = self.get_frame(self.frame)
                    # Špeciálna logika pre golem (typ 3)
                    elif self.enemy_type == 3:  # golem
                        # rovnaký systém ako pre crow a worm
                        if self.last_move[0] < 0:  # doľava
                            if self.last_direction == "up":  # ak ide po hornej ceste
                                self.rotation = 180
                            else:  # ak ide po spodnej ceste
                                self.rotation = 0
                            self.flip_x = True
                        elif self.last_move[0] > 0:  # doprava
                            if self.last_direction == "up":  # ak ide po hornej ceste
                                self.rotation = 180
                            else:  # ak ide po spodnej ceste
                                self.rotation = 0
                            self.flip_x = False
                        elif self.last_move[1] < 0:  # hore
                            if self.last_direction == "right":  # ak ide z pravej strany
                                self.rotation = 270
                            else:  # ak ide z ľavej strany
                                self.rotation = 90
                            self.flip_x = False
                        elif self.last_move[1] > 0:  # dole
                            if self.last_direction == "right":  # ak ide z pravej strany
                                self.rotation = 270
                            else:  # ak ide z ľavej strany
                                self.rotation = 90
                            self.flip_x = True  # pridáme horizontálne otočenie pri pohybe dole
                        
                        # Aktualizácia posledného smeru len pri horizontálnom pohybe
                        if self.last_move[0] != 0:  # len pri pohybe doľava/doprava
                            if self.last_move[0] < 0:
                                self.last_direction = "left"
                            else:
                                self.last_direction = "right"
                        
                        self.current_frame = self.get_frame(self.frame)
                    # Flip pre ostatné typy (nie pre typ 1, 2, 3, ktoré používajú rotáciu)
                    elif self.last_move and self.last_move[0] < 0 and self.enemy_type == 4:
                        self.current_frame = pygame.transform.flip(self.current_frame, True, False)

    def draw(self):
        if not self.alive:
            return
            
        self.update_animation()
        
        # Ak nie je v death animácii, aktualizujeme pozíciu a health bar
        if not self.is_dying:
            self.move()
            self.draw_health_bar()
            x = self.x
            y = self.y
        else:
            # Počas death animácie - fixná pozícia
            if not self.death_position:
                self.death_position = (self.x, self.y)
            x = self.death_position[0]
            y = self.death_position[1]
        
        # Výber správneho framu podľa stavu
        if self.is_dying and self.enemy_type in [1, 2, 3, 4]:
            current_frame = self.get_death_frame(self.death_frame)
        elif self.is_taking_damage and self.enemy_type in [1, 2, 3, 4]:
            current_frame = self.damage_frame
        else:
            current_frame = self.current_frame
            
        # Aplikovanie transformácií podľa typu nepriateľa
        if self.enemy_type in [1, 2, 3, 4]:  # crow, worm, golem a boss
            if self.flip_x:
                current_frame = pygame.transform.flip(current_frame, True, False)
            current_frame = pygame.transform.rotate(current_frame, self.rotation)
        
        self.window.blit(current_frame, 
                       (x + self.sprite_offset_x, 
                        y + self.sprite_offset_y))

    def is_dying_animation(self):
        return self.is_dying 