import pygame as pg
from settings import *
import random

class Player(pg.sprite.Sprite):

    def __init__(self, game, x, y, score):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((32, 32))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.rect.x = x
        self.rect.y = y
        self.lives = 4
        self.score = score

    def update(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] and self.rect.left > 0:
            self.vx = -PLAYER_VEL
        if keys[pg.K_RIGHT] and self.rect.right < WIDTH:
            self.vx = PLAYER_VEL
        if keys[pg.K_UP] and self.rect.top > 0:
            self.vy = -PLAYER_VEL
        if keys[pg.K_DOWN] and self.rect.bottom < HEIGHT:
            self.vy = PLAYER_VEL

        self.rect.x += self.vx
        self.rect.y += self.vy

class Moby(pg.sprite.Sprite):
    def __init__(self, game, player):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((32, 32))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(0, HEIGHT-self.rect.width)
        self.rect.x = WIDTH + 50
        self.speedx = random.randrange(8,12)
        self.player = player

    def update(self):
        self.rect.x -= self.speedx
        if self.rect.right < 0:
            self.rect.y = random.randrange(0, HEIGHT-self.rect.width)
            self.rect.x =WIDTH + 50
            self.speedy = random.randrange(8,12)
            self.player.score += 1

class Mobx(pg.sprite.Sprite):
    def __init__(self, game, player):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((32, 32))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH-self.rect.width)
        self.rect.y =-50
        self.speedy = random.randrange(8,12)
        self.player = player

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + self.rect.width:
            self.rect.x = random.randrange(0, WIDTH-self.rect.width)
            self.rect.y =-50
            self.speedy = random.randrange(8,12)
            self.player.score += 1
