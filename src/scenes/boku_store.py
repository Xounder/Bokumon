import pygame
from settings.settings import screen_height, screen_width
from ui import Renderer, FontSize, BoxComponent, TextBoxComponent, SelectionBoxComponent
from utils.timer import Timer


class BokuStore:
    def __init__(self, renderer: Renderer, player, bag):
        self.renderer = renderer
        self.box_component = BoxComponent(self.renderer)
        self.text_box_component = TextBoxComponent(self.renderer)
        self.selection_box_component = SelectionBoxComponent(self.renderer)

        self.player = player
        self.bag = bag
        self.timer = Timer(0.12)

        self.active = False
        self.set_store()
        self.items_disp = [
            [["Items", 5, 1], ["Potion", 20, 1]],
            [["Boku Balls", 5, 1], ["Boku Ball", 1, 1]],
            [["Boku Balls", 2, 1], ["Great Ball", 1.25, 1]],
            [["Boku Balls", 1, 2], ["Ultra Ball", 1.6, 1]],
            [["Items", 2, 1], ["Super Potion", 50, 1]],
            [["Items", 1, 2], ["Hyper Potion", 200, 1]],
        ]

    def set_store(self):
        self.close = False
        self.cant_buy = False
        self.select_buy = False
        self.text_select_buy = False
        self.select_player_boku = [0, False]
        self.select_trade = False
        self.cant_trade = False
        self.gain_tp = 0
        self.selected_action = [0, False]
        self.limit_visu_items = [0, 7]
        # sel_item|[cont_item, buy]|selected
        self.selected_item = [0, [1, False], False]

    def draw_select_action(self):
        list_choose = ["Buy", "Trade", "See ya!"]
        self.selection_box_component.draw_selection_box(
            text_list=list_choose,
            rect_color="#706880",
            text_size=FontSize.DOUBLE_EXTRA_LARGE,
            rect_position=(screen_width - 300, screen_height / 2 - 40),
            rect_size=(280, 200),
            selected_index=self.selected_action[0],
            selected_rect_radius=20,
            rect_radius=10,
            border_radius=10,
            has_inner_rect=True,
            inner_rect_radius=10,
            text_gap=30,
            text_spacing=50,
        )

        list_desc = [
            "Buy  an  item  using  Ticket  Points.",
            "Trade  a  Bokumon  to  obtain  a  Ticket  Points.",
            "See   you  later!",
        ]
        self.text_box_component.draw_text_box(
            text_list=[f"{list_desc[self.selected_action[0]]}"],
            rect_color="#607078",
            text_size=FontSize.DOUBLE_EXTRA_LARGE,
            rect_position=(20, screen_height - 120),
            rect_size=(screen_width - 40, 100),
            has_inner_rect=True,
            inner_rect_radius=5,
            border_radius=5,
            text_gap=30,
        )

    def draw_buy_items(self):
        self.box_component.draw_box(
            rect_color="#706880",
            rect_position=(200, 20),
            rect_size=(570, 450),
            rect_radius=10,
            border_radius=10,
            has_inner_rect=True,
            inner_rect_radius=10,
        )

        self.renderer.draw_text(
            f"Your   T.P:    {self.player.tickets}",
            "black",
            [220, 45],
            size=FontSize.MEDIUM,
        )
        self.renderer.draw_text(
            "Item",
            "black",
            [250, 90],
            size=FontSize.DOUBLE_EXTRA_LARGE,
        )
        self.renderer.draw_text(
            "Qnt.",
            "black",
            [480, 90],
            size=FontSize.DOUBLE_EXTRA_LARGE,
        )
        self.renderer.draw_text(
            "T.P",
            "black",
            [630, 90],
            size=FontSize.DOUBLE_EXTRA_LARGE,
        )

        self.renderer.draw_text(
            "*Obtain T.P Evolving, Upping or Trading a Bokumon",
            "black",
            [220, screen_height - 165],
            size=FontSize.MEDIUM,
        )

        # TODO: melhorar esta parte dos draw
        space_y = 0
        for i, item in enumerate(self.items_disp):
            if self.limit_visu_items[0] <= i <= self.limit_visu_items[1]:
                self.renderer.draw_text(
                    f"{item[1][0]}",
                    "black",
                    [250, 140 + space_y],
                    size=FontSize.EXTRA_LARGE,
                )
                self.renderer.draw_text(
                    f"{item[0][1]}",
                    "black",
                    [500, 140 + space_y],
                    size=FontSize.EXTRA_LARGE,
                    is_center=True,
                )
                self.renderer.draw_text(
                    f"{item[0][2]}",
                    "black",
                    [650, 140 + space_y],
                    size=FontSize.EXTRA_LARGE,
                    is_center=True,
                )
                if self.selected_item[0] == i:
                    color = "black" if not self.selected_item[2] else "red"
                    self.renderer.draw_rect(color, [235, 135 + space_y, 10, 10], 0, 20)
                space_y += 40
            elif i > self.limit_visu_items[1]:
                break

        if self.selected_item[2] or self.cant_buy:
            sel_item = self.items_disp[self.selected_item[0]]
            if self.cant_buy:
                msg = "Don't have any Ticket Points."
            elif self.text_select_buy:
                msg = f"Buy {self.selected_item[1][0]*sel_item[0][1]} {sel_item[1][0]} using {self.selected_item[1][0]*sel_item[0][2]} Ticket Points?"
            else:
                msg = f"{sel_item[1][0]} is selected."

            self.text_box_component.draw_text_box(
                text_list=[msg],
                rect_color="#607078",
                text_size=FontSize.DOUBLE_EXTRA_LARGE,
                rect_position=(20, screen_height - 120),
                rect_size=(screen_width - 50, 100),
                has_inner_rect=True,
                inner_rect_radius=5,
                border_radius=5,
                text_gap=30,
            )

        if self.selected_item[2]:
            zeros_txt = "000"
            zeros_txt = zeros_txt[: 3 - len(str(self.selected_item[1][0]))]

            self.text_box_component.draw_text_box(
                text_list=[f"x{zeros_txt}{self.selected_item[1][0]}"],
                rect_color="#607078",
                text_size=FontSize.EXTRA_LARGE,
                rect_position=(screen_width - 230, screen_height - 220),
                rect_size=(200, 100),
                rect_radius=5,
                has_inner_rect=True,
                inner_rect_radius=5,
                border_radius=5,
                is_center=True,
            )

        if self.selected_item[1][1]:
            self.selection_box_component.draw_selection_box(
                text_list=["Yes", "No"],
                rect_color="#607078",
                text_size=FontSize.LARGE,
                rect_position=(screen_width - 130, screen_height - 300),
                rect_size=(100, 100),
                selected_index=not self.select_buy,
                selected_rect_radius=20,
                rect_radius=5,
                border_radius=5,
                has_inner_rect=True,
                inner_rect_radius=5,
                text_gap=25,
            )

    def draw_trade(self):
        self.draw_player_trade()
        self.draw_merc_trade()

    def draw_merc_trade(self):
        self.box_component.draw_box(
            rect_color="#388888",
            rect_position=(350, screen_height / 2 - 200),
            rect_size=(420, screen_height / 2 + 60),
            rect_radius=10,
            border_radius=10,
            has_inner_rect=True,
            inner_rect_radius=10,
        )

        self.renderer.draw_text(
            "TRADE BOKUMON",
            "black",
            [430, screen_height / 2 - 160],
            size=FontSize.DOUBLE_EXTRA_LARGE,
        )
        self.renderer.draw_text(
            f"Your T.P:    {self.player.tickets}",
            "black",
            [370, screen_height - 160],
            size=FontSize.MEDIUM,
        )
        self.renderer.draw_text(
            "=>",
            "black",
            [550, screen_height / 2 - 10],
            size=FontSize.EXTRA_LARGE,
        )
        self.renderer.draw_text(
            "T.P",
            "black",
            [670, screen_height / 2 + 60],
            size=FontSize.EXTRA_LARGE,
        )

        self.box_component.draw_box(
            rect_color="#0078F8" if self.select_player_boku[1] else "white",
            rect_position=(380, screen_height / 2 - 50),
            rect_size=(110, 80),
            border_color="#3C6C70",
            border_width=5,
        )

        if self.select_player_boku[1]:
            sel_boku = self.player.bokumons[self.select_player_boku[0]]
            self.gain_tp = round(
                (
                    (
                        sel_boku.attack
                        + sel_boku.defense
                        + sel_boku.speed
                        + sel_boku.life
                    )
                    / 2
                )
                / sel_boku.level
            )
            # TODO: remover repetição 1
            self.renderer.draw_text(
                f"{sel_boku.name}",
                "black",
                [380, screen_height / 2 - 100],
                size=FontSize.EXTRA_LARGE,
            )
            self.renderer.draw_text(
                f"/{sel_boku.name}",
                "black",
                [380, screen_height / 2 - 70],
                size=FontSize.EXTRA_LARGE,
            )
            self.renderer.draw_text(
                f"Lv{sel_boku.level}",
                "black",
                [410, screen_height / 2 + 60],
                size=FontSize.EXTRA_LARGE,
            )
            self.renderer.draw_text(
                f"{self.gain_tp}",
                "black",
                [690, screen_height / 2],
                size=FontSize.EXTRA_LARGE,
                is_center=True,
            )

            sel_boku.draw_modified([450, screen_height / 2 + 5], 1.5)
            # choose
            self.selection_box_component.draw_selection_box(
                text_list=["Yes", "No"],
                rect_color="#388888",
                text_size=FontSize.LARGE,
                rect_position=(screen_width - 130, screen_height - 210),
                rect_size=(100, 100),
                selected_index=not self.select_trade,
                selected_rect_radius=20,
                rect_radius=5,
                border_radius=5,
                has_inner_rect=True,
                inner_rect_radius=5,
                text_gap=25,
            )
            # text
            self.text_box_component.draw_text_box(
                text_list=[
                    f"Trade  {sel_boku.name}  Lv{sel_boku.level}  for  {self.gain_tp}  Ticket Points?"
                ],
                rect_color="#607078",
                text_size=FontSize.DOUBLE_EXTRA_LARGE,
                rect_position=(20, screen_height - 110),
                rect_size=(screen_width - 50, 100),
                has_inner_rect=True,
                inner_rect_radius=5,
                border_radius=5,
                text_gap=30,
            )

        else:
            if self.cant_trade:
                self.text_box_component.draw_text_box(
                    text_list=["Can't trade any more"],
                    rect_color="#607078",
                    text_size=FontSize.DOUBLE_EXTRA_LARGE,
                    rect_position=(350, screen_height - 110),
                    rect_size=(420, 100),
                    rect_radius=5,
                    border_radius=5,
                    has_inner_rect=True,
                    inner_rect_radius=5,
                    is_center=True,
                )
            else:
                # TODO: remover repetição 2
                self.renderer.draw_text(
                    "Bokumon",
                    "black",
                    [380, screen_height / 2 - 80],
                    size=FontSize.EXTRA_LARGE,
                )
                self.renderer.draw_text(
                    "Lv",
                    "black",
                    [410, screen_height / 2 + 60],
                    size=FontSize.EXTRA_LARGE,
                )
                self.renderer.draw_text(
                    "0",
                    "black",
                    [690, screen_height / 2],
                    size=FontSize.EXTRA_LARGE,
                    is_center=True,
                )

    def draw_player_trade(self):
        # bokumon_player_section        
        self.box_component.draw_box(
            rect_color="#80A8B0",
            rect_position=(20, 10),
            rect_size=(300, screen_height - 20),
            border_color="#506070",
        )
        self.box_component.draw_box(
            rect_color="#388888",
            rect_position=(30, 20),
            rect_size=(280, screen_height - 40),
            border_color="#286860",
            border_width=5,
        )

        # bokumon's space
        self.box_component.draw_box(
            rect_color="#0078F8",
            rect_position=(40, screen_height / 2 - 70),
            rect_size=(110, 80),
            border_color="#3C6C70",
            border_width=5,
        )

        self.player.bokumons[0].draw_modified([110, screen_height / 2 - 15], 1.5)
        if self.select_player_boku[0] == 0:
            self.renderer.draw_rect("red", [40, screen_height / 2 - 70, 110, 80], 5)
        space_y = 20
        for i in range(5):
            if i + 1 <= len(self.player.bokumons) - 1:
                self.box_component.draw_box(
                    rect_color="#0078F8",
                    rect_position=(180, 20 + space_y),
                    rect_size=(110, 80),
                    border_color="#3C6C70",
                    border_width=5,
                )

                self.player.bokumons[i + 1].draw_modified([250, space_y + 75], 1.5)
                if self.select_player_boku[0] == i + 1:
                    self.renderer.draw_rect("red", [180, 20 + space_y, 110, 80], 5)
            space_y += 90

        self.text_box_component.draw_text_box(
            text_list=["CANCEL"],
            rect_color="#A0D0F0",
            text_size=FontSize.LARGE,
            rect_position=(195, 55 + space_y),
            rect_size=(100, 40),
            has_border=False,
            text_color="white",
            is_shadowed_text=True,
            is_center=True,
        )

        if self.select_player_boku[0] == 6:
            self.renderer.draw_rect("red", [195, 55 + space_y, 100, 40], 3, 5)

    def draw(self):
        if not self.selected_action[1]:
            self.draw_select_action()
        else:
            if self.selected_action[0] == 0:
                self.draw_buy_items()
            if self.selected_action[0] == 1:
                self.draw_trade()

    def update(self):
        if self.timer.run:
            self.timer.update()
        self.input()

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.timer.run:
            if keys[pygame.K_UP]:
                if not self.selected_action[1]:
                    self.selected_action[0] -= 1 if self.selected_action[0] > 0 else 0
                else:
                    if self.selected_action[0] == 0:
                        if not self.selected_item[2]:
                            self.selected_item[0] -= (
                                1 if self.selected_item[0] > 0 else 0
                            )
                            if (
                                self.selected_item[0] - 1 > 0
                                and self.limit_visu_items[1] > 7
                            ):
                                self.limit_visu_items[1] -= 1
                                self.limit_visu_items[0] -= 1
                        else:
                            if not self.selected_item[1][1]:
                                val_item = self.items_disp[self.selected_item[0]][0][2]
                                tp_count = self.selected_item[1][0] * val_item
                                self.selected_item[1][0] += (
                                    1 if tp_count < self.player.tickets else 0
                                )
                            else:
                                self.select_buy = True

                    elif self.selected_action[0] == 1:
                        if not self.select_player_boku[1]:
                            if self.select_player_boku[0] > 0:
                                if self.select_player_boku[0] - 1 < len(
                                    self.player.bokumons
                                ):
                                    self.select_player_boku[0] -= 1
                                else:
                                    self.select_player_boku[0] = (
                                        len(self.player.bokumons) - 1
                                    )
                            else:
                                self.select_player_boku[0] = 6
                        else:
                            self.select_trade = True

            elif keys[pygame.K_DOWN]:
                if not self.selected_action[1]:
                    self.selected_action[0] += 1 if self.selected_action[0] < 2 else 0
                else:
                    if self.selected_action[0] == 0:
                        if not self.selected_item[2]:
                            self.selected_item[0] += (
                                1
                                if self.selected_item[0] < len(self.items_disp) - 1
                                else 0
                            )
                            if self.selected_item[0] + 1 >= self.limit_visu_items[1]:
                                self.limit_visu_items[1] += 1
                                self.limit_visu_items[0] += 1
                        else:
                            if not self.selected_item[1][1]:
                                self.selected_item[1][0] -= (
                                    1 if self.selected_item[1][0] > 1 else 0
                                )
                            else:
                                self.select_buy = False

                    elif self.selected_action[0] == 1:
                        if not self.select_player_boku[1]:
                            if self.select_player_boku[0] < 6:
                                if self.select_player_boku[0] + 1 < len(
                                    self.player.bokumons
                                ):
                                    self.select_player_boku[0] += 1
                                else:
                                    self.select_player_boku[0] = 6
                            else:
                                self.select_player_boku[0] = 0
                        else:
                            self.select_trade = False

            elif keys[pygame.K_LEFT]:
                if not self.select_player_boku[1]:
                    if self.select_player_boku[0] > 0:
                        if self.select_player_boku[0] - 1 < len(self.player.bokumons):
                            self.select_player_boku[0] -= 1
                        else:
                            self.select_player_boku[0] = len(self.player.bokumons) - 1
                    else:
                        self.select_player_boku[0] = 6

            elif keys[pygame.K_RIGHT]:
                if not self.select_player_boku[1]:
                    if self.select_player_boku[0] < 6:
                        if self.select_player_boku[0] + 1 < len(self.player.bokumons):
                            self.select_player_boku[0] += 1
                        else:
                            self.select_player_boku[0] = 6
                    else:
                        self.select_player_boku[0] = 0

            if keys[pygame.K_z]:
                if not self.selected_action[1]:
                    if self.selected_action[0] == 0:
                        self.selected_action[1] = True
                    elif self.selected_action[0] == 1:
                        self.selected_action[1] = True
                    elif self.selected_action[0] == 2:
                        self.close = True
                        self.selected_action[0] = 0
                else:
                    if self.selected_action[0] == 0:
                        # buy choose
                        if not self.selected_item[2]:
                            if self.player.tickets > 0:
                                self.selected_item[2] = True
                                self.cant_buy = False
                            else:
                                self.cant_buy = True
                        else:
                            if not self.selected_item[1][1]:
                                self.selected_item[1][1] = True
                                self.text_select_buy = True
                            else:
                                if self.select_buy:  # buy
                                    item_list = self.items_disp[self.selected_item[0]]
                                    qnt = item_list[0][1] * self.selected_item[1][0]
                                    val = item_list[0][2] * self.selected_item[1][0]
                                    self.bag.buy_item(
                                        item_list[1], qnt, item_list[0][0]
                                    )
                                    self.player.tickets -= val

                                self.selected_item[1][1] = False
                                self.selected_item[1][0] = 1
                                self.selected_item[2] = False
                                self.select_buy = False
                                self.text_select_buy = False

                    elif self.selected_action[0] == 1:
                        # trade choose
                        if not self.select_player_boku[1]:
                            if self.select_player_boku[0] == 6:
                                self.selected_action[1] = False
                            else:
                                if len(self.player.bokumons) > 1:
                                    self.select_player_boku[1] = True
                                    self.cant_trade = False
                                else:
                                    self.cant_trade = True
                        else:
                            if not self.select_trade:
                                self.select_player_boku[1] = False
                            else:
                                self.select_player_boku[1] = False
                                self.select_trade = False
                                self.player.trade_bokumon(
                                    self.select_player_boku[0], self.gain_tp
                                )
                                self.gain_tp = 0
                                if (
                                    self.select_player_boku[0]
                                    > len(self.player.bokumons) - 1
                                ):
                                    self.select_player_boku[0] -= 1

            elif keys[pygame.K_x]:
                if not self.selected_action[1]:
                    self.close = True
                    self.selected_action[0] = 0
                else:
                    if self.selected_action[0] == 0:
                        if not self.selected_item[2]:
                            self.selected_action[1] = False
                        else:
                            if not self.selected_item[1][1]:
                                self.selected_item[2] = False
                                self.selected_item[1][0] = 1
                            else:
                                self.select_buy = False
                                self.text_select_buy = False
                                self.selected_item[1][1] = False

                    elif self.selected_action[0] == 1:
                        if not self.select_player_boku[1]:
                            self.selected_action[1] = False
                        else:
                            if self.select_player_boku[1]:
                                self.select_player_boku[1] = False
            self.timer.active()
