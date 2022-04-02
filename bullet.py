import arcade
from constants import *

class Bullet(arcade.Sprite):

    def __init__(self, direction, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.direction = direction

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
        if self.left < -self.width or self.right > SCREEN_WIDTH + self.width or self.top > SCREEN_HEIGHT + self.height or self.bottom < -self.height:
            self.sprite_lists[0].remove(self)
