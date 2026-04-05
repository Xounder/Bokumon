import pygame
from settings.settings import screen_height, screen_width
from ui import Renderer, FontSize, TextBoxComponent, SelectionBoxComponent
from utils import save_system
from utils.timer import Timer
from sprites import BokuMon


class Menu:
    def __init__(self, renderer: Renderer, player, bag):
        self.renderer = renderer
        self.text_box_component = TextBoxComponent(self.renderer)
        self.selection_box_component = SelectionBoxComponent(self.renderer)

        self.player = player
        self.bag = bag
        self.timer = Timer(0.12)

        self.selected = [0, False]
        self.selected_button = 1
        self.boku_selected = [1, False]
        self.confirm_button = 0
        self.intro = True
        self.msg = False
        self.select_new_game = False

        self.firts_bokumons = [
            BokuMon("Pan", self.renderer),
            BokuMon("Parrot", self.renderer),
            BokuMon("Monk", self.renderer),
        ]

    def draw(self):
        if self.select_new_game:
            self.select_first_bokumon()
            if self.boku_selected[1]:
                self.blit_select_continue(
                    (screen_width - 150, screen_height - 250), self.confirm_button
                )
        else:
            self.draw_overlay()
            if self.selected[1]:
                self.blit_select_continue(
                    (screen_width - 260, 180), self.selected_button
                )
            elif self.msg:
                self.text_box_component.draw_text_box(
                    text_list=["Don't  have  any  saved  game."],
                    rect_color="#00008B",
                    text_size=FontSize.DOUBLE_EXTRA_LARGE,
                    rect_position=(20, screen_height - 120),
                    rect_size=(screen_width - 50, 100),
                    border_radius=5,
                    has_inner_rect=True,
                    inner_rect_radius=5,
                    is_middle=True,
                )

    def draw_overlay(self):
        self.renderer.draw_rect("#00009F", (0, 0, screen_width, screen_height))
        pos = [[240, 145], [280, 345]]

        self.text_box_component.draw_text_box(
            text_list=["Continue   Game"],
            rect_color="#00008B",
            text_size=FontSize.DOUBLE_EXTRA_LARGE,
            rect_position=(110, 100),
            rect_size=(screen_width - 250, 100),
            border_radius=5,
            has_inner_rect=True,
            inner_rect_radius=5,
            is_center=True,
        )

        self.text_box_component.draw_text_box(
            text_list=["New   Game"],
            rect_color="#00008B",
            text_size=FontSize.DOUBLE_EXTRA_LARGE,
            rect_position=(110, 300),
            rect_size=(screen_width - 250, 100),
            border_radius=5,
            has_inner_rect=True,
            inner_rect_radius=5,
            is_center=True,
        )

        color = "red" if self.selected[1] else "black"
        self.renderer.draw_rect(
            color,
            (pos[self.selected[0]][0], pos[self.selected[0]][1], 10, 10),
            0,
            20,
        )

    def blit_select_continue(self, pos_rect, selected_button):
        self.selection_box_component.draw_selection_box(
            text_list=["Yes", "No"],
            rect_color="#00008B",
            text_size=FontSize.DOUBLE_EXTRA_LARGE,
            rect_position=(pos_rect[0], pos_rect[1]),
            rect_size=(120, screen_height / 4.5),
            selected_index=selected_button,
            selected_rect_radius=20,
            rect_radius=5,
            border_radius=5,
            has_inner_rect=True,
            inner_rect_radius=5,
            text_gap=30,
            text_spacing=50,
        )

    def select_first_bokumon(self):
        self.renderer.draw_rect("#00899F", (0, 0, screen_width, screen_height))
        self.renderer.draw_rect(
            "#19A99F",
            (60, screen_height / 2 - 100, screen_width - 100, 160),
        )

        self.text_box_component.draw_text_box(
            text_list=["Select  your  first  Bokumon!"],
            rect_color="#00008B",
            text_size=FontSize.DOUBLE_EXTRA_LARGE,
            rect_position=(20, screen_height - 120),
            rect_size=(screen_width - 50, 100),
            border_radius=5,
            has_inner_rect=True,
            inner_rect_radius=5,
            is_center=True,
        )

        space_x = 0
        for i, boku in enumerate(self.firts_bokumons):
            boku.draw_modified([130 + space_x, screen_height / 2 - 40], 0.7)
            self.renderer.draw_text(
                f"{boku.name}",
                "black",
                (160 + space_x, screen_height - 200),
                size=FontSize.DOUBLE_EXTRA_LARGE,
                is_center=True,
            )
            if self.boku_selected[0] == i:
                self.renderer.draw_rect(
                    "red",
                    (75 + space_x, screen_height / 2 - 95, 150, 150),
                    3,
                    20,
                )
            space_x += 250

    def update(self):
        if self.timer.run:
            self.timer.update()
        self.input()

    def input(self):
        if not self.timer.run:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                if self.select_new_game:
                    self.confirm_button = 0
                else:
                    if not self.selected[1] and not self.msg:
                        self.selected[0] = 0
                    else:
                        self.selected_button = 0
            elif keys[pygame.K_DOWN]:
                if self.select_new_game:
                    self.confirm_button = 1
                else:
                    if not self.selected[1] and not self.msg:
                        self.selected[0] = 1
                    else:
                        self.selected_button = 1

            if keys[pygame.K_LEFT]:
                if self.select_new_game and not self.boku_selected[1]:
                    self.boku_selected[0] -= 1 if self.boku_selected[0] > 0 else 0
            elif keys[pygame.K_RIGHT]:
                if self.select_new_game and not self.boku_selected[1]:
                    self.boku_selected[0] += 1 if self.boku_selected[0] < 2 else 0

            if keys[pygame.K_z]:
                if self.select_new_game:
                    if not self.boku_selected[1]:
                        self.boku_selected[1] = True
                    else:
                        if self.confirm_button == 0:
                            self.player.first_bokumon(
                                self.firts_bokumons[self.boku_selected[0]]
                            )
                            self.intro = False
                        else:
                            self.boku_selected[1] = False
                else:
                    if not self.selected[1]:
                        self.selected[1] = True
                        if self.selected[0] == 0 and not save_system.has_saved_game():
                            self.selected[1] = False
                            self.msg = True
                    else:
                        if self.selected_button == 0:
                            if self.selected[0] == 0:
                                self.load_game()
                                self.intro = False
                            else:
                                self.select_new_game = True
                        else:
                            self.selected[1] = False

            elif keys[pygame.K_x]:
                if self.select_new_game:
                    if not self.boku_selected[1]:
                        self.select_new_game = False
                    else:
                        self.boku_selected[1] = False
                        self.confirm_button = 1
                else:
                    if self.selected[1]:
                        self.selected[1] = False
                        self.selected_button = 1
                    elif self.msg:
                        self.msg = False
            self.timer.active()

    def load_game(self) -> None:
        # TODO: verificar melhor forma de carregar os dados e modificar a forma de enviar os dados
        # TODO: Mudar esse método para outro local (analisar melhor local)

        data = save_system.load_data()
        player_data = dict(list(data.items())[:-1])
        bag_data = data["bag"]

        self.bag.load_states(bag_data)
        self.player.load_states(player_data)
