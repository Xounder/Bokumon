import pygame
from settings import *
from timer import Timer
from support import *
from bokumon_summary import BokuSummary

class ViewBokumon:
    def __init__(self, screen, player):
        self.display_surface = screen
        self.player = player
        self.bokumon_summary = BokuSummary(self.display_surface, self.player)
        self.timer = Timer(0.12)
        self.msg_timer = Timer(1)
        self.active = False

        self.seted = False
        self.marked = [0, 0]
        self.switch = False
        self.fainted = False
        self.bag_values = [None, False, [], [False]]
        self.bag_used = False
        self.set_view()

        self.font_25 = pygame.font.Font('font/Pixeltype.ttf', 25)
        self.font_35 = pygame.font.Font('font/Pixeltype.ttf', 35)
        self.font_42 = pygame.font.Font('font/Pixeltype.ttf', 42)
        self.font_50 = pygame.font.Font('font/Pixeltype.ttf', 50)

        # select_action
        self.text_select_action = [['Summary', 'Switch', 'Cancel'], ['Shift', 'Summary', 'Cancel'], ['Send Out', 'Summary', 'Cancel']]
        self.list_selected = 0        
        self.selected_action = [0, False, '']
        # bokuball img
        self.boku_ball_img = [pygame.image.load('imgs/boku_ball.png').convert_alpha(), pygame.image.load('imgs/boku_ball2.png').convert_alpha()]

    def set_view(self):
        if not self.seted:
            self.timer.active()
            self.selected = False
            self.boku_limit = len(self.player.bokumons) - 1
            self.previous_marked = 1
            self.bag_used = False
            self.seted = True

    def draw_boku_ball(self, rect_center, scale, num):
        self.boku_ball_rect = self.boku_ball_img[num].get_rect(center = (rect_center))
        image_mod = pygame.transform.scale(self.boku_ball_img[num], (self.boku_ball_img[num].get_width()/scale, 
                                                                    self.boku_ball_img[num].get_height()/scale))
        self.display_surface.blit(image_mod, self.boku_ball_rect)

    def draw(self):
        if self.bokumon_summary.active:
            self.bokumon_summary.draw()
        else:
            self.draw_overlay()

    def update(self):
        if self.bokumon_summary.active:
            self.bokumon_summary.update()
        else:
            if self.timer.run:
                self.timer.update()
            if not self.msg_timer.run:
                self.input()
            self.set_view()

    def draw_overlay(self):
        space_y = 90
        prev_y = 20
        pygame.draw.rect(self.display_surface, 'green', (0, 0, screen_width, screen_height))
        pygame.draw.rect(self.display_surface, 'brown', (20, 100, 300, 200), 0, 5)
        if self.marked[0] == 0 or self.marked[1] == 0:
            if (self.selected or self.fainted or self.player.battle) and self.marked[0] == 0:
                color = 'red'
            else:
                color = 'black'
        else:
            color = 'white'
        #first bokumon
        pygame.draw.rect(self.display_surface, color, (20, 100, 300, 200), 7, 5)
        pygame.draw.rect(self.display_surface, 'black', (20, 100, 300, 200), 3, 5)
        self.status_txt(0, [[45, 240], [80, 245]], [[50, 245], [290, 270], [125, 170], [160, 200]], [215, 255, 26, 16])
        # bokuball
        if self.marked[0] == self.marked[1]:
            num = 1 if self.marked[0] == 0 else 0
        else:
            num = 1 if self.marked[1] == 0 else 0
        self.draw_boku_ball((40, 95), 0.7, num)
        self.player.bokumons[0].draw_modified((60, 125), 1.3)
        for i in range(1, 6):
            if i <= self.boku_limit:
                pygame.draw.rect(self.display_surface, 'brown', (370, prev_y, 400, space_y), 0, 5)
                if self.marked[0] == i or self.marked[1] == i:
                    if (self.selected or self.fainted or self.player.battle) and self.marked[0] == i:
                        color = 'red'
                    else:
                        color = 'black'
                else:
                    color = 'white'
                pygame.draw.rect(self.display_surface, color, (370, prev_y, 400, space_y), 7, 5)
                pygame.draw.rect(self.display_surface, 'black', (370, prev_y, 400, space_y), 3, 5)

                life_y = prev_y - 20
                self.status_txt(i, [[575, 45 + life_y], [605, 50 + life_y]], [[580, 50 + life_y], [740, 68 + life_y], 
                                                                                [430, 45 + life_y], [450, 75 + life_y]])
                # bokuball
                if self.marked[0] == self.marked[1]:
                    num = 1 if self.marked[0] == i else 0
                else:
                    num = 1 if self.marked[1] == i else 0
                self.draw_boku_ball((355, prev_y + 30), 0.7, num)
                self.player.bokumons[i].draw_modified((375, prev_y + 60), 1.3)
            else:
                pygame.draw.rect(self.display_surface, 'brown', (370, prev_y, 400, space_y), 5, 5)
            prev_y += space_y + 5

        # comentario
        action = self.text_select_action[self.list_selected][self.selected_action[0]]
        if not self.selected:
            text = 'Choose     a     Bokumon.'
        else:
            if action == 'Switch' and not self.selected_action[1]:
                text =  'Move to where?'
            else:
                text = 'Do  what  if  this  Bokumon?'
        pygame.draw.rect(self.display_surface, 'white', (20, 500, 500, 90))
        pygame.draw.rect(self.display_surface, 'blue', (20, 500, 500, 90), 5)
        pygame.draw.rect(self.display_surface, 'black', (20, 500, 500, 90), 3)
        blit_text(text , 'black', (50, 535), self.font_42)
        color = 'black' if self.marked[0] == 6 or self.marked[1] == 6 else 'white'

        pygame.draw.rect(self.display_surface, 'purple', (610, 520, 150, 50), 0, 50)
        pygame.draw.rect(self.display_surface, color, (610, 520, 150, 50), 5, 50)
        pygame.draw.rect(self.display_surface, 'black', (610, 520, 150, 50), 3, 50)
        blit_text('Cancel', 'black', (660, 535), self.font_42)
        # bokuball cancel
        self.draw_boku_ball((620, 545), 1, 1 if self.marked[0] == 6 else 0)
        self.blit_select_action()
        if (self.fainted or self.player.battle) and self.marked[0] == 0 and self.selected_action[2] == 'Shift_fail':
            if self.marked[0] == 0:
                tam = [(screen_height - 160), 150]
                pygame.draw.rect(self.display_surface, '#00008B', (0, tam[0], screen_width, tam[1]), 0, 3)
                pygame.draw.rect(self.display_surface, 'black', (0, tam[0], screen_width, tam[1]), 3, 5)
                pygame.draw.rect(self.display_surface, 'white', (10, tam[0] + 10, screen_width - 20, tam[1] - 20), 0, 5)   
                blit_text(f'{self.player.bokumons[0].atual_name} is already', 'black', (40, tam[0] + 40), self.font_50)
                blit_text('in battle!', 'black', (40, tam[0] + 80), self.font_50)
                
        elif self.bag_values[3][0]:
            self.draw_potion_use()
            self.msg_timer.update()
            if not self.msg_timer.run:
                self.deactive()
    
    def status_txt(self, num_boku, pos_rect, pos_text, tam=[140, 175, 20, 10]):
        life_font = self.font_25 if tam[0] == 140 else self.font_35
        boku_info = self.font_35 if tam[0] == 140 else self.font_42

        tam_life = tam[0] * self.player.bokumons[num_boku].atual_life / self.player.bokumons[num_boku].life
        pygame.draw.rect(self.display_surface, 'black', (pos_rect[0][0], pos_rect[0][1], tam[1], tam[2]), 0, 5)
        pygame.draw.rect(self.display_surface, 'green', (pos_rect[1][0], pos_rect[1][1], tam_life, tam[3]))
        blit_text_shadow('HP', 'red', (pos_text[0][0], pos_text[0][1]), font=life_font)
        blit_text_shadow(f'{round(self.player.bokumons[num_boku].atual_life)}/{self.player.bokumons[num_boku].life}', 
                                                        'white', (pos_text[1][0], pos_text[1][1]), font=self.font_35, right=True)
        blit_text_shadow(f'{self.player.bokumons[num_boku].atual_name}', 'white', (pos_text[2][0], pos_text[2][1]), font=boku_info)
        blit_text_shadow(f'Lv{self.player.bokumons[num_boku].level}', 'white', (pos_text[3][0], pos_text[3][1]), font=boku_info)

    def draw_potion_use(self):
        tam = [(screen_height - 160), 150]
        pygame.draw.rect(self.display_surface, '#00008B', (0, tam[0], screen_width, tam[1]), 0, 3)
        pygame.draw.rect(self.display_surface, 'black', (0, tam[0], screen_width, tam[1]), 3, 5)
        pygame.draw.rect(self.display_surface, 'white', (10, tam[0] + 10, screen_width - 20, tam[1] - 20), 0, 5)   
        blit_text(f'{self.player.bokumons[0].atual_name} HP was restored', 'black', (40, tam[0] + 40), self.font_50)
        blit_text(f'by {self.bag_values[0][1]} point(s).', 'black', (40, tam[0] + 80), self.font_50)

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.timer.run:
            if keys[pygame.K_UP]:
                if self.selected_action[1]:
                    self.selected_action[0] -= 1 if self.selected_action[0] > 0 else 0 
                else:
                    if self.marked[1] == 0:
                        self.move_select(6, 0, self.selected, False)
                        self.move_select(6, 1, False, False)
                    elif self.marked[1] > 0:
                        self.move_select(-1, 0, self.selected)
                        self.move_select(-1, 1, False)
            elif keys[pygame.K_DOWN]:
                if self.selected_action[1]:
                    list_action = self.text_select_action[self.list_selected]
                    self.selected_action[0] += 1 if self.selected_action[0] < len(list_action)-1 else 0 
                else:
                    if self.marked[1] == 0:
                        self.move_select(1, 0, self.selected)
                        self.move_select(1, 1, False)
                    elif 0 < self.marked[1] < 6:
                        self.move_select(1, 0, self.selected)
                        self.move_select(1, 1, False)
                    else:
                        self.move_select(0, 0, self.selected, False)
                        self.move_select(0, 1, False, False)
            elif keys[pygame.K_LEFT]:
                if not self.selected_action[1]:
                    if 0 < self.marked[1] < 6:
                        if self.marked[1] != 0:
                            self.previous_marked = self.marked[1]
                        self.move_select(0, 0, self.selected, False)
                        self.move_select(0, 1, False, False)
            elif keys[pygame.K_RIGHT]:
                if not self.selected_action[1]:
                    if self.marked[1] < 6:
                        self.move_select(self.previous_marked, 0, self.selected, False)
                        self.move_select(self.previous_marked, 1, False, False)

            if keys[pygame.K_z]: 
                if self.bag_values[1]:
                    if self.marked[0] == 6:
                        self.deactive()
                    else:
                        if self.bag_values[0][0].count('Potion') == 1:
                            if self.player.bokumons[self.marked[0]].restore_life(self.bag_values[0][1]):
                                self.bag_values[0][2] -= 1
                                if self.bag_values[0][2] <= 0:
                                    self.bag_values[2][0].pop(self.bag_values[2][1])
                                self.bag_values[1] = False
                                self.bag_values[3][0] = True  
                                self.msg_timer.active()                                          
                else:      
                    if not self.selected and not self.selected_action[1] and self.selected_action[2] == '':
                        if self.marked[0] == 6:
                            self.check_return()
                        else:
                            if not self.player.battle:
                                self.selected = True
                            self.selected_action[1] = True
                    elif self.selected_action[1]:
                        action = self.text_select_action[self.list_selected][self.selected_action[0]]
                        if action == 'Summary':
                            self.bokumon_summary.active = True
                            self.bokumon_summary.seted = False
                            self.bokumon_summary.set_summary(self.marked[0])
                        elif action == 'Cancel':
                            self.selected = False
                            self.selected_action[0] = 0
                            self.selected_action[1] = False
                        else: 
                            #Send Out, Shift e Switch
                            self.selected_action[1] = False
                            self.selected_action[2] = ''
                            if self.player.battle:
                                self.selected_action[0] = 0
                            if not self.player.battle:
                                self.selected_action[2] = 'Switch'

                            if self.fainted or self.player.battle:
                                if self.marked[0] != 6:
                                    if self.player.bokumon_is_alive(self.marked[0]) and self.marked[0] != 0:
                                        self.player.switch_bokumon([0, self.marked[0]], battle=True)   
                                        self.switch = True
                                        self.check_return()  
                                    else:
                                        self.selected_action[2] = 'Shift_fail'                       
                    else:                                       
                        if self.marked[1] == 6:
                            self.selected = False
                            self.selected_action[2] = ''
                            self.marked[0] = self.marked[1]
                        else:
                            self.player.switch_bokumon(self.marked)
                            self.selected_action[0] = 0
                            self.selected = False
                            self.selected_action[2] = ''
                            self.marked[0] = self.marked[1]

            elif keys[pygame.K_x]:
                if self.bag_values[1]:
                    self.bag_values[1] = False
                    self.deactive()
                else:
                    if self.selected or self.selected_action[1]:
                        self.selected = False
                        self.marked[0] = self.marked[1]
                        self.selected_action[1] = False
                        self.selected_action[0] = 0
                    else:
                        self.check_return()
            self.timer.active()

    def check_return(self):
        if self.fainted:
            if self.player.bokumon_is_alive(0):
                self.deactive()
        else:
            self.deactive()
    
    def deactive(self):
        self.active = False                    
        self.seted = False
        self.marked[0] = 0
        self.marked[1] = 0

    def move_select(self, num, pos, selected, sum=True):
        if sum:
            if not selected or self.fainted:
                sum = self.marked[pos] + num 
                if 0 <= sum <= self.boku_limit:
                    # caso o numero que vier seja negativo e estivermos no marked[0] = 0
                    if (num < 0 and sum > 0) or num > 0:
                        self.marked[pos] += num  
                else:
                    if num > 0:
                        self.marked[pos] = 6
                    else:
                        self.marked[pos] = 0 
        else:
            if not selected or self.fainted:
                self.marked[pos] = num

    def blit_select_action(self):
        if self.selected_action[1]:
            qnt_sel = len(self.text_select_action) - 2
            tam = [(screen_height - 160) - qnt_sel*40 , 150 + qnt_sel*40]
            # caixa de seleção do item
            pygame.draw.rect(self.display_surface, '#00008B', (screen_width - 250, tam[0], 220, tam[1]), 0, 3)
            pygame.draw.rect(self.display_surface, 'black', (screen_width - 250, tam[0], 220, tam[1]), 3, 5)
            pygame.draw.rect(self.display_surface, 'white', (screen_width - 240, tam[0] + 10, 200, tam[1] - 20), 0, 5)
            # possiveis seleções
            if self.fainted:
                self.list_selected = 2
            else:
                self.list_selected = self.player.battle

            space_y_sel = 40
            for i, sel in enumerate(self.text_select_action[self.list_selected]):
                blit_text(f'{sel}', 'black', (screen_width - 210, tam[0] + space_y_sel), self.font_50)
                if self.selected_action[0] == i:
                    # botão de seleção
                    pygame.draw.rect(self.display_surface, 'black', (screen_width - 230, tam[0] + space_y_sel + 5, 10, 10))
                space_y_sel += 45
