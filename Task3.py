import pygame as pg
import sys, random
from collections import deque
from pathlib import Path
CELL = 20
GRID_W, GRID_H = 30, 25
SPEED_START = 8
SPEED_MAX = 18
MARGIN = 2
FONT_NAME = None
try:
    HS_FILE = Path(__file__).with_name("snake_highscore.txt")
except NameError:
    HS_FILE = Path.cwd() / "snake_highscore.txt"

WIN_W, WIN_H = GRID_W * CELL, GRID_H * CELL

BG = (18, 18, 18)
GRID_COLOR = (30, 30, 30)
SNAKE_HEAD = (80, 220, 120)
SNAKE_BODY = (60, 180, 100)
FOOD = (220, 80, 110)
TEXT = (230, 230, 230)
PAUSE_OVERLAY = (0, 0, 0, 130)

def rand_empty_cell(occupied):
    total = GRID_W * GRID_H
    if len(occupied) >= total:
        return None
    while True:
        p = (random.randrange(GRID_W), random.randrange(GRID_H))
        if p not in occupied:
            return p

def load_high_score():
    try:
        return int(HS_FILE.read_text().strip())
    except Exception:
        return 0

def save_high_score(score):
    try:
        HS_FILE.write_text(str(score))
    except Exception:
        pass

class SnakeGame:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIN_W, WIN_H))
        pg.display.set_caption("Snake (Pygame)")
        self.clock = pg.time.Clock()
        self.font = pg.font.Font(FONT_NAME, 22)
        self.bigfont = pg.font.Font(FONT_NAME, 48)
        self.move_event = pg.USEREVENT + 1
        self.reset()

    def reset(self):
        cx, cy = GRID_W // 2, GRID_H // 2
        self.snake = deque([(cx - 1, cy), (cx, cy), (cx + 1, cy)])
        self.dir = (1, 0)
        self.next_dir = self.dir
        self.score = 0
        self.high_score = load_high_score()
        self.paused = False
        self.game_over = False
        self.food = rand_empty_cell(set(self.snake))
        if self.food is None:
            self.game_over = True
        self.update_timer()

    def update_timer(self):
        moves_per_sec = min(SPEED_START + self.score // 5, SPEED_MAX)
        interval_ms = max(30, int(1000 / moves_per_sec))
        pg.time.set_timer(self.move_event, interval_ms)

    def handle_input(self, evt):
        if evt.type == pg.KEYDOWN:
            k = evt.key
            if k == pg.K_ESCAPE:
                pg.quit(); sys.exit()
            if k == pg.K_p and not self.game_over:
                self.paused = not self.paused
            if k == pg.K_r:
                self.reset(); return

            if not self.game_over and not self.paused:
                if k in (pg.K_UP, pg.K_w): self.set_next_dir(0, -1)
                elif k in (pg.K_DOWN, pg.K_s): self.set_next_dir(0, 1)
                elif k in (pg.K_LEFT, pg.K_a): self.set_next_dir(-1, 0)
                elif k in (pg.K_RIGHT, pg.K_d): self.set_next_dir(1, 0)

    def set_next_dir(self, dx, dy):
        if (dx, dy) == (-self.dir[0], -self.dir[1]):
            return
        self.next_dir = (dx, dy)

    def step(self):
        if self.game_over or self.paused: return
        self.dir = self.next_dir
        hx, hy = self.snake[-1]
        nx, ny = hx + self.dir[0], hy + self.dir[1]

        if nx < 0 or nx >= GRID_W or ny < 0 or ny >= GRID_H or (nx, ny) in self.snake:
            self.game_over = True
            if self.score > self.high_score:
                save_high_score(self.score)
                self.high_score = self.score
            return

        self.snake.append((nx, ny))
        if (nx, ny) == self.food:
            self.score += 1
            self.update_timer()
            occupied = set(self.snake)
            self.food = rand_empty_cell(occupied)
            if self.food is None:
                self.game_over = True
                if self.score > self.high_score:
                    save_high_score(self.score)
                    self.high_score = self.score
        else:
            self.snake.popleft()

    def draw_grid(self):
        if MARGIN <= 0: return
        for x in range(0, WIN_W, CELL):
            pg.draw.line(self.screen, GRID_COLOR, (x, 0), (x, WIN_H), MARGIN)
        for y in range(0, WIN_H, CELL):
            pg.draw.line(self.screen, GRID_COLOR, (0, y), (WIN_W, y), MARGIN)

    def draw_cell(self, cell, color, inset=2):
        x, y = cell
        r = pg.Rect(x * CELL + inset, y * CELL + inset, CELL - 2 * inset, CELL - 2 * inset)
        pg.draw.rect(self.screen, color, r, border_radius=6)

    def draw_snake(self):
        for c in list(self.snake)[:-1]:
            self.draw_cell(c, SNAKE_BODY, inset=3)
        self.draw_cell(self.snake[-1], SNAKE_HEAD, inset=1)

    def draw_food(self):
        if self.food:
            self.draw_cell(self.food, FOOD, inset=4)

    def draw_hud(self):
        msg = f"Score: {self.score}   High: {max(self.high_score, self.score)}"
        surf = self.font.render(msg, True, TEXT)
        self.screen.blit(surf, (10, 8))

    def draw_pause(self):
        if not self.paused: return
        overlay = pg.Surface((WIN_W, WIN_H), pg.SRCALPHA)
        overlay.fill(PAUSE_OVERLAY)
        self.screen.blit(overlay, (0, 0))
        label = self.bigfont.render("PAUSED", True, TEXT)
        self.screen.blit(label, label.get_rect(center=(WIN_W // 2, WIN_H // 2)))

    def draw_game_over(self):
        if not self.game_over: return
        overlay = pg.Surface((WIN_W, WIN_H), pg.SRCALPHA)
        overlay.fill(PAUSE_OVERLAY)
        self.screen.blit(overlay, (0, 0))
        lines = [
            "GAME OVER",
            f"Score: {self.score}   High: {max(self.high_score, self.score)}",
            "Press R to restart, ESC to quit",
        ]
        dy = -30
        for i, text in enumerate(lines):
            fnt = self.bigfont if i == 0 else self.font
            surf = fnt.render(text, True, TEXT)
            rect = surf.get_rect(center=(WIN_W // 2, WIN_H // 2 + dy))
            self.screen.blit(surf, rect)
            dy += 40

    def run(self):
        while True:
            for evt in pg.event.get():
                if evt.type == pg.QUIT:
                    pg.quit(); sys.exit()
                elif evt.type == self.move_event:
                    self.step()
                else:
                    self.handle_input(evt)

            self.screen.fill(BG)
            self.draw_grid()
            self.draw_food()
            self.draw_snake()
            self.draw_hud()
            self.draw_pause()
            self.draw_game_over()

            pg.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    SnakeGame().run()
