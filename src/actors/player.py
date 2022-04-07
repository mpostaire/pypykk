from src.constants import *
from src.particles.particle import flower_explosion
from src.actors.bullet import Bullet
from src.actors.animated_sprite import AnimatedSprite

class Player(AnimatedSprite):

    def __init__(self, game, *args, **kwargs):
        idle_textures = {
            Direction.RIGHT: [game.ass.textures["gunberg_right"][0], game.ass.textures["gunberg_right"][1]],
            Direction.LEFT: [game.ass.textures["gunberg_left"][0], game.ass.textures["gunberg_left"][1]]
        }
        move_textures = {
            Direction.RIGHT: game.ass.textures["gunberg_right"],
            Direction.LEFT: game.ass.textures["gunberg_left"]
        }

        super().__init__(idle_textures, move_textures, *args, **kwargs)

        self.game = game
        self.scale = SPRITE_SCALING
        self.facing_direction = Direction.RIGHT

        self.blink_ammount = 8

        self.bullet_time = 0

        self.jump_duration = PLAYER_JUMP_DURATION

        self.max_air_jumps = 1
        self.n_jumps = 0
        self.air_jump_ready = False

        self.hp = 6

    def hit(self, damage):
        ret = super().hit(damage)
        if ret and self.hp <= 0:
            self.game.game_over = True
            self.game.ass.play_sound("game_over")
        elif ret:
            self.game.ass.play_sound("oof")
        return ret

    def update_player_speed(self, delta_time):
        # FIXME when a jump is released before max ammount, spamming jump key allows for more than 1 double jump
        # Calculate speed based on the keys pressed
        self.change_x = 0

        if self.game.physics_engine.can_jump():
            self.air_jump_ready = False
            self.n_jumps = 0
            self.jump_duration = PLAYER_JUMP_DURATION
            if self.game.up_pressed and not self.game.down_pressed:
                self.change_y = PLAYER_JUMP_SPEED

        elif self.jump_duration > 0 and self.game.up_pressed:
            self.jump_duration -= delta_time
            self.change_y = PLAYER_JUMP_SPEED

        elif not self.air_jump_ready and not self.game.up_pressed and self.n_jumps < self.max_air_jumps:
            self.air_jump_ready = True
            self.n_jumps += 1

        elif self.air_jump_ready and self.game.up_pressed:
            self.jump_duration = PLAYER_JUMP_DURATION
            flower_coordinates = (
                self.center_x + (self.width // 2),
                self.center_y - self.height // 2
            )
            flower_explosion(self.game, flower_coordinates[0], flower_coordinates[1], n_flowers=3, muted=False)
            self.change_y = PLAYER_JUMP_SPEED
            self.air_jump_ready = False

        if self.game.left_pressed and not self.game.right_pressed:
            self.change_x = -MOVEMENT_SPEED * delta_time
        elif self.game.right_pressed and not self.game.left_pressed:
            self.change_x = MOVEMENT_SPEED * delta_time

    def shoot(self, delta_time):
        self.bullet_time += delta_time
        if self.bullet_time < BULLET_RATE:
            return

        direction = None
        if self.game.shoot_up_pressed:
            if self.game.shoot_left_pressed:
                direction = Direction.UP_LEFT
            elif self.game.shoot_right_pressed:
                direction = Direction.UP_RIGHT
            else:
                direction = Direction.UP
        elif self.game.shoot_down_pressed:
            if self.game.shoot_left_pressed:
                direction = Direction.DOWN_LEFT
            elif self.game.shoot_right_pressed:
                direction = Direction.DOWN_RIGHT
            else:
                direction = Direction.DOWN
        elif self.game.shoot_left_pressed:
            direction = Direction.LEFT
        elif self.game.shoot_right_pressed:
            direction = Direction.RIGHT
        else:
            return

        self.bullet_time = 0

        bullet_x = 0
        if self.facing_direction == Direction.LEFT:
            bullet_x = self.game.gun_sprite.center_x - self.game.gun_sprite.width / 2
        else:
            bullet_x = self.game.gun_sprite.center_x + self.game.gun_sprite.width / 2

        bullet_y = self.game.gun_sprite.center_y + self.game.gun_sprite.height / 4
        self.game.bullet_list.append(Bullet(self.game,
                                            direction,
                                            self.game.ass.textures["flowers"][4],
                                            scale=SPRITE_SCALING * 3,
                                            center_x=bullet_x,
                                            center_y=bullet_y))
        self.game.ass.play_sound("pew")

    def update_animation(self, delta_time):
        # update facing direction in function of shoot direction and movement direction
        if self.game.shoot_left_pressed:
            self.facing_direction = Direction.LEFT
        elif self.game.shoot_right_pressed:
            self.facing_direction = Direction.RIGHT
        elif self.game.left_pressed:
            self.facing_direction = Direction.LEFT
        elif self.game.right_pressed:
            self.facing_direction = Direction.RIGHT
        
        super().update_animation(delta_time)

    def on_update(self, delta_time):
        """ Move the player """
        self.update_player_speed(delta_time)

        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time

        self.shoot(delta_time)

        self.update_animation(delta_time)

        self.blink_animation(delta_time)
