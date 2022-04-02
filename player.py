import arcade
from constants import *

class Player(arcade.Sprite):

    def on_update(self, delta_time):
        """ Move the player """
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time

        # Check for out-of-bounds
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1
