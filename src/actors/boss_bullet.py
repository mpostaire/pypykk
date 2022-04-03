import arcade
from src.constants import *
import random

class BossBullet(arcade.Sprite):

    def __init__(self, direction, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scale = 0.8
        self.direction = direction
        self.game = game

        self.all_textures = self.game.ass.textures["junk"]
        self.texture = random.choice(self.all_textures)

        self.damage = 1

    def on_update(self, delta_time):
        """ Move the bullet """
        if self.direction == Direction.UP:
            self.center_y += (BULLET_SPEED / 3) * delta_time
        elif self.direction == Direction.DOWN:
            self.center_y -= (BULLET_SPEED / 3) * delta_time
        elif self.direction == Direction.RIGHT:
            self.center_x += (BULLET_SPEED / 3) * delta_time
        elif self.direction == Direction.LEFT:
            self.center_x -= (BULLET_SPEED / 3) * delta_time
        elif self.direction == Direction.UP_LEFT:
            self.center_x -= ((BULLET_SPEED / 3) / 1.41) * delta_time
            self.center_y += ((BULLET_SPEED / 3) / 1.41) * delta_time
        elif self.direction == Direction.UP_RIGHT:
            self.center_x += ((BULLET_SPEED / 3) / 1.41) * delta_time
            self.center_y += ((BULLET_SPEED / 3) / 1.41) * delta_time
        elif self.direction == Direction.DOWN_LEFT:
            self.center_x -= ((BULLET_SPEED / 3) / 1.41) * delta_time
            self.center_y -= ((BULLET_SPEED / 3) / 1.41) * delta_time
        elif self.direction == Direction.DOWN_RIGHT:
            self.center_x += ((BULLET_SPEED / 3) / 1.41) * delta_time
            self.center_y -= ((BULLET_SPEED / 3) / 1.41) * delta_time

        # Check for out-of-bounds
        if self.center_x > self.game.camera.position[0] + self.game.camera.viewport_width or self.center_x < self.game.camera.position[0] or self.center_y > self.game.camera.position[1] + self.game.camera.viewport_height or self.center_y < self.game.camera.position[1]:
            self.sprite_lists[0].remove(self)
