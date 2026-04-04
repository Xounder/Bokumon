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
        is_middle: bool = False,
        is_center: bool = False,
        is_right: bool = False,
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
            is_middle,
            is_center,
            is_right,
        )
        self._draw_selection(
            selected_rect_color,
            rect_position,
            selected_rect_width,
            text_gap,
            text_spacing,
            selected_index,
            selected_rect_size,
        )

    def _draw_selection(
        self,
        color: str,
        position: tuple[int, int],
        width: int,
        text_gap: int,
        spacing: int,
        selected_index: int,
        size: int,
    ) -> None:
        position_x = position[0] + text_gap - 2 * size
        position_y = position[1] + text_gap - size / 2

        self.renderer.draw_rect(
            color,
            (position_x, position_y + spacing * selected_index, size, size),
            width,
        )

    # TODO: verificar como adicionar input/update neste componente
