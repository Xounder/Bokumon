import pygame
from settings.settings import *
from utils import save_system, render_utils
from utils.timer import Timer
from game_types import PlayerData


class MenuPlayer:
    def __init__(self, screen, player, view_bokumon, bag):
        self.display_surface = screen
        self.player = player
        self.view_bokumon = view_bokumon
        self.bag = bag
        self.choose = ""
        self.selected = 0
        self.close = False
        self.timer = Timer(0.12)
        self.saved = False

        self.font_20 = render_utils.load_font("Pixeltype", 20)
        self.font_25 = render_utils.load_font("Pixeltype", 25)
        self.font_35 = render_utils.load_font("Pixeltype", 35)
        self.font_42 = render_utils.load_font("Pixeltype", 42)
        self.font_50 = render_utils.load_font("Pixeltype", 50)

    def draw_overlay(self):
        pos = [screen_width - 200, 50]
        pygame.draw.rect(
            self.display_surface, "gray", (pos[0], pos[1], 190, screen_height - 200)
        )
        pygame.draw.rect(
            self.display_surface, "black", (pos[0], pos[1], 190, screen_height - 200), 4
        )

        pygame.draw.rect(
            self.display_surface,
            "gray",
            (50, screen_height - 130, screen_width - 220, 120),
        )
        pygame.draw.rect(
            self.display_surface,
            "black",
            (50, screen_height - 130, screen_width - 220, 120),
            4,
        )
        menu_list = ["Bokumon", "Bag", "Save", "Exit"]
        space_y = 40
        for i, name in enumerate(menu_list):
            render_utils.blit_shadow_text(
                name,
                "black",
                (pos[0] + 30, pos[1] + space_y),
                self.font_42,
                back_color="white",
            )
            if self.selected == i:
                # botão de seleção
                space_y_desc = 0
                if not self.saved:
                    for desc in menu_description[name]:
                        render_utils.blit_shadow_text(
                            desc,
                            "black",
                            (70, screen_height - 110 + space_y_desc),
                            self.font_42,
                            back_color="white",
                        )
                        space_y_desc += 35
                else:
                    if self.selected == 2:
                        render_utils.blit_shadow_text(
                            "Game Saved!",
                            "black",
                            (70, screen_height - 110 + space_y_desc),
                            self.font_42,
                            back_color="white",
                        )
                    else:
                        self.saved = False
                pygame.draw.rect(
                    self.display_surface,
                    "black",
                    (pos[0] + 10, pos[1] + space_y + 5, 10, 10),
                    4,
                )
            space_y += 60

    def draw(self):
        if self.choose == "":
            self.draw_overlay()
        elif self.choose == "BOKU":
            self.view_bokumon.draw()
        elif self.choose == "BAG":
            self.bag.draw()

    def update(self):
        if self.choose == "":
            if self.timer.run:
                self.timer.update()
            self.input()
        elif self.choose == "BOKU":
            if self.view_bokumon.active:
                self.view_bokumon.update()
            else:
                self.choose = ""
                self.timer.active()
        elif self.choose == "BAG":
            if self.bag.active:
                self.bag.update()
            else:
                self.choose = ""
                self.timer.active()

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.timer.run:
            if keys[pygame.K_UP]:
                self.selected -= 1 if self.selected > 0 else 0
            elif keys[pygame.K_DOWN]:
                self.selected += 1 if self.selected < 3 else 0

            if keys[pygame.K_x]:
                if self.choose == "":
                    self.close = True

            if keys[pygame.K_z]:
                if self.selected == 0:
                    self.view_bokumon.active = True
                    self.view_bokumon.seted = False
                    self.view_bokumon.timer.active()
                    self.choose = "BOKU"
                elif self.selected == 1:
                    self.bag.active = True
                    self.bag.seted = False
                    self.bag.in_battle = False
                    self.bag.timer.active()
                    self.choose = "BAG"
                    pass
                elif self.selected == 2:
                    self.save_game()
                    self.saved = True
                else:
                    self.close = True
            self.timer.active()

    def save_game(self) -> None:
        # TODO: Mudar esse método para outro local (analisar melhor local)
        player_bokumons = [bokumon.to_dict() for bokumon in self.player.bokumons]
        storage_bokumons = [
            bokumon.to_dict() for bokumon in self.player.bokumon_storage
        ]

        data: PlayerData = {
            "name": self.player.name,
            "status": self.player.previous_status,
            "position": self.player.position,
            "tickets": self.player.tickets,
            "bokumons": player_bokumons,
            "bokumonStorage": storage_bokumons,
            "bag": self.bag.all_items,
        }

        save_system.save_data(data)
