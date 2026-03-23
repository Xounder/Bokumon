import pygame
from typing import Self
from random import randint
from settings.settings import *
from settings.bokumons_settings import *
from ui import Renderer
from game_types import BokumonData


class BokuMon:
    def __init__(self, name, renderer: Renderer = None, wild=False, level=5):
        self.renderer = renderer

        img_surf = self.renderer.load_asset_image(f"bokumon/{name}", is_convert_alpha=True)
        self.image = self.renderer.scale_image(img_surf, (TILE_SIZE * 3, TILE_SIZE * 3))
        self.rect = self.image.get_rect(center=(boku_pos[0] if wild else boku_pos[1]))

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
        self.critical_chance = bokumon_stats[4]
        self.up_exp = (
            20 + self.level if self.level <= 5 else 25 * (abs(self.level - 5) + 1)
        )
        self.atual_exp = randint(0, round(self.up_exp / 2))
        self.all_exp = self.atual_exp
        self.atrib_ups = [0, 0, 0, 0, 0]
        self.ball = "Boku Ball"
        if wild:
            self.prevent_run = 5 + randint(0, level + 10)
            self.catch_rate = (
                randint(190, 255) - round(self.level, self.level * 2) - self.level
            )
            if self.catch_rate <= 0:
                self.catch_rate = randint(5, 40)

        # TODO: Remover codigo abaixo

        # attacks type (por hr so um atk normal)
        # Nome, dano, chance de acerto, PP
        a = (
            ["Crunch", 40, 90, [10, 10]]
            if self.name == "Snacks"
            else ["Punch", 40, 90, [10, 10]]
        )
        self.moves = [
            ["Scratch", 30, 100, [20, 20]],
            ["Headbutt", 50, 80, [10, 10]],
            ["Bite", 45, 85, [15, 15]],
            a,
        ]
        self.set_moves_pp()

    def apply_state(self, data: BokumonData) -> None:
        self.atual_name = data["atualName"]
        self.previous_name = data["name"]
        self.life = data["maxLife"]
        self.atual_life = data["atualLife"]
        self.attack = data["status"]["attack"]
        self.defense = data["status"]["defense"]
        self.speed = data["status"]["speed"]
        self.critical_chance = data["status"]["criticalChance"]
        self.atual_exp = data["status"]["atualExperience"]
        self.up_exp = data["status"]["upgradeExperience"]
        self.all_exp = data["status"]["totalExperience"]
        self.ball = data["bokuBall"]
        self.moves = data["moves"]

    def to_dict(self) -> BokumonData:
        return {
            "name": self.name,
            "atualName": self.atual_name,
            "level": self.level,
            "maxLife": self.life,
            "atualLife": self.atual_life,
            "bokuBall": self.ball,
            "status": {
                "attack": self.attack,
                "defense": self.defense,
                "speed": self.speed,
                "criticalChance": self.critical_chance,
                "atualExperience": self.atual_exp,
                "upgradeExperience": self.up_exp,
                "totalExperience": self.all_exp,
            },
            "moves": self.moves,  # TODO:separar em outros atributos
        }

    @classmethod
    def from_dict(cls, data: BokumonData) -> Self:
        player = cls(name=data["name"], level=data["level"])
        player.apply_state(data)
        return player

    def set_moves_pp(self):
        self.moves_pp = [
            self.moves[0][3],
            self.moves[1][3],
            self.moves[2][3],
            self.moves[3][3],
        ]

    def upgrade(self):
        # somente para os player_bokumons
        if self.atual_exp >= self.up_exp:
            self.all_exp += self.atual_exp
            self.atual_exp = 0
            self.level += 1
            self.up_exp = (
                20 + self.level if self.level <= 5 else 25 * (abs(self.level - 5) + 1)
            )
            self.atrib_ups = [
                randint(1, 3),
                randint(1, 3),
                randint(1, 3),
                randint(1, 3),
                randint(0, 1),
            ]
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
        # [[evoluir o boku, mostrar a evo],[evoluir o boku, mostrar a evo]]
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
        self.image = img_surf = self.renderer.load_asset_image(
            f"bokumon/{self.name}", is_convert_alpha=True
        )
        self.image = self.renderer.scale_image(img_surf, (TILE_SIZE * 3, TILE_SIZE * 3))
        self.evo_step = bokumons_evo_steps[self.name]  ###
        if self.evolved[0][1]:
            self.evolved[0][1] = True
        else:
            self.evolved[1][1] = True
        self.atrib_ups = [
            randint(1, 6),
            randint(1, 6),
            randint(1, 6),
            randint(1, 6),
            randint(1, 2),
        ]
        self.life += self.atrib_ups[0]
        self.atual_life = self.life
        self.attack += self.atrib_ups[1]
        self.defense += self.atrib_ups[2]
        self.speed += self.atrib_ups[3]
        self.critical_chance += self.atrib_ups[4]

    def draw(self, rect_center):
        self.rect.center = rect_center
        self.renderer.blit(self.image, self.rect)

    def draw_modified(self, rect_center, scale):
        self.rect.center = rect_center
        image_mod = self.renderer.scale_image(
            self.image,
            (self.image.get_width() / scale, self.image.get_height() / scale),
        )
        self.renderer.blit(image_mod, self.rect)

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
