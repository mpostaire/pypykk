import arcade
from player import Player
from bullet import Bullet
from constants import *

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """
        # Call the parent class initializer
        super().__init__(width, height, title)

        # Variables that will hold sprite lists
        self.player_list = None

        # Set up the player info
        self.player_sprite = None

        # Variables that will hold bullet lists
        self.bullet_list = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.shoot_left_pressed = False
        self.shoot_right_pressed = False
        self.shoot_up_pressed = False
        self.shoot_down_pressed = False

        self.bullet_time = 0

        # Set the background color
        arcade.set_background_color(arcade.color.WHITE)

    def setup(self):
        """ Set up the game and initialize the variables. """
        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Player("assets/treta gunberg.png",
                                    SPRITE_SCALING, center_x=SCREEN_WIDTH / 2, center_y=SCREEN_HEIGHT / 2)
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()

        # Draw all the sprites.
        self.player_list.draw()
        self.bullet_list.draw()

    def update_player_speed(self):
        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED


    def shoot(self):
        # TODO shoot diagonals
        if self.bullet_time < BULLET_RATE:
            return

        self.bullet_time = 0

        direction = None
        if self.shoot_up_pressed:
            if self.shoot_left_pressed:
                direction = Direction.UP_LEFT
            elif self.shoot_right_pressed:
                direction = Direction.UP_RIGHT
            else:
                direction = Direction.UP
        elif self.shoot_down_pressed:
            if self.shoot_left_pressed:
                direction = Direction.DOWN_LEFT
            elif self.shoot_right_pressed:
                direction = Direction.DOWN_RIGHT
            else:
                direction = Direction.DOWN
        elif self.shoot_left_pressed:
            direction = Direction.LEFT
        elif self.shoot_right_pressed:
            direction = Direction.RIGHT
        else:
            return

        self.bullet_list.append(Bullet(direction, "assets/bullet.png", SPRITE_SCALING,
                                        center_x=self.player_sprite.center_x, center_y=self.player_sprite.center_y))


    def on_update(self, delta_time):
        """ Movement and game logic """
        self.bullet_time += delta_time

        self.player_list.on_update(delta_time)
        self.bullet_list.on_update(delta_time)

        self.shoot()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.Z:
            self.up_pressed = True
            self.update_player_speed()
        elif key == arcade.key.S:
            self.down_pressed = True
            self.update_player_speed()
        elif key == arcade.key.Q:
            self.left_pressed = True
            self.update_player_speed()
        elif key == arcade.key.D:
            self.right_pressed = True
            self.update_player_speed()
        elif key == arcade.key.UP:
            self.shoot_up_pressed = True
        elif key == arcade.key.DOWN:
            self.shoot_down_pressed = True
        elif key == arcade.key.LEFT:
            self.shoot_left_pressed = True
        elif key == arcade.key.RIGHT:
            self.shoot_right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.Z:
            self.up_pressed = False
            self.update_player_speed()
        elif key == arcade.key.S:
            self.down_pressed = False
            self.update_player_speed()
        elif key == arcade.key.Q:
            self.left_pressed = False
            self.update_player_speed()
        elif key == arcade.key.D:
            self.right_pressed = False
            self.update_player_speed()
        elif key == arcade.key.UP:
            self.shoot_up_pressed = False
        elif key == arcade.key.DOWN:
            self.shoot_down_pressed = False
        elif key == arcade.key.LEFT:
            self.shoot_left_pressed = False
        elif key == arcade.key.RIGHT:
            self.shoot_right_pressed = False


def main():
    """ Main function """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
