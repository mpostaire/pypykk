import arcade
import random
from src.constants import *
from src.actors.bullet import Bullet
from src.actors.evil_car import EvilCar
from math import sin

class Boss(EvilCar):

    def __init__(self, game, collision_walls, *args, **kwargs):
        super().__init__(game, collision_walls, *args, **kwargs)

        self.idle_texture = {
            Direction.RIGHT: game.ass.textures["boss_car_right"],
            Direction.LEFT: game.ass.textures["boss_car_left"]
        }
        self.move_texture = {
            Direction.RIGHT: game.ass.textures["boss_car_right"],
            Direction.LEFT: game.ass.textures["boss_car_left"]
        }

        self.state = 'active'
        self.time_alive = 0

        self.shoot_time = 0
        self.shoot_max = random.uniform(0.5, 1)

        self.hp = 5 + max(0, self.game.score)

    def on_update(self, delta_time):
        # prevents large delta_time (due to loading) that can cause cars to be stuck in walls
        delta_time = min(delta_time, 0.03)

        self.think(delta_time)
        self.change_x = self.speed * self.dir
        self.change_y = (sin((self.time_alive + delta_time)*10) - sin(self.time_alive * 10)) * 300
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time

        self.update_animation(delta_time)

        self.blink_animation(delta_time)

        self.shoot(delta_time)
        self.update_sound(delta_time)

        self.time_alive += delta_time

    def shoot(self, delta_time):
        self.shoot_time += delta_time
        if self.shoot_time >= self.shoot_max:
            self.shoot_time = 0
            self.shoot_max = random.uniform(0.8, 1.5)
            if self.center_x > self.game.camera.position[0] and self.center_x < self.game.camera.position[0] + SCREEN_WIDTH and self.center_y > self.game.camera.position[1] and self.center_y < self.game.camera.position[1] + SCREEN_HEIGHT:
                self.game.ass.play_sound("boom")
            if random.random() < 0.5:
                for d in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
                    self.game.enemy_bullet_list.append(Bullet(self.game,
                                                                d,
                                                                random.choice(self.game.ass.textures["junk"]),
                                                                scale=SPRITE_SCALING * 4,
                                                                speed=BULLET_SPEED / 3,
                                                                center_x=self.center_x,
                                                                center_y=self.center_y))
            else:
                for d in [Direction.UP_LEFT, Direction.UP_RIGHT, Direction.DOWN_LEFT, Direction.DOWN_RIGHT]:
                    self.game.enemy_bullet_list.append(Bullet(self.game,
                                                                d,
                                                                random.choice(self.game.ass.textures["junk"]),
                                                                scale=SPRITE_SCALING * 4,
                                                                speed=BULLET_SPEED / 3,
                                                                center_x=self.center_x,
                                                                center_y=self.center_y))

    def hit(self, damage):
        ret = super().hit(damage)
        if ret and self.hp <= 0:
            self.game.score = 0
            self.game.win = True
        return ret
