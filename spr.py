import pygame as pg
from random import randint, choice
from cons import *

class SpriteSheet(object):

    def __init__(self, path):
        self.sprite_sheet = pg.image.load(path).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface([width, height], ).convert()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(BLACK)
        return image

def clip(surf,x,y,x_size,y_size):
    handle_surf = surf.copy()
    clipR = pg.Rect(x,y,x_size,y_size)
    handle_surf.set_clip(clipR)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()

class Score_counter():

    def __init__(self, path, game, log):
        self.game = game
        self.log = log

        self.character_order = ['0','1','2','3','4','5','6','7','8','9']
        font_img = pg.image.load(path).convert()
        font_img.set_colorkey((0, 0, 0))
        current_char_width = 0
        self.characters = {}
        character_count = 0
        for x in range(font_img.get_width()):
            c = font_img.get_at((x, 0))
            if c[0] == 127:
                char_img = clip(font_img, x - current_char_width, 0, current_char_width, font_img.get_height())
                self.characters[self.character_order[character_count]] = char_img.copy()
                character_count += 1
                current_char_width = 0
            else:
                current_char_width += 1

        self.space_width = self.characters['0'].get_width() * 4
        self.space_width_1 = self.characters['1'].get_width() * 4
        self.len_norm = 0

    def render(self, screen, text, loc):
        x_offset = 0
        ones = text.count("1", 0)
        length = len(text)

        if length > self.len_norm:
            self.len_norm = length
        if self.log == 1:
            new_posx = loc[0] - \
                       ((self.space_width * (self.len_norm - ones)) + (self.space_width_1 * ones)) / 2
        elif self.log == 0:
            new_posx = loc[0] - \
                       ((self.space_width * (self.len_norm - ones)) + (self.space_width_1 * ones))


        for char in text:
            if char != '1':
                screen.blit(pg.transform.scale(self.characters[char], (
                         self.characters[char].get_width() * 4, self.characters[char].get_height() * 4
                                             )), (new_posx + x_offset, loc[1]))

                x_offset += self.characters[char].get_width() * 4
            else:
                screen.blit(pg.transform.scale(self.characters[char], (
                    self.characters[char].get_width() * 4, self.characters[char].get_height() * 4
                )), (new_posx + x_offset, loc[1]))
                x_offset += self.characters[char].get_width() * 4

class Bg_sprite(pg.sprite.Sprite):

    def __init__(self, bg_time):
        pg.sprite.Sprite.__init__(self)
        super().__init__()
        sprite = SpriteSheet("res/bg.png")
        self.image = pg.transform.scale(sprite.get_image(bg_time, 0, 144, 256), (WIDTH, HEIGHT))
        self.rect = self.image.get_rect()
        self.last_update = pg.time.get_ticks()
        self.rect.x = 0
        self.rect.y = 0

    def update(self):
        self.rect.x = 0
        self.rect.y = 0

class Grnd_sprite(pg.sprite.Sprite):

    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        super().__init__()
        sprite = SpriteSheet("res/ground.png")
        self.game = game
        self.image = pg.transform.scale(sprite.get_image(0, 0, 168, 51), (584, 102))
        self.rect = self.image.get_rect()
        self.last_update = pg.time.get_ticks()
        self.rect.x = 0
        self.rect.bottom = HEIGHT


    def update(self):
        if self.game.game_over == False:
            self.x_change = 4
        else:
            self.x_change = 0

        self.rect.x -= self.x_change

        if abs(self.rect.left) >= 34:
            self.rect.x = 0

