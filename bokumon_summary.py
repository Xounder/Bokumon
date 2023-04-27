import pygame
from settings import *
from support import *
from timer import Timer

class BokuSummary:
    def __init__(self, screen, player):
        self.display_surface = screen
        self.player = player
        # vars
        self.seted = False
        self.active = False
        self.section = 0
        self.selected_move = [False, False, [0, 0]]
        self.boku_selected = None
        self.last_boku_pos = 0
        #fonts
        self.font_25 = pygame.font.Font('font/Pixeltype.ttf', 25)
        self.font_35 = pygame.font.Font('font/Pixeltype.ttf', 35)
        self.font_42 = pygame.font.Font('font/Pixeltype.ttf', 42)
        self.font_50 = pygame.font.Font('font/Pixeltype.ttf', 50)
        #boku_ball
        self.boku_ball_img = { 
            'Boku Ball': pygame.image.load('imgs/boku_ball.png').convert_alpha(),
            'Great Ball': pygame.image.load('imgs/great_ball.png').convert_alpha(),
            'Ultra Ball': pygame.image.load('imgs/ultra_ball.png').convert_alpha(),
        }
        #timer
        self.timer = Timer(0.12)

    def set_summary(self, boku_selected, view=True):
        if not self.seted:
            self.boku_selected = boku_selected
            self.view = view
            if not view:
                self.boku_local = self.player.bokumon_storage
            else:
                self.boku_local = self.player.bokumons
            self.section = 0
            self.selected_move = [False, False, [0, 0]]
            self.seted = True
    
    def draw(self):
        # parte de cima
        pygame.draw.rect(self.display_surface, [72, 152, 112], (0, 0, screen_width, 50))
        pygame.draw.rect(self.display_surface, [120, 216, 160], (-20, 0, screen_width/2 + 50, 50), 0, 20)
        move_x = screen_width/2 if not self.section == 1 else screen_width/2 + 50
        pygame.draw.rect(self.display_surface, [248, 232, 152], (-20, 0, move_x, 50), 0, 20)
        pygame.draw.rect(self.display_surface, 'black', (-20, 0, move_x, 50), 3, 20)
        pygame.draw.rect(self.display_surface, 'black', (-20, 0, screen_width + 30, 50), 3)
        section_text = 'Bokumon  Skill' if self.section == 0 else 'Know  Moves'
        blit_text(section_text, 'black', (10, 15), self.font_50)
        # dots
        color_1 = [192, 160, 96] if self.section == 0 else [248, 248, 248]
        color_2 = [192, 160, 96] if self.section == 1 else [248, 248, 248]
        pygame.draw.rect(self.display_surface, color_1, (screen_width/2 - 10, 12, 20, 25), 0, 30)
        pygame.draw.rect(self.display_surface, color_2, (screen_width/2 - 60, 12, 20, 25), 0, 30)
        # draw seção especifica
        if self.section == 0:
            self.draw_skill_move()
        else:
            self.draw_know_move()
        # bokumon
        pygame.draw.rect(self.display_surface, [120, 128, 144], (0, 49, screen_width/2, screen_height/2))
        pygame.draw.rect(self.display_surface, 'black', (-20, 49, screen_width/2 + 20, screen_height/2), 3)
        pygame.draw.rect(self.display_surface, [192, 192, 192], (5, 100, screen_width/2 - 15, screen_height/2 - 60))
        blit_text(f'Lv{self.boku_local[self.boku_selected].level}', 'black', (10, 60), self.font_50)
        blit_text(f'{self.boku_local[self.boku_selected].name}', 'black', (130, 60), self.font_50)
        self.boku_local[self.boku_selected].draw_modified((160, 200), 0.7)
        self.draw_boku_ball((screen_width/2 - 40, screen_height/2 + 30), 1.7)
        

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.timer.run:
            if keys[pygame.K_LEFT]:
                if not self.selected_move[0]:
                    self.section = 0
            elif keys[pygame.K_RIGHT]:
                if not self.selected_move[0]:
                    self.section = 1
            elif keys[pygame.K_UP]:
                if not self.selected_move[0]:
                    self.boku_selected -= 1 if self.boku_selected > 0 else 0
                else:
                    self.move_marked(-1, 0, self.selected_move[1])
                    self.move_marked(-1, 1, False)
            elif keys[pygame.K_DOWN]:
                if not self.selected_move[0]:
                    self.boku_selected += 1 if self.boku_selected < len(self.boku_local) - 1 else 0
                else:
                    self.move_marked(1, 0, self.selected_move[1])
                    self.move_marked(1, 1, False)

            if keys[pygame.K_z]:
                if not self.selected_move[0] and self.section == 1:
                    self.selected_move[0] = True
                elif self.selected_move[0]:
                    if self.selected_move[2][0] != 4:
                        self.selected_move[1] = True
                    else:
                        self.selected_move[0] = False
                        self.selected_move[2] = [0, 0]
                if self.selected_move[1] and self.selected_move[2][0] != self.selected_move[2][1]:
                    self.boku_local[self.boku_selected].switch_moves(self.selected_move[2])
                    self.selected_move[1] = False
                    self.selected_move[0] = False
                    self.selected_move[2][0] = self.selected_move[2][1]
                
            elif keys[pygame.K_x]:
                if not self.selected_move[0]:
                    self.active = False
                    self.last_boku_pos = self.boku_selected
                elif self.selected_move[1]:
                    self.selected_move[1] = False
                    self.selected_move[2][0] = self.selected_move[2][1]
                else:
                    self.selected_move[0] = False
            self.timer.active()
                
    def update(self):
        if self.timer.run:
            self.timer.update()
        self.input()

    def draw_boku_ball(self, rect_center, scale):
        bokumon_ball = self.boku_local[self.boku_selected].ball
        self.boku_ball_rect = self.boku_ball_img[bokumon_ball].get_rect(center = (rect_center))
        image_mod = pygame.transform.scale(self.boku_ball_img[bokumon_ball], (self.boku_ball_img[bokumon_ball].get_width()/scale, 
                                                                    self.boku_ball_img[bokumon_ball].get_height()/scale))
        self.display_surface.blit(image_mod, self.boku_ball_rect)

    def draw_skill_move(self):
        #bloco
        pygame.draw.rect(self.display_surface, [160, 178, 196], (0, 50, screen_width, screen_height))
            #details
        pygame.draw.rect(self.display_surface, [212, 228, 246], (0, 50, screen_width/2 + 3, screen_height/2 + 2))
        pygame.draw.rect(self.display_surface, [212, 228, 246], (screen_width/2 + 3, 50, screen_width/2 + 3, 3))
        # stats
            # life
        atual_boku = self.boku_local[self.boku_selected]
        pygame.draw.rect(self.display_surface, [232, 240, 248], (screen_width/2 + 120, 60, 250, 40), 0, 10)
        pygame.draw.rect(self.display_surface, 'black', (screen_width/2 + 10, 70, 120, 20), 0, 15)
        blit_text('HP', 'white', (screen_width/2 + 70, 82), self.font_35, center=True)
        blit_text(f'{atual_boku.atual_life}/{atual_boku.life}', 'black', (screen_width - 40, 70), self.font_50, right=True)
            #rect life
        pygame.draw.rect(self.display_surface, 'black', (screen_width/2 + 140, 100, 220, 20), 0, 5)
        blit_text('HP', 'yellow', (screen_width/2 + 145, 102), self.font_35)
        pygame.draw.rect(self.display_surface, 'white', (screen_width/2 + 175, 105, 178, 10))
        x_life =  178 * atual_boku.atual_life/atual_boku.life
        pygame.draw.rect(self.display_surface, 'green', (screen_width/2 + 175, 105, x_life, 10))
            # other stats
        space_y = 120
        name_list = ['ATTACK', 'DEFENSE', 'SPEED', 'CRIT']
        stats_list = [f'{atual_boku.attack}', f'{atual_boku.defense}', f'{atual_boku.speed}', f'{atual_boku.critical_chance}%']
        for i in range(4):
            pygame.draw.rect(self.display_surface, [232, 240, 248], (screen_width - 130, space_y, 100, 40), 0, 10)
            pygame.draw.rect(self.display_surface, 'black', (screen_width/2 + 10, space_y + 10, 120, 20), 0, 15)
            blit_text(name_list[i], 'white', (screen_width/2 + 70, space_y + 22), self.font_35, center=True)
            blit_text(stats_list[i], 'black', (screen_width - 40, space_y + 10), self.font_42, right=True)
            space_y += 60
        blit_text('Chance', 'white', (screen_width/2 + 70, space_y - 23), self.font_25, center=True)
        # parte de baixo
            # EXP
        pygame.draw.rect(self.display_surface, [200, 216, 232], (200, screen_height - 240, screen_width - 230, 100), 0, 10)
        pygame.draw.rect(self.display_surface, 'black', (10, screen_height - 210, 200, 20), 0, 15)
        blit_text('EXP', 'white', (110, screen_height - 197), self.font_42, center=True)
        blit_text('Exp.  Points', 'black', (240, screen_height - 220), self.font_50)
        blit_text('Next  Lv.', 'black', (240, screen_height - 170), self.font_50)
                # valores exp
        pygame.draw.rect(self.display_surface, [232, 240, 248], (screen_width - 260, space_y + 10, 230, 80))
        pygame.draw.rect(self.display_surface, [232, 240, 248], (screen_width - 260, space_y, 230, 50), 0, 10)
        pygame.draw.rect(self.display_surface, [232, 240, 248], (screen_width - 260, space_y + 50, 230, 50), 0, 10)
        blit_text(f'{atual_boku.all_exp}', 'black', (screen_width - 40, space_y + 20), self.font_42, right=True)
        blit_text(f'{round(atual_boku.up_exp - atual_boku.atual_exp)}', 'black', (screen_width - 40, space_y + 70), self.font_42, right=True)
                # divisoria
        pygame.draw.rect(self.display_surface, [232, 240, 248], (230, screen_height - 189, screen_width - 260, 3), 0, 10)
        pygame.draw.rect(self.display_surface, [200, 216, 232], (screen_width - 260, screen_height - 189, 220, 3), 0, 10)      
                # rect exp
        pygame.draw.rect(self.display_surface, 'black', (screen_width - 290, space_y + 100, 255, 20), 0, 10)
        blit_text('EXP', 'yellow', (screen_width - 280, space_y + 105), self.font_25)
        pygame.draw.rect(self.display_surface, 'white', (screen_width - 248, space_y + 103, 208, 14), 0, 20)
        pygame.draw.rect(self.display_surface, [137, 141, 145], (screen_width - 240, space_y + 105, 195, 10))
        x_exp =  195 * atual_boku.atual_exp/atual_boku.up_exp
        pygame.draw.rect(self.display_surface, 'blue', (screen_width - 240, space_y + 105, x_exp, 10))  


    def draw_know_move(self):
        atual_bokumon = self.boku_local[self.boku_selected]
        # bloco
        pygame.draw.rect(self.display_surface, [160, 178, 196], (0, screen_height/2 + 49, screen_width/2, screen_height/2))
        pygame.draw.rect(self.display_surface, [150, 158, 174], (screen_width/2 - 1, 49, screen_width/2 + 1, screen_height - 49))
        pygame.draw.rect(self.display_surface, 'black', (screen_width/2 - 1, 49, screen_width/2 + 1, screen_height - 49), 3)
        # moves
        space_y = 70
        for i in range(5):
            if i != 4:
                pygame.draw.rect(self.display_surface, [240, 240, 248], (screen_width/2 + 20, space_y, screen_width/2 - 35, 80), 0, 10)
                blit_text(f'{atual_bokumon.moves[i][0]}', 'black', (screen_width/2 + 130, space_y + 10), self.font_50)
                blit_text(f'PP', 'black', (screen_width/2 + 235, space_y + 53), self.font_42)
                blit_text(f'{atual_bokumon.moves_pp[i][0]}/{atual_bokumon.moves_pp[i][1]}', 'black', 
                                                                            (screen_width/2 + 270, space_y + 50), self.font_50)
            else:
                if self.selected_move[0]:
                    blit_text(f'Cancel', 'black', (screen_width/2 + 130, space_y + 10), self.font_50)

            if (self.selected_move[2][0] == i or self.selected_move[2][1] == i) and self.selected_move[0]:
                color = 'blue' if (self.selected_move[1] and self.selected_move[2][0] == i) else 'red'
                pygame.draw.rect(self.display_surface, color, (screen_width/2 + 20, space_y, screen_width/2 - 35, 80), 3, 10)
            space_y += 100 

        if self.selected_move[0]:
            # especification move
            pygame.draw.rect(self.display_surface, [232, 240, 248], (160, screen_height/2 + 90, 100, 40), 0, 10)
            pygame.draw.rect(self.display_surface, 'black', (20, screen_height/2 + 100, 120, 20), 0, 15)
            blit_text('POWER', 'white', (80, screen_height/2 + 112), self.font_35, center=True)

            pygame.draw.rect(self.display_surface, [232, 240, 248], (160, screen_height/2 + 140, 100, 40), 0, 10)
            pygame.draw.rect(self.display_surface, 'black', (20, screen_height/2 + 150, 120, 20), 0, 15)
            blit_text('ACCURACY', 'white', (80, screen_height/2 + 162), self.font_35, center=True)
            if self.selected_move[2][1] != 4:
                blit_text(f'{atual_bokumon.moves[self.selected_move[2][1]][1]}', 'black', (240, screen_height/2 + 100), self.font_42, right=True)
                blit_text(f'{atual_bokumon.moves[self.selected_move[2][1]][2]}', 'black', (240, screen_height/2 + 150), self.font_42, right=True)
    
    def move_marked(self, move, pos, selected):
        if not selected:
            expect_move = self.selected_move[2][pos] + move
            max = 4 if self.selected_move[0] and not self.selected_move[1] else 3
            if 0 <= expect_move <= max:
                self.selected_move[2][pos] = expect_move
                
