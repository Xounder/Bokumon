import pygame
from settings.settings import *
from ui import Renderer, FontSize, BoxComponent, TextBoxComponent
from utils.timer import Timer


class BokuSummary:
    def __init__(self, renderer: Renderer, player):
        self.renderer = renderer
        self.box_component = BoxComponent(self.renderer)
        self.text_box_component = TextBoxComponent(self.renderer)

        self.player = player
        # vars
        self.seted = False
        self.active = False
        self.section = 0
        self.selected_move = [False, False, [0, 0]]
        self.boku_selected = None
        self.last_boku_pos = 0
        # boku_ball
        self.boku_ball_img = {
            "Boku Ball": self.renderer.load_asset_image(
                "boku_ball", is_convert_alpha=True
            ),
            "Great Ball": self.renderer.load_asset_image(
                "great_ball", is_convert_alpha=True
            ),
            "Ultra Ball": self.renderer.load_asset_image(
                "ultra_ball", is_convert_alpha=True
            ),
        }
        # timer
        self.timer = Timer(0.12)

    def set_summary(self, boku_selected, view=True):
        if not self.seted:
            self.boku_selected = boku_selected
            self.view = view
            if not view:
                self.boku_local = self.player.bokumon_storage
            else:
                self.boku_local = self.player.bokumons
            self.section = 0
            self.selected_move = [False, False, [0, 0]]
            self.seted = True

    def draw(self):
        self.renderer.fill_screen("#A0B2C4")

        # parte de cima
        self.renderer.draw_rect("#489870", (0, 0, screen_width, 50))
        self.renderer.draw_rect(
            "#78D8A0",
            (-20, 0, screen_width / 2 + 50, 50),
            0,
            20,
        )

        move_x = screen_width / 2 if not self.section == 1 else screen_width / 2 + 50
        section_text = "Bokumon  Skill" if self.section == 0 else "Know  Moves"

        self.text_box_component.draw_text_box(
            text_list=[section_text],
            rect_color="#F8E898",
            text_size=FontSize.DOUBLE_EXTRA_LARGE,
            rect_position=(-20, 0),
            rect_size=(move_x, 50),
            rect_radius=20,
            border_radius=20,
            is_middle=True,
            text_gap=30,
        )

        self.renderer.draw_rect("black", (-20, 0, screen_width + 30, 50), 3)
        # dots
        color_1 = "#C0A060" if self.section == 0 else "#F8F8F8" # TODO: modificar / verificar uso de draw_circle
        color_2 = "#C0A060" if self.section == 1 else "#F8F8F8"
        self.renderer.draw_rect(color_1, (screen_width / 2 - 10, 12, 20, 25), 0, 30)
        self.renderer.draw_rect(color_2, (screen_width / 2 - 60, 12, 20, 25), 0, 30)
        # draw seção especifica
        if self.section == 0:
            self.draw_skill_move()
        else:
            self.draw_know_move()
        # bokumon
        self.box_component.draw_box(
            rect_color="#788090",
            rect_position=(-2, 49),
            rect_size=(screen_width / 2 + 2, screen_height / 2),
            has_inner_rect=True,
            inner_rect_position=(5, 100),
            inner_rect_size=(screen_width / 2 - 15, screen_height / 2 - 60),
            inner_rect_color="#C0C0C0",
        )

        self.renderer.draw_text(
            f"Lv{self.boku_local[self.boku_selected].level}",
            "black",
            (10, 70),
            size=FontSize.DOUBLE_EXTRA_LARGE,
        )
        self.renderer.draw_text(
            f"{self.boku_local[self.boku_selected].name}",
            "black",
            (130, 70),
            size=FontSize.DOUBLE_EXTRA_LARGE,
        )
        self.boku_local[self.boku_selected].draw_modified((160, 200), 0.7)
        self.draw_boku_ball((screen_width / 2 - 40, screen_height / 2 + 30), 1.7)

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.timer.run:
            if keys[pygame.K_LEFT]:
                if not self.selected_move[0]:
                    self.section = 0
            elif keys[pygame.K_RIGHT]:
                if not self.selected_move[0]:
                    self.section = 1
            elif keys[pygame.K_UP]:
                if not self.selected_move[0]:
                    self.boku_selected -= 1 if self.boku_selected > 0 else 0
                else:
                    self.move_marked(-1, 0, self.selected_move[1])
                    self.move_marked(-1, 1, False)
            elif keys[pygame.K_DOWN]:
                if not self.selected_move[0]:
                    self.boku_selected += (
                        1 if self.boku_selected < len(self.boku_local) - 1 else 0
                    )
                else:
                    self.move_marked(1, 0, self.selected_move[1])
                    self.move_marked(1, 1, False)

            if keys[pygame.K_z]:
                if not self.selected_move[0] and self.section == 1:
                    self.selected_move[0] = True
                elif self.selected_move[0]:
                    if self.selected_move[2][0] != 4:
                        self.selected_move[1] = True
                    else:
                        self.selected_move[0] = False
                        self.selected_move[2] = [0, 0]
                if (
                    self.selected_move[1]
                    and self.selected_move[2][0] != self.selected_move[2][1]
                ):
                    self.boku_local[self.boku_selected].switch_moves(
                        self.selected_move[2]
                    )
                    self.selected_move[1] = False
                    self.selected_move[0] = False
                    self.selected_move[2][0] = self.selected_move[2][1]

            elif keys[pygame.K_x]:
                if not self.selected_move[0]:
                    self.active = False
                    self.last_boku_pos = self.boku_selected
                elif self.selected_move[1]:
                    self.selected_move[1] = False
                    self.selected_move[2][0] = self.selected_move[2][1]
                else:
                    self.selected_move[0] = False
            self.timer.active()

    def update(self):
        if self.timer.run:
            self.timer.update()
        self.input()

    def draw_boku_ball(self, rect_center, scale):
        bokumon_ball = self.boku_local[self.boku_selected].ball
        self.boku_ball_rect = self.boku_ball_img[bokumon_ball].get_rect(
            center=(rect_center)
        )
        image_mod = self.renderer.scale_image(
            self.boku_ball_img[bokumon_ball],
            (
                self.boku_ball_img[bokumon_ball].get_width() / scale,
                self.boku_ball_img[bokumon_ball].get_height() / scale,
            ),
        )
        self.renderer.blit(image_mod, self.boku_ball_rect)

    def draw_skill_move(self):
        # details
        self.renderer.draw_rect(  # TODO: modificar para draw_line
            "#D4E4F6",
            (0, 50, screen_width / 2 + 3, screen_height / 2 + 2),
        )
        self.renderer.draw_rect(  # TODO: modificar para draw_line
            "#D4E4F6",
            (screen_width / 2 + 3, 50, screen_width / 2 + 3, 3),
        )

        # stats / life
        atual_boku = self.boku_local[self.boku_selected]

        self.text_box_component.draw_text_box(
            text_list=[f"{atual_boku.atual_life}/{atual_boku.life}"],
            rect_color="#E8F0F8",
            text_size=FontSize.DOUBLE_EXTRA_LARGE,
            rect_position=(screen_width / 2 + 120, 60),
            rect_size=(250, 40),
            rect_radius=10,
            has_border=False,
            is_right=True,
        )
        self.text_box_component.draw_text_box(
            text_list=["HP"],
            rect_color="black",
            text_size=FontSize.LARGE,
            rect_position=(screen_width / 2 + 10, 70),
            rect_size=(120, 20),
            rect_radius=15,
            has_border=False,
            text_color="white",
            is_center=True,
        )

        # rect life
        self.text_box_component.draw_text_box(
            text_list=["HP"],
            rect_color="black",
            text_size=FontSize.LARGE,
            rect_position=(screen_width / 2 + 140, 100),
            rect_size=(220, 20),
            rect_radius=5,
            has_border=False,
            text_color="yellow",
            text_gap=10,  # TODO: modificar para text_gap_x = 5, text_gap_y=10
        )

        x_life = 178 * atual_boku.atual_life / atual_boku.life

        self.box_component.draw_box(
            rect_color="white",
            rect_position=(screen_width / 2 + 175, 105),
            rect_size=(178, 10),
            rect_radius=0,
            inner_rect_position=(screen_width / 2 + 175, 105),
            inner_rect_size=(x_life, 10),
            has_border=False,
            has_inner_rect=True,
            inner_rect_color="green",
        )

        # other stats
        space_y = 120
        name_list = ["ATTACK", "DEFENSE", "SPEED", "CRIT"]
        stats_list = [
            f"{atual_boku.attack}",
            f"{atual_boku.defense}",
            f"{atual_boku.speed}",
            f"{atual_boku.critical_chance}%",
        ]
        for i in range(4):
            self.text_box_component.draw_text_box(
                text_list=[stats_list[i]],
                rect_color="#E8F0F8",
                text_size=FontSize.EXTRA_LARGE,
                rect_position=(screen_width - 130, space_y),
                rect_size=(100, 40),
                rect_radius=10,
                has_border=False,
                is_right=True,
            )
            self.text_box_component.draw_text_box(
                text_list=[name_list[i]],
                rect_color="black",
                text_size=FontSize.LARGE,
                rect_position=(screen_width / 2 + 10, space_y + 10),
                rect_size=(120, 20),
                rect_radius=15,
                has_border=False,
                text_color="white",
                is_center=True,
            )
            space_y += 60
        self.renderer.draw_text(
            "Chance",
            "white",
            (screen_width / 2 + 70, space_y - 20),
            size=FontSize.MEDIUM,
            is_center=True,
        )

        # parte de baixo / EXP
        self.renderer.draw_rect(
            "#C8D8E8",
            (200, screen_height - 240, screen_width - 230, 100),
            0,
            10,
        )
        self.renderer.draw_text(
            "Exp.  Points",
            "black",
            (240, screen_height - 210),
            size=FontSize.DOUBLE_EXTRA_LARGE,
        )
        self.renderer.draw_text(
            "Next  Lv.",
            "black",
            (240, screen_height - 160),
            size=FontSize.DOUBLE_EXTRA_LARGE,
        )

        self.text_box_component.draw_text_box(
            text_list=["EXP"],
            rect_color="black",
            text_size=FontSize.EXTRA_LARGE,
            rect_position=(10, screen_height - 210),
            rect_size=(200, 20),
            rect_radius=15,
            has_border=False,
            text_color="white",
            is_center=True,
        )

        # valores exp
        self.renderer.draw_rect(
            "#E8F0F8",
            (screen_width - 260, space_y + 10, 230, 80),
        )
        self.text_box_component.draw_text_box(
            text_list=[f"{atual_boku.all_exp}"],
            rect_color="#E8F0F8",
            text_size=FontSize.EXTRA_LARGE,
            rect_position=(screen_width - 260, space_y),
            rect_size=(230, 50),
            rect_radius=10,
            has_border=False,
            text_gap=30,  # TODO: modificar para text_gap_x = 30
            is_right=True,
        )
        self.text_box_component.draw_text_box(
            text_list=[f"{round(atual_boku.up_exp - atual_boku.atual_exp)}"],
            rect_color="#E8F0F8",
            text_size=FontSize.EXTRA_LARGE,
            rect_position=(screen_width - 260, space_y + 50),
            rect_size=(230, 50),
            rect_radius=10,
            has_border=False,
            text_gap=30,  # TODO: modificar para text_gap_x = 30
            is_right=True,
        )

        # divisoria
        self.renderer.draw_rect(  # TODO: modificar para draw_line
            "#E8F0F8",
            (230, screen_height - 189, screen_width - 260, 3),
            0,
            10,
        )
        self.renderer.draw_rect(  # TODO: modificar para draw_line
            "#C8D8E8",
            (screen_width - 260, screen_height - 189, 220, 3),
            0,
            10,
        )
        # rect exp
        self.text_box_component.draw_text_box(
            text_list=["EXP"],
            rect_color="black",
            text_size=FontSize.MEDIUM,
            rect_position=(screen_width - 290, space_y + 100),
            rect_size=(255, 20),
            rect_radius=10,
            has_border=False,
            text_color="yellow",
            text_gap=10,
        )

        self.renderer.draw_rect(
            "white",
            (screen_width - 248, space_y + 103, 208, 14),
            0,
            20,
        )

        x_exp = 195 * atual_boku.atual_exp / atual_boku.up_exp

        self.box_component.draw_box(
            rect_color="#898D91",
            rect_position=(screen_width - 240, space_y + 105),
            rect_size=(195, 10),
            rect_radius=0,
            inner_rect_position=(screen_width - 240, space_y + 105),
            inner_rect_size=(x_exp, 10),
            has_border=False,
            has_inner_rect=True,
            inner_rect_color="blue",
        )

    def draw_know_move(self):
        atual_bokumon = self.boku_local[self.boku_selected]

        # bloco
        self.box_component.draw_box(
            rect_color="#969EAE",
            rect_position=(screen_width / 2 - 1, 49),
            rect_size=(screen_width / 2 + 1, screen_height - 49),
        )

        # moves
        space_y = 70
        for i in range(5):
            if i != 4:
                self.renderer.draw_rect(
                    "#F0F0F8",
                    (screen_width / 2 + 20, space_y, screen_width / 2 - 35, 80),
                    0,
                    10,
                )
                self.renderer.draw_text(
                    f"{atual_bokumon.moves[i][0]}",
                    "black",
                    (screen_width / 2 + 130, space_y + 20),
                    size=FontSize.DOUBLE_EXTRA_LARGE,
                )
                self.renderer.draw_text(
                    f"PP",
                    "black",
                    (screen_width / 2 + 235, space_y + 60),
                    size=FontSize.EXTRA_LARGE,
                )
                self.renderer.draw_text(
                    f"{atual_bokumon.moves_pp[i][0]}/{atual_bokumon.moves_pp[i][1]}",
                    "black",
                    (screen_width / 2 + 270, space_y + 60),
                    size=FontSize.DOUBLE_EXTRA_LARGE,
                )
            else:
                if self.selected_move[0]:
                    self.renderer.draw_text(
                        f"Cancel",
                        "black",
                        (screen_width / 2 + 150, space_y + 40),
                        size=FontSize.DOUBLE_EXTRA_LARGE,
                    )

            if (
                self.selected_move[2][0] == i or self.selected_move[2][1] == i
            ) and self.selected_move[0]:
                color = "red"
                if (self.selected_move[1] and self.selected_move[2][0] == i):
                    color = "blue"

                self.renderer.draw_rect(
                    color,
                    (screen_width / 2 + 20, space_y, screen_width / 2 - 35, 80),
                    3,
                    10,
                )

            space_y += 100

        if self.selected_move[0]:
            text_power = ""
            text_accuracy = ""
            if self.selected_move[2][1] != 4:
                text_power = f"{atual_bokumon.moves[self.selected_move[2][1]][1]}"
                text_accuracy = f"{atual_bokumon.moves[self.selected_move[2][1]][2]}"

            self.text_box_component.draw_text_box(
                text_list=[text_power],
                rect_color="#E8F0F8",
                text_size=FontSize.EXTRA_LARGE,
                rect_position=(160, screen_height / 2 + 90),
                rect_size=(100, 40),
                rect_radius=10,
                has_border=False,
                is_right=True,
            )
            self.text_box_component.draw_text_box(
                text_list=[text_accuracy],
                rect_color="#E8F0F8",
                text_size=FontSize.EXTRA_LARGE,
                rect_position=(160, screen_height / 2 + 140),
                rect_size=(100, 40),
                rect_radius=10,
                has_border=False,
                is_right=True,
            )

            self.text_box_component.draw_text_box(
                text_list=["POWER"],
                rect_color="black",
                text_size=FontSize.LARGE,
                rect_position=(20, screen_height / 2 + 100),
                rect_size=(120, 20),
                rect_radius=15,
                has_border=False,
                text_color="white",
                is_center=True,
            )
            self.text_box_component.draw_text_box(
                text_list=["ACCURACY"],
                rect_color="black",
                text_size=FontSize.LARGE,
                rect_position=(20, screen_height / 2 + 150),
                rect_size=(120, 20),
                rect_radius=15,
                has_border=False,
                text_color="white",
                is_center=True,
            )

    def move_marked(self, move, pos, selected):
        if not selected:
            expect_move = self.selected_move[2][pos] + move
            max = 4 if self.selected_move[0] and not self.selected_move[1] else 3
            if 0 <= expect_move <= max:
                self.selected_move[2][pos] = expect_move
