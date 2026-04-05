import pygame
from settings.settings import screen_height, screen_width
from ui import Renderer, FontSize, BoxComponent, TextBoxComponent, SelectionBoxComponent
from utils.timer import Timer


class BokuStorage:
    def __init__(self, renderer: Renderer, player, boku_summary):
        self.renderer = renderer
        self.box_component = BoxComponent(self.renderer)
        self.text_box_component = TextBoxComponent(self.renderer)
        self.selection_box_component = SelectionBoxComponent(self.renderer)

        self.player = player
        self.boku_summary = boku_summary
        self.timer = Timer(0.12)

        self.close = False
        self.active = False
        self.withdraw = False
        self.deposit = False
        self.section_num = 0
        self.selected_action = [0, False]
        self.select_boku_box = [0, 0, False]
        self.select_player_boku = [0, False]
        self.select_boku_action = 0
        self.show_party = False
        self.change_pos = False

    def draw_player_bokumon(self):
        # bokumon data
        self.box_component.draw_box(
            rect_color="#9090A8",
            rect_position=(-5, 10),
            rect_size=(240, screen_height - 30),
            rect_radius=5,
            border_color="#505058",
            border_radius=5,
        )
        self.renderer.draw_rect("#707078", [-5, 13, 237, screen_height / 2 - 20])

        self.renderer.draw_text(
            "BKMN DATA",
            [248, 216, 144],
            [50, 45],
            size=FontSize.EXTRA_LARGE,
            is_shadowed_text=True,
        )

        self.box_component.draw_box(
            rect_color="#B8D4F4",
            rect_position=(15, 60),
            rect_size=(200, screen_height / 2 - 90),
            rect_radius=10,
            border_color="#606068",
            border_width=5,
            border_radius=10,
        )

        # image and status bokumon
        if self.deposit or (self.withdraw and self.select_boku_box[0] > 1):
            boku_sel = []
            if self.withdraw and self.select_boku_box[0] > 1:
                boku_pos = self.section_num * 30 + (
                    (self.select_boku_box[0] - 2) * 6 + self.select_boku_box[1]
                )
                boku_sel = self.player.bokumon_storage[boku_pos]
            else:
                if self.select_player_boku[0] < 6:
                    boku_sel = self.player.bokumons[self.select_player_boku[0]]
            if boku_sel:
                boku_sel.draw_modified([115, 160], 1)
                self.renderer.draw_text(
                    f"{boku_sel.atual_name}",
                    "white",
                    [20, 330],
                    size=FontSize.DOUBLE_EXTRA_LARGE,
                    is_shadowed_text=True,
                )
                self.renderer.draw_text(
                    f"/{boku_sel.name}",
                    "white",
                    [20, 370],
                    size=FontSize.DOUBLE_EXTRA_LARGE,
                    is_shadowed_text=True,
                )
                self.renderer.draw_text(
                    f"Lv{boku_sel.level}",
                    "white",
                    [50, 410],
                    size=FontSize.DOUBLE_EXTRA_LARGE,
                    is_shadowed_text=True,
                )

        if self.deposit or self.show_party:
            # bokumon_player_section
            self.box_component.draw_box(
                rect_color="#80A8B0",
                rect_position=(240, 0),
                rect_size=(300, screen_height - 20),
                border_color="#506070",
            )
            self.box_component.draw_box(
                rect_color="#388888",
                rect_position=(250, 10),
                rect_size=(280, screen_height - 40),
                border_color="#286860",
                border_width=5,
            )
            # bokumon's space
            self.box_component.draw_box(
                rect_color="#0078F8",
                rect_position=(260, screen_height / 2 - 70),
                rect_size=(110, 80),
                border_color="#3C6C70",
                border_width=5,
            )

            self.player.bokumons[0].draw_modified([330, screen_height / 2 - 15], 1.5)
            if self.select_player_boku[0] == 0:
                self.renderer.draw_rect(
                    "red",
                    [260, screen_height / 2 - 70, 110, 80],
                    5,
                )
            space_y = 20
            for i in range(5):
                if i + 1 <= len(self.player.bokumons) - 1:
                    self.box_component.draw_box(
                        rect_color="#0078F8",
                        rect_position=(400, 20 + space_y),
                        rect_size=(110, 80),
                        border_color="#3C6C70",
                        border_width=5,
                    )

                    self.player.bokumons[i + 1].draw_modified([470, space_y + 75], 1.5)
                    if self.select_player_boku[0] == i + 1:
                        self.renderer.draw_rect("red", [400, 20 + space_y, 110, 80], 5)
                space_y += 90

            self.text_box_component.draw_text_box(
                text_list=["CANCEL"],
                rect_color="#A0D0F0",
                text_size=FontSize.LARGE,
                rect_position=(415, 55 + space_y),
                rect_size=(100, 40),
                rect_radius=5,
                has_border=False,
                text_color="white",
                is_shadowed_text=True,
                shadow_color="black",
                is_center=True,
            )

            if self.select_player_boku[0] == 6:
                self.renderer.draw_rect("red", [415, 55 + space_y, 100, 40], 3, 5)

    def draw_poke_space(self):
        # TODO: modificar para fill
        self.renderer.draw_rect("#F8E4D8", [0, 0, screen_width, screen_height])

        self.box_component.draw_box(
            rect_color="#E0E0E0",
            rect_position=(240, 100),
            rect_size=(550, screen_height - 120),
            rect_radius=10,
            border_color="#9080B0",
            border_width=5,
            border_radius=10,
            has_inner_rect=True,
            inner_rect_gap=8,
            inner_rect_color="#B8B8B8",
            inner_rect_radius=10,
        )

        # section_num
        self.text_box_component.draw_text_box(
            text_list=[f"{self.section_num+1}"],
            rect_color="#F8F8F8",
            text_size=FontSize.LARGE,
            rect_position=(390, 40),
            rect_size=(250, 50),
            rect_radius=10,
            border_color="#9E92B2",
            border_width=5,
            border_radius=10,
            has_inner_rect=True,
            inner_rect_gap=8,
            inner_rect_color="#9088E0",
            inner_rect_radius=5,
            text_color="white",
            is_shadowed_text=True,
            shadow_color="black",
            is_center=True,
        )

        if self.select_boku_box[0] == 1:
            self.renderer.draw_rect("red", [395, 45, 240, 40], 3, 10)
        # party bokumon
        self.text_box_component.draw_text_box(
            text_list=["PARTY BOKUMON"],
            rect_color="#A49C9C",
            text_size=FontSize.LARGE,
            rect_position=(240, -10),
            rect_size=(195, 48),
            rect_radius=5,
            border_color="#506070",
            border_radius=5,
            has_inner_rect=True,
            inner_rect_gap=7,
            inner_rect_color="#A0E890",
            inner_rect_radius=5,
            text_color="white",
            is_shadowed_text=True,
            shadow_color="black",
            is_center=True,
        )

        if self.select_boku_box[0] == 0 and self.select_boku_box[1] == 0:
            self.renderer.draw_rect("red", [240, -10, 195, 48], 3, 5)
        # close box
        self.text_box_component.draw_text_box(
            text_list=["CLOSE BOX"],
            rect_color="#A0C8F0",
            text_size=FontSize.LARGE,
            rect_position=(screen_width - 200, 3),
            rect_size=(195, 30),
            rect_radius=10,
            border_color="#707078",
            border_radius=10,
            text_color="white",
            is_shadowed_text=True,
            shadow_color="black",
            is_center=True,
        )

        if self.select_boku_box[0] == 0 and self.select_boku_box[1] == 1:
            self.renderer.draw_rect("red", [screen_width - 200, 3, 195, 30], 3, 10)

        space = [310, 170]
        limit = [self.section_num * 30, (self.section_num + 1) * 30]
        cont = [1, 0]
        cont_mat = [0, 0]
        for i, boku_stor in enumerate(self.player.bokumon_storage):
            if limit[0] <= i < limit[1]:
                boku_stor.draw_modified(space, 1.5)
                if (
                    self.select_boku_box[0] > 1
                    and cont_mat[1] == self.select_boku_box[1]
                    and cont_mat[0] == self.select_boku_box[0] - 2
                ):
                    self.renderer.draw_rect(
                        "red",
                        [space[0] - 50, space[1] - 50, 70, 70],
                        3,
                        10,
                    )
                space[0] += 90
                cont[1] += 1
                cont_mat[1] += 1
                if cont[1] / 6 == cont[0]:
                    space[0] = 310
                    space[1] += 90
                    cont[0] += 1
                    cont_mat[1] = 0
                    cont_mat[0] += 1

    def draw_selection_pc(self):
        # parte de cima
        select_list = ["Withdraw Bokumon", "Deposit Bokumon", "See ya!"]
        self.selection_box_component.draw_selection_box(
            text_list=select_list,
            rect_color="white",
            text_size=FontSize.EXTRA_LARGE,
            rect_position=(20, 0),
            rect_size=(300, 150),
            selected_index=self.selected_action[0],
            selected_rect_radius=20,
            rect_radius=5,
            border_color="#706880",
            border_width=5,
            border_radius=5,
            text_gap=30,
            text_spacing=40,
        )

        # parte de baixo
        selected_text = [
            ["You  can  deposit  a  Bokumon  if  you", "have  any  in  a  Box."],
            ["You  can  deposit  your  party", "Bokumon  in  any  Box."],
            ["See   you   later!", ""],
        ]
        text_list = selected_text[self.selected_action[0]]
        text_size = FontSize.DOUBLE_EXTRA_LARGE

        if len(self.player.bokumons) == 6 and self.selected_action[0] == 0:
            text_list = ["Can't  take  any  more  Bokumon."]
            text_size = FontSize.EXTRA_LARGE
        elif len(self.player.bokumons) == 1 and self.selected_action[0] == 1:
            text_list = ["Can't  deposit  any  Bokumon."]
            text_size = FontSize.EXTRA_LARGE

        self.text_box_component.draw_text_box(
            text_list=text_list,
            rect_color="white",
            text_size=text_size,
            rect_position=(20, screen_height - 150),
            rect_size=(screen_width - 40, 140),
            rect_radius=20,
            border_color="#A0D0E0",
            border_radius=20,
            text_gap=40,
        )

    def draw_boku_action(self):
        list_choose = [
            ["Store", "Summary", "Cancel"],
            ["Withdraw", "Summary", "Cancel"],
        ]
        if self.deposit:
            j = 0
            name = self.player.bokumons[self.select_player_boku[0]].atual_name
        elif self.withdraw:
            tam = self.section_num * 30 + (
                (self.select_boku_box[0] - 2) * 6 + self.select_boku_box[1]
            )
            name = self.player.bokumon_storage[tam].atual_name
            j = 1

        self.selection_box_component.draw_selection_box(
            text_list=list_choose[j],
            rect_color="#706880",
            text_size=FontSize.DOUBLE_EXTRA_LARGE,
            rect_position=(screen_width - 300, screen_height / 2 - 40),
            rect_size=(280, 200),
            selected_index=self.select_boku_action,
            selected_rect_radius=20,
            rect_radius=10,
            border_radius=10,
            has_inner_rect=True,
            inner_rect_radius=10,
            text_gap=30,
            text_spacing=50,
        )

        text_list = [f"{name}  is  selected."]
        text_size = FontSize.DOUBLE_EXTRA_LARGE
        text_color = "black"
        is_shadowed_text = False

        if (
            len(self.player.bokumons) == 6
            and self.select_boku_action == 0
            and self.withdraw
        ):
            text_list = ["Can't  take  any  more  Bokumon."]
            text_size = FontSize.EXTRA_LARGE
            text_color = "gray"
            is_shadowed_text = True
        elif (
            len(self.player.bokumons) == 1
            and self.select_boku_action == 0
            and self.deposit
        ):
            text_list = ["Can't  deposit  any  Bokumon."]
            text_size = FontSize.EXTRA_LARGE
            text_color = "gray"
            is_shadowed_text = True

        self.text_box_component.draw_text_box(
            text_list=text_list,
            rect_color="#607078",
            text_size=text_size,
            rect_position=(screen_width - 560, screen_height - 120),
            rect_size=(540, 100),
            border_radius=5,
            has_inner_rect=True,
            inner_rect_radius=5,
            text_color=text_color,
            text_gap=30,
            is_shadowed_text=is_shadowed_text,
        )

    def draw(self):
        if self.boku_summary.active:
            self.boku_summary.draw()
        else:
            if not self.selected_action[1]:
                self.draw_selection_pc()
            else:
                self.draw_poke_space()
                self.draw_player_bokumon()
                if self.select_boku_box[2] or self.select_player_boku[1]:
                    self.draw_boku_action()

    def update(self):
        if self.boku_summary.active:
            self.boku_summary.update()
            self.change_pos = True
        else:
            if self.change_pos:
                pos = self.boku_summary.last_boku_pos
                self.section_num = int(pos / 30)
                pos -= self.section_num * 30
                self.select_boku_box[0] = int(pos / 6)
                pos -= self.select_boku_box[0] * 6
                self.select_boku_box[1] = pos
                self.select_boku_box[0] += 2
                self.change_pos = False
                self.timer.active()

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
                    if self.withdraw and not self.show_party:
                        if not self.select_boku_box[2]:
                            self.select_boku_box[0] -= (
                                1 if self.select_boku_box[0] > 0 else 0
                            )
                            if self.select_boku_box[0] == 1:
                                self.select_boku_box[1] = 0
                        else:
                            self.select_boku_action -= (
                                1 if self.select_boku_action > 0 else 0
                            )

                    elif self.deposit:
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
                            self.select_boku_action -= (
                                1 if self.select_boku_action > 0 else 0
                            )

            elif keys[pygame.K_DOWN]:
                if not self.selected_action[1]:
                    self.selected_action[0] += 1 if self.selected_action[0] < 2 else 0
                else:
                    if self.withdraw and not self.show_party:
                        if not self.select_boku_box[2]:
                            if self.select_boku_box[0] < 2:
                                self.select_boku_box[0] += 1
                                if self.select_boku_box[0] == 2:
                                    qnt_boku_sec = (
                                        len(self.player.bokumon_storage) - 1
                                    ) - (self.section_num * 30)
                                    qnt_boku_sec = (
                                        qnt_boku_sec if qnt_boku_sec > 0 else 0
                                    )
                                    self.select_boku_box[1] = (
                                        2 if qnt_boku_sec > 2 else qnt_boku_sec
                                    )
                            else:
                                section_total = (
                                    len(self.player.bokumon_storage)
                                    - self.section_num * 30
                                )
                                self.select_boku_box[0] += (
                                    1
                                    if (
                                        self.select_boku_box[0] - 1 < 5
                                        and (self.select_boku_box[0] - 1) * 6
                                        + self.select_boku_box[1]
                                        + 1
                                        <= section_total
                                    )
                                    else 0
                                )

                            if (
                                len(self.player.bokumon_storage) - 1
                            ) < 0 and self.select_boku_box[0] == 2:
                                self.select_boku_box[0] = 1
                        else:
                            self.select_boku_action += (
                                1 if self.select_boku_action < 2 else 0
                            )

                    elif self.deposit:
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
                            self.select_boku_action += (
                                1 if self.select_boku_action < 2 else 0
                            )

            elif keys[pygame.K_LEFT]:
                if self.withdraw and not self.show_party:
                    if not self.select_boku_box[2]:
                        if self.select_boku_box[0] == 0:
                            self.select_boku_box[1] = 0
                        elif self.select_boku_box[0] == 1:
                            self.section_num -= 1 if self.section_num > 0 else 0
                        else:
                            self.select_boku_box[1] -= (
                                1 if self.select_boku_box[1] > 0 else 0
                            )

                elif self.deposit:
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

            elif keys[pygame.K_RIGHT]:
                if self.withdraw and not self.show_party:
                    if not self.select_boku_box[2]:
                        if self.select_boku_box[0] == 0:
                            self.select_boku_box[1] = 1
                        elif self.select_boku_box[0] == 1:
                            self.section_num += (
                                1
                                if self.section_num
                                < int((len(self.player.bokumon_storage) - 1) / 30)
                                else 0
                            )
                        else:
                            section_total = (
                                len(self.player.bokumon_storage) - 1
                            ) - self.section_num * 30
                            self.select_boku_box[1] += (
                                1
                                if self.select_boku_box[1] < 5
                                and (self.select_boku_box[0] - 2) * 6
                                + self.select_boku_box[1]
                                < section_total
                                else 0
                            )
                elif self.deposit:
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

            if keys[pygame.K_z]:
                if not self.selected_action[1]:
                    if self.selected_action[0] == 0 and len(self.player.bokumons) < 6:
                        self.withdraw = True
                        self.deposit = False
                        self.selected_action[1] = True
                    elif self.selected_action[0] == 1 and len(self.player.bokumons) > 1:
                        self.withdraw = False
                        self.deposit = True
                        self.selected_action[1] = True
                    elif self.selected_action[0] == 2:
                        self.close = True
                        self.selected_action[0] = 0
                        self.section_num = 0
                else:
                    if self.withdraw:
                        if not self.show_party:
                            if not self.select_boku_box[2]:
                                if (
                                    self.select_boku_box[0] == 0
                                    and self.select_boku_box[1] == 0
                                ):
                                    # boku party
                                    self.show_party = True
                                    self.select_player_boku[0] = 6
                                elif (
                                    self.select_boku_box[0] == 0
                                    and self.select_boku_box[1] == 1
                                ):
                                    self.selected_action = [0, False]
                                    self.close = True
                                    self.select_boku_box = [0, 0, False]
                                    self.section_num = 0
                                elif self.select_boku_box[0] > 1:
                                    self.select_boku_box[2] = True
                            else:
                                boku_pos = self.section_num * 30 + (
                                    (self.select_boku_box[0] - 2) * 6
                                    + self.select_boku_box[1]
                                )
                                if self.select_boku_action == 0:
                                    # withdraw
                                    if len(self.player.bokumons) < 6:
                                        self.player.bokumon_pc_box(boku_pos)
                                        if (
                                            boku_pos
                                            > len(self.player.bokumon_storage) - 1
                                        ):
                                            if self.select_boku_box[1] > 0:
                                                self.select_boku_box[1] -= 1
                                            else:
                                                if self.section_num > 0:
                                                    self.section_num -= 1
                                                    self.select_boku_box[0] = 6
                                                    self.select_boku_box[1] = 5
                                                else:
                                                    self.select_boku_box[0] -= 1
                                                    self.select_boku_box[1] = 5

                                    self.select_boku_box[2] = False
                                    self.select_boku_action = 0
                                elif self.select_boku_action == 1:
                                    self.boku_summary.active = True
                                    self.boku_summary.seted = False
                                    self.boku_summary.set_summary(boku_pos, view=False)
                                    self.select_boku_box[2] = False
                                    self.change_pos = True
                                elif self.select_boku_action == 2:
                                    self.select_boku_box[2] = False
                                    self.select_boku_action = 0
                        else:
                            self.show_party = False

                    elif self.deposit:
                        if not self.select_player_boku[1]:
                            if self.select_player_boku[0] == 6:
                                self.selected_action[1] = False
                                self.select_player_boku[0] = 0
                            else:
                                self.select_player_boku[1] = True
                        else:
                            if self.select_boku_action == 0:
                                # store
                                if len(self.player.bokumons) > 1:
                                    self.player.bokumon_pc_box(
                                        self.select_player_boku[0], pc_to_player=False
                                    )
                                    if (
                                        self.select_player_boku[0]
                                        > len(self.player.bokumons) - 1
                                    ):
                                        self.select_player_boku[0] -= 1
                                self.select_player_boku[1] = False
                                self.select_boku_action = 0
                            elif self.select_boku_action == 1:
                                self.boku_summary.active = True
                                self.boku_summary.seted = False
                                self.boku_summary.set_summary(
                                    self.select_player_boku[0]
                                )
                            elif self.select_boku_action == 2:
                                self.select_player_boku[1] = False
                                self.select_boku_action = 0

            elif keys[pygame.K_x]:
                if not self.selected_action[1]:
                    self.close = True
                    self.select_boku_box = [0, 0, False]
                    self.section_num = 0
                    self.selected_action = [0, False]
                    self.select_player_boku = [0, False]
                else:
                    if self.select_boku_box[2] or self.select_player_boku[1]:
                        self.select_boku_box[2] = False
                        self.select_player_boku[1] = False
                        self.select_boku_action = 0
                    elif self.show_party:
                        self.show_party = False
                    else:
                        self.select_boku_box = [0, 0, False]
                        self.section_num = 0
                        self.selected_action[1] = False
                        self.select_player_boku = [0, False]
            self.timer.active()
