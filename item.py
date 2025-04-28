import pyray
from typing import List
from config import FRAMES_PER_SECOND
from dialog import Dialog

class Item:
    def __init__(self, pos: pyray.Vector2, time, item_data):
        self.pos = pos
        self.size = pyray.Vector2(100, 50)  # Dialog size, adjusted
        self.is_hit = False
        self.time = time * FRAMES_PER_SECOND
        self.alive = True
        self.in_assembly_line = False
        self.item_data = item_data

        self.timer_speed = 1

        # Dialog represents the item
        self.dialog = Dialog(self.item_data["label"], self.pos.x, self.pos.y, self.size.x, self.size.y, font_size=15)
        self.dialog.show()  # Always visible now

        self.ready_for_basket = False
        self.frames_on_line = 0
        self.frames_required_on_line = 30

        # Answer
        self.in_answer_box = False
        self.locked = False
        self.selected_answer = ""

    def compute_size(self, max_wrap_width: int):
        """Compute and set dialog.rect.width/height based on wrapped text + timer."""
        pad_x, pad_y = 8, 8
        wrap_w = min(max_wrap_width, int(self.size.x)) - 2 * pad_x
        lines = self._wrap_text(self.dialog.text, self.dialog.font_size, wrap_w)

        # Line height and timer height
        line_h = self.dialog.font_size + 4
        text_block_h = len(lines) * line_h
        timer_h = self.dialog.font_size + 4

        # Width = max(default, widest line + padding)
        needed_w = max(
            int(self.size.x),
            max(pyray.measure_text(line, self.dialog.font_size) for line in lines) + 2 * pad_x
        )
        needed_h = pad_y + text_block_h + pad_y + timer_h + pad_y

        # Apply
        self.dialog.rect.width = needed_w
        self.dialog.rect.height = needed_h

    def update(self, lines_rects: List[pyray.Rectangle], lines_answers: str):
        mouse_pos = pyray.get_mouse_position()
        item_rec = pyray.Rectangle(self.pos.x, self.pos.y, self.size.x, self.size.y)

        if pyray.is_mouse_button_pressed(pyray.MOUSE_BUTTON_LEFT):
            if pyray.check_collision_point_rec(mouse_pos, item_rec):
                self.is_hit = True

        if pyray.is_mouse_button_released(pyray.MOUSE_BUTTON_LEFT):
            self.is_hit = False

        if self.is_hit and not self.locked:
            self.pos.x = mouse_pos.x - (self.size.x // 2)
            self.pos.y = mouse_pos.y - (self.size.y // 2)

            self.time -= self.timer_speed
            if self.time <= 0:
                self.alive = False

        else:
            item_rect = self.get_rect()
            self.in_assembly_line = False
            for i, line_rect in enumerate(lines_rects):
                if pyray.check_collision_recs(line_rect, item_rect):
                    self.in_assembly_line = True
                    self.selected_answer = lines_answers[i]
                    break

            if self.in_assembly_line:
                self.pos = pyray.vector2_add(self.pos, pyray.Vector2(0, -1))

                self.frames_on_line += 1
                if self.frames_on_line >= self.frames_required_on_line:
                    self.ready_for_basket = True

            else:
                self.time -= self.timer_speed
                if self.time <= 0:
                    self.alive = False

                self.frames_on_line = 0
                self.ready_for_basket = False

        # Always keep dialog positioned with item
        self.dialog.rect.x = self.pos.x
        self.dialog.rect.y = self.pos.y

        if self.in_answer_box:
            self.locked = True
            self.timer_speed = 10

    def get_rect(self):
        return pyray.Rectangle(
            self.dialog.rect.x,
            self.dialog.rect.y,
            self.dialog.rect.width,
            self.dialog.rect.height
        )
        
    def _wrap_text(self, text: str, font_size: int, max_width: int) -> list[str]:
        """Split text into lines so no line is wider than max_width."""
        words = text.split()
        lines: list[str] = []
        if not words:
            return lines

        current = words[0]
        for w in words[1:]:
            test = current + ' ' + w
            if pyray.measure_text(test, font_size) <= max_width:
                current = test
            else:
                lines.append(current)
                current = w
        lines.append(current)
        return lines

    def draw(self):
        # 1) Wrap your paragraph
        pad_x, pad_y = 8, 8
        max_content_width = 400  # absolute cap if you need one (optional)
        raw_max_width = int(self.size.x)  # or some default
        wrap_width = raw_max_width - 2 * pad_x
        lines = self._wrap_text(self.dialog.text, self.dialog.font_size, wrap_width)

        # 2) Compute needed dimensions
        line_h = self.dialog.font_size + 4
        text_block_h = len(lines) * line_h
        timer_h = self.dialog.font_size + 4
        needed_w = max(
            raw_max_width,
            min(
                max(pyray.measure_text(line, self.dialog.font_size) for line in lines) + 2 * pad_x,
                max_content_width
            )
        )
        needed_h = pad_y + text_block_h + pad_y + timer_h + pad_y

        # 3) Apply to your dialog rectangle
        self.dialog.rect.width = needed_w
        self.dialog.rect.height = needed_h

        # 4) Draw box & border
        bg = pyray.DARKGRAY if not self.is_hit else pyray.Color(80, 80, 150, 255)
        pyray.draw_rectangle_rec(self.dialog.rect, bg)
        pyray.draw_rectangle_lines(
            int(self.dialog.rect.x),
            int(self.dialog.rect.y),
            int(self.dialog.rect.width),
            int(self.dialog.rect.height),
            pyray.RAYWHITE
        )

        # 5) Draw each wrapped line
        for i, line in enumerate(lines):
            x = int(self.dialog.rect.x + pad_x)
            y = int(self.dialog.rect.y + pad_y + i * line_h)
            pyray.draw_text(line, x, y, self.dialog.font_size, pyray.WHITE)

        # 6) Draw timer at bottom
        seconds = self.time // FRAMES_PER_SECOND
        timer = f"{seconds}s"
        tw = pyray.measure_text(timer, self.dialog.font_size)
        tx = int(self.dialog.rect.x + (self.dialog.rect.width - tw) / 2)
        ty = int(self.dialog.rect.y + self.dialog.rect.height - timer_h)
        color = pyray.YELLOW if seconds > 3 else pyray.RED
        pyray.draw_text(timer, tx, ty, self.dialog.font_size, color)
