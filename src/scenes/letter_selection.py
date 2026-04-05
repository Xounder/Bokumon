import pygame
from settings.settings import screen_height, screen_width
from ui import Renderer, FontSize, BoxComponent, TextBoxComponent
from utils.timer import Timer


class LetterSelection:
    def __init__(self, renderer: Renderer):
        self.renderer = renderer
        self.box_component = BoxComponent(self.renderer)
        self.text_box_component = TextBoxComponent(self.renderer)

        self.timer = Timer(0.12)

        self.active = False
        self.activate("Carbink", True)

        self.letter_selection = [
            ["A", "B", "C", "D", "E", "F", "G", "lower"],
            ["H", "I", "J", "K", "L", "M", "N", "BACK"],
            ["O", "P", "Q", "R", "S", "T", ".", "OK"],
            ["U", "V", "W", "X", "Y", "Z", ",", ""],
        ]

    def activate(self, name, first=False):
        if not first:
            self.active = True
        self.name_choosed = ""
        self.selected_button = [0, 0]
        self.letter_lower = False
        self.name_changed = False
        self.real_name = name

    def draw(self):
        self.draw_ballon_text()
        self.draw_buttons()
        self.draw_letters()

    def draw_letters(self):
        space = [0, 0]
        for i in range(4):
            for j in range(7):
                letter = self.letter_selection[i][j]
                letter = letter if not self.letter_lower else letter.lower()
                self.renderer.draw_text(
                    letter,
                    "white",
                    (110 + space[1], screen_height / 2 - 55 + space[0]),
                    size=FontSize.DOUBLE_EXTRA_LARGE,
                    is_center=True,
                    is_shadowed_text=True,
                )
                if self.selected_button[0] == i and self.selected_button[1] == j:
                    self.renderer.draw_rect(
                        "red",
                        (90 + space[1], screen_height / 2 - 75 + space[0], 40, 40),
                        3,
                        15,
                    )
                space[1] += 70
            space[1] = 0
            space[0] += 90

    def draw_ballon_text(self):
        self.renderer.fill_screen("#E0D858")

        self.box_component.draw_box(
            rect_color="#C0B8B0",
            rect_position=(100, 20),
            rect_size=(screen_width - 200, 150),
            rect_radius=15,
            border_color="#8C8C88",
            border_radius=15,
            has_inner_rect=True,
            inner_rect_radius=15,
        )

        self.renderer.draw_text(
            f"{self.real_name}'s nickname?",
            "black",
            (250, 70),
            size=FontSize.DOUBLE_EXTRA_LARGE,
        )

        spaces = "_ _ _ _ _ _ _ _ _ _"
        count_space = spaces[
            (0 if len(self.name_choosed) == 0 else 1) : (
                len(spaces) - len(self.name_choosed) * 2
            )
        ]
        word_modified = self.append_space(self.name_choosed)
        self.renderer.draw_text(
            f"{word_modified}{count_space}",
            "black",
            (250, 130),
            size=FontSize.DOUBLE_EXTRA_LARGE,
        )

    def append_space(self, word):
        new_word = ""
        if len(word) > 0:
            for letter in word:
                new_word += letter + " "
        return new_word

    def draw_buttons(self):
        self.box_component.draw_box(
            rect_color="#98C8E0",
            rect_position=(60, screen_height / 2 - 100),
            rect_size=(screen_width - 250, screen_height / 2 + 70),
            border_color="#6088A0",
        )
        self.box_component.draw_box(
            rect_color="#78A8C0",
            rect_position=(70, screen_height / 2 - 90),
            rect_size=(screen_width - 270, screen_height / 2 + 50),
            border_color="#487088",
        )

        space_y = -50
        text_list = ["lower", "BACK", "OK"]
        for i in range(3):
            color = "#D09870" if i == 0 else "#E0D858"
            color_sel = (
                "red"
                if self.selected_button[0] == i and self.selected_button[1] == 7
                else "black"
            )

            self.text_box_component.draw_text_box(
                text_list=[text_list[i]],
                rect_color="white",
                text_size=FontSize.DOUBLE_EXTRA_LARGE,
                rect_position=(screen_width - 185, screen_height / 2 + space_y),
                rect_size=(130, 50),
                rect_radius=15,
                border_color=color_sel,
                border_radius=15,
                has_inner_rect=True,
                inner_rect_gap=5,
                inner_rect_color=color,
                inner_rect_radius=10,
                is_center=True,
            )

            space_y += 120

    def update(self):
        if self.timer.run:
            self.timer.update()
        self.input()

    def input(self):
        if not self.timer.run:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                self.selected_button[0] -= 1 if self.selected_button[0] > 0 else 0
            elif keys[pygame.K_DOWN]:
                self.selected_button[0] += 1 if self.selected_button[0] < 3 else 0
                if (
                    self.letter_selection[self.selected_button[0]][
                        self.selected_button[1]
                    ]
                    == ""
                ):
                    self.selected_button[0] -= 1
            elif keys[pygame.K_LEFT]:
                if (
                    self.letter_selection[self.selected_button[0]][
                        self.selected_button[1]
                    ]
                    == "OK"
                ):
                    self.selected_button[0] += 1
                self.selected_button[1] -= 1 if self.selected_button[1] > 0 else 0
            elif keys[pygame.K_RIGHT]:
                self.selected_button[1] += 1 if self.selected_button[1] < 7 else 0
                if (
                    self.letter_selection[self.selected_button[0]][
                        self.selected_button[1]
                    ]
                    == ""
                ):
                    self.selected_button[0] -= 1

            if keys[pygame.K_x]:
                if len(self.name_choosed) > 0:
                    self.name_choosed = self.name_choosed[: len(self.name_choosed) - 1]
            elif keys[pygame.K_z]:
                if self.selected_button[1] == 7:
                    if self.selected_button[0] == 0:  # lower
                        self.letter_lower = not self.letter_lower
                    elif self.selected_button[0] == 1:  # back
                        self.name_choosed = self.name_choosed[
                            : len(self.name_choosed) - 1
                        ]
                    elif self.selected_button[0] == 2:
                        self.active = False
                        self.name_changed = True
                elif len(self.name_choosed) < 9:
                    letter = self.letter_selection[self.selected_button[0]][
                        self.selected_button[1]
                    ]
                    self.name_choosed += (
                        letter if not self.letter_lower else letter.lower()
                    )
            self.timer.active()
