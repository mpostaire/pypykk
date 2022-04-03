import arcade
from src.constants import *
import sys
class Player(arcade.Sprite):

    def __init__(self, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = game
        self.scale = SPRITE_SCALING
        self.facing_direction = Direction.RIGHT

        self.player_textures = {
            Direction.RIGHT: arcade.load_spritesheet("assets/GirlyGirl_walkcycle_right.png", 240, 240, 5, 9),
            Direction.LEFT: arcade.load_spritesheet("assets/GirlyGirl_walkcycle_left.png", 240, 240, 5, 9)
        }

        self.cur_texture = 0
        self.texture = self.player_textures[self.facing_direction][self.cur_texture]
        self.texture_time = 0
        self.idle_status = 0

        self.blink_time = 0
        self.blink_ammount = 8
        self.blink = self.blink_ammount

        self.hp = 4

    def hit(self, damage):
        if self.blink < self.blink_ammount:
            return False

        self.hp = max(0, self.hp - damage)
        self.game.health_label = f"Gunberg's health: {int(self.hp)}"

        self.blink = 0
        self.blink_time = 0

        if self.hp <= 0:
            self.game.game_over = True

        return True

    def update_animation(self, delta_time):
        self.texture_time += delta_time

        if (self.change_x != 0 or self.change_y != 0) and self.texture_time > 0.05:
            self.idle_status = 0
            self.texture_time = 0
            self.cur_texture = (self.cur_texture + 1) % len(self.player_textures[self.facing_direction])
            self.texture = self.player_textures[self.facing_direction][self.cur_texture]
        elif (self.change_x == 0 and self.change_y == 0):
            if self.idle_status == 0:
                self.texture_time = 0
                self.idle_status = 1
                self.cur_texture = 0
            elif self.idle_status == 1 and self.texture_time > 0.3:
                self.texture_time = 0
                self.idle_status = 2
                self.cur_texture = 1
            elif self.idle_status == 2 and self.texture_time > 0.3:
                self.texture_time = 0
                self.idle_status = 1
                self.cur_texture = 0

            self.texture = self.player_textures[self.facing_direction][self.cur_texture]
        
    def on_update(self, delta_time):
        """ Move the player """
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
