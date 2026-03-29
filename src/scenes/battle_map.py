import pygame
from random import randint
from settings.settings import *
from settings.bokumons_settings import bokumons_spawn_selector
from utils.timer import Timer
from ui import Renderer, FontSize
from sprites import BokuMon
from .battle_control import BattleControl
from .letter_selection import LetterSelection
from .bag import Bag


class BattleMap:
    def __init__(self, renderer: Renderer, player, view_bokumon, bag: Bag):
        self.renderer = renderer
        self.create_wild = True
        self.timer = Timer(0.12)
        self.msg_timer = Timer(1)
        self.other_msg_timer = Timer(1)
        self.battle_timer = Timer(0.02)

        self.active_timer_once = False

        # classes
        self.battle_control = BattleControl()
        self.view_bokumon = view_bokumon
        self.bag = bag
        self.name_selection = LetterSelection(self.renderer)
        self.set_battle(self.renderer, player, first=True)
        # var useds
        self.pressed_z = False
        self.show_msg = False
        self.selected_move = []
        self.msg_timer_runed = False
        # battle
        self.select = [0, 0]
        self.select_move = [0, 0]
        self.life_decrease_player = 0
        self.life_decrease_wild = 0
        self.bokumon_msg_turn = [False, False]  # wild, player
        # up
        self.gain_exp = False
        self.exp_points = 0
        self.up_bokumon = False
        # only_wild damage turn
        self.switch = False
        self.run = False
        self.sucess = False
        self.run_once_catch = [False, False]
        self.run_once_end_timer = [False, False]
        self.check_trade = False
        self.exp_calc = False
        self.check_catch = [False, False]
        # bokuball
        self.boku_ball_img = {
            "Boku Ball": self.renderer.load_asset_image("boku_ball", is_scale=True),
            "Great Ball": self.renderer.load_asset_image("great_ball", is_scale=True),
            "Ultra Ball": self.renderer.load_asset_image("ultra_ball", is_scale=True),
        }
        # battle background
        self.background = self.renderer.load_asset_image(
            "fight2", is_scale=True, scale=(screen_width, screen_height - 100)
        )

    def create_wild_bokumon(self, renderer: Renderer, player_bokumon):
        boku_name = bokumons_spawn_selector(player_bokumon.level)
        if player_bokumon.level <= 10:
            wild_lvl = abs(player_bokumon.level + randint(-3, 3))
        elif 17 <= player_bokumon.level <= 24:
            wild_lvl = abs(player_bokumon.level + randint(-8, 5))
        else:
            wild_lvl = abs(player_bokumon.level + randint(-15, 6))
        wild_lvl = wild_lvl if wild_lvl > 0 else player_bokumon.level
        self.wild_bokumon = BokuMon(boku_name, renderer, True, wild_lvl)

    def set_battle(self, renderer: Renderer, player, first=False, reset=False):
        if self.create_wild or first or reset:
            # seta o necessário para a batalha
            self.seted = True
            self.show_msg = False
            if not first:
                self.create_wild = False
            self.status = "MSG"
            self.battle_status = "BATTLE"
            self.show_boku = [True, False]
            self.cont_fight = True
            self.selected_choose = False
            self.bag.bag_used[0] = False
            self.player = player
            self.set_player_bokumon()
            if not reset:
                self.create_wild_bokumon(renderer, self.player.atual_bokumon)
            self.battle_control.set_first_bokumon(
                self.wild_bokumon, self.player_bokumon, first
            )
            self.overlay_text()
            # vida dos bokumons
            self.tam_player_life = (
                180 * self.player_bokumon.atual_life / self.player_bokumon.life
            )
            self.tam_wild_life = (
                180 * self.wild_bokumon.atual_life / self.wild_bokumon.life
            )

    def set_player_bokumon(self):
        self.player_bokumon = self.player.atual_bokumon
        if (
            self.player.bokumon_part_battle.count(
                self.player.bokumons.index(self.player_bokumon)
            )
            == 0
        ):
            self.player.bokumon_part_battle.append(
                self.player.bokumons.index(self.player_bokumon)
            )

    def overlay_text(self):
        # overlay
        self.in_battle_text = [
            "What will",
            f"{self.player_bokumon.atual_name.upper()} do?",
            "FIGHT",
            "BAG",
            "BOKUMON",
            "RUN",
        ]
        self.overlay_bokumon = [
            f"{self.wild_bokumon.name.upper()}",
            f"Lv{self.wild_bokumon.level}",
            f"{self.player_bokumon.atual_name.upper()}",
            f"Lv{self.player_bokumon.level}",
            f"{self.player_bokumon.atual_life}/{self.player_bokumon.life}",
        ]
        # move e pp - bokumon do player
        self.bokumon_moves = self.player_bokumon.moves
        self.bokumon_pp = self.player_bokumon.moves_pp

    def set_overlay_text(self, player=True):
        dec_factor = 0.1
        if player:
            self.overlay_bokumon[4] = (
                f"{int(self.player_bokumon.atual_life)}/{self.player_bokumon.life}"
            )
            self.overlay_bokumon[3] = f"Lv{self.player_bokumon.level}"
            # player_life
            if self.life_decrease_player > 1:
                self.life_decrease_player -= dec_factor
                self.player_bokumon.atual_life -= (
                    dec_factor if self.player_bokumon.atual_life >= dec_factor else 0
                )
                self.player_bokumon.atual_life = round(
                    self.player_bokumon.atual_life, 1
                )
                self.life_decrease_player = round(self.life_decrease_player, 1)
            else:
                self.player_bokumon.atual_life = int(self.player_bokumon.atual_life)
                self.life_decrease_player = 0
            self.tam_player_life = (
                180 * self.player_bokumon.atual_life / self.player_bokumon.life
            )
            # move e pp - bokumon do player
            self.bokumon_moves = self.player_bokumon.moves
            self.bokumon_pp = self.player_bokumon.moves_pp
        else:
            # wild_life
            if self.life_decrease_wild > 1:
                self.life_decrease_wild -= dec_factor
                self.wild_bokumon.atual_life -= (
                    dec_factor if self.wild_bokumon.atual_life >= dec_factor else 0
                )
                self.wild_bokumon.atual_life = round(self.wild_bokumon.atual_life, 1)
                self.life_decrease_wild = round(self.life_decrease_wild, 1)
            else:
                self.wild_bokumon.atual_life = int(self.wild_bokumon.atual_life)
                self.life_decrease_wild = 0
            self.tam_wild_life = (
                180 * self.wild_bokumon.atual_life / self.wild_bokumon.life
            )

    def selection_text(self):
        for i, text in enumerate(self.in_battle_text):
            if self.status == "FIGHT" and i < 2:
                # caso esteja na aba fight
                continue
            self.renderer.draw_text(
                text,
                "white",
                overlay_battle_pos[i],
                size=FontSize.DOUBLE_EXTRA_LARGE,
                is_shadowed_text=True,
            )

        # printa na tela os moves do bokumon com suas informações
        if self.status == "FIGHT":
            for i, move in enumerate(self.bokumon_moves):
                self.renderer.draw_text(
                    move[0],
                    "white",
                    bokumon_moves_pos[i],
                    size=FontSize.EXTRA_LARGE,
                    is_shadowed_text=True,
                )
                self.renderer.draw_text(
                    "PP",
                    "white",
                    [bokumon_moves_pos[i][0] - 10, bokumon_moves_pos[i][1] + 25],
                    size=FontSize.SMALL,
                    is_shadowed_text=True,
                )
                self.renderer.draw_text(
                    f"{self.bokumon_pp[i][0]}/{self.bokumon_pp[i][1]}",
                    "white",
                    [bokumon_moves_pos[i][0] + 5, bokumon_moves_pos[i][1] + 25],
                    size=FontSize.MEDIUM,
                    is_shadowed_text=True,
                )
                self.renderer.draw_text(
                    "PW",
                    "white",
                    [bokumon_moves_pos[i][0] + 60, bokumon_moves_pos[i][1] + 25],
                    size=FontSize.SMALL,
                    is_shadowed_text=True,
                )
                self.renderer.draw_text(
                    f"{self.bokumon_moves[i][1]}",
                    "white",
                    [bokumon_moves_pos[i][0] + 78, bokumon_moves_pos[i][1] + 25],
                    size=FontSize.MEDIUM,
                    is_shadowed_text=True,
                )
                self.renderer.draw_text(
                    "ACC",
                    "white",
                    [bokumon_moves_pos[i][0] + 103, bokumon_moves_pos[i][1] + 25],
                    size=FontSize.SMALL,
                    is_shadowed_text=True,
                )
                self.renderer.draw_text(
                    f"{self.bokumon_moves[i][2]}",
                    "white",
                    [bokumon_moves_pos[i][0] + 126, bokumon_moves_pos[i][1] + 25],
                    size=FontSize.MEDIUM,
                    is_shadowed_text=True,
                )
            # botão de seleção
            button_pos = select_move_button_pos[self.select_move[0]][
                self.select_move[1]
            ]
        else:
            button_pos = select_button_pos[self.select[0]][self.select[1]]
        self.renderer.draw_rect("black", (button_pos[0], button_pos[1], 10, 10))

    def draw_boku_ball(self, rect_center, player_boku_ball=True):
        boku_ball = (
            self.player_bokumon.ball if player_boku_ball else self.bag.used_item[0]
        )
        self.boku_ball_rect = self.boku_ball_img[boku_ball].get_rect(
            center=(rect_center)
        )
        self.renderer.blit(self.boku_ball_img[boku_ball], self.boku_ball_rect)

    def draw_overlay(self):
        self.renderer.blit(self.background, (0, 0))
        self.renderer.draw_rect(
            "red",
            (0, screen_height - screen_height / 4.5, screen_width, screen_height / 4.5),
        )
        self.renderer.draw_rect(
            "black",
            (
                0,
                screen_height - screen_height / 4.5,
                screen_width,
                screen_height / 4.5 + 2,
            ),
            5,
        )
        if self.status == "" or self.status == "FIGHT":
            self.renderer.draw_rect(
                "gray",
                (
                    screen_width / 2,
                    screen_height - screen_height / 4.5,
                    screen_width / 2,
                    screen_height / 4.5,
                ),
            )
            self.renderer.draw_rect(
                "black",
                (
                    screen_width / 2,
                    screen_height - screen_height / 4.5,
                    screen_width / 2,
                    screen_height / 4.5,
                ),
                4,
            )
        # printa na tela o conteudo de batalha
        if self.bag.bag_used[0]:
            self.status = "DONT-FIGHT"
        if self.status == "DONT-FIGHT":
            self.player_not_attack()
        if self.status == "" or self.status == "FIGHT":
            self.selection_text()
        else:
            if self.seted:
                # inicio da batalha
                if (
                    not self.pressed_z
                    and not self.msg_timer.run
                    and not self.view_bokumon.switch
                ):
                    self.renderer.draw_text(
                        f"Wild {self.wild_bokumon.name.capitalize()} appeared!",
                        "white",
                        bokumon_moves_pos[0],
                        size=FontSize.EXTRA_LARGE,
                        is_shadowed_text=True,
                    )
                else:
                    if not self.msg_timer.run:
                        self.msg_timer.active()
                        self.show_msg = True
                        # se trocado durante a batalha (não foi derrotado) toma dano
                        if self.view_bokumon.switch:
                            self.view_bokumon.switch = False
                            if not self.view_bokumon.fainted:
                                self.switch = True
                            self.view_bokumon.fainted = False
                            self.check_trade = False
                    self.draw_boku_ball(boku_pos[1])
                    self.renderer.draw_text(
                        f"Go {self.player_bokumon.atual_name}!",
                        "white",
                        bokumon_moves_pos[0],
                        FontSize.EXTRA_LARGE,
                        is_shadowed_text=True,
                    )

                if self.show_msg and not self.msg_timer.run:
                    self.seted = False
                    if not self.switch:
                        self.status = ""
                    self.show_boku[1] = True
            else:
                if self.switch:
                    # se trocou toma dano
                    self.switch = False
                    self.status = "SWITCH"
                    self.bokumon_msg_turn[0] = True
                    self.battle_control.only_wild_attack_round()
                    self.life_decrease_player = self.battle_control.player_damage
                    self.msg_timer.active()
                    self.in_battle_message()

                if self.bokumon_msg_turn[0] or self.bokumon_msg_turn[1]:
                    if not self.msg_timer.run and not self.msg_timer_runed:
                        self.msg_timer.active()
                        self.msg_timer_runed = True
                    self.in_battle_message()

                if self.battle_control.end_battle and self.battle_status == "END":
                    self.end_battle()

        self.bokumons_info()

    def bokumons_info(self):
        # player bokumon info
        self.renderer.draw_rect(
            "purple",
            (screen_width / 2 + 60, screen_height / 2 + 30, 300, 120),
            0,
            5,
        )
        self.renderer.draw_rect(
            "black",
            (screen_width / 2 + 60, screen_height / 2 + 30, 300, 125),
            3,
            5,
        )
        # exp bar
        self.renderer.draw_rect(
            "black",
            (screen_width / 2 + 60, screen_height - screen_height / 4.5 - 20, 300, 20),
            border_radius=5,
        )
        self.renderer.draw_rect(
            "white",
            (screen_width / 2 + 110, screen_height - screen_height / 4.5 - 12, 240, 5),
        )
        tam_x_exp = 240 * self.player_bokumon.atual_exp / self.player_bokumon.up_exp
        self.renderer.draw_rect(
            "blue",
            (
                screen_width / 2 + 110,
                screen_height - screen_height / 4.5 - 12,
                tam_x_exp,
                5,
            ),
        )
        self.renderer.draw_text(
            "EXP",
            "white",
            (screen_width / 2 + 70, screen_height - screen_height / 4.5 - 15),
            size=FontSize.MEDIUM,
            is_shadowed_text=True,
        )
        # life bar
        self.renderer.draw_rect(
            "black",
            (screen_width / 2 + 120, screen_height - screen_height / 2 + 80, 220, 26),
            0,
            5,
        )
        self.renderer.draw_rect(
            "green",
            (
                screen_width / 2 + 155,
                screen_height - screen_height / 2 + 85,
                self.tam_player_life,
                16,
            ),
        )
        self.renderer.draw_text(
            "HP",
            "red",
            (screen_width / 2 + 125, screen_height - screen_height / 2 + 85),
            size=FontSize.LARGE,
            is_shadowed_text=True,
        )

        # wild bokumon info
        self.renderer.draw_rect("purple", (30, 50, 300, 100), 0, 10)
        self.renderer.draw_rect("black", (30, 50, 300, 100), 3, 10)
        # life bar
        self.renderer.draw_rect("black", (90, 100, 220, 26), 0, 5)
        self.renderer.draw_rect("green", (125, 105, self.tam_wild_life, 16))
        self.renderer.draw_text(
            "HP", "red", (95, 105), size=FontSize.LARGE, is_shadowed_text=True
        )

        # info wild and player bokumon
        for i, text in enumerate(self.overlay_bokumon):
            self.renderer.draw_text(
                text,
                "white",
                overlay_bokumon_pos[i],
                size=FontSize.EXTRA_LARGE,
                is_shadowed_text=True,
            )

    def draw(self):
        if self.view_bokumon.active:
            self.view_bokumon.draw()
        elif self.bag.active:
            self.bag.draw()
        elif self.name_selection.active:
            self.name_selection.draw()
        else:
            self.draw_overlay()
            if self.show_boku[0] and not self.battle_control.catch_bokumon:
                self.wild_bokumon.draw(boku_pos[0])
            if self.show_boku[1]:
                self.player_bokumon.draw(boku_pos[1])
            self.up_info()

    def update(self):
        if self.view_bokumon.active:
            self.active_timer_once = True
            self.view_bokumon.update()
        elif self.bag.active:
            self.bag.update()
            self.active_timer_once = True
        elif self.name_selection.active:
            self.name_selection.update()
        else:
            # caso haja a troca de bokumons no meio da luta
            if self.active_timer_once:
                self.timer.active()
                self.active_timer_once = False
                self.player_bokumon.atual_life = int(self.player_bokumon.atual_life)
                self.set_overlay_text()
            if self.view_bokumon.switch:
                self.set_battle(self.renderer, self.player, reset=True)
                self.select_move = [0, 0]
            if self.name_selection.name_changed:
                if self.name_selection.name_choosed != "":
                    self.wild_bokumon.atual_name = self.name_selection.name_choosed
                self.name_selection.name_changed = False
                self.change_map_catch()
            if self.battle_status == "END":
                if self.battle_control.winner == "wild":
                    self.show_boku[1] = False
                else:
                    self.show_boku[0] = False
            else:
                self.show_boku[0] = True

            self.set_battle(self.renderer, self.player)
            if self.msg_timer.run:
                self.msg_timer.update()
            if self.other_msg_timer.run:
                self.other_msg_timer.update()
            if self.timer.run:
                self.timer.update()
            self.input()

        """if self.player_bokumon.atual_life < 1 or self.wild_bokumon.atual_life < 1 and not self.run_once_end_timer[0]:
            if not self.player.bokumon_alive():
                self.status = 'MSG'
                self.other_msg_timer.active()
                self.run_once_end_timer[0] = True
                self.battle_control.end_battle = True"""

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.timer.run:
            if self.status == "":
                self.select_change(self.select, keys)
            elif self.status == "FIGHT":
                self.select_change(self.select_move, keys)

            if keys[pygame.K_z]:
                if self.seted or self.status == "MSG" or self.status == "DONT-FIGHT":
                    self.pressed_z = True
                elif self.status == "FIGHT":
                    self.player_bokumon.atual_life = int(self.player_bokumon.atual_life)
                    self.wild_bokumon.atual_life = int(self.wild_bokumon.atual_life)
                    self.bokumon_msg_turn = [True, True]

                    if self.select_move == [0, 0]:
                        i = 0
                    elif self.select_move == [0, 1]:
                        i = 1
                    elif self.select_move == [1, 0]:
                        i = 2
                    elif self.select_move == [1, 1]:
                        i = 3

                    if self.set_selected_move(i):
                        self.battle_control.attack_round(self.selected_move)
                        self.life_decrease_wild = self.battle_control.wild_damage
                        self.life_decrease_player = self.battle_control.player_damage
                        self.status = "MSG"
                else:
                    if self.select == [0, 0]:
                        self.status = "FIGHT"
                    elif self.select == [0, 1]:
                        # bag
                        self.bag.active = True
                        self.bag.seted = False
                        self.bag.in_battle = True
                        self.bag.timer.active()
                    elif self.select == [1, 0]:
                        if self.status != "SWITCH":
                            # aba bokumon
                            self.view_bokumon.active = True
                            self.view_bokumon.seted = False
                            self.view_bokumon.in_battle = True
                            self.view_bokumon.timer.active()
                    elif self.select == [1, 1]:
                        # verifica a chance de fugir
                        self.status = "DONT-FIGHT"
                        self.other_msg_timer.active()
                        self.run = True

            elif keys[pygame.K_x]:
                if self.status == "FIGHT":
                    self.status = ""
                    self.select_move = [0, 0]
            else:
                self.pressed_z = False
            self.timer.active()

    def set_selected_move(self, pos):
        if self.bokumon_pp[pos][0] > 0:
            self.selected_move = self.player_bokumon.moves[pos]
            return True
        return False

    def select_change(self, select, keys):
        # modifica o botão de seleção
        if select[0] == 1:
            if keys[pygame.K_UP]:
                select[0] = 0
        elif select[0] == 0:
            if keys[pygame.K_DOWN]:
                select[0] = 1

        if select[1] == 1:
            if keys[pygame.K_LEFT]:
                select[1] = 0
        elif select[1] == 0:
            if keys[pygame.K_RIGHT]:
                select[1] = 1

    def in_battle_message(self):
        if (
            self.battle_status != "END"
            and self.status != "DONT-FIGHT"
            and self.status != "SWITCH"
        ):
            self.attack_message()
        elif self.status == "DONT-FIGHT" or self.status == "SWITCH":
            self.only_attack_wild()

    def attack_message(self):
        if self.battle_control.first_turn == "wild":
            if self.battle_control.critical[0]:
                self.critical_message(0)
            elif self.bokumon_msg_turn[0]:
                self.blit_attack_text(player=False)
            elif self.battle_control.critical[1]:
                self.critical_message(1)
            else:
                self.blit_attack_text(player=True, end=True)
        else:
            if self.battle_control.critical[1]:
                self.critical_message(1)
            elif self.bokumon_msg_turn[1]:
                self.blit_attack_text(player=True)
            elif self.battle_control.critical[0]:
                self.critical_message(0)
            else:
                self.blit_attack_text(player=False, end=True)

        if (
            self.player_bokumon.atual_life < 1 or self.wild_bokumon.atual_life < 1
        ) and (self.life_decrease_wild < 1 and self.life_decrease_player < 1):
            self.battle_status = "END"

    def blit_attack_text(self, player, end=False, only_wild=False):
        if player:
            if not self.battle_control.miss_attack[1]:
                self.renderer.draw_text(
                    f"{self.player_bokumon.atual_name} used ",
                    "white",
                    bokumon_moves_pos[0],
                    size=FontSize.EXTRA_LARGE,
                    is_shadowed_text=True,
                )
                self.renderer.draw_text(
                    f"{self.selected_move[0]}!",
                    "white",
                    bokumon_moves_pos[2],
                    size=FontSize.EXTRA_LARGE,
                    is_shadowed_text=True,
                )
                # redução da vida do wild
                self.set_overlay_text(player=False)
            else:
                self.renderer.draw_text(
                    f"{self.player_bokumon.atual_name} missed!",
                    "white",
                    bokumon_moves_pos[0],
                    size=FontSize.EXTRA_LARGE,
                    is_shadowed_text=True,
                )

            if not self.msg_timer.run and self.life_decrease_wild < 1:
                self.bokumon_msg_turn[1] = False
                self.battle_control.miss_attack[1] = False
                if end:
                    self.status = ""
                    self.msg_timer_runed = False
                else:
                    self.msg_timer.active()
        else:
            if not self.battle_control.miss_attack[0]:
                self.renderer.draw_text(
                    f"Wild {self.wild_bokumon.name.capitalize()} used ",
                    "white",
                    bokumon_moves_pos[0],
                    size=FontSize.EXTRA_LARGE,
                    is_shadowed_text=True,
                )
                self.renderer.draw_text(
                    f"{self.battle_control.wild_selected_move[0]}!",
                    "white",
                    bokumon_moves_pos[2],
                    size=FontSize.EXTRA_LARGE,
                    is_shadowed_text=True,
                )
                # redução da vida do player
                self.set_overlay_text()
            else:
                self.renderer.draw_text(
                    f"Wild {self.wild_bokumon.name.capitalize()} missed!",
                    "white",
                    bokumon_moves_pos[0],
                    size=FontSize.EXTRA_LARGE,
                    is_shadowed_text=True,
                )

            if not self.msg_timer.run and self.life_decrease_player < 1:
                self.battle_control.miss_attack[0] = False
                if not only_wild:
                    self.bokumon_msg_turn[0] = False
                    if end:
                        self.status = ""
                        self.msg_timer_runed = False
                    else:
                        self.msg_timer.active()
                else:
                    self.status = ""
                    if not self.battle_control.end_battle:
                        self.bokumon_msg_turn[0] = False
                    else:
                        self.status = "MSG"
                        self.battle_status = "END"
                        self.msg_timer.active()
                        self.select = [0, 0]

    def critical_message(self, i):
        if self.battle_control.critical[i]:
            self.renderer.draw_text(
                "A critical hit!",
                "white",
                bokumon_moves_pos[0],
                size=FontSize.EXTRA_LARGE,
                is_shadowed_text=True,
            )
            if not self.msg_timer.run:
                self.battle_control.critical[i] = False
                self.msg_timer.active()

    def only_attack_wild(self):
        if self.battle_control.critical[0]:
            self.critical_message(0)
        elif self.bokumon_msg_turn[0]:
            self.blit_attack_text(player=False, only_wild=True)

    def player_not_attack(self):
        if not self.selected_choose:
            if self.run:
                self.sucess = True if self.battle_control.run_chance() else False
            elif self.bag.bag_used[0]:
                self.sucess = (
                    True if self.bag.used_item[0].count("Potion") == 0 else False
                )
                if self.bag.used_item[0].count("Ball") == 1:
                    self.battle_control.catch_bokumon_chance(self.bag.used_item[1])
                    if self.battle_control.catch_bokumon:
                        self.player.catch_bokumon(self.wild_bokumon)
                    self.other_msg_timer.active()

            elif self.switch:
                self.sucess = True if self.status == "SWITCH" else False
            self.selected_choose = True

        if not self.bokumon_msg_turn[0]:
            if self.other_msg_timer.run:
                if self.run:
                    self.run_message(self.sucess)
                elif self.switch:
                    pass
                elif self.bag.bag_used[0]:
                    self.catch_message(self.battle_control.catch_bokumon)
            else:
                if self.sucess:
                    if self.run:
                        self.run = False
                        self.change_map()
                    elif self.switch:
                        pass
                    elif self.bag.bag_used[0]:
                        if self.bag.used_item[0].count("Ball") == 1:
                            self.catch_message(self.battle_control.catch_bokumon)
                        elif self.bag.used_item[0].count("Potion") == 1:
                            pass
                else:
                    self.bokumon_msg_turn[0] = True
                    self.battle_control.only_wild_attack_round()
                    self.life_decrease_player = self.battle_control.player_damage
                    self.msg_timer.active()
        else:
            self.selected_choose = False
            self.bag.bag_used[0] = False
            self.in_battle_message()

    def run_message(self, run):
        if run:
            self.renderer.draw_text(
                "Got away safely!",
                "white",
                bokumon_moves_pos[0],
                size=FontSize.EXTRA_LARGE,
                is_shadowed_text=True,
            )
        else:
            self.renderer.draw_text(
                "Can't escape!",
                "white",
                bokumon_moves_pos[0],
                size=FontSize.EXTRA_LARGE,
                is_shadowed_text=True,
            )

    def catch_message(self, catch):
        if catch:
            if self.other_msg_timer.run and not self.run_once_catch[0]:
                self.renderer.draw_text(
                    "3...2...1!",
                    "white",
                    bokumon_moves_pos[0],
                    size=FontSize.EXTRA_LARGE,
                    is_shadowed_text=True,
                )
                self.draw_boku_ball(boku_pos[0], player_boku_ball=False)
                self.msg_timer.active()
            else:
                if self.msg_timer.run and not self.run_once_catch[1]:
                    self.renderer.draw_text(
                        f"Gotcha {self.wild_bokumon.name.capitalize()} was caught!",
                        "white",
                        bokumon_moves_pos[0],
                        size=FontSize.EXTRA_LARGE,
                        is_shadowed_text=True,
                    )
                    self.draw_boku_ball(boku_pos[0], player_boku_ball=False)
                    self.wild_bokumon.ball = self.bag.used_item[0]
                else:
                    self.draw_boku_ball(boku_pos[0], player_boku_ball=False)
                    self.run_once_catch = [True, True]
                    if (
                        len(self.player.bokumon_part_battle) > 0 or self.gain_exp > 0
                    ) and not self.check_catch[0]:
                        self.bokumon_exp_earned(self.player.bokumon_part_battle[0])
                        if len(self.player.bokumon_part_battle) == 1 and self.pressed_z:
                            self.check_catch[0] = True
                            self.timer.active()
                            self.pressed_z = False
                    else:
                        self.renderer.draw_text(
                            "Change name of bokumon?",
                            "white",
                            bokumon_moves_pos[0],
                            size=FontSize.EXTRA_LARGE,
                            is_shadowed_text=True,
                        )
                        self.blit_select_cont_fight()

                        if self.pressed_z and not self.check_catch[1]:
                            self.check_catch[1] = True
                            if not self.cont_fight:
                                self.change_map_catch()
                            else:
                                self.name_selection.activate(self.wild_bokumon.name)

        else:
            if self.other_msg_timer.run:
                txt = (
                    "3..." if self.battle_control.ball_shake_times == 1 else "3...2..."
                )
                self.renderer.draw_text(
                    txt,
                    "white",
                    bokumon_moves_pos[0],
                    size=FontSize.EXTRA_LARGE,
                    is_shadowed_text=True,
                )
                self.msg_timer.active()
                self.show_boku[0] = False
                self.draw_boku_ball(boku_pos[0], player_boku_ball=False)
            else:
                self.renderer.draw_text(
                    f"Aww! {self.wild_bokumon.name.capitalize()} was not caught!",
                    "white",
                    bokumon_moves_pos[0],
                    size=FontSize.EXTRA_LARGE,
                    is_shadowed_text=True,
                )
                self.show_boku[0] = True
                if self.pressed_z:
                    self.sucess = False

    def end_battle(self):
        if self.status != "DONT-FIGHT" and not self.run_once_end_timer[0]:
            self.status = "MSG"
            self.other_msg_timer.active()
            self.run_once_end_timer[0] = True

        if self.battle_control.winner == "wild":
            if self.other_msg_timer.run and not self.run_once_end_timer[1]:
                self.renderer.draw_text(
                    f"{self.player_bokumon.atual_name} ",
                    "white",
                    bokumon_moves_pos[0],
                    size=FontSize.EXTRA_LARGE,
                    is_shadowed_text=True,
                )
                self.renderer.draw_text(
                    "fainted!",
                    "white",
                    bokumon_moves_pos[2],
                    size=FontSize.EXTRA_LARGE,
                    is_shadowed_text=True,
                )
            else:
                self.run_once_end_timer[1] = True
                if not self.player.bokumon_alive():
                    self.renderer.draw_text(
                        "You've Lost",
                        "white",
                        bokumon_moves_pos[0],
                        size=FontSize.EXTRA_LARGE,
                        is_shadowed_text=True,
                    )
                    if self.pressed_z:
                        self.change_map()
                else:
                    self.renderer.draw_text(
                        "Use next bokumon?",
                        "white",
                        bokumon_moves_pos[0],
                        size=FontSize.EXTRA_LARGE,
                        is_shadowed_text=True,
                    )
                    self.blit_select_cont_fight()

                    if self.pressed_z and not self.check_trade:
                        self.check_trade = True
                        if not self.cont_fight:
                            self.view_bokumon.switch = False
                            self.change_map()
                        else:
                            self.battle_status = "BATTLE"
                            self.view_bokumon.switch = True
                            self.view_bokumon.active = True
                            self.view_bokumon.fainted = True
                            self.view_bokumon.seted = False

        elif self.battle_control.winner == "player":
            if self.other_msg_timer.run and not self.run_once_end_timer[1]:
                self.renderer.draw_text(
                    f"Wild {self.wild_bokumon.name.capitalize()} ",
                    "white",
                    bokumon_moves_pos[0],
                    size=FontSize.EXTRA_LARGE,
                    is_shadowed_text=True,
                )
                self.renderer.draw_text(
                    "fainted!",
                    "white",
                    bokumon_moves_pos[2],
                    size=FontSize.EXTRA_LARGE,
                    is_shadowed_text=True,
                )
            else:
                self.run_once_end_timer[1] = True
                if (
                    not self.pressed_z
                    or len(self.player.bokumon_part_battle) > 1
                    or self.gain_exp > 0
                ):
                    self.bokumon_exp_earned(self.player.bokumon_part_battle[0])
                else:
                    self.change_map()

    def change_map(self):
        self.player_bokumon.atual_life = int(self.player_bokumon.atual_life)
        self.player.battle = False
        self.create_wild = True
        self.select = [0, 0]
        self.select_move = [0, 0]
        self.run_once_end_timer = [False, False]
        self.exp_calc = False
        self.check_trade = False
        self.player.reset_bokumons_position()

    def change_map_catch(self):
        self.run_once_catch = [False, False]
        self.selected_choose = False
        self.bag.bag_used[0] = False
        self.battle_control.catch_bokumon = False
        self.draw_boku_ball(boku_pos[0], player_boku_ball=False)
        self.check_catch = [False, False]
        self.change_map()

    def up_info(self):
        if self.up_bokumon:
            if self.other_msg_timer.run:
                ups = [
                    "Life ",
                    f"+{self.player_bokumon.atrib_ups[0]}",
                    "Attack ",
                    f"+{self.player_bokumon.atrib_ups[1]}",
                    "Defense ",
                    f"+{self.player_bokumon.atrib_ups[2]}",
                    "Speed ",
                    f"+{self.player_bokumon.atrib_ups[3]}",
                    "Crit.Chance ",
                    f"+{self.player_bokumon.atrib_ups[4]}",
                ]
            else:
                ups = [
                    "Life ",
                    f"{self.player_bokumon.life}",
                    "Attack ",
                    f"{self.player_bokumon.attack}",
                    "Defense ",
                    f"{self.player_bokumon.defense}",
                    "Speed ",
                    f"{self.player_bokumon.speed}",
                    "Crit.Chance ",
                    f"{self.player_bokumon.critical_chance}",
                ]

            self.renderer.draw_rect(
                "gray",
                (screen_width / 2 + 120, screen_height / 2 - 200, 220, 220),
            )
            self.renderer.draw_rect(
                "black",
                (screen_width / 2 + 120, screen_height / 2 - 200, 220, 220),
                3,
            )
            for i in range(0, len(ups), 2):
                self.renderer.draw_text(
                    ups[i],
                    "black",
                    (screen_width / 2 + 149, screen_height / 2 - 180 + (20 * i)),
                    size=FontSize.MEDIUM,
                    is_shadowed_text=True,
                    shadow_color="white",
                )
                self.renderer.draw_text(
                    ups[i + 1],
                    "black",
                    (screen_width / 2 + 278, screen_height / 2 - 180 + (20 * i)),
                    size=FontSize.MEDIUM,
                    is_shadowed_text=True,
                    shadow_color="white",
                )

            if not self.msg_timer.run and self.up_bokumon:
                if self.pressed_z:
                    self.up_bokumon = False

    def bokumon_exp_earned(self, boku):
        if not self.exp_calc:
            self.gain_exp = self.battle_control.get_exp_points()
            self.exp_points = self.gain_exp
            self.exp_calc = True
            self.player.tickets += 1
            self.player.del_bokumon_dont_part()

        self.renderer.draw_text(
            f"{self.player.bokumons[boku].atual_name} gained ",
            "white",
            bokumon_moves_pos[0],
            size=FontSize.EXTRA_LARGE,
            is_shadowed_text=True,
        )
        self.renderer.draw_text(
            f"{round(self.exp_points)} Exp.Points!",
            "white",
            bokumon_moves_pos[2],
            size=FontSize.EXTRA_LARGE,
            is_shadowed_text=True,
        )
        if self.gain_exp > 0 and not self.up_bokumon:
            self.gain_exp -= 0.5
            self.player.bokumons[boku].atual_exp += 0.5
            if self.player.bokumons[boku].upgrade():
                self.set_overlay_text()
                self.other_msg_timer.active()
                self.up_bokumon = True

        if (
            self.gain_exp <= 0
            and len(self.player.bokumon_part_battle) > 1
            and not self.up_bokumon
        ):
            self.player.bokumon_part_battle.pop(0)
            self.gain_exp = self.exp_points

    def blit_select_cont_fight(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            self.cont_fight = True
            pos = 0
        elif key[pygame.K_DOWN]:
            self.cont_fight = False
            pos = 1
        else:
            if self.cont_fight:
                pos = 0
            else:
                pos = 1
        self.renderer.draw_rect(
            "#00008B",
            (
                screen_width - 120,
                screen_height - screen_height / 4.5,
                120,
                screen_height / 4.5,
            ),
        )
        self.renderer.draw_rect(
            "black",
            (
                screen_width - 120,
                screen_height - screen_height / 4.5,
                120,
                screen_height / 4.5,
            ),
            5,
        )
        self.renderer.draw_rect(
            "black",
            (select_cont_fight[pos][0], select_cont_fight[pos][1], 10, 10),
        )
        self.renderer.draw_text(
            "Yes",
            "white",
            [screen_width - 85, screen_height - screen_height / 4.5 + 30],
            size=FontSize.DOUBLE_EXTRA_LARGE,
            is_shadowed_text=True,
        )
        self.renderer.draw_text(
            "No",
            "white",
            [screen_width - 85, screen_height - screen_height / 4.5 + 80],
            size=FontSize.DOUBLE_EXTRA_LARGE,
            is_shadowed_text=True,
        )
