import pygame
from settings.settings import ASSETS_PATH, SPRITE_SIZE


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


def blit_text(
    text: str,
    color: str,
    position: tuple,
    font: pygame.font.Font,
    right: bool = False,
    center: bool = False,
) -> None:
    display_surface = pygame.display.get_surface()
    overlay_text = font.render(text, False, color)

    if right:
        overlay_text_rect = overlay_text.get_rect(topright=(position))
    elif center:
        overlay_text_rect = overlay_text.get_rect(center=(position))
    else:
        overlay_text_rect = overlay_text.get_rect(topleft=(position))

    display_surface.blit(overlay_text, overlay_text_rect)


def blit_shadow_text(
    text: str,
    color: str,
    position: tuple,
    font: pygame.font.Font,
    back_color: str = "black",
    right: bool = False,
    center: bool = False,
) -> None:
    TEXT_OFFSET = 2

    blit_text(
        text,
        back_color,
        [position[0] + TEXT_OFFSET, position[1] + TEXT_OFFSET],
        font,
        right,
        center,
    )
    blit_text(text, color, position, font, right, center)
