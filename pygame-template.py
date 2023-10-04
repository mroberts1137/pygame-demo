import pygame
import random
import os

WIDTH = 800
HEIGHT = 600
FPS = 30

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

game_folder = os.path.dirname(__file__)
graphics_folder = os.path.join(game_folder, "Graphics")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(graphics_folder, "Player/p1_stand.png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)

    def update(self):
        self.rect.x += 5


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Game Name')
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# Game Loop

running = True

while running:
    clock.tick(FPS)

    # Process input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()


    # Render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()


pygame.quit()