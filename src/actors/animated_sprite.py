import arcade
import random
from src.constants import *

class AnimatedSprite(arcade.Sprite):

    def __init__(self, idle_texture, move_texture, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.scale = SPRITE_SCALING

        self.texture_time = 0

        self.facing_direction = Direction.RIGHT

        self.idle_texture = idle_texture
        self.move_texture = move_texture
        self.cur_idle_texture = 0
        self.cur_move_texture = 0

        self.texture = self.idle_texture[self.facing_direction][self.cur_idle_texture]

        self.blink_time = 0
        self.blink_ammount = 4
        self.blink_step = self.blink_ammount

        self.sound_time = 0
        self.sound_max = random.uniform(1, 3)

        self.hp = 2

    def hit(self, damage):
        if self.blink_step < self.blink_ammount:
            return False

        self.hp = max(0, self.hp - damage)

        self.blink()
        return True

    def update_animation(self, delta_time):
        self.texture_time += delta_time

        # moving
        if (self.change_x != 0 or self.change_y != 0) and self.texture_time > 0.05:
            self.texture_time = 0
            self.cur_idle_texture = -1
            self.cur_move_texture = (self.cur_move_texture + 1) % len(self.move_texture[self.facing_direction])
            self.texture = self.move_texture[self.facing_direction][self.cur_move_texture]
        # idling
        elif (self.change_x == 0 and self.change_y == 0):
            if self.texture_time > 0.3:
                self.texture_time = 0
                self.cur_move_texture = 0
                self.cur_idle_texture = (self.cur_idle_texture + 1) % len(self.idle_texture[self.facing_direction])
                self.texture = self.idle_texture[self.facing_direction][self.cur_idle_texture]
            else:
                self.texture = self.idle_texture[self.facing_direction][self.cur_idle_texture]

    def blink_animation(self, delta_time):
        # blink on hit
        self.blink_time += delta_time
        if self.blink_step < self.blink_ammount and self.blink_time >= 0.06:
            self.blink_step += 1
            self.blink_time = 0
            self.alpha = 255 if self.alpha == 0 else 0
        elif self.blink_step >= self.blink_ammount:
            self.alpha = 255

    def blink(self):
        self.blink_step = 0
        self.blink_time = 0

    def update_sound(self, delta_time):
        if not self.sound:
            return

        self.sound_time += delta_time
        if self.sound_time >= self.sound_max:
            self.sound_time = 0
            self.soud_max = random.uniform(1, 3)
            if self.center_x > self.game.camera.position[0] and self.center_x < self.game.camera.position[0] + SCREEN_WIDTH and self.center_y > self.game.camera.position[1] and self.center_y < self.game.camera.position[1] + SCREEN_HEIGHT:
                self.game.ass.play_sound(self.sound)

    def on_update(self, delta_time):
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time

        self.update_animation(delta_time)

        self.blink_animation(delta_time)

        self.update_sound(delta_time)
