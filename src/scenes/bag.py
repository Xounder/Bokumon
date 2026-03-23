import pygame
from settings.settings import *
from ui import Renderer, FontSize
from utils.timer import Timer


class Bag:
    def __init__(self, renderer: Renderer, view_bokumon):
        self.renderer = renderer
        self.view_bokumon = view_bokumon
        self.timer = Timer(0.12)

        self.section = "Items"
        self.seted = False
        self.active = False
        self.in_battle = False
        self.active_timer_once = False
        self.set_bag()

        # bag
        self.bag_used = [False]
        self.used_item = False

        # toss item
        self.toss = False
        self.toss_values = [1, True]
        self.pressed_z = [False, False]

        self.all_items = {
            "Items": [["Potion", 20, 5]],
            "Key Items": [],
            "Boku Balls": [["Boku Ball", 1, 5]],
        }
        self.items_description = {
            "Boku Ball": [
                "A  ball  thrown  to  catch  a  wild",
                "Bokumon.  Its  is  designed  in  a",
                "capsule  style.",
            ],
            "Great Ball": [
                "A  good,  quality  Ball  that  offers",
                "a  higher  Bokumon  catch  rate  than",
                "a  standard  Boku Ball.",
            ],
            "Ultra Ball": [
                "A  very  high-grade  Ball  that  offers",
                "a  higher  Bokumon  catch  rate  than",
                "a  Great Ball.",
            ],
            "Potion": [
                "A spray-type wound medicine.",
                "Its restores the HP of one Bokumon",
                "by 20 points.",
            ],
            "Super Potion": [
                "A spray-type wound medicine.",
                "Its restores the HP of one Bokumon",
                "by 50 points.",
            ],
            "Hyper Potion": [
                "A spray-type wound medicine.",
                "Its restores the HP of one Bokumon",
                "by 200 points.",
            ],
        }
        # [fora de batalha, em batalha]
        self.items_selections = {
            "Boku Ball": [["Toss", "Cancel"], ["Use", "Cancel"]],
            "Great Ball": [["Toss", "Cancel"], ["Use", "Cancel"]],
            "Ultra Ball": [["Toss", "Cancel"], ["Use", "Cancel"]],
            "Potion": [["Use", "Toss", "Cancel"], ["Use", "Cancel"]],
            "Super Potion": [["Use", "Toss", "Cancel"], ["Use", "Cancel"]],
            "Hyper Potion": [["Use", "Toss", "Cancel"], ["Use", "Cancel"]],
        }
        self.items_image = {
            "Boku Ball": self.renderer.load_asset_image("boku_ball", is_scale=True),
            "Great Ball": self.renderer.load_asset_image("great_ball", is_scale=True),
            "Ultra Ball": self.renderer.load_asset_image("ultra_ball", is_scale=True),
            "Potion": self.renderer.load_asset_image("potion", is_scale=True),
            "Super Potion": self.renderer.load_asset_image(
                "super_potion", is_scale=True
            ),
            "Hyper Potion": self.renderer.load_asset_image(
                "hyper_potion", is_scale=True
            ),
        }

    def set_bag(self):
        if not self.seted:
            self.timer.active()
            self.marked = {"Items": [0, 0], "Key Items": [0, 0], "Boku Balls": [0, 0]}
            self.selected_item = []
            self.limit_visu_items = {
                "Items": [0, 6],
                "Key Items": [0, 6],
                "Boku Balls": [0, 6],
            }

            self.selected = False
            self.bag_used = [False]
            self.used_item = False

    def load_states(self, data: dict) -> None:
        for section, item in data.items():
            self.all_items[section] = item

    def buy_item(self, item, qnt, section):
        for i, item_bag in enumerate(self.all_items[section]):
            if item_bag[0] == item[0]:
                self.all_items[section][i][2] += qnt
                return
        self.all_items[section].append([item[0], item[1], qnt])

    def draw(self):
        if not self.view_bokumon.active:
            self.draw_overlay()
        else:
            self.view_bokumon.draw()

    def draw_overlay(self):
        self.renderer.draw_rect('#655FFF', (0, 0, screen_width, screen_height))
        # Items
        self.renderer.draw_rect(
            "orange",
            (250, 20, screen_width - 270, screen_height - 200),
            0,
            5,
        )
        self.renderer.draw_rect(
            "black",
            (250, 17, screen_width - 270, screen_height - 197),
            3,
            5,
        )
        self.renderer.draw_rect(
            "#ECD580",
            (300, 40, screen_width - 350, screen_height - 250),
            0,
            5,
        )
        self.renderer.draw_rect(
            "black",
            (300, 40, screen_width - 350, screen_height - 250),
            3,
            5,
        )
        # Nome seção
        self.renderer.draw_rect("black", (18, 17, 240, 106), 3, 5)
        self.renderer.draw_rect("orange", (20, 20, 250, 100), 0, 3)
        self.renderer.blit_shadow_text(
            f"{self.section}",
            "white",
            (140, 80),
            size=FontSize.DOUBLE_EXTRA_LARGE,
            center=True,
        )
        # parte de baixo
        self.renderer.draw_rect(
            "blue",
            (0, screen_height - 150, screen_width, 150),
            0,
            3,
        )
        self.renderer.draw_rect(
            "black",
            (0, screen_height - 150, screen_width, 150),
            3,
            5,
        )
        # image rect
        self.renderer.draw_rect("white", (20, screen_height - 120, 90, 90), 0, 5)
        self.renderer.draw_rect("black", (20, screen_height - 120, 90, 90), 3, 5)
        if self.selected:
            # aviso de seleção (caixa de texto)
            self.renderer.draw_rect(
                "white",
                (140, screen_height - 140, 420, 130),
                0,
                5,
            )
            self.renderer.draw_rect(
                "black",
                (140, screen_height - 140, 420, 130),
                3,
                5,
            )
        space_y = 0
        for i, item in enumerate(self.all_items[self.section]):
            if (
                self.limit_visu_items[self.section][0]
                <= i
                <= self.limit_visu_items[self.section][1]
            ):
                self.renderer.blit_shadow_text(
                    f"{item[0]}",
                    "black",
                    (330, 60 + space_y),
                    size=FontSize.DOUBLE_EXTRA_LARGE,
                    back_color="gray",
                )
                self.renderer.blit_shadow_text(
                    f"X   {item[2]}",
                    "black",
                    (650, 60 + space_y),
                    size=FontSize.DOUBLE_EXTRA_LARGE,
                    back_color="gray",
                )
                if self.marked[self.section][0] == i:
                    # botão de seleção
                    color = "black" if not self.selected else "red"
                    self.renderer.draw_rect(color, (315, 65 + space_y, 10, 10), 0, 20)
                    space_y_desc = 0
                    if not self.selected:
                        item_rect = self.items_image[item[0]].get_rect(
                            center=(65, screen_height - 75)
                        )
                        self.renderer.blit(self.items_image[item[0]], item_rect)
                        # descrição
                        for desc in self.items_description[item[0]]:
                            self.renderer.blit_shadow_text(
                                desc,
                                "white",
                                (140, screen_height - 120 + space_y_desc),
                                size=FontSize.DOUBLE_EXTRA_LARGE,
                            )
                            space_y_desc += 40
                    else:
                        item_rect = self.items_image[item[0]].get_rect(
                            center=(65, screen_height - 75)
                        )
                        self.renderer.blit(self.items_image[item[0]], item_rect)
                        if not self.toss:
                            # aviso de seleção
                            self.renderer.blit_text(
                                f"{item[0]}  is",
                                "black",
                                (140 + 20, screen_height - 110),
                                size=FontSize.DOUBLE_EXTRA_LARGE,
                            )
                            self.renderer.blit_text(
                                "selected.",
                                "black",
                                (140 + 20, screen_height - 65),
                                size=FontSize.DOUBLE_EXTRA_LARGE,
                            )
                        # pega o item respectivo e ve se está em batalha ou não
                        self.selected_item = (
                            self.items_selections[item[0]][self.in_battle]
                            if self.selected
                            else self.items_selections[item[0]][self.in_battle]
                        )
                        qnt_sel = len(self.selected_item) - 2 if not self.toss else 0
                        tam = [(screen_height - 150) - qnt_sel * 40, 150 + qnt_sel * 40]
                        # caixa de seleção do item
                        self.renderer.draw_rect(
                            "#00008B",
                            (screen_width - 230, tam[0], 220, tam[1]),
                            0,
                            3,
                        )
                        self.renderer.draw_rect(
                            "black",
                            (screen_width - 230, tam[0], 220, tam[1]),
                            3,
                            5,
                        )
                        self.renderer.draw_rect(
                            "white",
                            (screen_width - 220, tam[0] + 10, 200, tam[1] - 20),
                            0,
                            5,
                        )
                        # possiveis seleções
                        if self.toss:
                            self.toss_item()
                        else:
                            space_y_sel = 40
                            for j, sel in enumerate(self.selected_item):
                                self.renderer.blit_text(
                                    f"{sel}",
                                    "black",
                                    (screen_width - 190, tam[0] + space_y_sel),
                                    size=FontSize.DOUBLE_EXTRA_LARGE,
                                )
                                if self.marked[self.section][1] == j:
                                    # botão de seleção
                                    self.renderer.draw_rect(
                                        "black",
                                        (
                                            screen_width - 210,
                                            tam[0] + space_y_sel + 5,
                                            10,
                                            10,
                                        ),
                                        0,
                                        20,
                                    )
                                space_y_sel += 45
                space_y += 50
            elif i > self.limit_visu_items[self.section][1]:
                break

    def update(self):
        if not self.view_bokumon.active:
            if self.bag_used[0]:
                self.active = False
            if self.active_timer_once:
                self.timer.active()
                self.active_timer_once = False
            if self.timer.run:
                self.timer.update()
            self.input()
        else:
            self.active_timer_once = True
            self.view_bokumon.update()

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.timer.run:
            self.marked[self.section][0] = (
                self.marked[self.section][0]
                if self.marked[self.section][0] < len(self.all_items[self.section]) - 1
                else len(self.all_items[self.section]) - 1
            )

            if keys[pygame.K_UP]:
                if self.toss:
                    if not self.pressed_z[0]:
                        self.toss_values[0] += (
                            1
                            if self.toss_values[0]
                            < self.all_items[self.section][
                                self.marked[self.section][0]
                            ][2]
                            else 0
                        )
                    else:
                        self.toss_values[1] = True
                else:
                    if not self.selected:
                        self.marked[self.section][0] -= (
                            1 if self.marked[self.section][0] > 0 else 0
                        )
                    else:
                        self.marked[self.section][1] -= (
                            1 if self.marked[self.section][1] > 0 else 0
                        )

                    if (
                        self.marked[self.section][0] - 1
                        == self.limit_visu_items[self.section][0]
                    ):
                        if self.limit_visu_items[self.section][0] > 0:
                            self.limit_visu_items[self.section][0] -= 1
                            self.limit_visu_items[self.section][1] -= 1

            elif keys[pygame.K_DOWN]:
                if self.toss:
                    if not self.pressed_z[0]:
                        self.toss_values[0] -= 1 if self.toss_values[0] > 1 else 0
                    else:
                        self.toss_values[1] = False
                else:
                    if not self.selected:
                        self.marked[self.section][0] += (
                            1
                            if self.marked[self.section][0]
                            < len(self.all_items[self.section]) - 1
                            else 0
                        )
                    else:
                        self.marked[self.section][1] += (
                            1
                            if self.marked[self.section][1]
                            < len(self.selected_item) - 1
                            else 0
                        )

                    if (
                        self.marked[self.section][0]
                        > self.limit_visu_items[self.section][1] - 1
                    ):
                        if (
                            self.limit_visu_items[self.section][1]
                            < len(self.all_items[self.section]) - 1
                        ):
                            self.limit_visu_items[self.section][1] += 1
                            self.limit_visu_items[self.section][0] += 1

            elif keys[pygame.K_LEFT]:
                if not self.selected:
                    if self.section == "Boku Balls":
                        self.section = "Key Items"
                    elif self.section == "Key Items":
                        self.section = "Items"
            elif keys[pygame.K_RIGHT]:
                if not self.selected:
                    if self.section == "Items":
                        self.section = "Key Items"
                    elif self.section == "Key Items":
                        self.section = "Boku Balls"

            if keys[pygame.K_x]:
                if self.selected:
                    self.selected = False
                    self.marked[self.section][1] = 0
                else:
                    self.active = False
                self.reset_toss()

            elif keys[pygame.K_z]:
                if self.toss:
                    if not self.pressed_z[0]:
                        self.pressed_z[0] = True
                    else:
                        self.pressed_z[1] = True
                else:
                    if not self.selected:
                        if len(self.all_items[self.section]) > 0:
                            self.selected = True
                    else:
                        self.what_to_do(
                            self.selected_item[self.marked[self.section][1]]
                        )
            self.timer.active()

    def what_to_do(self, name):
        if name == "Cancel":
            self.selected = False
        elif name == "Use":
            self.use_item()
            self.selected = False
        elif name == "Toss":
            self.toss = True

    def use_item(self):
        item = self.all_items[self.section][self.marked[self.section][0]]
        if item[0].count("Potion") == 1:
            self.view_bokumon.active = True
            self.view_bokumon.seted = False
            self.view_bokumon.timer.active()
            self.view_bokumon.bag_values = [
                item,
                True,
                [self.all_items[self.section], self.marked[self.section][0]],
                self.bag_used,
            ]
            self.used_item = item

        elif item[0].count("Ball") == 1:
            item[2] -= 1
            if item[2] <= 0:
                self.all_items[self.section].pop(self.marked[self.section][0])
            self.used_item = item
            self.bag_used[0] = True
            self.active = False

    def toss_item(self):
        # aviso de seleção
        item = self.all_items[self.section][self.marked[self.section][0]]
        if item[2] > 1:
            if not self.pressed_z[0]:
                self.renderer.blit_text(
                    f"Toss out how many",
                    "black",
                    (140 + 20, screen_height - 110),
                    size=FontSize.DOUBLE_EXTRA_LARGE,
                )
                self.renderer.blit_text(
                    f"{item[0]}(s)?",
                    "black",
                    (140 + 20, screen_height - 65),
                    size=FontSize.DOUBLE_EXTRA_LARGE,
                )
                zeros_txt = "000"
                zeros_txt = zeros_txt[: 3 - len(str(self.selected_item[1][0]))]
                self.renderer.blit_text(
                    f"x{zeros_txt}{self.toss_values[0]}",
                    "black",
                    (screen_width - 150, screen_height - 80),
                    size=FontSize.EXTRA_LARGE,
                )
            else:
                if not self.pressed_z[1]:
                    self.renderer.blit_text(
                        f"Throw away {self.toss_values[0]} of",
                        "black",
                        (140 + 20, screen_height - 110),
                        size=FontSize.DOUBLE_EXTRA_LARGE,
                    )
                    self.renderer.blit_text(
                        "this item?",
                        "black",
                        (140 + 20, screen_height - 65),
                        size=FontSize.DOUBLE_EXTRA_LARGE,
                    )
                    # botão de seleção
                    self.renderer.blit_text(
                        "Yes",
                        "black",
                        (screen_width - 165, screen_height - 110),
                        size=FontSize.DOUBLE_EXTRA_LARGE,
                    )
                    self.renderer.blit_text(
                        "No",
                        "black",
                        (screen_width - 160, screen_height - 65),
                        size=FontSize.DOUBLE_EXTRA_LARGE,
                    )

                    pos = (
                        screen_height - 100
                        if self.toss_values[1]
                        else screen_height - 60
                    )
                    self.renderer.draw_rect(
                        "black",
                        (screen_width - 180, pos, 10, 10),
                        0,
                        20,
                    )
                else:
                    if self.toss_values[1]:
                        item[2] -= self.toss_values[0]
                    self.reset_toss()
        else:
            if not self.pressed_z[0]:
                self.renderer.blit_text(
                    f"Throw away 1 of",
                    "black",
                    (140 + 20, screen_height - 110),
                    size=FontSize.DOUBLE_EXTRA_LARGE,
                )
                self.renderer.blit_text(
                    "this item?",
                    "black",
                    (140 + 20, screen_height - 65),
                    size=FontSize.DOUBLE_EXTRA_LARGE,
                )
            else:
                if self.toss_values[1]:
                    item[2] -= 1
                self.reset_toss()

        if item[2] <= 0:
            self.all_items[self.section].pop(self.marked[self.section][0])

    def reset_toss(self):
        self.toss_values = [1, True]
        self.pressed_z = [False, False]
        self.toss = False
        self.selected = False
