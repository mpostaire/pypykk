from enum import Enum

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    UP_LEFT = 4
    UP_RIGHT = 5
    DOWN_LEFT = 6
    DOWN_RIGHT = 7

SPRITE_SCALING = 0.2

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Treta Gunberg"

MOVEMENT_SPEED = 200
BULLET_SPEED = 400
BULLET_RATE = 0.2

TILE_SCALING = 2.5
GRAVITY = 1.0

PLAYER_MOVEMENT_SPEED = 1
PLAYER_JUMP_SPEED = 15
PLAYER_AIR_DECELERATE = 5
PLAYER_JUMP_DURATION = 0.1
