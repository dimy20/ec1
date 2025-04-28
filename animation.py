import pyray
from config import FRAMES_PER_SECOND, DEBUG

class Animation:
    def __init__(self, texture, rects, speed, repeat=True):
        self.texture = texture
        self.rects = rects

        # Animation props
        self.playing = False
        self.frames_count = 0
        self.current_frame = 0
        self.frames_delay = int(speed * FRAMES_PER_SECOND)

        self.total_frames = len(rects)
        self.repeat = repeat

        # Draw rectangle
        self.draw_rect = pyray.Rectangle(0, 0, 0, 0)

    def play(self, where_rect: pyray.Rectangle):
        self.draw_rect = where_rect
        self.playing = True

    def stop(self):
        self.playing = False

    def update(self):
        if self.playing:
            self.frames_count += 1
            if self.frames_count >= self.frames_delay:
                self.frames_count = 0
                self.current_frame += 1

                if self.current_frame == self.total_frames:
                    if self.repeat:
                        self.current_frame = 0
                    else:
                        self.current_frame = 0
                        self.stop()

    def draw_current_frame(self):
        rec = self.rects[self.current_frame]
        pyray.draw_texture_pro(self.texture, rec, self.draw_rect, pyray.Vector2(0, 0), 0.0, pyray.WHITE)
        if DEBUG:
            pyray.draw_rectangle_lines(
                int(self.draw_rect.x),
                int(self.draw_rect.y),
                int(self.draw_rect.width),
                int(self.draw_rect.height),
                pyray.RED
            )
