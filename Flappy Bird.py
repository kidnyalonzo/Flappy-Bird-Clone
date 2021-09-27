import sys
from webbrowser import open_new_tab

import winxpgui

from spr import *

start = True

class Game:
    def __init__(self):
        pg.init()
        #pg.mixer.init()
        self.menu_running, self.game_running, self.game_over, self.flying = True, False, False, False
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), 0)
        pg.display.set_caption(TITLE)
        pg.display.set_icon(pg.image.load(ICON))
        self.score_counter = Score_counter("res/num_b.png", self, 1)

        self.clock = pg.time.Clock()

        self.sound_sys()
        #record the last best in the program temporarily. Will change if new high score was met by high score checker
        with open(high_score, 'r') as score_open:
            score_readline = score_open.readlines()
            self.high_score_rec = int(score_readline[0])
            self.bron_medal = int(score_readline[1])
            self.silv_medal = int(score_readline[2])
            self.gold_medal = int(score_readline[3])
            self.plat_medal = int(score_readline[4])
            self.dia_medal = int(score_readline[5])

        self.bg_general = pg.sprite.Group()
        self.bg_general.add(Bg_sprite(0))
        self.bg_general.add(Grnd_sprite(self))

    def sound_sys(self):
        for snd in sfx_list:
            sfx.append(pg.mixer.Sound(snd))

    def high_score_check(self):
        with open(high_score, 'r') as score_open:
            score_readline = score_open.readlines()
            last = int(score_readline[0])
        if last <= int(self.score):
            score_readline[0] = str(self.score) + "\n"
            self.high_score_rec = self.score
            with open(high_score, 'w') as score_open:
                score_open.writelines(score_readline)
            return self.score
        elif last > int(self.score):
            return self.score
        score_open.close()

        return last



    def new_pipe(self):
        self.pipe_height = randint(-100, 100)
        t = Pipe(self, 1, int(HEIGHT / 2) + self.pipe_height, self.pipe_type)
        b = Pipe(self, -1, int(HEIGHT / 2) + self.pipe_height, self.pipe_type)
        self.pipe_sprites.add(t)
        self.pipe_sprites.add(b)

    def start(self):
        self.game_running, self.menu_running, self.game_over, self.flying = True, False, False, False
        #pipe
        self.pipe_frequency = 1500
        pass_pipe = False
        self.last_pipe = pg.time.get_ticks() - self.pipe_frequency
        self.score = 0
        self.score_limit = 1000000


        '''sprite adding, make this compact'''

        self.plyr_sprite = pg.sprite.Group()
        self.pipe_sprites = pg.sprite.Group()

        day = choice([0, 146])

        if day == 0:
            self.pipe_type = 26
        elif day == 146:
            self.pipe_type = 0

        self.background = pg.sprite.Group()
        self.foreground = pg.sprite.Group()
        self.background.add(Bg_sprite(day))
        self.foreground.add(Grnd_sprite(self))

        player = choice([0, 13, 26])
        self.plyr_sprite.add(Player(self, player))
        self.foreground.add(Instruction_sprite(self, 0))
        self.foreground.add(Instruction_sprite(self, 1))
        self.test_go = Gameover_sprite(self)

        '''buttons'''
        self.menu_but = Buttons(2, (116, 600))
        self.restart_but = Buttons(3, (316, 600))

        while self.game_running:
            self.clock.tick(fps)

            if self.flying:
                self.time_now = pg.time.get_ticks()
            else:
                self.time_now = 0

            if self.time_now - self.last_pipe > self.pipe_frequency:
                self.new_pipe()
                self.last_pipe = self.time_now

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if self.game_over == True:
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            g.menu()
                    if self.menu_but.is_clicked(event):
                        g.menu()
                    if self.restart_but.is_clicked(event):
                        g.start()

            #collision
            if pg.sprite.groupcollide(self.pipe_sprites, self.plyr_sprite, False, False) and not self.game_over:
                pg.mixer.Sound.play(sfx[2])
                pg.mixer.Sound.play(sfx[3])
                self.game_over = True

            self.background.update()
            self.plyr_sprite.update()
            self.pipe_sprites.update()
            self.foreground.update()
            self.background.draw(self.screen)
            self.pipe_sprites.draw(self.screen)
            self.plyr_sprite.draw(self.screen)
            self.foreground.draw(self.screen)


            # score
            if len(self.pipe_sprites) > 0:
                if self.plyr_sprite.sprites()[0].rect.left > self.pipe_sprites.sprites()[0].rect.left \
                        and self.plyr_sprite.sprites()[0].rect.right < self.pipe_sprites.sprites()[0].rect.right \
                        and pass_pipe == False:
                    pass_pipe = True
                if pass_pipe:
                    if self.plyr_sprite.sprites()[0].rect.left > self.pipe_sprites.sprites()[0].rect.right:
                        pg.mixer.Sound.play(sfx[1])
                        self.score += 1
                        pass_pipe = False

            if self.flying:
                self.score_counter.render(self.screen, str(self.score), (216, 100))

            if self.game_over == True:
                self.high_score_check()
                self.test_go.check_score()
                self.test_go.update()
                self.menu_but.update()
                self.restart_but.update()
                self.test_go.draw(self.screen)
            pg.display.flip()

    def menu(self):
        self.game_running, self.menu_running, self.game_over, self.flying, self.scoremenu_running = False, True, False, False, False

        self.button_sprites = pg.sprite.Group()
        buttons = [
            Buttons(5, (216, 309)),
            Buttons(6, (216, 369)),
            Buttons(7, (216, 429)),
            Buttons(8, (216, 489))
        ]
        for i in buttons:
            self.button_sprites.add(i)

        self.title = Title((41, 120))

        while self.menu_running:
            self.clock.tick(fps)

            self.bg_general.update()
            self.bg_general.draw(self.screen)

            self.title.update()
            self.button_sprites.update()
            self.title.draw(self.screen)
            self.button_sprites.draw(self.screen)

            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()
                    if event.key == pg.K_f:
                        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)

                if buttons[0].is_clicked(event):
                    g.start()
                if buttons[1].is_clicked(event):
                    g.score_menu()
                if buttons[2].is_clicked(event):
                    open_new_tab('https://zakdionlyon.itch.io/flappy-bird-clone')
                if buttons[3].is_clicked(event):
                    open_new_tab('https://www.facebook.com/sharer/sharer.php?u=https://zakdionlyon.itch.io/flappy-bird-clone')

    def score_menu(self):
        self.scoremenu_running, self.menu_running = True, False

        '''board'''
        board = pg.transform.scale(SpriteSheet("res/options.png").get_image(0, 200, 113, 173), (113 * 3, 173 * 3))
        board_rect = board.get_rect()
        board_rect.center = (216, 304)

        '''buttons'''
        self.menu_but = Buttons(2, (216,  600))

        '''best score and medal amount display'''
        best_score = Score_counter("res/num_s.png", self, 1)
        achievements = []
        for x in range(5):
            achievements.append(Score_counter("res/num_s.png", self, 0))

        while self.scoremenu_running:
            self.clock.tick(fps)

            self.bg_general.update()
            self.menu_but.update()
            self.bg_general.draw(self.screen)

            self.screen.blit(board, board_rect)

            best_score.render(self.screen, str(self.high_score_rec), (216, 494))
            achievements[0].render(self.screen, str(self.bron_medal), (344, 98))
            achievements[1].render(self.screen, str(self.silv_medal), (344, 172))
            achievements[2].render(self.screen, str(self.gold_medal), (344, 245))
            achievements[3].render(self.screen, str(self.plat_medal), (344, 319))
            achievements[4].render(self.screen, str(self.dia_medal), (344, 392))
            self.menu_but.draw(self.screen)
            pg.display.flip()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        g.menu()
                if self.menu_but.is_clicked(event):
                    g.menu()



g = Game()

g.menu()
