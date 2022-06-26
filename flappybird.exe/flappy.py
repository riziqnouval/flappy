import pygame
import sys
from random import choice
from pygame import mixer
from pygame.locals import*

# variable layar
WIDTH = 480
HEIGHT = 600
FPS = 37


# variable warna
PUTIH = (255, 255, 255)
HITAM = (0, 0, 0)
MERAH = (255, 0, 0)
HIJAU = (0, 255, 0)
BIRU = (0, 0, 255)

# variable background
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("flappybird.exe")
clock = pygame.time.Clock()


# game variabel
gravity = 0
score = 0
pos_list = [[-300, 350], [-400, 250], [-200, 450], [-450, 150], [-50, 550], [-350, 300], [-250, 400]]
mouse_pos = (0, 0)

# fungsi pipa
def create_pipe():
    y_pos = choice(pos_list)
    p1 = Top(y_pos[0])
    p2 = Bottom(y_pos[1])
    detection = DetectionPoint(p2.rect.x, y_pos[1])
    pipes.add(p1)
    pipes.add(p2)
    all_sprites.add(p1)
    all_sprites.add(p2)
    detect_group.add(detection)
    all_sprites.add(detection)


def show_text(text, font_size, font_color, x, y):
    font = pygame.font.SysFont(None, font_size)
    font_surface = font.render(text, True, font_color)
    screen.blit(font_surface, (x,y))

def game_over_screen():
    screen.fill(HITAM)
    show_text("GAME OVER", 40, MERAH, WIDTH//2 - 95, HEIGHT//4)
    show_text("SCORE : {}". format(score), 25, PUTIH, WIDTH//2 - 50, HEIGHT//4 + 50)
    show_text("PRESS ANY KEY TO CONTINUE", 25, PUTIH, WIDTH//2 - 135, HEIGHT//2 + 100)

    pygame.display.flip()
    waiting_game_over = True
    while waiting_game_over:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYUP:
                waiting_game_over = False


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image = pygame.image.load("eyebrow.png")
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT // 2

    def update(self):
        global game_over
        if self.rect.y <= 0:
            self.rect.y = 0
        if self.rect.y > HEIGHT:
            game_over = True


class Pipe(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 500))
        self.image.fill(HIJAU)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + 10

    def update(self):
        self.rect.x -= 4
        if self.rect.x < -20:
            self.kill()
        
        
class Top(Pipe):
    def __init__(self, y):
        super().__init__()
        self.rect.y = y

class Bottom(Pipe):
    def __init__(self, y):
        super().__init__()
        self.rect.y = y

class DetectionPoint(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 120))
        self.image.set_colorkey(HITAM)
        # self.image.fill(PUTIH)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y

        self.hit = False

    def update(self):
        self.rect.x -= 4
        if self.rect.x < -20:
            self.kill()


# load sound
score_sound = pygame.mixer.Sound('boom.wav')

# background sound
mixer.music.load("turu deck (2).wav")
mixer.music.play(-1)


all_sprites = pygame.sprite.Group()
detect_group = pygame.sprite.Group()
pipes = pygame.sprite.Group()
bird = Bird()

create_pipe()

all_sprites.add(bird)


# game loop
game_over = False
run = True
while run:
    if game_over:
        game_over_screen()
        all_sprites = pygame.sprite.Group()
        detect_group = pygame.sprite.Group()
        pipes = pygame.sprite.Group()
        bird = Bird()

        create_pipe()

        all_sprites.add(bird)
        score = 0
        game_over = False
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                gravity = 0
                gravity -= 5

    gravity += 0.4
    bird.rect.y += gravity


    # check collision bird w detection_point
    bird_hit_point = pygame.sprite.spritecollide(bird, detect_group, False)
    if bird_hit_point and not bird_hit_point[0].hit:
        score += 1
        bird_hit_point[0].hit = True
        score_sound.play()
    
    # check collision bird w pipe
    bird_hit_pipe = pygame.sprite.spritecollide(bird, pipes, False)
    if bird_hit_pipe:
        game_over = True
    
    if len(pipes) <= 0:
        create_pipe()
    
    all_sprites.update()
    screen.fill(HITAM)
    all_sprites.draw(screen)
    show_text(str(score), 32, PUTIH, WIDTH//2, HEIGHT//4 - 100)
    
    pygame.display.flip()


pygame.quit()