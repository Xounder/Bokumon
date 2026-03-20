import pygame
from random import randint
from maps.map import map_1
from settings.settings import *
from utils.support import load_asset_image
from utils.timer import Timer
from game_types import PlayerData
from .bokumon import BokuMon


class Player:
    def __init__(self, screen, camera):
        self.display_surface = screen
        self.import_assets()
        self.name = "gold"
        self.frame_index = 0
        self.status = "down"
        self.previous_status = "down"
        self.position = [round(len(map_1) / 2), round(len(map_1[0]) / 2)]
        self.previous_position = self.position

        self.camera = camera
        self.battle = False
        self.bokumons_restored = False
        self.use_pc = False
        self.use_store = False
        self.tickets = 0
        # image
        self.image = self.frames[self.status][self.frame_index]
        self.rect = self.image.get_rect(
            topleft=(
                (self.position[0] * TILE_SIZE) - self.camera[0],
                (self.position[1] * TILE_SIZE) - self.camera[1],
            )
        )
        # player bokumon
        self.bokumons: list[BokuMon] = [BokuMon("Pan", self.display_surface)]
        self.atual_bokumon: BokuMon = self.bokumons[0]
        self.bokumons_battle = [0, 1, 2, 3, 4, 5]
        self.bokumon_part_battle = []
        self.reseted_pos = False
        # bokumon storage
        self.bokumon_storage: list[BokuMon] = []
        # timer inputs
        self.timer = Timer(0.12)

    def import_assets(self):
        self.frames = {"up": [], "down": [], "left": [], "right": []}
        for direction in self.frames:
            path = f"player/{direction}"
            for i in range(3):
                image = load_asset_image(
                    f"{path}/{i}",
                    is_convert_alpha=True,
                    is_scale=True,
                    scale=(TILE_SIZE, TILE_SIZE),
                )
                self.frames[direction].append(image)

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.timer.run:
            if keys[pygame.K_UP]:
                if self.status != "up":
                    self.status = "up"
                else:
                    self.move_player([0, -1])
            elif keys[pygame.K_DOWN]:
                if self.status != "down":
                    self.status = "down"
                else:
                    self.move_player([0, 1])
            elif keys[pygame.K_LEFT]:
                if self.status != "left":
                    self.status = "left"
                else:
                    self.move_player([-1, 0])
            elif keys[pygame.K_RIGHT]:
                if self.status != "right":
                    self.status = "right"
                else:
                    self.move_player([1, 0])
            elif keys[pygame.K_s]:
                self.previous_status = self.status
                self.status = "menu"
            else:
                self.frame_index = 0
                self.move_player([0, 0])

            if keys[pygame.K_z]:
                if (
                    map_1[self.position[1] - 1][self.position[0]] == "H"
                    and self.status == "up"
                ):
                    self.bokumon_restore()
                    self.status = "down"
                elif (
                    map_1[self.position[1] - 1][self.position[0]] == "P"
                    and self.status == "up"
                ):
                    self.use_pc = True
                elif (
                    map_1[self.position[1] - 1][self.position[0]] == "S"
                    and self.status == "up"
                ):
                    self.use_store = True
            self.timer.active()

    def move_player(self, move):
        expect_pos = [self.position[0] + move[0], self.position[1] + move[1]]
        self.previous_position = self.position

        if expect_pos[0] < 0 or expect_pos[0] > len(map_1[0]) - 1:
            return
        if expect_pos[1] < 0 or expect_pos[1] > len(map_1) - 1:
            return
        if map_1[expect_pos[1]][expect_pos[0]] == "H":
            return
        if map_1[expect_pos[1]][expect_pos[0]] == "P":
            return
        if map_1[expect_pos[1]][expect_pos[0]] == "S":
            return

        self.position = expect_pos
        self.rect.topleft = (
            ((self.position[0] * TILE_SIZE) - self.camera[0]),
            (self.position[1] * TILE_SIZE) - self.camera[1],
        )
        if (
            map_1[expect_pos[1]][expect_pos[0]] == "G"
            and self.previous_position != self.position
            and self.bokumon_alive()
        ):
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
                # talvez fazer um bokumon_alive sem essa parte e outro com (nsei)
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
        for i in range(len(self.bokumon_part_battle) - 1, -1, -1):
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

    def load_states(self, data: PlayerData) -> None:
        self.name = data["name"]
        self.previous_status = data["status"]
        self.position = data["position"]
        self.tickets = data["tickets"]

        for bokumon_data in data["bokumons"]:
            self.bokumons.append(BokuMon.from_dict(bokumon_data))

        for bokumon_data in data["bokumons"]:
            self.bokumon_storage.append(BokuMon.from_dict(bokumon_data))
