import arcade
from src.constants import *

class Gun(arcade.Sprite):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scale = SPRITE_SCALING * 4

        self.gun_textures = {
            Direction.RIGHT: arcade.load_texture("assets/gun.png"),
            Direction.LEFT: arcade.load_texture("assets/gun.png", flipped_horizontally=True)
        }

    def on_update(self, player):
        self.texture = self.gun_textures[player.facing_direction]
        if player.facing_direction == Direction.LEFT:
            self.center_x = player.center_x - player.width / 2
            self.center_y = player.center_y - player.height / 4
        else:
            self.center_x = player.center_x + player.width / 2
            self.center_y = player.center_y - player.height / 4
