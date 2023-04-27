import pygame
from settings import screen_height, screen_width
from support import blit_text, blit_text_shadow
from timer import Timer

class LetterSelection:
    def __init__(self, screen):
        self.display_surface = screen
        self.timer = Timer(0.12)
        
        
        self.active = False
        self.activate('Carbink', True)

        self.letter_selection = [['A', 'B', 'C', 'D', 'E', 'F', 'G', 'lower'],
                                 ['H', 'I', 'J', 'K', 'L', 'M', 'N', 'BACK'],
                                 ['O', 'P', 'Q', 'R', 'S', 'T', '.', 'OK'],
                                 ['U', 'V', 'W', 'X', 'Y', 'Z', ',', '']]

        self.font_20 = pygame.font.Font('font/Pixeltype.ttf', 20)
        self.font_25 = pygame.font.Font('font/Pixeltype.ttf', 25)
        self.font_35 = pygame.font.Font('font/Pixeltype.ttf', 35)
        self.font_42 = pygame.font.Font('font/Pixeltype.ttf', 42)
        self.font_50 = pygame.font.Font('font/Pixeltype.ttf', 50)

    def activate(self, name, first=False):
        if not first:
            self.active = True
        self.name_choosed = ''
        self.selected_button = [0, 0]
        self.letter_lower = False
        self.name_changed = False
        self.real_name = name

    def draw(self):
        self.draw_ballon_text()
        self.draw_buttons()
        self.draw_letters()

    def draw_letters(self):
        space = [0, 0]
        for i in range(4):
            for j in range(7):
                letter = self.letter_selection[i][j]
                letter = letter if not self.letter_lower else letter.lower()
                blit_text_shadow(letter, 'white', (110 + space[1], screen_height/2 - 50 + space[0]), self.font_50, center=True)
                if self.selected_button[0] == i and self.selected_button[1] == j:
                    pygame.draw.rect(self.display_surface, 'red', (90 + space[1], screen_height/2 - 75 + space[0], 40, 40), 3, 15)
                space[1] += 70
            space[1] = 0
            space[0] += 90

    def draw_ballon_text(self):
        pygame.draw.rect(self.display_surface, [224, 216, 88], (0, 0, screen_width, screen_height))
        pygame.draw.rect(self.display_surface, [192, 184, 176], (100, 20, screen_width - 200, 150), 0, 15)
        pygame.draw.rect(self.display_surface, [140, 140, 136], (100, 20, screen_width - 200, 150), 3, 15)
        pygame.draw.rect(self.display_surface, 'white', (110, 30, screen_width - 220, 130), 0, 15)
        blit_text(f"{self.real_name}'s nickname?", 'black', (250, 60), self.font_50)
        spaces = '_ _ _ _ _ _ _ _ _ _'
        count_space = spaces[(0 if len(self.name_choosed)== 0 else 1):(len(spaces) - len(self.name_choosed)*2)]
        word_modified = self.append_space(self.name_choosed)
        blit_text(f'{word_modified}{count_space}', 'black', (250, 120), self.font_50)
    
    def append_space(self, word):
        new_word = ''
        if len(word) > 0:
            for letter in word:
                new_word += letter + ' '
        return new_word
        
    def draw_buttons(self):
        pygame.draw.rect(self.display_surface, [152, 200, 224], (60, screen_height/2 - 100, screen_width - 250, screen_height/2 + 70))
        pygame.draw.rect(self.display_surface, [96, 136, 160], (60, screen_height/2 - 100, screen_width - 250, screen_height/2 + 70), 3)
        pygame.draw.rect(self.display_surface, [120, 168, 192], (70, screen_height/2 - 90, screen_width - 270, screen_height/2 + 50))
        pygame.draw.rect(self.display_surface, [72, 112, 136], (70, screen_height/2 - 90, screen_width - 270, screen_height/2 + 50), 3)
        space_y = - 50
        text_list = ['lower', 'BACK', 'OK']
        for i in range(3):
            color = [208, 152, 112] if i == 0 else [224, 216, 88]
            color_sel = 'red' if self.selected_button[0] == i and self.selected_button[1] == 7 else 'black'
            pygame.draw.rect(self.display_surface, 'white', (screen_width - 185, screen_height/2 + space_y, 130, 50), 0, 15)
            pygame.draw.rect(self.display_surface, color_sel, (screen_width - 185, screen_height/2 + space_y, 130, 50), 3, 15)
            pygame.draw.rect(self.display_surface, color, (screen_width - 180, screen_height/2 + 5 + space_y, 120, 40), 0, 10)
            blit_text(text_list[i], 'white', (screen_width - 120, screen_height/2 + 30 + space_y), self.font_50, center=True)
            space_y += 120

    def update(self):
        if self.timer.run:
            self.timer.update()
        self.input()

    def input(self):
        if not self.timer.run:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                self.selected_button[0] -= 1 if self.selected_button[0] > 0 else 0
            elif keys[pygame.K_DOWN]:
                self.selected_button[0] += 1 if self.selected_button[0] < 3 else 0
                if self.letter_selection[self.selected_button[0]][self.selected_button[1]] == '':
                    self.selected_button[0] -= 1
            elif keys[pygame.K_LEFT]:
                if self.letter_selection[self.selected_button[0]][self.selected_button[1]] == 'OK':
                    self.selected_button[0] += 1
                self.selected_button[1] -= 1 if self.selected_button[1] > 0 else 0
            elif keys[pygame.K_RIGHT]:
                self.selected_button[1] += 1 if self.selected_button[1] < 7 else 0
                if self.letter_selection[self.selected_button[0]][self.selected_button[1]] == '':
                    self.selected_button[0] -= 1

            if keys[pygame.K_x]:
                if len(self.name_choosed) > 0:
                    self.name_choosed = self.name_choosed[:len(self.name_choosed)-1]
            elif keys[pygame.K_z]:
                if self.selected_button[1] == 7:
                    if self.selected_button[0] == 0: #lower
                        self.letter_lower = not self.letter_lower
                    elif self.selected_button[0] == 1: #back
                        self.name_choosed = self.name_choosed[:len(self.name_choosed)-1]
                    elif self.selected_button[0] == 2:
                        self.active = False
                        self.name_changed = True
                elif len(self.name_choosed) < 9:
                    letter = self.letter_selection[self.selected_button[0]][self.selected_button[1]]
                    self.name_choosed += letter if not self.letter_lower else letter.lower()
            self.timer.active()
    