import pygame
import sys
from dataclasses import dataclass

WIN_W, WIN_H = 900, 600
FPS = 60
PADDLE_WIDTH, PADDLE_HEIGHT = 12, 100
BALL_SIZE = 16
PADDLE_SPEED = 6
BALL_SPEED_START = 5
FONT_NAME = None  

pygame.init()
screen = pygame.display.set_mode((WIN_W, WIN_H))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()
font = pygame.font.SysFont(FONT_NAME, 36)
@dataclass
class Paddle:
    x: int
    y: int
    w: int = PADDLE_WIDTH
    h: int = PADDLE_HEIGHT
    speed: int = PADDLE_SPEED

    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def move(self, dy):
        self.y += dy
 
        if self.y < 0:
            self.y = 0
        elif self.y + self.h > WIN_H:
            self.y = WIN_H - self.h

    def draw(self, surf):
        pygame.draw.rect(surf, (255, 255, 255), self.rect())

@dataclass
class Ball:
    x: float
    y: float
    size: int = BALL_SIZE
    vx: float = BALL_SPEED_START
    vy: float = BALL_SPEED_START

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.size, self.size)

    def reset(self, direction=1):
        self.x = WIN_W // 2 - self.size // 2
        self.y = WIN_H // 2 - self.size // 2
   
        self.vx = BALL_SPEED_START * direction
        self.vy = BALL_SPEED_START * (1 if pygame.time.get_ticks() % 2 == 0 else -1)

    def update(self):
        self.x += self.vx
        self.y += self.vy
    
        if self.y <= 0:
            self.y = 0
            self.vy *= -1
        if self.y + self.size >= WIN_H:
            self.y = WIN_H - self.size
            self.vy *= -1

    def draw(self, surf):
        pygame.draw.rect(surf, (255, 255, 255), self.rect())
left = Paddle(20, WIN_H // 2 - PADDLE_HEIGHT // 2)
right = Paddle(WIN_W - 20 - PADDLE_WIDTH, WIN_H // 2 - PADDLE_HEIGHT // 2)
ball = Ball(WIN_W // 2, WIN_H // 2)
ball.reset(direction=1)

score_left = 0
score_right = 0

paused = False

def draw_center_line():
    for y in range(0, WIN_H, 30):
        pygame.draw.rect(screen, (255,255,255), (WIN_W//2 - 2, y + 10, 4, 20))

def draw_scores():
    left_surf = font.render(str(score_left), True, (255,255,255))
    right_surf = font.render(str(score_right), True, (255,255,255))
    screen.blit(left_surf, (WIN_W//4 - left_surf.get_width()//2, 20))
    screen.blit(right_surf, (3*WIN_W//4 - right_surf.get_width()//2, 20))

def clamp_ball_speed():
   
    max_speed = 14
    if abs(ball.vx) > max_speed:
        ball.vx = max_speed * (1 if ball.vx > 0 else -1)
    if abs(ball.vy) > max_speed:
        ball.vy = max_speed * (1 if ball.vy > 0 else -1)

running = True
while running:
    dt = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_r:
    
                score_left = 0
                score_right = 0
                left.y = WIN_H // 2 - left.h // 2
                right.y = WIN_H // 2 - right.h // 2
                ball.reset(direction=1)
                paused = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        left.move(-left.speed)
    if keys[pygame.K_s]:
        left.move(left.speed)
    if keys[pygame.K_UP]:
        right.move(-right.speed)
    if keys[pygame.K_DOWN]:
        right.move(right.speed)

    if not paused:
        ball.update()
        if ball.rect().colliderect(left.rect()):
            ball.x = left.x + left.w
            ball.vx = -ball.vx

            offset = (ball.y + ball.size/2) - (left.y + left.h/2)
            ball.vy += offset * 0.03
            ball.vx *= 1.03  
        if ball.rect().colliderect(right.rect()):
            ball.x = right.x - ball.size
            ball.vx = -ball.vx
            offset = (ball.y + ball.size/2) - (right.y + right.h/2)
            ball.vy += offset * 0.03
            ball.vx *= 1.03

        clamp_ball_speed()

        if ball.x < 0:
            score_right += 1
            ball.reset(direction=1)
        elif ball.x > WIN_W:
            score_left += 1
            ball.reset(direction=-1)
    screen.fill((0, 0, 0))
    draw_center_line()
    left.draw(screen)
    right.draw(screen)
    ball.draw(screen)
    draw_scores()

    hint = "W/S - Left | ↑/↓ - Right | SPACE - Pause | R - Reset | ESC - Quit"
    hint_surf = pygame.font.SysFont(FONT_NAME, 18).render(hint, True, (200,200,200))
    screen.blit(hint_surf, (WIN_W//2 - hint_surf.get_width()//2, WIN_H - 30))

    if paused:
        p_surf = font.render("PAUSED", True, (255, 255, 0))
        screen.blit(p_surf, (WIN_W//2 - p_surf.get_width()//2, WIN_H//2 - p_surf.get_height()//2))

    pygame.display.flip()

pygame.quit()
sys.exit()
