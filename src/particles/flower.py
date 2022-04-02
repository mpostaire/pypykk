import arcade
from src.constants import *
import random

class FlowerParticle(arcade.Sprite):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scale = SPRITE_SCALING * 3

        flower_textures = arcade.load_spritesheet("assets/flowers.png", 32, 32, 15, 45)
        self.texture = random.choice(flower_textures)

    def on_update(self, delta_time):
        pass
