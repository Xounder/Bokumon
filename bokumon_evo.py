import pygame
from timer import Timer
from settings import screen_height, screen_width
from random import randint
from support import *

class BokuEvo:
    def __init__(self, screen, player):
        self.display_surface = screen
        self.player = player
        self.atual_bokumon = self.player.atual_bokumon
        self.timer = Timer(0.12)
        self.msg_timer = Timer(2.5)        

        self.activate(first_time=True)
        self.pressed_z = False
        self.pressed_x = False

        self.background = pygame.transform.scale(pygame.image.load('imgs/fight2.png'), (screen_width, screen_height - 100))
        self.font_42 = pygame.font.Font('font/Pixeltype.ttf', 42)
        self.font_25 = pygame.font.Font('font/Pixeltype.ttf', 25)

    def draw(self):
        self.display_surface.blit(self.background, (0,0))
        if not self.cancel:
            if self.show_msg and self.msg_timer.run:
                self.atual_bokumon.draw((screen_width/2, screen_height/2))
                for gas in self.list_gas:
                    pygame.draw.circle(self.display_surface, 'gray', (gas[0] + randint(-50, 50), gas[1] + randint(-50, 50)), 10)
                pygame.draw.rect(self.display_surface, 'white', [0, screen_height - 130, screen_width, 130])
                pygame.draw.rect(self.display_surface, 'black', [0, screen_height - 130, screen_width, 130], 3)
                blit_text(f'{self.atual_bokumon.name} is evolving...', 'black', [20, screen_height - 80], self.font_42)
                if self.pressed_x:
                    self.cancel = True
                    if self.atual_bokumon.evolved[0][0] and not self.atual_bokumon.evolved[0][1]:
                        self.atual_bokumon.evolved[0][0] = False
                    else:
                        self.atual_bokumon.evolved[1][0] = False
            else:
                if not self.evolve:
                    if not self.atual_bokumon.evolved[0][1]:
                        self.atual_bokumon.evolved[0][1] = True
                        self.player.tickets += 10
                    else:
                        self.atual_bokumon.evolved[1][1] = True
                        self.player.tickets += 25
                        
                    self.atual_bokumon.evolve()
                    self.show_msg = False
                    self.evolve = True
                    self.up_bokumon = True
                    self.msg_timer.active()
                    
                self.atual_bokumon.draw((screen_width/2, screen_height/2))
                pygame.draw.rect(self.display_surface, 'white', [0, screen_height - 130, screen_width, 130])
                pygame.draw.rect(self.display_surface, 'black', [0, screen_height - 130, screen_width, 130], 3)
                blit_text(f'{self.atual_bokumon.previous_name} evolved to {self.atual_bokumon.name}', 'black', [20, screen_height - 80], self.font_42)
                
                self.up_info()
                    
        else:
            self.atual_bokumon.draw((screen_width/2, screen_height/2))
            pygame.draw.rect(self.display_surface, 'white', [0, screen_height - 130, screen_width, 130])
            pygame.draw.rect(self.display_surface, 'black', [0, screen_height - 130, screen_width, 130], 3)
            blit_text(f"{self.atual_bokumon.name} don't evolve", 'black', [20, screen_height - 80], self.font_42)
            if self.pressed_z:
                self.active = False

    def update(self):
        if self.timer.run:
            self.timer.update()
        if self.msg_timer.run:
            self.msg_timer.update()
        self.input()
    
    def input(self):
        keys = pygame.key.get_pressed()
        if not self.timer.run:
            if keys[pygame.K_z]:
                self.pressed_z = True
            elif keys[pygame.K_x]:
                self.pressed_x = True
            else:
                self.pressed_z = False
                self.pressed_x = False
            self.timer.active()
    
    def activate(self, first_time=False):
        if not first_time:
            self.active = True
        else:
            self.active = False
        self.show_msg = True
        self.cancel = False
        self.evolve = False
        self.list_gas = []
        self.msg_timer.active()
        for i in range(300):
            self.list_gas.append([screen_width/2 + randint(-100, 100), screen_height/2 + randint(-100, 100)])

    
    def up_info(self):
        if self.up_bokumon:
            if self.msg_timer.run:
                ups = ['Life ', f'+{self.player.atual_bokumon.atrib_ups[0]}', 'Attack ', f'+{self.player.atual_bokumon.atrib_ups[1]}', 
                        'Defense ', f'+{self.player.atual_bokumon.atrib_ups[2]}', 'Speed ', f'+{self.player.atual_bokumon.atrib_ups[3]}',
                        'Crit.Chance ', f'+{self.player.atual_bokumon.atrib_ups[4]}']
            else:
                ups = ['Life ', f'{self.player.atual_bokumon.life}', 'Attack ', f'{self.player.atual_bokumon.attack}', 
                            'Defense ', f'{self.player.atual_bokumon.defense}', 'Speed ', f'{self.player.atual_bokumon.speed}',
                            'Crit.Chance ', f'{self.player.atual_bokumon.critical_chance}']

            pygame.draw.rect(self.display_surface, 'gray', (screen_width/2 + 120, screen_height/2 - 200, 220, 220))
            pygame.draw.rect(self.display_surface, 'black', (screen_width/2 + 120, screen_height/2 - 200, 220, 220), 3)
            for i in range(0, len(ups), 2):
                blit_text_shadow(ups[i], 'black', (screen_width/2 + 149, screen_height/2 - 180 + (20 * i)), 
                                                                            font=self.font_25, back_color='white')
                blit_text_shadow(ups[i+1], 'black', (screen_width/2 + 278, screen_height/2 - 180 + (20 * i)), 
                                                                            font=self.font_25, back_color='white')

            if not self.msg_timer.run and self.up_bokumon:
                if self.pressed_z:
                    self.up_bokumon = False  
                    self.active = False
