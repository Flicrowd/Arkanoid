import pygame
from random import randrange

width = 1200
height = 700
fps = 60

paddle_w = 300
paddle_h = 30
paddle = pygame.Rect(width / 2 - paddle_w / 2, height - paddle_h - 10, paddle_w, paddle_h)
p_speed = 15

ball_r = 267
ball_speed = 3
ball_d = ball_r * 2
ball = pygame.Rect(randrange(ball_d, width - ball_d), height / 2, ball_d, ball_d)
dx = 1
dy = -1

blocks = [
    pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50)
    for i in range(10)
    for j in range(4)
]

color8locks = [
    (randrange(30, 256), randrange(30,256), randrange(30, 256))
    for i in range(10)
    for j in range(4)
]


trail = []

pygame.init()
sc = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption("Arkanoid")
bg = pygame.image.load("bg.jpg").convert()
game_over = pygame.image.load("game_over.jpg").convert()
win = pygame.image.load("win.jpg").convert()

def collision(dx, dy, ball, rect):
    if dx > 0:
        x = ball.right - rect.left
    else:
        x = rect.right - ball.left
    if dy > 0:
        y = ball.bottom - rect.top
    else:
        y = rect.bottom - ball.top

    if abs (x - y) < 10:
        dx = -dx
        dy = -dy
    elif x > y:
        dy = -dy
    elif x < y:
        dx = -dx

    return dx, dy 

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()
    sc.blit(bg, (0, 0))
    pygame.draw.rect(sc, pygame.Color("darkorange"), paddle)
    pygame.draw.circle(sc, pygame.Color("white"), ball.center, ball_r)

    [
        pygame.draw.rect(sc, color8locks[color], block)
        for color, block in enumerate(blocks)
    ]

    surface = pygame.Surface((width,height), pygame.SRCALPHA)
    trail.append([ball.centerx, ball.centery, dx, dy, 255])
    for element in trail:
        element[0] += element[2]
        element[1] += element[3]
        if element[4] >= 0: element[4] /= 2
        if len(trail) > 8: trail.remove(element)
        pygame.draw.circle(surface, (0, 255, 157, int(element[4])), (int(element[0]), int(element[1])), ball_r)
        sc.blit(surface, (0,0))
    ball.x += ball_speed * dx
    ball.y += ball_speed * dy
    ball.x += ball_speed * dx
    ball.y += ball_speed * dy

    if ball.centerx < ball_r or ball.centerx > width - ball_r:
        dx = -dx
    elif ball.centery < ball_r:
        dy = -dy
    elif ball.colliderect(paddle) and dy > 0:
        dx, dy = collision(dx, dy, ball, paddle)

    hit = ball.collidelist(blocks)

    if hit != -1:
        block = blocks.pop(hit)
        dx, dy = collision(dx, dy, ball, block)
        fps += 2

 #   if ball.bottom > height or not len(blocks):
      #  exit()
    
    if not len(blocks):
        win = pygame.transform.scale(win, (sc.get_width(), sc.get_height()))
        sc.blit(win, (0, 0))
    elif ball.bottom > height:
        game_over = pygame.transform.scale(game_over, (sc.get_width(), sc.get_height()))
        sc.blit(game_over, (0, 0))
        
    key = pygame.key.get_pressed()
    if (key[pygame.K_LEFT] or key[pygame.K_a]) and paddle.left > 0:
        paddle.left -= p_speed
    elif (key[pygame.K_RIGHT] or key[pygame.K_d]) and paddle.right < width:
        paddle.right += p_speed


    pygame.display.flip()
    clock.tick(fps)
