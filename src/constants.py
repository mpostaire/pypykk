from enum import Enum
import arcade

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
BULLET_SPEED = 800
BULLET_RATE = 0.2

TILE_SCALING = 2.5
GRAVITY = 1.0

PLAYER_MOVEMENT_SPEED = 1
PLAYER_JUMP_SPEED =10
PLAYER_AIR_DECELERATE = 5
PLAYER_JUMP_DURATION = 0.15

PARTICLE_TIME = 2

# TODO add explosion sound
sounds = {
    "game_over": arcade.load_sound("assets/yaaaoooow.wav"),
    "pew": [
        arcade.load_sound("assets/pew_00.mp3"),
        arcade.load_sound("assets/pew_01.mp3"),
        arcade.load_sound("assets/pew_02.mp3")
    ],
    "ploof": [
        arcade.load_sound("assets/ploof_00.wav"),
        arcade.load_sound("assets/ploof_01.wav"),
        arcade.load_sound("assets/ploof_02.wav")
    ],
    "vroom": [
        arcade.load_sound("assets/vroom_00.mp3"),
        arcade.load_sound("assets/vroom_01.mp3"),
        arcade.load_sound("assets/vroom_02.mp3")
    ],
    "step": arcade.load_sound("assets/step.wav"),  # FIXME this sound is horrible for the ears in game
    "oof": [
        arcade.load_sound("assets/oof_00.wav"),
        arcade.load_sound("assets/oof_01.wav")
    ],
    "music": arcade.load_sound("assets/Gilles Stella - Libre de droit.m4a")
}
