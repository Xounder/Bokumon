from random import randint
import math

class BattleControl:
    def __init__(self):
        self.player_bokumon = None
        self.wild_bokumon = None
        self.end_battle = False
        self.winner = None
        self.player_damage = 0
        self.wild_damage = 0
        self.exp_points = 0
        self.rounds = 0
        self.critical = [False, False]
        self.miss_attack = [False, False]
        self.catch_bokumon = False
        self.ball_shake_times = 0
        self.wild_selected_move = None

    def set_first_bokumon(self, wild_bokumon, player_bokumon, first=False):
        if not first:
            self.choose_first()
        self.wild_bokumon = wild_bokumon
        self.player_bokumon = player_bokumon
        self.end_battle = False
        self.winner = None
        self.exp_points = 0
        self.rounds = 0

    def choose_first(self):
        if self.player_bokumon.speed < self.wild_bokumon.speed:
            self.first_turn = 'wild'
        else:
            self.first_turn = 'player'
    
    def catch_bokumon_chance(self, ball_effective):
        self.catch_bokumon = False
        self.ball_shake_times = 0
        max_catch = ((3*self.wild_bokumon.life - 2*self.wild_bokumon.life) * (self.wild_bokumon.catch_rate*ball_effective)) / (3*self.wild_bokumon.life)
        max_catch = (2**20 - 2**4) / (math.sqrt(math.sqrt((2**24 - 2**16) / max_catch)))
        catch_value = ((3*self.wild_bokumon.life - 2*self.wild_bokumon.atual_life) * (self.wild_bokumon.catch_rate*ball_effective)) / (3*self.wild_bokumon.life)
        catch = (2**20 - 2**4) / (math.sqrt(math.sqrt((2**24 - 2**16) / catch_value)))
        for i in range(3):
            rand = randint(0, round(max_catch*(2 - (self.wild_bokumon.catch_rate/1000)*3)))
            self.ball_shake_times += 1
            if rand > catch:
                break                
        if self.ball_shake_times == 3:
            self.catch_bokumon = True
        
    def critical_hit(self, damage, attack_bokumon):
        chance = randint(1, 100) 
        if chance <= attack_bokumon.critical_chance and attack_bokumon.critical_chance > 0:
            if attack_bokumon.wild:
                self.critical[0] = True
            else:
                self.critical[1] = True
            return damage * 2
        else:
            if attack_bokumon.wild:
                self.critical[0] = False
            else:
                self.critical[1] = False
            return damage

    def player_attack_turn(self, select_move):
        self.wild_damage = self.attack_bokumon(self.player_bokumon, self.wild_bokumon, select_move)
    
    def wild_attack_turn(self):
        self.player_damage = self.attack_bokumon(self.wild_bokumon, self.player_bokumon)

    def attack_bokumon(self, attack_bokumon, defend_bokumon, select_move=''):
        if select_move == '':
            select_move = attack_bokumon.moves[0]
            self.wild_selected_move = select_move
            for move in attack_bokumon.moves:
                # dano >, pp > 0 ou accurancy >, pp > 0
                if move[1] > select_move[1] and move[3][0] > 0 :
                    select_move = move
                    self.wild_selected_move = select_move
                elif move[2] > select_move[2] and move[3][0] > 0:
                    select_move = move
                    self.wild_selected_move = select_move
                    
        atk = attack_bokumon.attack
        defense = defend_bokumon.defense
        damage = (self.critical_hit(2*attack_bokumon.level, attack_bokumon)/5 + 2) * select_move[1] * atk/defense
        damage = int(((damage)/50 + 2) * (randint(217, 255)/255))
        # chance de erro do atk
        chance = randint(0, 100)
        select_move[3][0] -= 1
        if chance > select_move[2]:
            damage = 0
            if attack_bokumon.wild:
                self.miss_attack[0] = True
                self.critical[0] = False
            else:
                self.miss_attack[1] = True
                self.critical[1] = False
        else:
            if attack_bokumon.wild:
                self.miss_attack[0] = False
            else:
                self.miss_attack[1] = False
        return damage

    def is_end_battle(self):
        if int(self.wild_bokumon.atual_life) - int(self.wild_damage) < 1:
            self.wild_bokumon.atual_life = 0
            self.end_battle = True
            self.winner = 'player'
            self.exp_points = self.get_exp_points()
            self.player_damage = 0
            return True
        elif int(self.player_bokumon.atual_life) - int(self.player_damage) < 1:
            self.player_bokumon.atual_life = 0
            self.end_battle = True
            self.winner = 'wild'
            self.wild_damage = 0
            return True
        return False
    
    def get_exp_points(self):
        exp = self.wild_bokumon.level * randint(1, 3) + self.rounds * randint(1, 3) + randint(0, 10)
        return exp
         
    def attack_round(self, select_move):
        self.choose_first()
        self.reset_attack()
        # primeiro a atacar
        if not self.is_end_battle():
            if self.first_turn == 'wild':
                self.wild_attack_turn()
                if not self.is_end_battle():
                    self.player_attack_turn(select_move)
            else:
                self.player_attack_turn(select_move)
                if not self.is_end_battle():
                    self.wild_attack_turn()
            self.rounds += 1
                
    def only_wild_attack_round(self):
        self.reset_attack()
        # primeiro a atacar
        if not self.is_end_battle():
            self.wild_attack_turn()
            self.is_end_battle()
            self.rounds += 1
                
    def run_chance(self):
        chance = randint(0, 100)
        if chance >= self.wild_bokumon.prevent_run:
            return True
        return False            
    
    def reset_attack(self):
        self.wild_damage = 0
        self.player_damage = 0
        self.critical = [False, False]
        self.miss_attack = [False, False]
        self.player_bokumon.atual_life = int(self.player_bokumon.atual_life)
        self.wild_bokumon.atual_life = int(self.wild_bokumon.atual_life)
