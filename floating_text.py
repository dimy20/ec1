import pyray

class FloatingText:
    def __init__(self, text, x, y, color, duration=60):
        self.text = text
        self.pos = pyray.Vector2(x, y)
        
        # Accept either tuple or Color
        if isinstance(color, tuple):
            self.color = pyray.Color(color[0], color[1], color[2], 255)
        else:
            self.color = color
        
        self.frames_left = duration
        self.alpha = 255

    def update(self):
        self.pos.y -= 0.5  # Move upward a little every frame
        self.frames_left -= 1
        self.alpha = max(0, int(255 * (self.frames_left / 60)))  # Fade out slowly

    def draw(self):
        faded_color = pyray.Color(self.color.r, self.color.g, self.color.b, self.alpha)
        pyray.draw_text(self.text, int(self.pos.x), int(self.pos.y), 24, faded_color)

    def is_alive(self):
        return self.frames_left > 0
