import pygame
from settings import screen_height, screen_width
from support import blit_text
from bokumon import BokuMon
from support import *
from timer import Timer

class Menu:
    def __init__(self, screen, player, bag):
        self.display_surface = screen
        self.player = player
        self.bag = bag
        self.timer = Timer(0.12)

        self.selected = [0, False]
        self.selected_button = 1
        self.boku_selected = [1, False]
        self.confirm_button = 0
        self.intro = True
        self.msg = False
        self.select_new_game = False

        self.font_25 = pygame.font.Font('font/Pixeltype.ttf', 25)
        self.font_35 = pygame.font.Font('font/Pixeltype.ttf', 35)
        self.font_42 = pygame.font.Font('font/Pixeltype.ttf', 42)
        self.font_50 = pygame.font.Font('font/Pixeltype.ttf', 50)

        self.firts_bokumons = [BokuMon(self.display_surface, 'Pan'), BokuMon(self.display_surface, 'Parrot'), BokuMon(self.display_surface, 'Monk')]

    def draw(self):
        if self.select_new_game:
            self.select_first_bokumon()
            if self.boku_selected[1]:
                self.blit_select_continue((screen_width - 150, screen_height - 250), self.confirm_button)
        else:
            self.draw_overlay()
            if self.selected[1]:
                self.blit_select_continue((screen_width - 260, 180), self.selected_button)
            elif self.msg:
                self.blit_msg("Don't  have  any  saved  game.")

    def draw_overlay(self):
        pygame.draw.rect(self.display_surface, '#00009F', (0, 0, screen_width, screen_height))
        pos = [[240, 145], [280, 345]]
        pygame.draw.rect(self.display_surface, '#00008B', (110, 100, screen_width - 250, 100), 0, 3)
        pygame.draw.rect(self.display_surface, 'black', (110, 100, screen_width - 250, 100), 3, 5)
        pygame.draw.rect(self.display_surface, 'white', (120, 110, screen_width - 270, 80), 0, 5)
        blit_text('Continue   Game', 'black', [380, 155], font=self.font_50, center=True)
        pygame.draw.rect(self.display_surface, '#00008B', (110, 300, screen_width - 250, 100), 0, 3)
        pygame.draw.rect(self.display_surface, 'black', (110, 300, screen_width - 250, 100), 3, 5)
        pygame.draw.rect(self.display_surface, 'white', (120, 310, screen_width - 270, 80), 0, 5)
        blit_text('New   Game', 'black', [380, 355], font=self.font_50, center=True)
        color = 'red' if self.selected[1] else 'black'
        pygame.draw.rect(self.display_surface, color, (pos[self.selected[0]][0], pos[self.selected[0]][1], 10, 10), 0, 20)
        
    def blit_select_continue(self, pos_rect, selected_button): 
        pygame.draw.rect(self.display_surface, '#00008B', (pos_rect[0], pos_rect[1], 120, screen_height/4.5), 0, 3)
        pygame.draw.rect(self.display_surface, 'black', (pos_rect[0], pos_rect[1], 120, screen_height/4.5), 3, 5)
        pygame.draw.rect(self.display_surface, 'white', (pos_rect[0] + 10, pos_rect[1] + 10, 100, screen_height/4.5 - 20), 0, 5)
        pos = [[pos_rect[0] + 20, pos_rect[1] + 40], [pos_rect[0] + 20, pos_rect[1] + 90]]
        pygame.draw.rect(self.display_surface, 'black', (pos[selected_button][0], pos[selected_button][1], 10, 10), 0, 20)
        blit_text('Yes', 'black', (pos[0][0] + 20, pos[0][1] - 10), font=self.font_50)
        blit_text('No', 'black', (pos[1][0] + 20, pos[1][1] - 10), font=self.font_50)

    def select_first_bokumon(self):
        pygame.draw.rect(self.display_surface, '#00899F', (0, 0, screen_width, screen_height))
        pygame.draw.rect(self.display_surface, '#19A99F', (60, screen_height/2 - 100, screen_width - 100, 160))
        self.blit_msg('Select  your  first  Bokumon!')
        space_x = 0
        for i, boku in enumerate(self.firts_bokumons):
            boku.draw_modified([130 + space_x, screen_height/2 - 40], 0.7)
            blit_text(f'{boku.name}', 'black', (160 + space_x, screen_height - 200), font=self.font_50, center=True)
            if self.boku_selected[0] == i:
                pygame.draw.rect(self.display_surface, 'red', (75 + space_x, screen_height/2 - 95, 150, 150), 3, 20)
            space_x += 250

    def blit_msg(self, msg):
        pygame.draw.rect(self.display_surface, '#00008B', (20, screen_height - 120, screen_width - 50, 100), 0, 3)
        pygame.draw.rect(self.display_surface, 'black', (20, screen_height - 120, screen_width - 50, 100), 3, 5)
        pygame.draw.rect(self.display_surface, 'white', (30, screen_height - 110, screen_width - 70, 80), 0, 5)
        blit_text(msg, 'black', (80, screen_height - 80), font=self.font_50)

    def update(self):
        if self.timer.run:
            self.timer.update()
        self.input()

    def input(self):
        if not self.timer.run:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                if self.select_new_game:
                    self.confirm_button = 0
                else:
                    if not self.selected[1] and not self.msg:
                        self.selected[0] = 0
                    else:
                        self.selected_button = 0
            elif keys[pygame.K_DOWN]:
                if self.select_new_game:
                    self.confirm_button = 1
                else:
                    if not self.selected[1] and not self.msg:
                        self.selected[0] = 1
                    else:
                        self.selected_button = 1

            if keys[pygame.K_LEFT]:
                if self.select_new_game and not self.boku_selected[1]:
                    self.boku_selected[0] -= 1 if self.boku_selected[0] > 0 else 0
            elif keys[pygame.K_RIGHT]: 
                if self.select_new_game and not self.boku_selected[1]:
                    self.boku_selected[0] += 1 if self.boku_selected[0] < 2 else 0

            if keys[pygame.K_z]:
                if self.select_new_game:
                    if not self.boku_selected[1]:
                        self.boku_selected[1] = True
                    else:
                        if self.confirm_button == 0:
                            self.player.first_bokumon(self.firts_bokumons[self.boku_selected[0]])
                            self.intro = False
                        else:
                            self.boku_selected[1] = False
                else:
                    if not self.selected[1]:
                        self.selected[1] = True
                        if self.selected[0] == 0 and not load_game():
                            self.selected[1] = False
                            self.msg = True
                    else:
                        if self.selected_button == 0:
                            if self.selected[0] == 0:
                                self.load_saved_game()
                                self.intro = False
                            else:
                                self.select_new_game = True
                        else:
                            self.selected[1] = False

            elif keys[pygame.K_x]:
                if self.select_new_game:
                    if not self.boku_selected[1]:
                        self.select_new_game = False
                    else:
                        self.boku_selected[1] = False
                        self.confirm_button = 1
                else:
                    if self.selected[1]:
                        self.selected[1] = False
                        self.selected_button = 1
                    elif self.msg:
                        self.msg = False
            self.timer.active()


    def load_saved_game(self):
        # carrega o game salvo
        words = load_game()
        bk_state = []
        bk_store = []
        bag_list = []
        # player_states
        ply_state = [words[0][0], words[0][1], text_to_list(words[0][2]), int(words[0][3])]
        # bokumons_states
        for i, word in enumerate(words[1]):
            bk_state.append(list_text_to_int(word))
        for word in words[2]:
            bk_store.append(list_text_to_int(word))
        bk_state = self.adjust_list(bk_state)
        bk_store = self.adjust_list(bk_store)
        # bag_states
        for i in range(3, 6):
            if words[i][0] != '':
                bag_list.append(self.adjust_list_bag(words, i))
            else:
                bag_list.append([])

        self.bag.load_bag(bag_list)
        self.player.load_states(ply_state, bk_state, bk_store)
    
    def adjust_list(self, list_state):
        # retorna a lista ajustada
        aux = []
        for i, bk in enumerate(list_state):
            if i % 5 != 0:
                list_state[i] = text_to_list(list_state[i][0])
        for i in range(int(len(list_state)/5)):
            aux.append(list_state[(i*5):((i+1)*5)])
        return aux
    
    def adjust_list_bag(self, bag_list, pos):
        # retorna a lista da bag ajustada
        aux = []
        for i, word in enumerate(bag_list[pos]):
            aux.append(text_to_list(word[0]))
            aux[i][0] = aux[i][0].replace("'", '')
            aux[i][0] = self.add_space(aux[i][0])
            aux[i][1] = float(aux[i][1]) if aux[i][0].count('Ball') == 1 else int(aux[i][1])
        return aux

    def add_space(self, word):
        # adiciona o espaço retirado, na hora do load, à palavra
        cont = 0
        pos = 0
        for i, l in enumerate(word):
            if l.isupper():
                cont += 1
                pos = i
        if cont == 2:
            word = word[0:pos] + ' ' + word[pos:len(word)]
        return word