class Player(pg.sprite.Sprite):

    def __init__(self, game, type):
        pg.sprite.Sprite.__init__(self)
        #super().__init__()
        sprite = SpriteSheet("res/faby.png")
        self.game = game
        #cons for player
        self.current_sprite = 0
        self.counter = 0
        self.delay = 7
        self.velocity = 0
        self.acc_limit = 10

        self.idle = 1.5
        self.clicked = False

        #init player
        self.sprite = []
        self.sprite.append(pg.transform.scale(sprite.get_image(0, type, 17, 12), (51, 36)))
        self.sprite.append(pg.transform.scale(sprite.get_image(17, type, 17, 12), (51, 36)))
        self.sprite.append(pg.transform.scale(sprite.get_image(34, type, 17, 12), (51, 36)))

        self.image = self.sprite[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = (100 , 384)

    def update(self):

        self.counter += 1
        if not self.game.game_over:

            # movement control
            '''additional controls'''
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.game.flying = True
                self.clicked = True
                self.velocity = -10
                pg.mixer.Sound.play(sfx[0])
            if pg.mouse.get_pressed()[0] == 0:
                self.clicked = False

            if self.game.flying:

                # animation handling
                if self.counter > self.delay:
                    self.counter = 0
                    self.current_sprite += 1
                    if self.current_sprite >= 3:
                        self.current_sprite = 0

                self.image = self.sprite[self.current_sprite]
                self.image = pg.transform.rotate(self.sprite[self.current_sprite], self.velocity * -2)

                #physics handing
                self.acceleration = 0.5

            else:
                self.acceleration = 0
                if self.counter > self.delay:
                    self.counter = 0
                    self.current_sprite += 1
                    if self.current_sprite >= 3:
                        self.current_sprite = 0


                if self.rect.y > 404:
                    self.idle = -1
                elif self.rect.y < 364:
                    self.idle = 1.5

                self.rect.y += self.idle
                self.image = self.sprite[self.current_sprite]

        else:
            self.image = pg.transform.rotate(self.sprite[self.current_sprite], -90)
            self.acceleration = 1

        self.velocity += self.acceleration

        if self.velocity > self.acc_limit:
            self.velocity = self.acc_limit

        if self.rect.bottom < 666:
            self.rect.y += int(self.velocity)
        # end game
        elif self.rect.bottom >= 666:
            if not self.game.game_over:
                pg.mixer.Sound.play(sfx[2])
            self.game.flying = False
            self.game.game_over = True

class Pipe(pg.sprite.Sprite):

    def __init__(self, game, pos, y, pipe_type):
        pg.sprite.Sprite.__init__(self)
        sprite = SpriteSheet("res/pipes.png")
        self.image = pg.transform.scale(sprite.get_image(pipe_type, 0, 26, 160), (78, 560))
        self.game = game
        self.rect = self.image.get_rect()
        self.pipe_gap = 75
        self.pipe_height = randint(-100, 100)
        #pipe position
        if pos == 1:
            self.image = pg.transform.flip(self.image, False, True)
            self.rect.bottomleft = [WIDTH, y  - self.pipe_gap]
        if pos == -1:
            self.rect.topleft = [WIDTH, y + self.pipe_gap]

    def update(self):
        if not self.game.game_over and self.game.flying:
            self.scroll_speed = 4
        else:
            self.scroll_speed = 0

        self.rect.x -= self.scroll_speed

        if self.rect.right < 0:
            self.kill()

class Instruction_sprite(pg.sprite.Sprite):

    def __init__(self, game, part):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.part = part
        self.prt = [
            [97, 0, 59, 51],
            [0, 0, 92, 25]
        ]
        self.scale = [self.prt[self.part][2] * 3, self.prt[self.part][3] * 3]
        self.new_scale = [self.prt[self.part][2] * 3, self.prt[self.part][3] * 3]
        self.scale_change = [3, 1]

        self.image = pg.transform.scale(SpriteSheet("res/options.png").get_image(self.prt[self.part][0], self.prt[self.part][1],
                                                                                 self.prt[self.part][2], self.prt[self.part][3]),
                                        (self.scale[0], self.scale[1]))
        self.rect = self.image.get_rect()
        if self.part == 0:
            self.rect.center = (216, 484)
        elif self.part == 1:
            self.rect.center = (216, 150)
        self.int_opacity = self.image.set_alpha(255)
        self.opacity = self.image.get_alpha()

    def update(self):
        if self.new_scale[0] < self.scale[0] - 10:
            self.scale_change = [1, 1]
        elif self.new_scale[0] > self.scale[0] + 10:
            self.scale_change = [-1, -1]

        self.new_scale[0] += self.scale_change[0]
        self.new_scale[1] += self.scale_change[1]

        self.image = pg.transform.scale(SpriteSheet("res/options.png").get_image(self.prt[self.part][0], self.prt[self.part][1],
                                                                                 self.prt[self.part][2], self.prt[self.part][3]),
                                        (self.new_scale[0], self.new_scale[1]))
        self.rect = self.image.get_rect()
        if self.part == 0:
            self.rect.center = (216, 484)
        elif self.part == 1:
            self.rect.center = (216, 150)

        if self.game.flying:

            self.opacity -= 5
            self.image.set_alpha(self.opacity)

            if self.opacity <= 0:
                self.kill()

class Buttons(pg.sprite.Sprite):
    def __init__(self, index, pos):
        pg.sprite.Sprite.__init__(self)
        self.index = index
        self.sprite_up = []
        self.sprite_down = []
        for x in range(9):
            self.sprite_up.append(pg.transform.scale(
                SpriteSheet("res/options.png").get_image(game_buttons[x][0], game_buttons[x][1], game_buttons[x][2],game_buttons[x][3]),
                (game_buttons[x][2] * 3, game_buttons[x][3] * 3))
            )
        for x in range(9):
            self.sprite_down.append(pg.transform.scale(
                SpriteSheet("res/options.png").get_image(game_buttons[x][0], game_buttons[x][1], game_buttons[x][2], game_buttons[x][3] - 1),
                (game_buttons[x][2] * 3, game_buttons[x][3] * 3))
            )
        self.image = self.sprite_up[self.index]
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = self.pos

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_clicked(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.image = self.sprite_down[self.index]
                    self.rect.center = (self.rect.centerx, self.rect.centery + 1)
                    pg.mixer.Sound.play(sfx[5])
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.image = self.sprite_up[self.index]
                    self.rect.center = self.pos
                    pg.mixer.Sound.play(sfx[6])
                    return self.rect.collidepoint(event.pos)

class Title(pg.sprite.Sprite):
    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self)
        self.scale = [title[0][2] * 3, title[0][3] * 3]
        self.title =  pg.transform.scale(SpriteSheet("res/options.png").get_image(title[0][0], title[0][1],
                                                                                  title[0][2], title[0][3]),
                                        [title[0][2] * 3, title[0][3] * 3])

        self.title_rect = self.title.get_rect()
        self.title_rect.topleft = pos

        bird_sprite = [
            (0, 0, 17, 12),
            (17, 0, 17, 12),
            (34, 0, 17, 12)
        ]
        self.bird_list = []
        self.index_bird = 0  # randint(0, 2)

        self.counter = 0
        self.counter2 = 0
        self.delay = 7
        self.delay2 = 2
        self.move = 1

        for x in range(3):
            self.bird_list.append(
                pg.transform.scale(SpriteSheet("res/faby.png").get_image(bird_sprite[x][0], bird_sprite[x][1],
                                                                         bird_sprite[x][2], bird_sprite[x][3]),
                                   [bird_sprite[x][2] * 4, bird_sprite[x][3] * 4]))

        self.image = self.bird_list[self.index_bird]
        self.rect = self.image.get_rect()
        self.rect.midleft = (self.title_rect.right + 13, self.title_rect.centery - 5)

    def update(self):
        self.counter += 1
        self.counter2 += 1
        if self.counter > self.delay:
            self.counter = 0
            self.index_bird += 1
            if self.index_bird > 2:
                self.index_bird = 0

        if self.rect.y > 120:
            self.move = -1
        elif self.rect.y < 110:
            self.move = 1
        if self.counter2 > self.delay2:
            self.counter2 = 0
            self.rect.y += self.move
            self.title_rect.y += self.move

        self.image = self.bird_list[self.index_bird]

    def draw(self, screen):
        screen.blit(self.title, self.title_rect)
        screen.blit(self.image, self.rect)

class Gameover_sprite(pg.sprite.Sprite):

    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.board = pg.transform.scale(SpriteSheet("res/options.png").get_image(0, 142, 113, 57), (113 * 3, 57 * 3))
        self.medal_list = []
        self.counter = 0
        self.delay = 10
        self.vel = 15
        self.board_height_limit = 334

        for x in range(5):
            self.medal_list.append(pg.transform.scale(SpriteSheet("res/options.png").get_image(medal[x][0], medal[x][1],
                                                                                          medal[x][2], medal[x][3]),
                               (medal[x][2] * 3, medal[x][3] * 3)))

        self.go_title = pg.transform.scale(SpriteSheet("res/options.png").get_image(0, 25, 96, 21), (96 * 4, 21 * 4))
        self.go_title_rect = self.go_title.get_rect()
        self.go_title_rect.center = (216, 200)
        self.go_title.set_alpha(0)
        self.opacity = self.go_title.get_alpha()

        self.board_rect = self.board.get_rect()
        self.board_rect.midtop = (216, HEIGHT)

        self.type = 0
        self.medal = self.medal_list[self.type]
        self.medal_rect = self.medal.get_rect()
        self.medal_rect.center = (120, self.board_height_limit + 95)
        self.tally = True

        self.new_best = pg.transform.scale(SpriteSheet("res/options.png").get_image(98, 54, 16, 7), (16 * 3, 7 * 3))
        self.new_best_rect = self.new_best.get_rect()
        self.new_best_rect.center = (256, 366)

        self.score = Score_counter("res/num_s.png", self.game, 0)
        self.high_score = Score_counter("res/num_s.png", self.game, 0)

    def check_score(self):
        if self.game.score in range(10, 20):
            self.type = 0
            if self.tally:
                self.game.bron_medal += 1
                with open(high_score, 'r') as medal_file:
                    medal_readline = medal_file.readlines()
                    medal_readline[1] = str(self.game.bron_medal) + "\n"
                with open(high_score, 'w') as medal_file:
                    medal_file.writelines(medal_readline)
                medal_file.close()
                self.tally = False

        elif self.game.score in range(20, 30):
            self.type = 1
            if self.tally:
                self.game.silv_medal += 1
                with open(high_score, 'r') as medal_file:
                    medal_readline = medal_file.readlines()
                    medal_readline[2] = str(self.game.silv_medal) + "\n"
                with open(high_score, 'w') as medal_file:
                    medal_file.writelines(medal_readline)
                medal_file.close()
                self.tally = False

        elif self.game.score in range(30, 50):
            self.type = 2
            if self.tally:
                self.game.gold_medal += 1
                with open(high_score, 'r') as medal_file:
                    medal_readline = medal_file.readlines()
                    medal_readline[3] = str(self.game.gold_medal) + "\n"
                with open(high_score, 'w') as medal_file:
                    medal_file.writelines(medal_readline)
                medal_file.close()
                self.tally = False

        elif self.game.score in range(50, 100):
            self.type = 3
            if self.tally:
                self.game.plat_medal += 1
                with open(high_score, 'r') as medal_file:
                    medal_readline = medal_file.readlines()
                    medal_readline[4] = str(self.game.plat_medal) + "\n"
                with open(high_score, 'w') as medal_file:
                    medal_file.writelines(medal_readline)
                medal_file.close()
                self.tally = False

        elif self.game.score >= 100:
            self.type = 4
            if self.tally:
                self.game.dia_medal += 1
                with open(high_score, 'r') as medal_file:
                    medal_readline = medal_file.readlines()
                    medal_readline[5] = str(self.game.dia_medal) + "\n"
                with open(high_score, 'w') as medal_file:
                    medal_file.writelines(medal_readline)
                medal_file.close()
                self.tally = False

        return

    def update(self):

        if self.opacity >= 255:
            self.opacity = 255

        if self.board_rect.y >= self.board_height_limit:
            self.board_rect.y -= self.vel
        else:
            self.counter += 1
            self.opacity += 15
            if self.counter >= self.delay:
                self.counter = self.delay



        self.go_title.set_alpha(self.opacity)
        self.medal = self.medal_list[self.type]

    def draw(self, screen):
        screen.blit(self.board, self.board_rect)
        screen.blit(self.go_title, self.go_title_rect)

        if self.board_rect.y <= self.board_height_limit:
            self.game.menu_but.draw(screen)
            self.game.restart_but.draw(screen)
            self.score.render(screen, str(self.game.score), (350, 384))
            self.high_score.render(screen, str(self.game.high_score_rec), (350, 444))
            if self.game.score >= self.game.high_score_rec:
                if self.game.score != 0:
                    screen.blit(self.new_best, self.new_best_rect)
            if self.counter == self.delay:
                if self.game.score >= 10:
                    screen.blit(self.medal, self.medal_rect)