import arcade
from src.constants import *
import random

class SmokeParticle(arcade.Sprite):

    def __init__(self, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scale = random.uniform(0.75, 2)

        self.game = game

        flower_textures = arcade.load_spritesheet("assets/smoke.png", 16, 16, 2, 3)
        self.texture = random.choice(flower_textures)
        self.elapsed = 0

        self.vel_y = random.uniform(50, 150)

        self.max_time = PARTICLE_TIME / 2

    def on_update(self, delta_time):
        self.elapsed += delta_time

        percent_elapsed = self.elapsed / self.max_time
        self.alpha = max(255 - (percent_elapsed * 255), 0)

        self.center_y += self.vel_y * delta_time

        if self.elapsed >= self.max_time:
            self.game.particle_list.remove(self)
