import arcade
from src.constants import *
import random

class FlowerParticle(arcade.Sprite):

    def __init__(self, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scale = random.uniform(0.5, 1)

        self.game = game

        flower_textures = arcade.load_spritesheet("assets/flowers.png", 32, 32, 15, 45)
        self.texture = random.choice(flower_textures)
        self.elapsed = 0

        self.vel_x = random.uniform(-150, 150)
        self.vel_y = random.uniform(50, 500)

    def on_update(self, delta_time):
        self.elapsed += delta_time

        percent_elapsed = self.elapsed / PARTICLE_TIME
        self.alpha = max(255 - (percent_elapsed * 255), 0)

        self.center_x += self.vel_x * delta_time
        self.vel_y -= GRAVITY * 16
        self.center_y += self.vel_y * delta_time

        if self.elapsed >= PARTICLE_TIME:
            self.game.particle_list.remove(self)
