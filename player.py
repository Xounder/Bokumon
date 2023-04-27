import pygame
from settings import *
from map import map_1
from bokumon import BokuMon
from random import randint
from timer import Timer

class Player: 
    def __init__(self, screen, camera):
        self.display_surface = screen
        self.import_assets()
        self.name = 'gold'
        self.frame_index = 0
        self.status = 'down'
        self.previous_status = 'down'
        self.position = [round(len(map_1)/2), round(len(map_1[0])/2)]
        self.previous_position = self.position

        self.camera = camera
        self.battle = False
        self.bokumons_restored = False
        self.use_pc = False
        self.use_store = False
        self.tickets = 0
        # image
        self.image = self.frames[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft= ((self.position[0] * tile_size) - self.camera[0], (self.position[1] * tile_size) - self.camera[1]))
        # player bokumon
        self.bokumons = [BokuMon(self.display_surface, 'Pan')]
        self.atual_bokumon = self.bokumons[0]
        self.bokumons_battle = [0, 1, 2, 3, 4, 5]
        self.bokumon_part_battle = []
        self.reseted_pos = False
        # bokumon storage 
        self.bokumon_storage = []
        # timer inputs
        self.timer = Timer(0.12)

    def import_assets(self):
        self.frames = {'up': [], 'down': [], 'left': [], 'right': []}
        for direction in self.frames:
            path = 'imgs/player/' + direction + '/'
            for i in range(3):
                image = pygame.transform.scale(pygame.image.load(path + f'{i}.png').convert_alpha(), (tile_size, tile_size))
                self.frames[direction].append(image)

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.timer.run:
            if keys[pygame.K_UP]:
                if self.status != 'up':
                    self.status = 'up'
                else:
                    self.move_player([0, -1])
            elif keys[pygame.K_DOWN]:
                if self.status != 'down':
                    self.status = 'down'
                else:
                    self.move_player([0, 1])
            elif keys[pygame.K_LEFT]:
                if self.status != 'left':
                    self.status = 'left'
                else:
                    self.move_player([-1, 0])
            elif keys[pygame.K_RIGHT]:
                if self.status != 'right':
                    self.status = 'right'
                else:
                    self.move_player([1, 0])
            elif keys[pygame.K_s]:
                self.previous_status = self.status
                self.status = 'menu'
            else:
                self.frame_index = 0 
                self.move_player([0, 0])

            if keys[pygame.K_z]:
                if map_1[self.position[1]-1][self.position[0]] == 'H' and self.status == 'up':
                    self.bokumon_restore()
                    self.status = 'down'
                elif map_1[self.position[1]-1][self.position[0]] == 'P' and self.status == 'up':
                    self.use_pc = True
                elif map_1[self.position[1]-1][self.position[0]] == 'S' and self.status == 'up':
                    self.use_store = True
            self.timer.active()
    
    def move_player(self, move):
        expect_pos = [self.position[0] + move[0], self.position[1] + move[1]]
        self.previous_position = self.position

        if expect_pos[0] < 0 or expect_pos[0] > len(map_1[0]) - 1:
            return
        if expect_pos[1] < 0 or expect_pos[1] > len(map_1) - 1:
            return
        if map_1[expect_pos[1]][expect_pos[0]] == 'H':
            return
        if map_1[expect_pos[1]][expect_pos[0]] == 'P':
            return
        if map_1[expect_pos[1]][expect_pos[0]] == 'S':
            return
                    
        self.position = expect_pos
        self.rect.topleft = (((self.position[0] * tile_size) - self.camera[0]), (self.position[1] * tile_size) - self.camera[1])
        if map_1[expect_pos[1]][expect_pos[0]] == 'G' and self.previous_position != self.position and self.bokumon_alive():
            # caso esteja na grama verificar possiveis batalhas
            if self.wild_bokumon_chance():
                self.bokumons_restored = False
                self.battle = True
                self.bokumons_battle = [0, 1, 2, 3, 4, 5]
                self.reseted_pos = False
                if not self.bokumon_is_alive(0):
                    for i in range(1, 6):
                        if self.bokumon_is_alive(i):
                            self.bokumons_battle[0] = i
                            self.bokumons_battle[i] = 0
                            self.switch_bokumon([0, i])
                            break

    def wild_bokumon_chance(self, limit=6):
        # chance de aparecer o bokumon selvagem
        chance = randint(0, 10)
        if chance <= limit:
            return True
            
    def animate(self):
        self.frame_index += 0.09
        if self.frame_index >= len(self.frames[self.status]):
            self.frame_index = 0
        self.image = self.frames[self.status][int(self.frame_index)]

    def update(self):
        if self.timer.run:
            self.timer.update()
        self.animate()
        self.input()            
        
    def draw(self):
        self.display_surface.blit(self.image, self.rect)
    
    def bokumon_alive(self):
        for i, bokumon in enumerate(self.bokumons):
            if bokumon.atual_life > 0:
                #talvez fazer um bokumon_alive sem essa parte e outro com (nsei)
                if i == 0:
                    self.atual_bokumon = self.bokumons[0]
                else:
                    self.atual_bokumon = self.bokumons[i]
                return True
        return False
    
    def bokumon_is_alive(self, num):
        if self.bokumons[num].atual_life > 0:
            return True
        return False
    
    def switch_bokumon(self, num_bokumon, battle=False):
        aux = self.bokumons[num_bokumon[0]]
        self.bokumons[num_bokumon[0]] = self.bokumons[num_bokumon[1]]
        self.bokumons[num_bokumon[1]] = aux
        self.atual_bokumon = self.bokumons[0]
        if battle:
            if self.bokumon_part_battle.count(num_bokumon[1]) == 0:
                self.bokumon_part_battle.append(num_bokumon[1])
            self.switch_bokumon_battle(num_bokumon)
    
    def switch_bokumon_battle(self, num_bokumon):
        aux = self.bokumons_battle[num_bokumon[0]]
        self.bokumons_battle[num_bokumon[0]] = self.bokumons_battle[num_bokumon[1]]
        self.bokumons_battle[num_bokumon[1]] = aux
    
    def del_bokumon_dont_part(self):
        for i in range(len(self.bokumon_part_battle)-1, -1, -1):
            if self.bokumons[self.bokumon_part_battle[i]].atual_life <= 0:
                self.bokumon_part_battle.pop(i)
    
    def reset_bokumons_position(self):
        if not self.reseted_pos:
            for i in range(len(self.bokumons)):
                index_i = self.bokumons_battle.index(i)
                aux = self.bokumons_battle[i]
                self.bokumons_battle[i] = self.bokumons_battle[index_i]
                self.bokumons_battle[index_i] = aux
                self.switch_bokumon([i, index_i])
            self.reseted_pos = True

    def bokumon_pc_box(self, boku_num, pc_to_player=True):
        if pc_to_player:
            self.bokumons.append(self.bokumon_storage[boku_num])
            self.bokumon_storage.pop(boku_num)
        else:
            self.bokumon_storage.append(self.bokumons[boku_num])
            self.bokumons.pop(boku_num)
            self.atual_bokumon = self.bokumons[0]

    def trade_bokumon(self, boku_num, gain_tp):
        self.tickets += gain_tp
        self.bokumons.pop(boku_num)

    def bokumon_restore(self):
        if not self.bokumons_restored:
            for bokumon in self.bokumons:
                bokumon.restore_all()
            self.bokumons_restored = True
    
    def catch_bokumon(self, new_bokumon):
        new_bokumon.wild = False
        if len(self.bokumons) < 6:
            self.bokumons.append(new_bokumon)
        else:
            self.bokumon_storage.append(new_bokumon)
    
    #   LOAD GAME 
    def first_bokumon(self, new_bokumon):
        self.bokumons.append(new_bokumon)
        self.bokumons.pop(0)
        self.atual_bokumon = self.bokumons[0]

    def load_states(self, player_state, bokumon_state, bokumon_store):
        # player
        self.name = player_state[0]
        self.previous_status = player_state[1]
        self.position = player_state[2]
        self.tickets = player_state[3]
        # player bokumons
        self.load_state_bokumons(bokumon_state, self.bokumons)
        # storage bokumons
        if bokumon_store:
            self.load_state_bokumons(bokumon_store, self.bokumon_storage)

    def load_state_bokumons(self, list_state, self_list):
        for i, boku in enumerate(list_state):
            if i > len(self_list) - 1:
                self_list.append(BokuMon(self.display_surface, boku[0][0]))
            img_surf = pygame.image.load(f'imgs/bokumon/{boku[0][0]}.png').convert_alpha()
            self_list[i].image = pygame.transform.scale(img_surf, (tile_size*3, tile_size*3))
            self_list[i].name = boku[0][0]
            self_list[i].previous_name = self_list[i].name 
            self_list[i].level = boku[0][1]
            self_list[i].life = boku[0][2]
            self_list[i].atual_life = boku[0][3]
            self_list[i].attack = boku[0][4]
            self_list[i].defense = boku[0][5]
            self_list[i].speed = boku[0][6]
            self_list[i].critical_chance = boku[0][7]
            self_list[i].atual_exp = boku[0][8]
            self_list[i].up_exp = boku[0][9]
            self_list[i].all_exp = boku[0][10]
            self_list[i].ball = boku[0][11]
            self_list[i].atual_name = boku[0][12]
            self_list[i].step_evolution()
            for j in range(1, 5):
                self_list[i].moves[j-1] = [boku[j][0].replace("'", ''), boku[j][1], boku[j][2], [boku[j][3], boku[j][4]]]
            self_list[i].moves_pp = [self_list[i].moves[0][3], self_list[i].moves[1][3], 
                                         self_list[i].moves[2][3], self_list[i].moves[3][3]]
