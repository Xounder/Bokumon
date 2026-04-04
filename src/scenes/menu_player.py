import pygame
from settings.settings import *
from ui import Renderer, FontSize, TextBoxComponent, SelectionBoxComponent
from utils import save_system
from utils.timer import Timer
from game_types import PlayerData


class MenuPlayer:
    def __init__(self, renderer: Renderer, player, view_bokumon, bag):
        self.renderer = renderer
        self.text_box_component = TextBoxComponent(self.renderer)
        self.selection_box_component = SelectionBoxComponent(self.renderer)

        self.player = player
        self.view_bokumon = view_bokumon
        self.bag = bag
        self.choose = ""
        self.selected = 0
        self.previous_selected = 0
        self.close = False
        self.timer = Timer(0.12)
        self.show_saved_feedback = False

    def draw_overlay(self):
        pos = [screen_width - 200, 50]
        menu_list = ["Bokumon", "Bag", "Save", "Exit"]

        self.selection_box_component.draw_selection_box(
            text_list=menu_list,
            rect_color="gray",
            text_size=FontSize.EXTRA_LARGE,
            rect_position=(pos[0], pos[1]),
            rect_size=(190, screen_height - 200),
            selected_index=self.selected,
            text_gap=40,
            text_spacing=60,
            is_shadowed_text=True,
            shadow_color="white",
        )

        text_list = (
            menu_description[menu_list[self.selected]]
            if not self.show_saved_feedback
            else ["Game Saved!"]
        )

        self.text_box_component.draw_text_box(
            text_list=text_list,
            rect_color="gray",
            text_size=FontSize.EXTRA_LARGE,
            rect_position=(50, screen_height - 130),
            rect_size=(screen_width - 220, 120),
            is_shadowed_text=True,
            shadow_color="white",
        )


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

            if self.selected != self.previous_selected:
                self.show_saved_feedback = False

            self.previous_selected = self.selected

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
                    self.show_saved_feedback = True
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
