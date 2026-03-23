from settings.settings import *
from maps.map import map_1
from ui import Renderer
from sprites import Player
from .bag import Bag
from .boku_storage import BokuStorage
from .boku_store import BokuStore
from .battle_map import BattleMap
from .view_bokumon import ViewBokumon
from .bokumon_evo import BokuEvo
from .menu_player import MenuPlayer
from .menu_game import Menu


class Level:
    def __init__(self, renderer: Renderer):
        self.renderer = renderer
        self.map = map_1
        self.camera = [0, 0]
        self.map_tile_images = {
            "G": self.renderer.load_asset_image(
                "ground/grass/0",
                is_convert=True,
                is_scale=True,
                scale=(TILE_SIZE, TILE_SIZE),
            ),
            "T": self.renderer.load_asset_image(
                "ground/sand/0",
                is_convert=True,
                is_scale=True,
                scale=(TILE_SIZE, TILE_SIZE),
            ),
            "H": self.renderer.load_asset_image(
                "boku_center/heal_point",
                is_convert=True,
                is_scale=True,
                scale=(TILE_SIZE, TILE_SIZE),
            ),
            "P": self.renderer.load_asset_image(
                "boku_center/pc",
                is_convert=True,
                is_scale=True,
                scale=(TILE_SIZE, TILE_SIZE),
            ),
            "S": self.renderer.load_asset_image(
                "trader", is_convert=True, is_scale=True, scale=(TILE_SIZE, TILE_SIZE)
            ),
        }
        self.player = Player(self.renderer, self.camera)
        self.view_bokumon = ViewBokumon(self.renderer, self.player)
        self.bag = Bag(self.renderer, self.view_bokumon)
        self.battle_map = BattleMap(
            self.renderer, self.player, self.view_bokumon, self.bag
        )
        self.menu_player = MenuPlayer(
            self.renderer, self.player, self.view_bokumon, self.bag
        )
        # evolução
        self.boku_evo = BokuEvo(self.renderer, self.player)
        # boku_storage
        self.boku_storage = BokuStorage(
            self.renderer, self.player, self.view_bokumon.bokumon_summary
        )
        # boku_store
        self.boku_store = BokuStore(self.renderer, self.player, self.bag)
        # retirar
        self.menu_game = Menu(self.renderer, self.player, self.bag)
        self.change_map = False

    def draw_map(self):
        self.determine_camera()
        for line, line_map in enumerate(self.map):
            for col, tile in enumerate(line_map):
                x_map = col * TILE_SIZE - self.camera[0]
                y_map = line * TILE_SIZE - self.camera[1]
                self.renderer.blit(self.map_tile_images[tile], (x_map, y_map))

    def update(self):
        if self.menu_game.intro:
            self.menu_game.update()
        else:
            if self.boku_evo.active:
                self.boku_evo.update()
            else:
                if self.player.battle:
                    self.change_map = True
                else:
                    self.change_map = False

                if not self.change_map:
                    if self.boku_storage.active:
                        self.boku_storage.update()
                        if self.boku_storage.close:
                            self.boku_storage.close = False
                            self.boku_storage.active = False
                            self.player.timer.active()

                    elif self.boku_store.active:
                        self.boku_store.update()
                        if self.boku_store.close:
                            self.boku_store.close = False
                            self.boku_store.active = False
                            self.player.timer.active()

                    elif self.player.status != "menu":
                        self.player.update()
                    else:
                        if not self.menu_player.close:
                            self.menu_player.update()
                        else:
                            self.menu_player.close = False
                            self.player.status = self.player.previous_status

                elif self.change_map:
                    self.battle_map.set_battle(self.renderer, self.player)
                    self.battle_map.update()

                if self.player.atual_bokumon.evolved[0][0]:
                    if not self.player.atual_bokumon.evolved[0][1]:
                        self.boku_evo.activate()
                elif self.player.atual_bokumon.evolved[1][0]:
                    if not self.player.atual_bokumon.evolved[1][1]:
                        self.boku_evo.activate()

    def draw(self):
        if self.menu_game.intro:
            self.menu_game.draw()
        elif self.boku_evo.active:
            self.boku_evo.draw()
        else:
            if not self.change_map:
                self.draw_map()
                self.player.draw()
                if self.player.status == "menu":
                    self.menu_player.draw()
                if self.player.use_pc:
                    self.boku_storage.active = True
                    self.boku_storage.timer.active()
                    self.player.use_pc = False
                if self.player.use_store:
                    self.boku_store.active = True
                    self.boku_store.timer.active()
                    self.player.use_store = False
                if self.boku_storage.active:
                    self.boku_storage.draw()
                if self.boku_store.active:
                    self.boku_store.draw()
            else:
                self.battle_map.draw()

    def determine_camera(self):
        # movimenta a tela para seguir o player
        max_y = len(self.map) - round(screen_height / TILE_SIZE)
        y_pos = self.player.position[1] - round(screen_height / TILE_SIZE / 2)
        max_x = len(self.map[0]) - round(screen_width / TILE_SIZE)
        x_pos = self.player.position[0] - round(screen_width / TILE_SIZE / 2)

        if 0 <= y_pos <= max_y:
            self.camera[1] = y_pos * TILE_SIZE
        elif y_pos < 0:
            self.camera[1] = 0
        else:
            self.camera[1] = max_y * TILE_SIZE

        if 0 <= x_pos <= max_x:
            self.camera[0] = x_pos * TILE_SIZE
        elif x_pos < 0:
            self.camera[0] = 0
        else:
            self.camera[0] = max_x * TILE_SIZE
