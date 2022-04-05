from random import choice, random, uniform
import arcade
from src.constants import *
from src.particles import particle
from src.particles.flower import FlowerParticle
from src.actors.animated_sprite import AnimatedSprite

class Junk(AnimatedSprite):

    def __init__(self, game, *args, **kwargs):
        idle_textures = {
            Direction.RIGHT: [choice(game.ass.textures["junk"])],
            Direction.LEFT: [choice(game.ass.textures["junk"])]
        }
        move_textures = {
            Direction.RIGHT: [choice(game.ass.textures["junk"])],
            Direction.LEFT: [choice(game.ass.textures["junk"])]
        }
        super().__init__(idle_textures, move_textures, *args, **kwargs)
        self.game = game

        self.scale = TILE_SCALING * 0.5
        self.boyancy = self.height * self.scale * 0.15 * random()
        self.y_offsets = [-self.boyancy, 0, self.boyancy, 0]
        self.y_offset_idx = 0
        self.boyancy_time = 0
        self.boyancy_max_time = 1 + 0.25 * random()

        self.base_y = self.center_y

        self.sound = "ploof"
        
        self.hp = 5
        self.damage = 1
        self.score = 1

    def on_update(self, delta_time):
        super().on_update(delta_time)
        self.think(delta_time)

    def hit(self, damage):
        ret = super().hit(damage)
        if ret and self.hp <= 0:
            self.game.enemy_list.remove(self)
            particle.flower_explosion(self.game, self.center_x, self.center_y)
            self.game.score -= self.score
        return ret

    def think(self, dt):
        self.boyancy_time += dt
        if self.boyancy_time >= self.boyancy_max_time:
            self.boyancy_time = 0
            self.y_offset_idx = (self.y_offset_idx + 1) % len(self.y_offsets)
        self.center_y = self.base_y + self.y_offsets[self.y_offset_idx]


            


