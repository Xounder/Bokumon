import pygame
from settings.settings import *
from ui import Renderer, FontSize, BoxComponent, TextBoxComponent, SelectionBoxComponent
from utils.timer import Timer


class Bag:
    def __init__(self, renderer: Renderer, view_bokumon):
        self.renderer = renderer
        self.box_component = BoxComponent(self.renderer)
        self.text_box_component = TextBoxComponent(self.renderer)
        self.selection_box_component = SelectionBoxComponent(self.renderer)

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
        # TODO: verificar mover essa parte para a pasta data
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
        # TODO: modificar esse agora
        self.renderer.fill_screen("#655FFF")
        # Items
        self.box_component.draw_box(
            rect_color="orange",
            rect_position=(250, 20),
            rect_size=(screen_width - 270, screen_height - 200),
            rect_radius=5,
            border_radius=5,
        )

        # TODO: verificar possibilidade de usar text_box_component aqui
        self.box_component.draw_box(
            rect_color="#ECD580",
            rect_position=(300, 40),
            rect_size=(screen_width - 350, screen_height - 250),
            rect_radius=5,
            border_radius=5,
        )

        # Nome seção
        self.renderer.draw_rect("black", (18, 20, 240, 106), 3, 5)
        self.text_box_component.draw_text_box(
            text_list=[f"{self.section}"],
            rect_color="orange",
            text_size=FontSize.DOUBLE_EXTRA_LARGE,
            rect_position=(20, 23),
            rect_size=(250, 100),
            rect_radius=5,
            has_border=False,
            text_color="white",
            is_shadowed_text=True,
            is_center=True,
        )
        
        # parte de baixo
        self.box_component.draw_box(
            rect_color="blue",
            rect_position=(0, screen_height - 150),
            rect_size=(screen_width, 150),
            rect_radius=5,
            border_radius=5,
        )

        # image rect
        self.box_component.draw_box(
            rect_color="white",
            rect_position=(20, screen_height - 120),
            rect_size=(90, 90),
            rect_radius=5,
            border_radius=5,
        )

        space_y = 0
        for i, item in enumerate(self.all_items[self.section]):
            if (
                self.limit_visu_items[self.section][0]
                <= i
                <= self.limit_visu_items[self.section][1]
            ):
                self.renderer.draw_text(
                    f"{item[0]}",
                    "black",
                    (330, 70 + space_y),
                    size=FontSize.DOUBLE_EXTRA_LARGE,
                    is_shadowed_text=True,
                    shadow_color="gray",
                )
                self.renderer.draw_text(
                    f"X   {item[2]}",
                    "black",
                    (650, 70 + space_y),
                    size=FontSize.DOUBLE_EXTRA_LARGE,
                    is_shadowed_text=True,
                    shadow_color="gray",
                )
                if self.marked[self.section][0] == i:
                    # botão de seleção
                    color = "black" if not self.selected else "red"
                    self.renderer.draw_rect(color, (315, 65 + space_y, 10, 10), 0, 20)
                    space_y_desc = 0

                    item_rect = self.items_image[item[0]].get_rect(
                        center=(65, screen_height - 75)
                    )
                    self.renderer.blit(self.items_image[item[0]], item_rect)

                    if not self.selected:
                        # descrição
                        
                        # TODO: mover esse print do texto para dentro do rect que ele aparece (utilizar text_box_component)
                        for desc in self.items_description[item[0]]:
                            self.renderer.draw_text(
                                desc,
                                "white",
                                (140, screen_height - 120 + space_y_desc),
                                size=FontSize.DOUBLE_EXTRA_LARGE,
                                is_shadowed_text=True,
                            )
                            space_y_desc += 40
                    else:
                        if not self.toss:
                            text_list = [f"{item[0]}  is", "selected."]

                            self.text_box_component.draw_text_box(
                                text_list=text_list,
                                rect_color="white",
                                text_size=FontSize.DOUBLE_EXTRA_LARGE,
                                rect_position=(140, screen_height - 140),
                                rect_size=(420, 130),
                                text_gap=30,
                            )

                        # pega o item respectivo e ve se está em batalha ou não
                        self.selected_item = (
                            self.items_selections[item[0]][self.in_battle]
                            if self.selected
                            else self.items_selections[item[0]][self.in_battle]
                        )
                        qnt_sel = len(self.selected_item) - 2 if not self.toss else 0
                        tam = [(screen_height - 150) - qnt_sel * 40, 150 + qnt_sel * 40]

                        # possiveis seleções
                        if self.toss:
                            self.toss_item(tam)
                        else:
                            # caixa de seleção do item
                            self.selection_box_component.draw_selection_box(
                                text_list=self.selected_item,
                                rect_color="#00008B",
                                text_size=FontSize.DOUBLE_EXTRA_LARGE,
                                rect_position=(screen_width - 230, tam[0]),
                                rect_size=(220, tam[1]),
                                selected_index=self.marked[self.section][1],
                                selected_rect_radius=20,
                                rect_radius=5,
                                border_radius=5,
                                has_inner_rect=True,
                                inner_rect_radius=5,
                                text_gap=30,
                                text_spacing=50,
                            )

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

    def toss_item(self, tam): # TODO: verficar como remover o 'tam', foi colocado temporariamente
        # aviso de seleção
        
        item = self.all_items[self.section][self.marked[self.section][0]]
        if item[2] > 1:
            if not self.pressed_z[0]:
                # TODO: modificar para mudar o texto baseado na condicional, tentar utilizar apenas um text_box_component
                self.renderer.draw_text(
                    f"Toss out how many",
                    "black",
                    (140 + 20, screen_height - 110),
                    size=FontSize.DOUBLE_EXTRA_LARGE,
                )
                self.renderer.draw_text(
                    f"{item[0]}(s)?",
                    "black",
                    (140 + 20, screen_height - 65),
                    size=FontSize.DOUBLE_EXTRA_LARGE,
                )

                zeros_txt = "000"
                zeros_txt = zeros_txt[: 3 - len(str(self.selected_item[1][0]))]
                self.text_box_component.draw_text_box(
                    text_list=[f"x{zeros_txt}{self.toss_values[0]}"],
                    rect_color="#00008B",
                    text_size=FontSize.EXTRA_LARGE,
                    rect_position=(screen_width - 230, tam[0]),
                    rect_size=(220, tam[1]),
                    rect_radius=5,
                    border_radius=5,
                    has_inner_rect=True,
                    inner_rect_radius=5,
                    is_center=True,
                )
            else:
                if not self.pressed_z[1]:
                    # TODO: modificar para apenas um text_box_component (esse tbm)
                    self.renderer.draw_text(
                        f"Throw away {self.toss_values[0]} of",
                        "black",
                        (140 + 20, screen_height - 110),
                        size=FontSize.DOUBLE_EXTRA_LARGE,
                    )
                    self.renderer.draw_text(
                        "this item?",
                        "black",
                        (140 + 20, screen_height - 65),
                        size=FontSize.DOUBLE_EXTRA_LARGE,
                    )
                    # botão de seleção
                    # TODO: transformar esse em um componente de escolha - Yes/No (verificar nome do componente)
                    self.selection_box_component.draw_selection_box(
                        text_list=["Yes", "No"],
                        rect_color="#00008B",
                        text_size=FontSize.DOUBLE_EXTRA_LARGE,
                        rect_position=(screen_width - 230, tam[0]),
                        rect_size=(220, tam[1]),
                        selected_index=not self.toss_values[1],
                        selected_rect_radius=20,
                        rect_radius=5,
                        border_radius=5,
                        has_inner_rect=True,
                        inner_rect_radius=5,
                        text_gap=30,
                        text_spacing=50,
                    )
                else:
                    if self.toss_values[1]:
                        item[2] -= self.toss_values[0]
                    self.reset_toss()
        else:
            if not self.pressed_z[0]:
                # TODO: modificar para apenas um text_box_component (esse tbm)
                self.renderer.draw_text(
                    f"Throw away 1 of",
                    "black",
                    (140 + 20, screen_height - 110),
                    size=FontSize.DOUBLE_EXTRA_LARGE,
                )
                self.renderer.draw_text(
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
