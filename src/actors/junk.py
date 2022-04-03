from random import choice, random
import arcade
from src.constants import *
from src.particles import particle
from src.particles.flower import FlowerParticle

class Junk(arcade.Sprite):

    def __init__(self, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scale = SPRITE_SCALING
        self.facing_direction = Direction.RIGHT
        dims = [
            (16, 45),
            (39, 55),
            (36, 44),
            (51, 48)
        ]
        self.all_textures = [
            arcade.load_texture(f'assets/junk_0{i}.png', width=dims[i][0], height=dims[i][1])
            for i in range(3)
        ]
        self.game = game
        self.cur_texture = 0
        self.texture = choice(self.all_textures)
        self.scale = TILE_SCALING * 0.5
        self.boyancy = self.height * self.scale * 0.15 * random()
        self.y_offsets = [-self.boyancy, 0, self.boyancy, 0]
        self.y_offset_idx = 0
        self.boyancy_time = 0
        self.boyancy_max_time = 1 + 0.25*random()
        self.blink_time = 0
        self.blink_ammount = 4
        self.blink = self.blink_ammount
        self.base_y = self.center_y

        self.hp = 5
        self.damage = 1


    def on_update(self, delta_time):

        self.think(delta_time)
        # blink on hit
        self.blink_time += delta_time
        if self.blink < self.blink_ammount and self.blink_time >= 0.06:
            self.blink += 1
            self.blink_time = 0
            self.alpha = 255 if self.alpha == 0 else 0
        elif self.blink >= self.blink_ammount:
            self.alpha = 255

    def hit(self, damage):
        if self.blink < self.blink_ammount:
            return False

        self.hp -= damage

        self.blink = 0
        self.blink_time = 0

        if self.hp <= 0:
            self.game.enemy_list.remove(self)
            particle.flower_explosion(self.game, self.center_x, self.center_y)
        return True

    def think(self, dt):
        self.boyancy_time += dt
        if self.boyancy_time >= self.boyancy_max_time:
            self.boyancy_time = 0
            self.y_offset_idx = (self.y_offset_idx + 1) % len(self.y_offsets)
        self.center_y = self.base_y + self.y_offsets[self.y_offset_idx]


            


