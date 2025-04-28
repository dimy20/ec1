import pyray
from config import WINDOW_W, WINDOW_H, LOADING_TIME
from animation import Animation
import random
from typing import List
from assembly_line import AssemblyLine
from item import Item
from level import generate_random_level, level_configs
from floating_text import FloatingText
import json
import sys

MAX_TRIES = 50

def find_non_overlapping_pos(width, height, existing_items, x_min, x_max, y_min, y_max):
    """
    Return an (x,y) so Rectangle(x,y,width,height) fits entirely within
    [x_min..x_max]×[y_min..y_max] and doesn’t overlap existing_items.
    """
    # ensure we have room
    x_max_allowed = max(x_min, x_max - width)
    y_max_allowed = max(y_min, y_max - height)

    for _ in range(MAX_TRIES):
        x = random.randint(x_min, x_max_allowed)
        y = random.randint(y_min, y_max_allowed)
        candidate = pyray.Rectangle(x, y, width, height)
        if not any(pyray.check_collision_recs(candidate, it.get_rect()) for it in existing_items):
            return x, y
    # fallback
    return x_min, y_min

def build_atlas_rects(texture: pyray.Texture2D, x_count, y_count):
    sprite_w = texture.width // x_count
    sprite_h = texture.height // y_count 
    print(texture.width)
    rects = []

    y = 0
    for _ in range(y_count):
        x = 0
        for _ in range(x_count):
            rect = pyray.Rectangle(x, y, sprite_w, sprite_h)
            rects.append(rect)
            x += sprite_w
        y += sprite_h
    return rects

def build_assembly_lines(n, labels, padding=100) -> List[AssemblyLine]:
    lines = []
    x, y = 35, 100
    for i in range(n):
        lines.append(
            AssemblyLine(rows=10, sprite_size=64, x=x, y=y, answer_label=labels[i])
        )
        x += 70 + padding
    return lines

class Game:
    def __init__(self):
        pyray.init_window(WINDOW_W, WINDOW_H, "Boot assembly line")
        pyray.set_target_fps(60)
        
        self.items: List[Item] = []
        self.floating_texts: List[FloatingText] = []
        self.current_level = 0
        self.game_over = False
        self.game_over_timer = LOADING_TIME

        self.start_new_level()

        self.mouse_held_down = False
        self.explosion_texture = pyray.load_texture("./assets/explosion.png")
        self.explosion_rects = build_atlas_rects(texture=self.explosion_texture, x_count=3, y_count=3)
        self.explosions = []

        self.loading_level = False
        self.loading_timer = LOADING_TIME

        pyray.init_audio_device()
        self.explosion_sound = pyray.load_sound("assets/explosion.mp3")
        self.next_level_sound = pyray.load_sound("assets/next_level.mp3")
        self.success_sound = pyray.load_sound("assets/coin.mp3")

    def start_new_level(self):
        self.points = 0
        cfg = level_configs[self.current_level]
        level_data = generate_random_level(
            num_answers=cfg["num_answers"],
            items_per_answer=cfg["items_per_answer"],
            num_distractors=cfg["num_distractors"]
        )
        self.levels = [level_data]
        self.lines = build_assembly_lines(cfg["num_answers"], labels=level_data["answers"])

        for item_data in self.levels[0]["items"]:
            item = Item(
                pyray.Vector2(0, 0),
                time=random.randint(*cfg["time_start_range"]),
                item_data=item_data
            )

            max_wrap = (WINDOW_W // 2) - 16
            item.compute_size(max_wrap)

            x, y = find_non_overlapping_pos(
                width=int(item.dialog.rect.width),
                height=int(item.dialog.rect.height),
                existing_items=self.items,
                x_min=WINDOW_W // 2,
                x_max=WINDOW_W,
                y_min=100,
                y_max=WINDOW_H
            )

            item.pos.x = x
            item.pos.y = y
            item.dialog.rect.x = x
            item.dialog.rect.y = y

            self.items.append(item)

    def draw(self):
        pyray.begin_drawing()
        pyray.clear_background(pyray.BLACK)

        if self.loading_level:
            pyray.draw_text(f"Cargando Nivel {self.current_level + 1}", WINDOW_W//2 - 100, WINDOW_H//2, 24, pyray.YELLOW)
        elif self.game_over:
            pyray.draw_text("GAME OVER", WINDOW_W//2 - 100, WINDOW_H//2, 24, pyray.YELLOW)
        else:
            for line in self.lines:
                line.draw()

            for item in self.items:
                if item.alive:
                    item.draw()

            for e in self.explosions:
                e.draw_current_frame()

            pyray.draw_text(f"Puntos: {self.points}", WINDOW_W-200, 20, 24, pyray.YELLOW)

            for f in self.floating_texts:
                f.draw()

        pyray.end_drawing()

    def animations_left(self):
        return any(e.playing for e in self.explosions)

    def check_answer(self, item):
        if item.item_data["correct_answer"] == item.selected_answer:
            self.points += 100
            self.floating_texts.append(FloatingText("+100", WINDOW_W-260, 30, pyray.GREEN))
            pyray.play_sound(self.success_sound)
        else:
            self.floating_texts.append(FloatingText("-50", WINDOW_W-260, 30, pyray.RED))
            pyray.play_sound(self.explosion_sound)
            self.points -= 50

    def update(self):
        for line in self.lines:
            line.update(items=self.items)

        for exp in self.explosions:
            exp.update()

        self.explosions = [e for e in self.explosions if e.playing]

        for item in self.items:
            lines_rects = [line.get_rect() for line in self.lines]
            line_answers = [line.answer.label for line in self.lines]
            item.update(lines_rects=lines_rects, lines_answers=line_answers)

            if not item.alive:
                explosion_animation = Animation(
                    texture=self.explosion_texture,
                    rects=self.explosion_rects,
                    speed=0.08,
                    repeat=False
                )
                explosion_animation.play(where_rect=item.dialog.rect)
                self.explosions.append(explosion_animation)

                if item.in_answer_box:
                    self.check_answer(item)
                else:
                    if item.item_data["correct_answer"] is not None:
                        self.floating_texts.append(FloatingText("-25", WINDOW_W-260, 30, pyray.RED))
                        self.points -= 25
                        pyray.play_sound(self.explosion_sound)
                    else:
                        self.floating_texts.append(FloatingText("-0", WINDOW_W-260, 30, pyray.GREEN))

        self.items = [item for item in self.items if item.alive]

        for text in self.floating_texts:
            text.update()

        self.floating_texts = [text for text in self.floating_texts if text.is_alive()]

        if len(self.items) == 0 and not self.animations_left() and not self.loading_level:
            if self.points > 0:
                if self.current_level < len(level_configs) - 1:
                    self.current_level += 1

                self.loading_level = True
                pyray.play_sound(self.next_level_sound)
            else:
                self.game_over = True

        if self.loading_level:
            self.loading_timer -= 1
            if self.loading_timer <= 0:
                self.start_new_level()
                self.loading_level = False
                self.loading_timer = LOADING_TIME

        if self.game_over:
            self.game_over_timer -= 1
            if self.game_over_timer <= 0:
                sys.exit(1)

    def run(self):
        while not pyray.window_should_close():
            self.update()
            self.draw()
        
    def close(self):
        pyray.close_window()
        pyray.close_audio_device()

if __name__ == "__main__":
    game = Game()
    print(len(game.items))

    game.run()
    game.close()
