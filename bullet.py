import arcade
from constants import *

class Bullet(arcade.Sprite):

    def __init__(self, direction, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.direction = direction

    def on_update(self, delta_time):
        """ Move the bullet """
        if self.direction == "up":
            self.center_y += BULLET_SPEED * delta_time
        elif self.direction == "down":
            self.center_y -= BULLET_SPEED * delta_time
        elif self.direction == "right":
            self.center_x += BULLET_SPEED * delta_time
        elif self.direction == "left":
            self.center_x -= BULLET_SPEED * delta_time

        # Check for out-of-bounds
        if self.left < -self.width or self.right > SCREEN_WIDTH + self.width or self.top > SCREEN_HEIGHT + self.height or self.bottom < -self.height:
            self.sprite_lists[0].remove(self)
