import arcade
import random
from src.constants import *
from src.particles import particle
from src.actors.animated_sprite import AnimatedSprite

class EvilCar(AnimatedSprite):

    def __init__(self, game, *args, **kwargs):
        idle_textures = {
            Direction.RIGHT: game.ass.textures["evil_car_right"],
            Direction.LEFT: game.ass.textures["evil_car_left"]
        }
        move_textures = {
            Direction.RIGHT: game.ass.textures["evil_car_right"],
            Direction.LEFT: game.ass.textures["evil_car_left"]
        }
        super().__init__(idle_textures, move_textures, *args, **kwargs)
        self.game = game

        self.state = 'spawning'
        self.speed = 300 + random.random() * 150
        self.dir = 1
        self.gravity = 10
        self.scale = TILE_SCALING * 0.25

        self.smoke_time = 0

        self.sound = "vroom"

        self.hp = 5
        self.damage = 1
        self.score = 2

    def update_animation(self, delta_time):
        super().update_animation(delta_time)

        self.smoke_time += delta_time
        if self.smoke_time > 0.5:
            self.smoke_time = 0
            smoke_x = 0
            if self.facing_direction == Direction.RIGHT:
                smoke_x = self.center_x - self.width / 2
            else:
                smoke_x = self.center_x + self.width / 2
            particle.smoke(self.game, smoke_x, self.center_y)

    def on_update(self, delta_time):
        if self.state == 'spawning':
            self.think(delta_time)
            self.change_x = 0
            self.change_y = - self.gravity
        else:
            self.think(delta_time)
            self.change_y = 0
            self.change_x = self.dir * self.speed
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time

        self.update_animation(delta_time)

        self.blink_animation(delta_time)

        self.update_sound(delta_time)

    def hit(self, damage):
        ret = super().hit(damage)
        if ret and self.hp <= 0:
            self.game.enemy_list.remove(self)
            particle.flower_explosion(self.game, self.center_x, self.center_y)
            self.game.score -= self.score
        return ret

    def think(self, dt):
        wall_hit_list = arcade.check_for_collision_with_list(
            self,
            self.game.scene['walls']
        )
        if self.state == 'spawning':
            if len(wall_hit_list) > 0:
                self.state = 'active'
                self.center_y += self.gravity * dt * 2
                
        else:
            if len(wall_hit_list) > 0:
                self.dir *= - 1
                if self.facing_direction == Direction.RIGHT:
                    self.facing_direction = Direction.LEFT
                else:
                    self.facing_direction = Direction.RIGHT
