import pygame
from settings.settings import ASSETS_PATH, SPRITE_SIZE
from .renderer_types import FontSize


class Renderer:
    def __init__(self, display_surface: pygame.Surface) -> None:
        self.display_surface = display_surface
        self.fonts = self._create_fonts()

    def _get_font_pixels(self, size: FontSize) -> int:
        return {
            FontSize.SMALL: 20,
            FontSize.MEDIUM: 25,
            FontSize.LARGE: 35,
            FontSize.EXTRA_LARGE: 42,
            FontSize.DOUBLE_EXTRA_LARGE: 50,
        }[size]

    def _create_fonts(self) -> dict[FontSize, pygame.font.Font]:
        return {
            size: self._load_font("Pixeltype", self._get_font_pixels(size))
            for size in FontSize
        }

    def _load_font(
        self, font_name: str, font_size: int, extension: str = "ttf"
    ) -> pygame.font.Font:
        font_path = f"{ASSETS_PATH}/font/{font_name}.{extension}"
        return pygame.font.Font(font_path, font_size)

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

    def draw_rect(
        self,
        color: str | tuple[int, int, int],
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

    def draw_text(
        self,
        text: str,
        color: str,
        position: tuple,
        size: FontSize,
        is_shadowed_text: bool = False,
        shadow_color: str = "black",
        is_right: bool = False,
        is_center: bool = False,
    ) -> None:
        if is_shadowed_text:
            TEXT_OFFSET = 2

            self._blit_text(
                text,
                shadow_color,
                (position[0] + TEXT_OFFSET, position[1] + TEXT_OFFSET),
                size,
                is_right,
                is_center,
            )

        self._blit_text(text, color, position, size, is_right, is_center)

    def _blit_text(
        self,
        text: str,
        color: str,
        position: tuple,
        size: FontSize,
        is_right: bool = False,
        is_center: bool = False,
    ) -> None:
        font = self.fonts[size]
        overlay_text = font.render(text, False, color)

        if is_right:
            overlay_text_rect = overlay_text.get_rect(topright=(position))
        elif is_center:
            overlay_text_rect = overlay_text.get_rect(center=(position))
        else:
            overlay_text_rect = overlay_text.get_rect(topleft=(position))

        self.blit(overlay_text, overlay_text_rect)
