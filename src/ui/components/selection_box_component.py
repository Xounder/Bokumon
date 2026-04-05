from ui.renderer import Renderer
from ui.renderer_types import FontSize
from .text_box_component import TextBoxComponent


class SelectionBoxComponent:
    def __init__(self, renderer: Renderer) -> None:
        self.renderer = renderer
        self.text_box_component = TextBoxComponent(self.renderer)

    def draw_selection_box(
        self,
        text_list: list[str],
        rect_color: str,
        text_size: FontSize,
        rect_position: tuple[int, int],
        rect_size: tuple[int, int],
        selected_index: int,
        selected_rect_color: str = "black",
        selected_rect_width: int = 4,
        selected_rect_size: int = 10,
        selected_rect_radius: int = 0,
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
        text_spacing: int = 35,
        is_shadowed_text: bool = False,
        shadow_color: str = "black",
    ) -> None:
        self.text_box_component.draw_text_box(
            text_list,
            rect_color,
            text_size,
            rect_position,
            rect_size,
            rect_radius,
            has_border,
            border_color,
            border_width,
            border_radius,
            has_inner_rect,
            inner_rect_position,
            inner_rect_size,
            inner_rect_gap,
            inner_rect_color,
            inner_rect_radius,
            text_color,
            text_gap,
            text_spacing,
            is_shadowed_text,
            shadow_color,
        )

        text_position = self.text_box_component.resolve_text_position(
            rect_position=rect_position,
            rect_size=rect_size,
            text_gap=text_gap,
            is_calculate_resolve_content_rect=True,
            has_inner_rect=has_inner_rect,
            inner_rect_gap=inner_rect_gap,
            inner_rect_position=inner_rect_position,
            inner_rect_size=inner_rect_size,
        )

        self._draw_selection(
            selected_rect_color,
            text_position,
            selected_rect_width,
            text_spacing,
            selected_index,
            selected_rect_size,
            selected_rect_radius,
        )

    def _draw_selection(
        self,
        color: str,
        position: tuple[int, int],
        width: int,
        spacing: int,
        selected_index: int,
        size: int,
        border_radius: int,
    ) -> None:
        position_x = position[0] - 2 * size
        position_y = position[1] - size / 2

        self.renderer.draw_rect(
            color,
            (position_x, position_y + spacing * selected_index, size, size),
            width,
            border_radius,
        )

    # TODO: verificar como adicionar input/update neste componente
