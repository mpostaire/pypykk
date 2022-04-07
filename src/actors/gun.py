import arcade
from src.constants import *

class Gun(arcade.Sprite):

    def __init__(self, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scale = 2
        self.game = game

        self.gun_textures = {
            Direction.RIGHT: self.game.ass.textures["gun_right"],
            Direction.LEFT: self.game.ass.textures["gun_left"]
        }

    def on_update(self, player):
        self.texture = self.gun_textures[player.facing_direction]
        if player.facing_direction == Direction.LEFT:
            self.center_x = player.center_x - player.width / 2
            self.center_y = player.center_y - player.height / 4
        else:
            self.center_x = player.center_x + player.width / 2
            self.center_y = player.center_y - player.height / 4
