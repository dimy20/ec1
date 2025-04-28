import pyray

class Dialog:
    def __init__(self, text, x, y, width, height, font_size=24):
        self.text = text
        self.rect = pyray.Rectangle(x, y, width, height)
        self.font_size = font_size
        self.visible = True

        # Colors (you can tweak these)
        self.bg_color = pyray.Color(50, 50, 50, 200)  # semi-transparent dark gray
        self.border_color = pyray.RAYWHITE
        self.text_color = pyray.RAYWHITE

    def draw(self):
        if not self.visible:
            return

        # Draw background
        pyray.draw_rectangle_rec(self.rect, self.bg_color)
        
        # Draw border
        pyray.draw_rectangle_lines(
            int(self.rect.x),
            int(self.rect.y),
            int(self.rect.width),
            int(self.rect.height),
            self.border_color
        )
        
        # Center the text
        text_width = pyray.measure_text(self.text, self.font_size)
        text_x = int(self.rect.x + (self.rect.width - text_width) / 2)
        text_y = int(self.rect.y + 10)

        pyray.draw_text(self.text, text_x, text_y, self.font_size, self.text_color)

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True
