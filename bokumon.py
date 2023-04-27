import pygame
from settings import *
from random import randint
from bokumons_settings import *

class BokuMon:
    def __init__(self, screen, name, wild=False,level=5):
        self.display_surface = screen
        img_surf = pygame.image.load(f'imgs/bokumon/{name}.png').convert_alpha()
        self.image = pygame.transform.scale(img_surf, (tile_size*3, tile_size*3))
        self.rect = self.image.get_rect(center= (boku_pos[0] if wild else boku_pos[1]))

        # atributes
        self.name = name
        self.previous_name = name
        self.atual_name = name
        self.wild = wild
        self.step_evolution()

        self.level = level
        dif_level = self.level - 5
        bokumon_stats = initial_atrib(self.name, dif_level)
        self.life = bokumon_stats[0]
        self.atual_life = self.life
        self.attack = bokumon_stats[1]
        self.defense = bokumon_stats[2]
        self.speed = bokumon_stats[3]
        self.critical_chance =  bokumon_stats[4]
        self.up_exp = 20 + self.level if self.level <= 5 else 25 * (abs(self.level-5) + 1)
        self.atual_exp = randint(0, round(self.up_exp/2))
        self.all_exp = self.atual_exp
        self.atrib_ups = [0, 0, 0, 0, 0]
        self.ball = 'Boku Ball'
        if wild:
            self.prevent_run = 5 + randint(0, level + 10) 
            self.catch_rate = randint(190, 255) - round(self.level, self.level*2) - self.level
            if self.catch_rate <= 0:
                self.catch_rate = randint(5, 40)
        # attacks type (por hr so um atk normal)
            # Nome, dano, chance de acerto, PP
        a =  ['Crunch', 40, 90, [10, 10]] if self.name == 'Snacks' else  ['Punch', 40, 90, [10, 10]]
        self.moves = [['Scratch', 30, 100, [20, 20]], ['Headbutt', 50, 80, [10, 10]], ['Bite', 45, 85, [15, 15]], a]
        self.moves_pp = [self.moves[0][3], self.moves[1][3], self.moves[2][3], self.moves[3][3]]
        
    def upgrade(self):
        # somente para os player_bokumons
        if self.atual_exp >= self.up_exp:
            self.all_exp += self.atual_exp
            self.atual_exp = 0
            self.level += 1
            self.up_exp = 20 + self.level if self.level <= 5 else 25 * (abs(self.level-5) + 1)
            self.atrib_ups = [randint(1, 3), randint(1, 3), randint(1, 3), randint(1, 3), randint(0, 1)]
            self.life += self.atrib_ups[0]
            self.atual_life = self.life
            self.attack += self.atrib_ups[1]
            self.defense += self.atrib_ups[2]
            self.speed += self.atrib_ups[3]
            self.critical_chance += self.atrib_ups[4]
            if not self.evolved[0][0]:
                if self.level >= bokumons_evo_lvl[self.name]:
                    self.evolved[0][0] = True
            elif not self.evolved[1][0]:
                if self.level >= bokumons_evo_lvl[self.name]:
                    self.evolved[1][0] = True
            return True
        return False

    def step_evolution(self):
        #[[evoluir o boku, mostrar a evo],[evoluir o boku, mostrar a evo]]
        self.evo_step = bokumons_evo_steps[self.name]
        if len(self.evo_step) == 2:
            self.evolved = [[False, False], [False, False]]
        elif len(self.evo_step) == 1:
            self.evolved = [[True, True], [False, False]]
        else:
            self.evolved = [[True, True], [True, True]]

    def evolve(self):
        self.previous_name = self.name
        self.name = self.evo_step[0]
        self.image = img_surf = pygame.image.load(f'imgs/bokumon/{self.name}.png').convert_alpha()
        self.image = pygame.transform.scale(img_surf, (tile_size*3, tile_size*3))
        self.evo_step = bokumons_evo_steps[self.name] ###
        if self.evolved[0][1]:
            self.evolved[0][1] = True
        else:
            self.evolved[1][1] = True
        self.atrib_ups = [randint(1, 6), randint(1, 6), randint(1, 6), randint(1, 6), randint(1, 2)]
        self.life += self.atrib_ups[0]
        self.atual_life = self.life
        self.attack += self.atrib_ups[1]
        self.defense += self.atrib_ups[2]
        self.speed += self.atrib_ups[3]
        self.critical_chance += self.atrib_ups[4]

    def draw(self, rect_center):
        self.rect.center = rect_center
        self.display_surface.blit(self.image, self.rect)
    
    def draw_modified(self, rect_center, scale):
        self.rect.center = rect_center
        image_mod = pygame.transform.scale(self.image, (self.image.get_width()/scale, self.image.get_height()/scale))
        self.display_surface.blit(image_mod, self.rect)

    
    def update(self):
        pass

    def restore_life(self, pot):
        if 0 < self.atual_life < self.life:
            hp_restored = self.atual_life + pot
            self.atual_life = hp_restored if hp_restored <= self.life else self.life
            return True
        return False
    
    def restore_all(self):
        self.atual_life = self.life
        for move in self.moves:
            move[3][0] = move[3][1]
    
    def switch_moves(self, num_move):
        aux = self.moves[num_move[0]]
        self.moves[num_move[0]] = self.moves[num_move[1]]
        self.moves[num_move[1]] = aux