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

MUTED_STATUS = False

CAMERA_MOVE_SPEED = 0.5

# When arcade Camera.zoom() will be implemented, these will not be necessary to zoom the screen
# (utils function to voncert coordinates will be useless as well)
SPRITE_SCALING = 3
TILE_SCALING = 2.5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Treta Gunberg"

BULLET_SPEED = 800
BULLET_RATE = 0.2

GRAVITY = 1.0

PLAYER_HP = 6
PLAYER_MOVEMENT_SPEED = 200
PLAYER_JUMP_SPEED = 600
PLAYER_JUMP_DURATION = 0.2

PARTICLE_TIME = 2

STARTING_LEVEL = 0
STARTING_SCORE = 10
