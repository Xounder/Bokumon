from ui.renderer import Renderer
from ui.renderer_types import FontSize
from ui.components.box_component import BoxComponent


class TextBoxComponent:
    def __init__(self, renderer: Renderer) -> None:
        self.renderer = renderer
        self.box_component = BoxComponent(self.renderer)

    def draw_text_box(
        self,
        text_list: list[str],
        rect_color: str,
        text_size: FontSize,
        rect_position: tuple[int, int],
        rect_size: tuple[int, int],
        rect_radius: int = 3,
        has_border: bool = True,
        border_color: str = "black",
        border_width: int = 3,
        border_radius: int = 0,
        has_inner_rect: bool = False,
        inner_rect_position: tuple[int, int] = (),
        inner_rect_size: tuple[int, int] = (),
        inner_rect_gap: int = 10,
        inner_rect_color: str = "white",
        inner_rect_radius: int = 0,
        text_color: str = "black",
        text_gap: int = 20,
        text_spacing: int | None = None,
        is_shadowed_text: bool = False,
        shadow_color: str = "black",
        is_middle: bool = False,
        is_center: bool = False,
        is_right: bool = False,
    ) -> None:
        last_rect_position, last_rect_size = self.box_component.resolve_content_rect(
            rect_position,
            rect_size,
            has_inner_rect,
            inner_rect_gap,
            inner_rect_position,
            inner_rect_size,
        )

        self.box_component.draw_box(
            rect_color=rect_color,
            rect_position=rect_position,
            rect_size=rect_size,
            inner_rect_position=last_rect_position,
            inner_rect_size=last_rect_size,
            rect_radius=rect_radius,
            has_border=has_border,
            border_color=border_color,
            border_width=border_width,
            border_radius=border_radius,
            has_inner_rect=has_inner_rect,
            inner_rect_color=inner_rect_color,
            inner_rect_radius=inner_rect_radius,
        )
        self._draw_text_list(
            text_list,
            text_color,
            text_size,
            last_rect_position,
            last_rect_size,
            text_gap,
            text_spacing,
            is_shadowed_text,
            shadow_color,
            is_middle,
            is_center,
            is_right,
        )

    def _draw_text_list(
        self,
        text_list: list[str],
        text_color: str,
        text_size: FontSize,
        rect_position: tuple[int, int],
        rect_size: tuple[int, int],
        text_gap: int,  # TODO: dividir em gap horizontal e vertical / modificar nome
        text_spacing: int | None,
        is_shadowed_text: bool,
        shadow_color: str,
        is_middle: bool,  # TODO: modificar para enum Alignment
        is_center: bool,  # TODO: modificar para enum Alignment
        is_right: bool,  # TODO: modificar para enum Alignment
    ) -> None:
        spacing = text_spacing or self._get_text_spacing(text_size)

        text_position = self.resolve_text_position(
            rect_position=rect_position,
            rect_size=rect_size,
            text_gap=text_gap,
            is_calculate_resolve_content_rect=False,
            is_middle=is_middle,
            is_center=is_center,
            is_right=is_right,
        )

        for index, text in enumerate(text_list):
            self._draw_text(
                text,
                text_color,
                text_size,
                (text_position[0], text_position[1] + spacing * index),
                is_shadowed_text,
                shadow_color,
                is_center,
                is_right,
            )

    def resolve_text_position(
        self,
        rect_position: tuple[int, int],
        rect_size: tuple[int, int],
        text_gap: int,
        is_calculate_resolve_content_rect: bool,
        has_inner_rect: bool = False,
        inner_rect_gap: int = 10,
        inner_rect_position: tuple[int, int] = (),
        inner_rect_size: tuple[int, int] = (),
        is_middle: bool = False,
        is_center: bool = False,
        is_right: bool = False,
    ) -> tuple[tuple[int, int], tuple[int, int]]:
        last_rect_position = rect_position

        if is_calculate_resolve_content_rect:
            last_rect_position, _ = self.box_component.resolve_content_rect(
                rect_position,
                rect_size,
                has_inner_rect,
                inner_rect_gap,
                inner_rect_position,
                inner_rect_size,
            )

        text_position = [
            last_rect_position[0] + text_gap,
            last_rect_position[1] + text_gap,
        ]

        if is_middle:
            text_position[1] = rect_position[1] + rect_size[1] / 2
        elif is_center:
            text_position[0] = rect_position[0] + rect_size[0] / 2
            text_position[1] = rect_position[1] + rect_size[1] / 2
        elif is_right:
            text_position[0] = rect_position[0] + rect_size[0] - text_gap / 2

        return text_position

    def _draw_text(
        self,
        text: str,
        text_color: str,
        text_size: FontSize,
        rect_position: tuple[int, int],
        is_shadowed_text: bool,
        shadow_color: str,
        is_center: bool,
        is_right: bool,
    ) -> None:
        self.renderer.draw_text(
            text=text,
            color=text_color,
            position=rect_position,
            size=text_size,
            is_shadowed_text=is_shadowed_text,
            shadow_color=shadow_color,
            is_center=is_center,
            is_right=is_right,
        )

    def _get_text_spacing(self, size: FontSize) -> int:
        match size:
            case FontSize.SMALL | FontSize.MEDIUM | FontSize.LARGE:
                return 35
            case FontSize.EXTRA_LARGE:
                return 40
            case FontSize.DOUBLE_EXTRA_LARGE:
                return 45

    # TODO: verificar como adicionar input/update neste componente
