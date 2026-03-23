import pygame
from settings.settings import ASSETS_PATH, SPRITE_SIZE


class Renderer:
    def __init__(self, display_surface: pygame.Surface) -> None:
        self.display_surface = display_surface

    def load_asset_image(
        self,
        image_name: str,
        extesion: str = "png",
        is_convert: bool = False,
        is_convert_alpha: bool = False,
        is_scale: bool = False,
        scale: tuple = (SPRITE_SIZE, SPRITE_SIZE),
    ) -> pygame.Surface:
        image_path = f"{ASSETS_PATH}/imgs/{image_name}.{extesion}"
        image = pygame.image.load(image_path)

        if is_convert:
            image = image.convert()

        if is_convert_alpha:
            image = image.convert_alpha()

        if is_scale:
            image = self.scale_image(image, scale)

        return image

    def scale_image(self, image: pygame.Surface, scale: tuple) -> pygame.Surface:
        return pygame.transform.scale(image, scale)

    def load_font(
        self, font_name: str, font_size: int, extension: str = "ttf"
    ) -> pygame.font.Font:
        font_path = f"{ASSETS_PATH}/font/{font_name}.{extension}"
        return pygame.font.Font(font_path, font_size)

    def draw_rect(
        self,
        color: (
            str | tuple[int, int, int]
        ),  # TODO: remover tuple dos arquivos, preferir str
        rect: tuple[int, int, int, int],
        width: int = 0,
        border_radius: int = -1,
        border_top_left_radius: int = -1,
        border_top_right_radius: int = -1,
        border_bottom_left_radius: int = -1,
        border_bottom_right_radius: int = -1,
    ) -> pygame.Rect:
        pygame.draw.rect(
            self.display_surface,
            color,
            rect,
            width,
            border_radius,
            border_top_left_radius,
            border_top_right_radius,
            border_bottom_left_radius,
            border_bottom_right_radius,
        )

    def draw_circle(
        self,
        color: str | tuple[int, int, int],
        center: tuple[int, int],
        radius: float,
        width: int = 0,
        draw_top_right: bool = False,
        draw_top_left: bool = False,
        draw_bottom_left: bool = False,
        draw_bottom_right: bool = False,
    ) -> pygame.Rect:
        pygame.draw.circle(
            self.display_surface,
            color,
            center,
            radius,
            width,
            draw_top_right,
            draw_top_left,
            draw_bottom_left,
            draw_bottom_right,
        )

    def blit(self, image: pygame.Surface, rect: tuple[int, int]) -> None:
        self.display_surface.blit(image, rect)

    def blit_text(
        self,
        text: str,
        color: str,
        position: tuple,
        font: pygame.font.Font,
        right: bool = False,
        center: bool = False,
    ) -> None:
        overlay_text = font.render(text, False, color)

        if right:
            overlay_text_rect = overlay_text.get_rect(topright=(position))
        elif center:
            overlay_text_rect = overlay_text.get_rect(center=(position))
        else:
            overlay_text_rect = overlay_text.get_rect(topleft=(position))

        self.display_surface.blit(overlay_text, overlay_text_rect)

    def blit_shadow_text(
        self,
        text: str,
        color: str,
        position: tuple,
        font: pygame.font.Font,
        back_color: str = "black",
        right: bool = False,
        center: bool = False,
    ) -> None:
        TEXT_OFFSET = 2

        self.blit_text(
            text,
            back_color,
            [position[0] + TEXT_OFFSET, position[1] + TEXT_OFFSET],
            font,
            right,
            center,
        )
        self.blit_text(text, color, position, font, right, center)
