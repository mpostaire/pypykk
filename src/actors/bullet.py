import arcade
from src.constants import *

class Bullet(arcade.Sprite):

    def __init__(self, direction, camera, player, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scale = SPRITE_SCALING
        self.direction = direction
        self.camera = camera
        self.player = player

    def on_update(self, delta_time):
        """ Move the bullet """
        if self.direction == Direction.UP:
            self.center_y += BULLET_SPEED * delta_time
        elif self.direction == Direction.DOWN:
            self.center_y -= BULLET_SPEED * delta_time
        elif self.direction == Direction.RIGHT:
            self.center_x += BULLET_SPEED * delta_time
        elif self.direction == Direction.LEFT:
            self.center_x -= BULLET_SPEED * delta_time
        elif self.direction == Direction.UP_LEFT:
            self.center_x -= (BULLET_SPEED / 1.41) * delta_time
            self.center_y += (BULLET_SPEED / 1.41) * delta_time
        elif self.direction == Direction.UP_RIGHT:
            self.center_x += (BULLET_SPEED / 1.41) * delta_time
            self.center_y += (BULLET_SPEED / 1.41) * delta_time
        elif self.direction == Direction.DOWN_LEFT:
            self.center_x -= (BULLET_SPEED / 1.41) * delta_time
            self.center_y -= (BULLET_SPEED / 1.41) * delta_time
        elif self.direction == Direction.DOWN_RIGHT:
            self.center_x += (BULLET_SPEED / 1.41) * delta_time
            self.center_y -= (BULLET_SPEED / 1.41) * delta_time

        # Check for out-of-bounds
        if self.center_x > self.camera.position[0] + self.camera.viewport_width or self.center_x < self.camera.position[0] or self.center_y > self.camera.position[1] + self.camera.viewport_height or self.center_y < self.camera.position[1]:
            self.sprite_lists[0].remove(self)
