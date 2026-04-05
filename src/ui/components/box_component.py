from ui.renderer import Renderer


class BoxComponent:
    def __init__(self, renderer: Renderer) -> None:
        self.renderer = renderer

    def draw_box(
        self,
        rect_color: str,
        rect_position: tuple[int, int],
        rect_size: tuple[int, int],
        inner_rect_position: tuple[int, int] = (),
        inner_rect_size: tuple[int, int] = (),
        rect_radius: int = 3,
        has_border: bool = True,
        border_color: str = "black",
        border_width: int = 3,
        border_radius: int = 0,
        has_inner_rect: bool = False,
        inner_rect_gap: int = 10,
        inner_rect_color: str = "white",
        inner_rect_radius: int = 0,
    ) -> None:
        inner_rect_position, inner_rect_size = self.resolve_content_rect(
            rect_position,
            rect_size,
            has_inner_rect,
            inner_rect_gap,
            inner_rect_position,
            inner_rect_size,
        )

        self.renderer.draw_rect(
            color=rect_color,
            rect=(rect_position, rect_size),
            border_radius=rect_radius,
        )

        if has_border:
            self.renderer.draw_rect(
                color=border_color,
                rect=(rect_position, rect_size),
                width=border_width,
                border_radius=border_radius,
            )

        if has_inner_rect:
            self.renderer.draw_rect(
                color=inner_rect_color,
                rect=(inner_rect_position, inner_rect_size),
                border_radius=inner_rect_radius,
            )

    def resolve_content_rect(
        self,
        rect_position: tuple[int, int],
        rect_size: tuple[int, int],
        has_inner_rect: bool,
        inner_rect_gap: int,
        inner_rect_position: tuple[int, int] = (),
        inner_rect_size: tuple[int, int] = (),
    ) -> tuple[tuple[int, int], tuple[int, int]]:
        if inner_rect_position and inner_rect_size:
            return inner_rect_position, inner_rect_size

        if has_inner_rect:
            inner_rect_position = (
                rect_position[0] + inner_rect_gap,
                rect_position[1] + inner_rect_gap,
            )
            inner_rect_size = (
                rect_size[0] - 2 * inner_rect_gap,
                rect_size[1] - 2 * inner_rect_gap,
            )
            return inner_rect_position, inner_rect_size

        return rect_position, rect_size
