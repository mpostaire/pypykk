import arcade
import random
from src.constants import *
from src.particles import particle
from src.particles.flower import FlowerParticle
from src.actors.boss_bullet import BossBullet
from math import sin

class Boss(arcade.Sprite):

    def __init__(self, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scale = SPRITE_SCALING
        self.facing_direction = Direction.RIGHT
        self.game = game

        self.car_textures = {
            Direction.RIGHT: self.game.ass.textures["boss_car_right"],
            Direction.LEFT: self.game.ass.textures["boss_car_left"],
        }
        self.game = game
        self.cur_texture = 0
        self.texture = self.car_textures[self.facing_direction][self.cur_texture]
        self.texture_time = 0
        self.state = 'active'
        self.speed = 300 + random.random() * 150
        self.time_alive = 0
        self.dir = 1
        self.gravity = 10
        self.scale = TILE_SCALING * 0.25

        self.smoke_time = 0

        self.blink_time = 0
        self.blink_ammount = 4
        self.blink = self.blink_ammount

        self.sound_time = 0
        self.sound_max = random.uniform(1, 3)

        self.shoot_time = 0
        self.shoot_max = random.uniform(0.5, 1)

        self.hp = 5 + self.game.score
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
        if self.smoke_time > 0.01:
            self.smoke_time = 0
            smoke_x = 0
            if self.facing_direction == Direction.RIGHT:
                smoke_x = self.center_x - self.width / 2
            else:
                smoke_x = self.center_x + self.width / 2
            particle.smoke(self.game, smoke_x, self.center_y)

    def on_update(self, delta_time):
        """ Move the player """
        self.think(delta_time)
        self.change_x = self.speed * self.dir
        self.change_y = (sin((self.time_alive + delta_time)*10) - sin(self.time_alive * 10)) * 300
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

        # shoot
        self.shoot_time += delta_time
        if self.shoot_time >= self.shoot_max:
            self.shoot_time = 0
            self.shoot_max = random.uniform(1, 3)
            if random.random() < 0.5:
                self.game.enemy_bullet_list.append(BossBullet(Direction.UP, self.game, center_x=self.center_x, center_y=self.center_y))
                self.game.enemy_bullet_list.append(BossBullet(Direction.DOWN, self.game, center_x=self.center_x, center_y=self.center_y))
                self.game.enemy_bullet_list.append(BossBullet(Direction.LEFT, self.game, center_x=self.center_x, center_y=self.center_y))
                self.game.enemy_bullet_list.append(BossBullet(Direction.RIGHT, self.game, center_x=self.center_x, center_y=self.center_y))
            else:
                self.game.enemy_bullet_list.append(BossBullet(Direction.UP_LEFT, self.game, center_x=self.center_x, center_y=self.center_y))
                self.game.enemy_bullet_list.append(BossBullet(Direction.UP_RIGHT, self.game, center_x=self.center_x, center_y=self.center_y))
                self.game.enemy_bullet_list.append(BossBullet(Direction.DOWN_LEFT, self.game, center_x=self.center_x, center_y=self.center_y))
                self.game.enemy_bullet_list.append(BossBullet(Direction.DOWN_RIGHT, self.game, center_x=self.center_x, center_y=self.center_y))

        # sound
        self.sound_time += delta_time
        if self.sound_time >= self.sound_max:
            self.sound_time = 0
            self.soud_max = random.uniform(1, 3)
            if self.center_x > self.game.camera.position[0] and self.center_x < self.game.camera.position[0] + SCREEN_WIDTH and self.center_y > self.game.camera.position[1] and self.center_y < self.game.camera.position[1] + SCREEN_HEIGHT:
                self.game.ass.play_sound("vroom")

        self.time_alive += delta_time

    def hit(self, damage):
        if self.blink < self.blink_ammount:
            return False

        self.hp -= damage

        self.blink = 0
        self.blink_time = 0

        if self.hp <= 0:
            self.game.enemy_list.remove(self)
            particle.flower_explosion(self.game, self.center_x, self.center_y, n_flowers=100)
            self.game.score = 0
            self.game.win = True
        return True

    def think(self, dt):
        wall_hit_list = arcade.check_for_collision_with_lists(
            self,
            [self.game.scene['walls'], self.game.scene['invis_walls']]
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
