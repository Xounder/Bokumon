import pygame
from settings.settings import screen_height, screen_width
from ui import Renderer, FontSize
from utils.timer import Timer


class BokuStorage:
    def __init__(self, renderer: Renderer, player, boku_summary):
        self.renderer = renderer
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
        self.renderer.draw_rect([144, 144, 168], [-10, 5, 250, screen_height - 20])
        self.renderer.draw_rect([248, 224, 208], [-10, 5, 250, screen_height - 20], 5)
        self.renderer.draw_rect(
            [112, 112, 120],
            [-5, 10, 240, screen_height / 2 - 20],
            0,
            5,
        )
        self.renderer.draw_rect([80, 80, 88], [-10, 8, 245, screen_height - 26], 3, 5)
        self.renderer.draw_rect(
            [184, 212, 244],
            [15, 60, 200, screen_height / 2 - 90],
            0,
            10,
        )
        self.renderer.draw_rect(
            [96, 96, 104],
            [15, 60, 200, screen_height / 2 - 90],
            5,
            10,
        )
        self.renderer.blit_shadow_text(
            "BKMN DATA",
            [248, 216, 144],
            [50, 35],
            size=FontSize.EXTRA_LARGE,
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
                self.renderer.blit_shadow_text(
                    f"{boku_sel.atual_name}",
                    "white",
                    [20, 320],
                    size=FontSize.DOUBLE_EXTRA_LARGE,
                )
                self.renderer.blit_shadow_text(
                    f"/{boku_sel.name}",
                    "white",
                    [20, 360],
                    size=FontSize.DOUBLE_EXTRA_LARGE,
                )
                self.renderer.blit_shadow_text(
                    f"Lv{boku_sel.level}",
                    "white",
                    [50, 400],
                    size=FontSize.DOUBLE_EXTRA_LARGE,
                )

        if self.deposit or self.show_party:
            # bokumon_player_section
            self.renderer.draw_rect([56, 136, 136], [240, 0, 300, screen_height - 20])
            self.renderer.draw_rect(
                [128, 168, 176],
                [240, 0, 300, screen_height - 20],
                10,
            )
            self.renderer.draw_rect(
                [80, 96, 112],
                [240, 0, 300, screen_height - 20],
                3,
            )
            self.renderer.draw_rect(
                [40, 104, 96],
                [250, 10, 280, screen_height - 40],
                5,
            )
            # bokumon's space
            self.renderer.draw_rect(
                [60, 108, 112],
                [260, screen_height / 2 - 70, 110, 80],
                5,
            )
            self.renderer.draw_rect(
                [0, 120, 248],
                [265, screen_height / 2 - 65, 100, 70],
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
                self.renderer.draw_rect(
                    [60, 108, 112],
                    [400, 20 + space_y, 110, 80],
                    5,
                )
                if i + 1 <= len(self.player.bokumons) - 1:
                    self.renderer.draw_rect(
                        [0, 120, 248],
                        [405, 25 + space_y, 100, 70],
                    )
                    self.player.bokumons[i + 1].draw_modified([470, space_y + 75], 1.5)
                    if self.select_player_boku[0] == i + 1:
                        self.renderer.draw_rect("red", [400, 20 + space_y, 110, 80], 5)
                space_y += 90

            self.renderer.draw_rect(
                [160, 208, 240],
                [415, 55 + space_y, 100, 40],
                0,
                5,
            )
            self.renderer.blit_shadow_text(
                "CANCEL",
                "white",
                [
                    428,
                    65 + space_y,
                ],
                size=FontSize.LARGE,
                back_color="black",
            )
            if self.select_player_boku[0] == 6:
                self.renderer.draw_rect("red", [415, 55 + space_y, 100, 40], 3, 5)

    def draw_poke_space(self):
        self.renderer.draw_rect([248, 228, 216], [0, 0, screen_width, screen_height])
        # bokumon_space
        self.renderer.draw_rect(
            [184, 184, 184],
            [240, 100, 550, screen_height - 120],
            0,
            10,
        )
        self.renderer.draw_rect(
            [224, 224, 224],
            [244, 104, 541, screen_height - 129],
            5,
            10,
        )
        self.renderer.draw_rect(
            [144, 128, 176],
            [240, 100, 550, screen_height - 120],
            5,
            10,
        )
        # section_num
        self.renderer.draw_rect([144, 136, 224], [390, 40, 250, 50], 0, 10)
        self.renderer.draw_rect([248, 248, 248], [395, 45, 240, 40], 3, 10)
        self.renderer.draw_rect([158, 146, 178], [390, 40, 250, 50], 5, 10)
        self.renderer.blit_shadow_text(
            f"{self.section_num+1}",
            "white",
            [515, 65],
            size=FontSize.LARGE,
            back_color="black",
            center=True,
        )
        if self.select_boku_box[0] == 1:
            self.renderer.draw_rect("red", [395, 45, 240, 40], 3, 10)
        # party bokumon
        self.renderer.draw_rect([164, 156, 156], [240, -10, 195, 48], 0, 5)
        self.renderer.draw_rect([160, 232, 144], [248, 3, 180, 30], 0, 5)
        self.renderer.blit_shadow_text(
            f"PARTY BOKUMON", "white", [258, 8], size=FontSize.LARGE, back_color="black"
        )
        self.renderer.draw_rect([80, 96, 112], [240, -10, 195, 48], 3, 5)
        if self.select_boku_box[0] == 0 and self.select_boku_box[1] == 0:
            self.renderer.draw_rect("red", [240, -10, 195, 48], 3, 5)
        # close box
        self.renderer.draw_rect(
            [160, 200, 240],
            [screen_width - 200, 3, 195, 30],
            0,
            10,
        )
        self.renderer.draw_rect(
            [112, 112, 120],
            [screen_width - 200, 3, 195, 30],
            3,
            10,
        )
        self.renderer.blit_shadow_text(
            f"CLOSE BOX",
            "white",
            [screen_width - 160, 8],
            size=FontSize.LARGE,
            back_color="black",
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
        self.renderer.draw_rect("white", [20, 0, 300, 150], 0, 5)
        self.renderer.draw_rect([112, 104, 128], [20, 0, 300, 150], 5, 5)
        select_list = ["Withdraw Bokumon", "Deposit Bokumon", "See ya!"]
        space_y = 20
        for i, sel in enumerate(select_list):
            self.renderer.blit_text(
                sel,
                "black",
                [50, space_y],
                size=FontSize.EXTRA_LARGE,
            )
            if i == self.selected_action[0]:
                self.renderer.draw_rect("black", [35, space_y + 5, 10, 10], 0, 20)
            space_y += 40
        # parte de baixo
        self.renderer.draw_rect(
            "white",
            [20, screen_height - 150, screen_width - 40, 140],
            0,
            20,
        )
        self.renderer.draw_rect(
            [160, 208, 224],
            [20, screen_height - 150, screen_width - 40, 140],
            5,
            20,
        )
        selected_text = [
            ["You  can  deposit  a  Bokumon  if  you", "have  any  in  a  Box."],
            ["You  can  deposit  your  party", "Bokumon  in  any  Box."],
            ["See   you   later!", ""],
        ]

        if len(self.player.bokumons) == 6 and self.selected_action[0] == 0:
            self.renderer.blit_text(
                "Can't  take  any  more  Bokumon.",
                "black",
                [50, screen_height - 120],
                size=FontSize.EXTRA_LARGE,
            )
        elif len(self.player.bokumons) == 1 and self.selected_action[0] == 1:
            self.renderer.blit_text(
                "Can't  deposit  any  Bokumon.",
                "black",
                [50, screen_height - 120],
                size=FontSize.EXTRA_LARGE,
            )
        else:
            self.renderer.blit_text(
                selected_text[self.selected_action[0]][0],
                "black",
                [50, screen_height - 120],
                size=FontSize.DOUBLE_EXTRA_LARGE,
            )
            self.renderer.blit_text(
                selected_text[self.selected_action[0]][1],
                "black",
                [50, screen_height - 70],
                size=FontSize.DOUBLE_EXTRA_LARGE,
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
        self.renderer.draw_rect(
            [112, 104, 128],
            [screen_width - 300, screen_height / 2 - 40, 280, 200],
            0,
            10,
        )
        self.renderer.draw_rect(
            "black",
            [screen_width - 300, screen_height / 2 - 40, 280, 200],
            3,
            10,
        )
        self.renderer.draw_rect(
            "white",
            [screen_width - 290, screen_height / 2 - 30, 260, 180],
            0,
            10,
        )
        space_y = 0
        for i, text in enumerate(list_choose[j]):
            self.renderer.blit_text(
                f"{text}",
                "black",
                [screen_width - 260, screen_height / 2 - 10 + space_y],
                size=FontSize.DOUBLE_EXTRA_LARGE,
            )
            if self.select_boku_action == i:
                self.renderer.draw_rect(
                    "black",
                    [screen_width - 275, screen_height / 2 - 5 + space_y, 10, 10],
                    0,
                    20,
                )
            space_y += 50

        self.renderer.draw_rect(
            [96, 112, 120],
            [screen_width - 560, screen_height - 120, 540, 100],
            0,
            5,
        )
        self.renderer.draw_rect(
            "black",
            [screen_width - 560, screen_height - 120, 540, 100],
            3,
            5,
        )
        self.renderer.draw_rect(
            "white",
            [screen_width - 550, screen_height - 110, 520, 80],
            0,
            5,
        )
        if (
            len(self.player.bokumons) == 6
            and self.select_boku_action == 0
            and self.withdraw
        ):
            self.renderer.blit_shadow_text(
                "Can't  take  any  more  Bokumon.",
                "gray",
                [screen_width - 530, screen_height - 90],
                size=FontSize.EXTRA_LARGE,
            )
        elif (
            len(self.player.bokumons) == 1
            and self.select_boku_action == 0
            and self.deposit
        ):
            self.renderer.blit_shadow_text(
                "Can't  deposit  any  Bokumon.",
                "gray",
                [screen_width - 530, screen_height - 90],
                size=FontSize.EXTRA_LARGE,
            )
        else:
            self.renderer.blit_text(
                f"{name}  is  selected.",
                "black",
                [screen_width - 530, screen_height - 90],
                size=FontSize.DOUBLE_EXTRA_LARGE,
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
