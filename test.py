import pygame

width = 1200
height = 700

paddle_w = 300
paddle_h = 30

pygame.init()
sc = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption("Arkanoid")
bg = pygame.image.load("bg.jpg").convert()
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()
    sc.blit(bg, (0, 0))

