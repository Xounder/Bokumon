import pygame
import os
import json
from settings.settings import ASSETS_PATH, SAVE_PATH, SPRITE_SIZE


def blit_text(text, color, pos, font, right=False, center=False):
    display_surface = pygame.display.get_surface()
    overlay_txt = font.render(text, False, color)
    if right:
        overlay_txt_rect = overlay_txt.get_rect(topright=(pos))
    elif center:
        overlay_txt_rect = overlay_txt.get_rect(center=(pos))
    else:
        overlay_txt_rect = overlay_txt.get_rect(topleft=(pos))

    display_surface.blit(overlay_txt, overlay_txt_rect)


def blit_text_shadow(
    text, color, pos, font, back_color="black", right=False, center=False
):
    blit_text(text, back_color, [pos[0] + 2, pos[1] + 2], font, right, center)
    blit_text(text, color, pos, font, right, center)


def load_asset_image(
    image_name: str,
    extesion: str = "png",
    is_convert: bool = False,
    is_convert_alpha: bool = False,
    is_scale: bool = False,
    scale: tuple = (SPRITE_SIZE, SPRITE_SIZE),
) -> pygame.surface.Surface:
    image_path = f"{ASSETS_PATH}/imgs/{image_name}.{extesion}"
    image = pygame.image.load(image_path)

    if is_convert:
        image = image.convert()

    if is_convert_alpha:
        image = image.convert_alpha()

    if is_scale:
        image = scale_image(image, scale)

    return image


def scale_image(image: pygame.surface.Surface, scale: tuple) -> pygame.surface.Surface:
    return pygame.transform.scale(image, scale)


def load_font(
    font_name: str, font_size: int, extension: str = "ttf"
) -> pygame.font.Font:
    font_path = f"{ASSETS_PATH}/font/{font_name}.{extension}"
    return pygame.font.Font(font_path, font_size)


def save_game(player, bag):  # TODO: adicionar tipagens
    #### TODO: Mudar esse método para outro local (analisar melhor local)
    player_bokumons = [_bokumon_to_dict(bokumon) for bokumon in player.bokumons]
    storage_bokumons = [_bokumon_to_dict(bokumon) for bokumon in player.bokumon_storage]

    data = {
        "name": player.name,
        "status": player.previous_status,
        "position": player.position,
        "tickets": player.tickets,
        "bokumons": player_bokumons,
        "bokumonStorage": storage_bokumons,
        "bag": bag.all_items,
    }

    try:
        os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)

        with open(SAVE_PATH, "w") as file:
            json.dump(data, file, indent=4)

    except OSError as e:
        print(f"Erro ao salvar o jogo: {e}")


def _bokumon_to_dict(bokumon):  # TODO: adicionar tipagens
    #### TODO: Mudar esse método para outro local (analisar melhor local)
    return {
        "name": bokumon.name,
        "atualName": bokumon.atual_name,
        "level": bokumon.level,
        "maxLife": bokumon.life,
        "atualLife": bokumon.atual_life,
        "bokuBall": bokumon.ball,
        "status": {
            "attack": bokumon.attack,
            "defense": bokumon.defense,
            "speed": bokumon.speed,
            "criticalChance": bokumon.critical_chance,
            "atualExperience": bokumon.atual_exp,
            "upgradeExperience": bokumon.up_exp,
            "totalExperience": bokumon.all_exp,
        },
        "moves": bokumon.moves,  # TODO:separar em outros atributos
    }


def load_game() -> None:
    #### TODO: Mudar esse método para outro local (analisar melhor local)
    with open(SAVE_PATH, "r") as file:
        return json.loads(file.read())
