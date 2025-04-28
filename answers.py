import pyray
from item import Item
from typing import List

class Answer:
    def __init__(self, label: str, x: int, y: int, width: int = 120, height: int = 60):
        self.label = label
        self.rect = pyray.Rectangle(x, y, width, height)
        self.font_size = 20
        self.bg_color = pyray.DARKGRAY
        self.border_color = pyray.WHITE
        self.text_color = pyray.YELLOW
        self.active = True  # If you want to later enable/disable it visually

    def update(self, items: List[Item]):
        for item in items:
            item_rect = item.get_rect()
            if pyray.check_collision_recs(item_rect, self.rect):
                item.in_answer_box = True

    def _wrap_text(self, text: str, font_size: int, max_width: int) -> list[str]:
        """Split text into lines so that no line is wider than max_width."""
        words = text.split()
        if not words:
            return []

        lines = []
        current = words[0]

        for word in words[1:]:
            test = current + ' ' + word
            if pyray.measure_text(test, font_size) <= max_width:
                current = test
            else:
                lines.append(current)
                current = word
        lines.append(current)
        return lines

    def draw(self):
        if not self.active:
            return

        # Draw background & border
        pyray.draw_rectangle_rec(self.rect, self.bg_color)
        pyray.draw_rectangle_lines(
            int(self.rect.x), int(self.rect.y),
            int(self.rect.width), int(self.rect.height),
            self.border_color
        )

        # Wrap the label into lines, with a little horizontal padding
        padding_x = 8
        max_text_width = int(self.rect.width) - 2 * padding_x
        lines = self._wrap_text(self.label, self.font_size, max_text_width)

        # Compute total text block height and starting y to vertically center
        line_height = self.font_size + 4   # add a bit of spacing between lines
        total_height = len(lines) * line_height
        start_y = int(self.rect.y + (self.rect.height - total_height) / 2)

        # Draw each line centered horizontally
        for i, line in enumerate(lines):
            tw = pyray.measure_text(line, self.font_size)
            x = int(self.rect.x + (self.rect.width - tw) / 2)
            y = start_y + i * line_height
            pyray.draw_text(line, x, y, self.font_size, self.text_color)
