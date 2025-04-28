import pyray
from config import DEBUG
from item import Item
from typing import List
from answers import Answer

class AssemblyLine:
    def __init__(self, rows, sprite_size, x, y, answer_label):
        self.texture = pyray.load_texture("assets/Conveyor.png")

        self.sprite_w, self.sprite_h = 16, 16  # real sprite size
        self.sprite_size = sprite_size  # Desired size on screen

        # Dimensions
        self.num_rows = rows
        self.pos = pyray.Vector2(x, y)

        # Animation Stuff
        self.frames_count = 0
        self.current_frame = 0
        self.frames_delay = 2

        self.total_frames = self.texture.width // self.sprite_w

        width = 120
        height = 60

        line_center_x = x + (sprite_size // 2)
        xprime = line_center_x - (width // 2)
        yprime = y - 30 - (height // 2)
        
        pos_answer = (xprime, yprime)
        self.answer: Answer = Answer(answer_label, pos_answer[0], pos_answer[1], width=width, height=height)

    def update(self, items: List[Item]):
        self.animation_update()

        line_rect = self.get_rect()

        for item in items:
            item_rect = item.get_rect()
            item.in_assembly_line = pyray.check_collision_recs(line_rect, item_rect)
        
        self.answer.update(items=items)

    def get_rect(self) -> pyray.Rectangle:
        w = self.sprite_size
        h = self.num_rows * self.sprite_size
        return pyray.Rectangle(self.pos.x, self.pos.y, w, h)

    def animation_update(self):
        self.frames_count += 1
        if self.frames_count >= self.frames_delay:
            self.frames_count = 0
            self.current_frame = (self.current_frame + 1) % self.total_frames

    def draw(self):
        rec = pyray.Rectangle(
            self.current_frame * self.sprite_w,
            0,
            self.sprite_w,
            self.sprite_h
        )
        for i in range(self.num_rows):
            posy = self.pos.y + (self.sprite_size * i)
            pyray.draw_texture_pro(
                self.texture,
                rec,
                pyray.Rectangle(self.pos.x, posy, self.sprite_size, self.sprite_size),
                pyray.Vector2(0, 0),
                0.0,
                pyray.WHITE
            )

        if DEBUG:
            pyray.draw_rectangle_lines(
                int(self.pos.x),
                int(self.pos.y),
                self.sprite_size,
                self.sprite_size * self.num_rows,
                pyray.RED
            )

        self.answer.draw()
