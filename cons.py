fps = 60

WIDTH = 432
HEIGHT = 768

FS_WIDTH = 768
FS_HEIGHT = 768

TITLE = "Flappy Bird"
ICON = "res/icon.png"

BLACK = (0, 0, 0)

#score data handling
high_score = 'gw3RMV2pqwe-34.dat'

#x, y, width, height
title = [
    (0, 47, 89, 24)
]

medal = [
    (0, 72, 22, 22),
    (22, 72, 22, 22),
    (44, 72, 22, 22),
    (66, 72, 22, 22),
    (88, 72, 22, 22),
]

game_buttons = [
    (0, 96, 13, 14), #pause 0
    (42, 111, 13, 14), #play 1
    (14, 96, 40, 14), #menu 2
    (56, 111, 39, 14), #restart 3
    (55, 96, 40, 14), #ok 4
    (0, 126, 40, 14), #start  5
    (96, 111, 40, 14), #score 6
    (96, 96, 39, 14), #rate 7
    (0, 111, 40, 14), #share 8
]

sfx = []
sfx_list = [
    'res/flap.wav',
    'res/point.wav',
    'res/hit.wav',
    'res/die.wav',
    'res/swoosh_board.wav',
    'res/select_1.wav',
    'res/select_0.wav'
]