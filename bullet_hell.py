import pygame as pg
import random
from os import path
from settings import *
from sprites import *

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.font_name = pg.font.match_font('arial')
        self.clock = pg.time.Clock()
        self.go = False
        self.mode = 2
        self.load_data()

    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.snd_dir = path.join(self.game_folder, 'snd')
        self.hit_sound = pg.mixer.Sound(path.join(self.snd_dir, 'hurt.wav'))
        self.die_sound = pg.mixer.Sound(path.join(self.snd_dir, 'death.wav'))

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.player = Player(self, 0, HEIGHT-32, 0)
        if self.mode == 1:
            spawn = 8
            self.player.lives = 8
        if self.mode == 2:
            spawn = 10
            self.player.lives = 6
        if self.mode == 3:
            spawn = 12
            self.player.lives = 4
        if self.mode == 4:
            spawn = 16
            self.player.lives = 3
        if self.mode == 5:
            spawn = 20
            self.player.lives = 1
        for i in range(spawn):
            Mobx(self, self.player)
            Moby(self, self.player)
        pg.mixer.music.load(path.join(self.snd_dir, 'battleThemeA.mp3'))

    def run(self):
        # Game loop
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

    def update(self):
        self.all_sprites.update()
        # player/mob collision
        hits = pg.sprite.spritecollide(self.player, self.mobs, True)
        if hits:
            self.player.lives -= 1
            self.hit_sound.play()

        if self.player.lives <= 0:
            self.playing = False
            self.die_sound.play()

    def draw_text(self, surf, text, size, x, y, color):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(self.player.score), 18, WIDTH/2, 10, WHITE)
        self.draw_text(self.screen, "Lives left: " + str(self.player.lives), 20, WIDTH - 100, 10, WHITE)
        pg.display.flip()

    def show_start_screen(self):
        pg.mixer.music.load(path.join(self.snd_dir, 'b423b42.wav'))
        pg.mixer.music.play(loops=-1)
        while not self.go:
            self.screen.fill(BGCOLOR)
            self.draw_text(self.screen, "Bullet Hell", 50, WIDTH/2, 50, WHITE)
            self.draw_text(self.screen, "Arrow keys to move.Press any key to start!", 30, WIDTH/2, HEIGHT/2, WHITE)
            self.draw_text(self.screen, "Player is green.Obstacles are red!", 30, WIDTH/2, HEIGHT/2 - 50, WHITE)
            self.draw_text(self.screen, "Press 1 for easy mode!", 30, WIDTH/2, HEIGHT/2 + 50, WHITE)
            self.draw_text(self.screen, "Press 2 for normal mode(default)", 30, WIDTH/2, HEIGHT/2 + 80, WHITE)
            self.draw_text(self.screen, "Press 3 for hard mode!", 30, WIDTH/2, HEIGHT/2 + 110, WHITE)
            self.draw_text(self.screen, "Press 4 for expert mode!", 30, WIDTH/2, HEIGHT/2 + 140, WHITE)
            self.draw_text(self.screen, "Press 5 for impossible mode!", 30, WIDTH/2, HEIGHT/2 + 170, WHITE)
            self.draw_text(self.screen, "When you die, the gamemode stays the same until you change it!", 30, WIDTH/2, HEIGHT-60, RED)
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.KEYUP:
                    if event.key == pg.K_1:
                        self.mode = 1
                    if event.key == pg.K_2:
                        self.mode = 2
                    if event.key == pg.K_3:
                        self.mode = 3
                    if event.key == pg.K_4:
                        self.mode = 4
                    if event.key == pg.K_5:
                        self.mode = 5
                    self.go = True
                if event.type == pg.QUIT:
                    self.go = False
                    self.playing = False
                    pg.quit()
        pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        pg.mixer.music.load(path.join(self.snd_dir, 'b423b42.wav'))
        pg.mixer.music.play(loops=-1)
        self.died = True
        while self.died:
            self.screen.fill(BGCOLOR)
            self.draw_text(self.screen, "Bullet Hell", 50, WIDTH/2, 50, WHITE)
            self.draw_text(self.screen, "Arrow keys to move.Press any key to restart!", 30, WIDTH/2, HEIGHT/2, WHITE)
            self.draw_text(self.screen, "Score: " + str(self.player.score), 30, WIDTH/2, HEIGHT/2-50, WHITE)
            self.draw_text(self.screen, "Press 1 for easy mode!", 30, WIDTH/2, HEIGHT/2 + 50, WHITE)
            self.draw_text(self.screen, "Press 2 for normal mode(default)", 30, WIDTH/2, HEIGHT/2 + 80, WHITE)
            self.draw_text(self.screen, "Press 3 for hard mode!", 30, WIDTH/2, HEIGHT/2 + 110, WHITE)
            self.draw_text(self.screen, "Press 4 for expert mode!", 30, WIDTH/2, HEIGHT/2 + 140, WHITE)
            self.draw_text(self.screen, "Press 5 for impossible mode!", 30, WIDTH/2, HEIGHT/2 + 170, WHITE)
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.KEYUP:
                    if event.key == pg.K_1:
                        self.mode = 1
                    if event.key == pg.K_2:
                        self.mode = 2
                    if event.key == pg.K_3:
                        self.mode = 3
                    if event.key == pg.K_4:
                        self.mode = 4
                    if event.key == pg.K_5:
                        self.mode = 5
                    self.died = False
                if event.type == pg.QUIT:
                    self.died = False
                    self.playing = False
                    pg.quit()
        pg.mixer.music.fadeout(500)

g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
