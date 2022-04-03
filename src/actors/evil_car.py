import arcade
from random import random
from src.constants import *
from src.particles import particle
from src.particles.flower import FlowerParticle

class EvilCar(arcade.Sprite):

    def __init__(self, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scale = SPRITE_SCALING
        self.facing_direction = Direction.RIGHT

        self.car_textures = {
            Direction.RIGHT: arcade.load_spritesheet("assets/evil_car_0_right.png", 576//2, 118, 2, 2),
            Direction.LEFT: arcade.load_spritesheet("assets/evil_car_0_left.png", 576//2, 118, 2, 2),
        }
        self.game = game
        self.cur_texture = 0
        self.texture = self.car_textures[self.facing_direction][self.cur_texture]
        self.texture_time = 0
        self.state = 'spawning'
        self.speed = 300 + random() * 150
        self.dir = 1
        self.gravity = 10
        self.scale = TILE_SCALING * 0.25

        self.smoke_time = 0

        self.blink_time = 0
        self.blink_ammount = 4
        self.blink = self.blink_ammount

        self.hp = 5
        self.damage = 1

    def update_animation(self, delta_time):
        self.texture_time += delta_time

        if (self.change_x != 0 or self.change_y != 0) and self.texture_time > 0.05:
            self.texture_time = 0
            self.cur_texture = (self.cur_texture + 1) % len(self.car_textures[self.facing_direction])
            self.texture = self.car_textures[self.facing_direction][self.cur_texture]
        elif (self.change_x == 0 and self.change_y == 0):
            if self.cur_texture != 0:
                self.texture_time = 0
                self.cur_texture = 0
            self.texture = self.car_textures[self.facing_direction][self.cur_texture]

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
        """ Move the player """
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
            self.game.score -= 2
        return True

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

            


