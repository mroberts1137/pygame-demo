import pygame
import numpy as np
import random
from os import path
import spritesheet

game_folder = path.dirname(__file__)
graphics_folder = path.join(game_folder, "Graphics")

WIDTH = 800
HEIGHT = 600
FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

font_name = pygame.font.match_font('arial')

def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT-126)
        self.xspeed = 0
        self.yspeed = 0
        self.direction = 0
        self.animation_frame = 0
        self.animation_delay = 3
        self.animation_timer = self.animation_delay

    def update(self):
        self.xspeed = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.left_press()
        if keystate[pygame.K_d]:
            self.right_press()
        if not keystate[pygame.K_a] and not keystate[pygame.K_d]:
            self.animation_timer = 0
            self.animation_frame = 0
            self.animate("stand")
        self.rect.x += self.xspeed
        self.rect.y += self.yspeed
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def left_press(self):
        self.xspeed = -5
        self.direction = 2
        self.animation_timer -= 1
        if self.animation_timer < 0:
            self.animation_timer = self.animation_delay
            self.animation_frame = np.mod(self.animation_frame + 1, len(p1_walking))
            self.animate("walk")

    def right_press(self):
        self.xspeed = 5
        self.direction = 0
        self.animation_timer -= 1
        if self.animation_timer < 0:
            self.animation_timer = self.animation_delay
            self.animation_frame = np.mod(self.animation_frame + 1, len(p1_walking))
            self.animate("walk")

    def animate(self, animation):
        if animation == "stand":
            player_img = p1_stand
        elif animation == "walk":
            player_img = p1_walking[self.animation_frame]

        if self.direction == 0:
            self.image = pygame.transform.flip(player_img, False, False)
        elif self.direction == 2:
            self.image = pygame.transform.flip(player_img, True, False)

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(mob_img, (36, 18))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH)
        self.rect.y = random.randrange(HEIGHT)
        self.xspeed = random.randrange(-3, 3)
        self.yspeed = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.xspeed
        self.rect.y += self.yspeed
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dir):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 10))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.direction = dir
        self.speed = 15

    def update(self):
        if self.direction == 0:
         self.rect.x += self.speed
        elif self.direction == 2:
         self.rect.x -= self.speed

        if self.rect.left > WIDTH or self.rect.right < 0:
            self.kill()

'''
Game code start - Initialize pygame
'''

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Game Name')
clock = pygame.time.Clock()

# Assets (any use of pygame must come after pygame.init())
background = pygame.image.load(path.join(graphics_folder, "SMB1-1BG.png")).convert()
background_rect = background.get_rect()

p1_spritesheet = spritesheet.Spritesheet(path.join(graphics_folder, "Player/p1_spritesheet.png"))
p1_walk01 = (0, 0, 72, 97)
p1_walk02 = (73, 0, 72, 97)
p1_walk03 = (146, 0, 72, 97)
p1_walk04 = (0, 98, 72, 97)
p1_walk05 = (73, 98, 72, 97)
p1_walk06 = (146, 98, 72, 97)
p1_walk07 = (219, 0, 72, 97)
p1_walk08 = (292, 0, 72, 97)
p1_walk09 = (219, 98, 72, 97)
p1_walk10 = (365, 0, 72, 97)
p1_walk11 = (292, 98, 72, 97)
p1_walking_coords = [p1_walk01, p1_walk02, p1_walk03, p1_walk04, p1_walk05, p1_walk06, p1_walk07, p1_walk08, p1_walk09, p1_walk10, p1_walk11]

p1_walking = p1_spritesheet.image_list(p1_walking_coords, colorkey=BLACK)
p1_duck = p1_spritesheet.image_at((365, 98, 69, 71), colorkey=BLACK)
p1_front = p1_spritesheet.image_at((0, 196, 66, 92), colorkey=BLACK)
p1_hurt = p1_spritesheet.image_at((438, 0, 69, 92), colorkey=BLACK)
p1_jump = p1_spritesheet.image_at((438, 93, 67, 94), colorkey=BLACK)
p1_stand = p1_spritesheet.image_at((67, 196, 66, 92), colorkey=BLACK)

player_img = p1_stand

mob_img = pygame.image.load(path.join(graphics_folder, "Enemies/flyFly1.png")).convert()



all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(10):
    m = Mob()
    mobs.add(m)
    all_sprites.add(m)


'''
Game Loop
'''

running = True

while running:
    clock.tick(FPS)

    # Process input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:
                player.shoot()

    # Update
    all_sprites.update()
    collisions = pygame.sprite.spritecollide(player, mobs, False)
    collisions = pygame.sprite.groupcollide(mobs, bullets, True, True)


    # Render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, "Sample text", 18, 16, 16)
    pygame.display.flip()


pygame.quit()