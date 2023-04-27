import pygame
from settings import screen_height, screen_width
from support import *
from timer import Timer

class BokuStore:
    def __init__(self, screen, player, bag):
        self.display_surface = screen
        self.player = player
        self.bag = bag
        self.timer = Timer(0.12)

        self.active = False
        self.set_store()
        self.items_disp = [[['Items', 5, 1], ['Potion', 20, 1]], [['Boku Balls', 5, 1], ['Boku Ball', 1, 1]], 
                           [['Boku Balls', 2, 1], ['Great Ball', 1.25, 1]], [['Boku Balls', 1, 2], ['Ultra Ball', 1.6, 1]],
                           [['Items', 2, 1], ['Super Potion', 50, 1]], [['Items', 1, 2], ['Hyper Potion', 200, 1]]]

        self.font_20 = pygame.font.Font('font/Pixeltype.ttf', 20)
        self.font_25 = pygame.font.Font('font/Pixeltype.ttf', 25)
        self.font_35 = pygame.font.Font('font/Pixeltype.ttf', 35)
        self.font_42 = pygame.font.Font('font/Pixeltype.ttf', 42)
        self.font_50 = pygame.font.Font('font/Pixeltype.ttf', 50)


    def set_store(self):
        self.close = False
        self.cant_buy = False
        self.select_buy = False
        self.text_select_buy = False
        self.select_player_boku = [0, False]
        self.select_trade = False
        self.cant_trade = False
        self.gain_tp = 0
        self.selected_action = [0, False]
        self.limit_visu_items = [0, 7]
                        #sel_item|[cont_item, buy]|selected
        self.selected_item = [0, [1, False], False]

    def draw_select_action(self):
        list_choose = ['Buy', 'Trade', 'See ya!']
        pygame.draw.rect(self.display_surface, [112, 104, 128], [screen_width - 300, screen_height/2 - 40, 280, 200], 0, 10)
        pygame.draw.rect(self.display_surface, 'black', [screen_width - 300, screen_height/2 - 40, 280, 200], 3, 10)
        pygame.draw.rect(self.display_surface, 'white', [screen_width - 290, screen_height/2 - 30, 260, 180], 0, 10)
        space_y = 0
        for i, text in enumerate(list_choose):
            blit_text(f'{text}', 'black', [screen_width - 260, screen_height/2 - 10 + space_y], self.font_50)
            if self.selected_action[0] == i:
                pygame.draw.rect(self.display_surface, 'black', [screen_width - 275, screen_height/2 - 5 + space_y, 10, 10], 0, 20)
            space_y += 50
        
        list_desc = ['Buy  an  item  using  Ticket  Points.', 'Trade  a  Bokumon  to  obtain  a  Ticket  Points.', 'See   you  later!']
        pygame.draw.rect(self.display_surface, [96, 112, 120], [20, screen_height - 120, screen_width - 40, 100], 0, 5)
        pygame.draw.rect(self.display_surface, 'black', [20, screen_height - 120, screen_width - 40, 100], 3, 5)
        pygame.draw.rect(self.display_surface, 'white', [30, screen_height - 110, screen_width - 60, 80], 0, 5)
        blit_text(f'{list_desc[self.selected_action[0]]}', 'black', [50, screen_height - 90], self.font_50)

    def draw_buy_items(self):
        pygame.draw.rect(self.display_surface, [112, 104, 128], [200, 20, 570, 450], 0, 10)
        pygame.draw.rect(self.display_surface, 'black', [200, 20, 570, 450], 3, 10)
        pygame.draw.rect(self.display_surface, 'white', [210, 30, 550, 430], 0, 10)
        
        blit_text(f'Your   T.P:    {self.player.tickets}', 'black', [220, 40], self.font_25)
        blit_text('Item', 'black', [250, 80], self.font_50)
        blit_text('Qnt.', 'black', [480, 80], self.font_50)
        blit_text('T.P', 'black', [630, 80], self.font_50)

        blit_text('*Obtain T.P Evolving, Upping or Trading a Bokumon', 'black', [220, screen_height-155], self.font_25)
        space_y = 0
        for i, item in enumerate(self.items_disp):
            if self.limit_visu_items[0] <= i <= self.limit_visu_items[1]:
                blit_text(f'{item[1][0]}', 'black', [250, 130 + space_y], self.font_42)
                blit_text(f'{item[0][1]}', 'black', [500, 140 + space_y], self.font_42, center=True)
                blit_text(f'{item[0][2]}', 'black', [650, 140 + space_y], self.font_42, center=True)
                if self.selected_item[0] == i:
                    color = 'black' if not self.selected_item[2] else 'red'
                    pygame.draw.rect(self.display_surface, color, [235, 135 + space_y, 10, 10], 0, 20)
                space_y += 40
            elif i > self.limit_visu_items[1]:
                break

        if self.selected_item[2] or self.cant_buy:
            pygame.draw.rect(self.display_surface, [96, 112, 120], [20, screen_height - 120, screen_width - 50, 100], 0, 5)
            pygame.draw.rect(self.display_surface, 'black', [20, screen_height - 120, screen_width - 50, 100], 3, 5)
            pygame.draw.rect(self.display_surface, 'white', [30, screen_height - 110, screen_width - 70, 80], 0, 5)
            sel_item = self.items_disp[self.selected_item[0]]
            if self.cant_buy:
                msg = "Don't have any Ticket Points."
            elif self.text_select_buy:
                msg = f"Buy {self.selected_item[1][0]*sel_item[0][1]} {sel_item[1][0]} using {self.selected_item[1][0]*sel_item[0][2]} Ticket Points?"
            else:
                msg =f'{sel_item[1][0]} is selected.'
            blit_text(msg, 'black', [50, screen_height - 90], self.font_50)

        if self.selected_item[2]:
            pygame.draw.rect(self.display_surface, [96, 112, 120], [screen_width - 230, screen_height - 220, 200, 100], 0, 5)
            pygame.draw.rect(self.display_surface, 'black', [screen_width - 230, screen_height - 220, 200, 100], 3, 5)
            pygame.draw.rect(self.display_surface, 'white', [screen_width - 220, screen_height - 210, 180, 80], 0, 5)
            zeros_txt = '000'
            zeros_txt = zeros_txt[:3-len(str(self.selected_item[1][0]))]
            blit_text(f'x{zeros_txt}{self.selected_item[1][0]}', 'black', [screen_width - 165, screen_height - 180], self.font_42)

        if self.selected_item[1][1]:
            pygame.draw.rect(self.display_surface, [96, 112, 120], [screen_width - 130, screen_height - 300, 100, 100], 0, 5)
            pygame.draw.rect(self.display_surface, 'black', [screen_width - 130, screen_height - 300, 100, 100], 3, 5)
            pygame.draw.rect(self.display_surface, 'white', [screen_width - 120, screen_height - 290, 80, 80], 0, 5)
            blit_text('Yes', 'black', [screen_width - 100, screen_height - 280], self.font_35)
            blit_text('No', 'black', [screen_width - 100, screen_height - 240], self.font_35)
            sel_y = screen_height - 275 if self.select_buy else screen_height - 235
            pygame.draw.rect(self.display_surface, 'black', [screen_width - 115, sel_y, 10, 10], 0, 20)
        
    def draw_trade(self):
        self.draw_player_trade()
        self.draw_merc_trade()

    def draw_merc_trade(self):
        pygame.draw.rect(self.display_surface, [56, 136, 136], [350, screen_height/2 - 200, 420, screen_height/2 + 60], 0, 10)
        pygame.draw.rect(self.display_surface, 'black', [350, screen_height/2 - 200, 420, screen_height/2 + 60], 3, 10)
        pygame.draw.rect(self.display_surface, 'white', [360, screen_height/2 - 190, 400, screen_height/2 + 40], 0, 10)
        blit_text('TRADE BOKUMON', 'black', [430, screen_height/2 - 170], self.font_50)
        blit_text(f'Your T.P:    {self.player.tickets}', 'black', [370, screen_height - 170], self.font_25)
        blit_text('=>', 'black', [550, screen_height/2 - 20], self.font_42)
        blit_text('T.P', 'black', [670, screen_height/2 + 50], self.font_42)
        pygame.draw.rect(self.display_surface, [60, 108, 112], [380, screen_height/2 - 50, 110, 80], 5)

        if self.select_player_boku[1]:
            sel_boku = self.player.bokumons[self.select_player_boku[0]]
            self.gain_tp = round(((sel_boku.attack + sel_boku.defense + sel_boku.speed + sel_boku.life)/2)/sel_boku.level)
            blit_text(f'{sel_boku.name}', 'black', [380, screen_height/2 - 110], self.font_42)
            blit_text(f'/{sel_boku.name}', 'black', [380, screen_height/2 - 80], self.font_42)
            blit_text(f'Lv{sel_boku.level}', 'black', [410, screen_height/2 + 50], self.font_42)
            blit_text(f'{self.gain_tp}', 'black', [690, screen_height/2 - 10], self.font_42, center=True)
            pygame.draw.rect(self.display_surface, [0, 120, 248], [385, screen_height/2 - 45, 100, 70])
            sel_boku.draw_modified([450, screen_height/2 + 5], 1.5)
            # choose
            pygame.draw.rect(self.display_surface, [56, 136, 136], [screen_width - 130, screen_height - 210, 100, 100], 0, 5)
            pygame.draw.rect(self.display_surface, 'black', [screen_width - 130, screen_height - 210, 100, 100], 3, 5)
            pygame.draw.rect(self.display_surface, 'white', [screen_width - 120, screen_height - 200, 80, 80], 0, 5)
            blit_text('Yes', 'black', [screen_width - 100, screen_height - 190], self.font_35)
            blit_text('No', 'black', [screen_width - 95, screen_height - 150], self.font_35)
            sel_y = screen_height - 185 if self.select_trade else screen_height - 145
            pygame.draw.rect(self.display_surface, 'black', [screen_width - 115, sel_y, 10, 10], 0, 20)
            # text
            pygame.draw.rect(self.display_surface, [96, 112, 120], [20, screen_height - 110, screen_width - 50, 100], 0, 5)
            pygame.draw.rect(self.display_surface, 'black', [20, screen_height - 110, screen_width - 50, 100], 3, 5)
            pygame.draw.rect(self.display_surface, 'white', [30, screen_height - 100, screen_width - 70, 80], 0, 5)
            blit_text(f'Trade  {sel_boku.name}  Lv{sel_boku.level}  for  {self.gain_tp}  Ticket Points?', 'black', [50, screen_height - 80], self.font_50)
        else:
            if self.cant_trade:
                pygame.draw.rect(self.display_surface, [96, 112, 120], [350, screen_height - 110, 420, 100], 0, 5)
                pygame.draw.rect(self.display_surface, 'black', [350, screen_height - 110, 420, 100], 3, 5)
                pygame.draw.rect(self.display_surface, 'white', [360, screen_height - 100, 400, 80], 0, 5)
                blit_text("Can't trade any more", 'black', [380, screen_height - 75], self.font_50)
            else:
                blit_text('Bokumon', 'black', [380, screen_height/2 - 90], self.font_42)
                blit_text('Lv', 'black', [410, screen_height/2 + 50], self.font_42)
                blit_text('0', 'black', [690, screen_height/2 - 10], self.font_42, center=True)


    def draw_player_trade(self):
        #bokumon_player_section
        pygame.draw.rect(self.display_surface, [56, 136, 136], [20, 10, 300, screen_height - 20])
        pygame.draw.rect(self.display_surface, [128, 168, 176], [20, 10, 300, screen_height - 20], 10)
        pygame.draw.rect(self.display_surface, [80, 96, 112], [20, 10, 300, screen_height - 20], 3)
        pygame.draw.rect(self.display_surface, [40, 104, 96], [30, 20, 280, screen_height - 40], 5)
        #bokumon's space
        pygame.draw.rect(self.display_surface, [60, 108, 112], [40, screen_height/2 - 70, 110, 80], 5)
        pygame.draw.rect(self.display_surface, [0, 120, 248], [45, screen_height/2 - 65, 100, 70])
        self.player.bokumons[0].draw_modified([110, screen_height/2 - 15], 1.5)
        if self.select_player_boku[0] == 0:
            pygame.draw.rect(self.display_surface, 'red', [40, screen_height/2 - 70, 110, 80], 5)
        space_y = 20
        for i in range(5):
            pygame.draw.rect(self.display_surface, [60, 108, 112], [180, 20 + space_y, 110, 80], 5)
            if i+1 <= len(self.player.bokumons)-1:
                pygame.draw.rect(self.display_surface, [0, 120, 248], [185, 25 + space_y, 100, 70])
                self.player.bokumons[i+1].draw_modified([250, space_y + 75], 1.5)
                if self.select_player_boku[0] == i+1:
                    pygame.draw.rect(self.display_surface, 'red', [180, 20 + space_y, 110, 80], 5)
            space_y += 90
        
        pygame.draw.rect(self.display_surface, [160, 208, 240], [195, 55 + space_y, 100, 40], 0, 5)
        blit_text_shadow('CANCEL', 'white', [208, 65 + space_y,], self.font_35, back_color='black')
        if self.select_player_boku[0] == 6:
            pygame.draw.rect(self.display_surface, 'red', [195, 55 + space_y, 100, 40], 3, 5)
        
    def draw(self):
        if not self.selected_action[1]:
            self.draw_select_action()
        else:
            if self.selected_action[0] == 0:
                self.draw_buy_items()
            if self.selected_action[0] == 1:
                self.draw_trade()
            
    def update(self):
        if self.timer.run:
            self.timer.update()
        self.input()

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.timer.run:
            if keys[pygame.K_UP]:
                if not self.selected_action[1]:
                    self.selected_action[0] -= 1 if self.selected_action[0] > 0 else 0
                else:
                    if self.selected_action[0] == 0:
                        if not self.selected_item[2]:
                            self.selected_item[0] -= 1 if self.selected_item[0] > 0 else 0
                            if self.selected_item[0] - 1 > 0 and self.limit_visu_items[1] > 7:
                                self.limit_visu_items[1] -= 1
                                self.limit_visu_items[0] -= 1
                        else:
                            if not self.selected_item[1][1]:
                                val_item = self.items_disp[self.selected_item[0]][0][2]
                                tp_count = self.selected_item[1][0] * val_item
                                self.selected_item[1][0] += 1 if tp_count < self.player.tickets else 0
                            else:
                                self.select_buy = True
                    
                    elif self.selected_action[0] == 1:
                        if not self.select_player_boku[1]:
                            if self.select_player_boku[0] > 0: 
                                if self.select_player_boku[0] - 1 < len(self.player.bokumons):
                                    self.select_player_boku[0] -= 1 
                                else:
                                    self.select_player_boku[0] = len(self.player.bokumons)-1
                            else:
                                self.select_player_boku[0] = 6
                        else:
                            self.select_trade = True                            
                        
            elif keys[pygame.K_DOWN]:
                if not self.selected_action[1]:
                    self.selected_action[0] += 1 if self.selected_action[0] < 2 else 0
                else:
                    if self.selected_action[0] == 0:
                        if not self.selected_item[2]:
                            self.selected_item[0] += 1 if self.selected_item[0] < len(self.items_disp)-1 else 0
                            if self.selected_item[0] + 1 >= self.limit_visu_items[1]:
                                self.limit_visu_items[1] += 1
                                self.limit_visu_items[0] += 1
                        else:
                            if not self.selected_item[1][1]:
                                self.selected_item[1][0] -= 1 if self.selected_item[1][0] > 1 else 0
                            else:
                                self.select_buy = False

                    elif self.selected_action[0] == 1:
                        if not self.select_player_boku[1]:
                            if self.select_player_boku[0] < 6: 
                                if self.select_player_boku[0] + 1 < len(self.player.bokumons):
                                    self.select_player_boku[0] += 1 
                                else:
                                    self.select_player_boku[0] = 6
                            else:
                                self.select_player_boku[0] = 0 
                        else:
                            self.select_trade = False

            elif keys[pygame.K_LEFT]:
                if not self.select_player_boku[1]:
                    if self.select_player_boku[0] > 0: 
                        if self.select_player_boku[0] - 1 < len(self.player.bokumons):
                            self.select_player_boku[0] -= 1 
                        else:
                            self.select_player_boku[0] = len(self.player.bokumons)-1
                    else:
                        self.select_player_boku[0] = 6

            elif keys[pygame.K_RIGHT]:
                if not self.select_player_boku[1]:
                    if self.select_player_boku[0] < 6: 
                        if self.select_player_boku[0] + 1 < len(self.player.bokumons):
                            self.select_player_boku[0] += 1 
                        else:
                            self.select_player_boku[0] = 6
                    else:
                        self.select_player_boku[0] = 0 

            if keys[pygame.K_z]:
                if not self.selected_action[1]:
                    if self.selected_action[0] == 0:
                        self.selected_action[1] = True 
                    elif self.selected_action[0] == 1:
                        self.selected_action[1] = True 
                    elif self.selected_action[0] == 2:
                        self.close = True
                        self.selected_action[0] = 0
                else:
                    if self.selected_action[0] == 0:
                        # buy choose
                        if not self.selected_item[2]:
                            if self.player.tickets > 0:
                                self.selected_item[2] = True
                                self.cant_buy = False
                            else:
                                self.cant_buy = True
                        else:
                            if not self.selected_item[1][1]:
                                self.selected_item[1][1] = True
                                self.text_select_buy = True
                            else:
                                if self.select_buy:  #buy
                                    item_list = self.items_disp[self.selected_item[0]]
                                    qnt = item_list[0][1]*self.selected_item[1][0]
                                    val = item_list[0][2]*self.selected_item[1][0]
                                    self.bag.buy_item(item_list[1], qnt, item_list[0][0])
                                    self.player.tickets -= val

                                self.selected_item[1][1] = False
                                self.selected_item[1][0] = 1
                                self.selected_item[2] = False
                                self.select_buy = False  
                                self.text_select_buy = False

                    elif self.selected_action[0] == 1:
                        # trade choose
                        if not self.select_player_boku[1]:
                            if self.select_player_boku[0] == 6:
                                self.selected_action[1] = False
                            else:
                                if len(self.player.bokumons) > 1:
                                    self.select_player_boku[1] = True
                                    self.cant_trade = False
                                else:
                                    self.cant_trade = True
                        else:
                            if not self.select_trade:
                                self.select_player_boku[1] = False
                            else:
                                self.select_player_boku[1] = False
                                self.select_trade = False
                                self.player.trade_bokumon(self.select_player_boku[0], self.gain_tp)
                                self.gain_tp = 0
                                if self.select_player_boku[0] > len(self.player.bokumons)-1:
                                        self.select_player_boku[0] -= 1
         
            elif keys[pygame.K_x]:
                if not self.selected_action[1]:
                    self.close = True
                    self.selected_action[0] = 0
                else:
                    if self.selected_action[0] == 0:
                        if not self.selected_item[2]:
                            self.selected_action[1] = False
                        else:
                            if not self.selected_item[1][1]:
                                self.selected_item[2] = False
                                self.selected_item[1][0] = 1
                            else:
                                self.select_buy = False
                                self.text_select_buy = False
                                self.selected_item[1][1] = False
                    
                    elif self.selected_action[0] == 1:
                        if not self.select_player_boku[1]:
                            self.selected_action[1] = False
                        else:
                            if self.select_player_boku[1]:
                                self.select_player_boku[1] = False
            self.timer.active()