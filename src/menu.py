import arcade
import random
from src.constants import *
from src.assets import AssetManager
from src.particles import particle
from src.level import Level

class Menu(arcade.View):

    def on_draw(self):
        """ Draw this view. GUI elements are automatically drawn. """
        self.clear()

        if self.load == 0:
            arcade.draw_text(f"Treta Gunberg:",
                (SCREEN_WIDTH / 2) - 128,
                (SCREEN_HEIGHT / 2) + 32,
                arcade.color.BLACK,
                32)
            arcade.draw_text(f"Loading...",
                (SCREEN_WIDTH / 2) - 48,
                (SCREEN_HEIGHT / 2) - 32,
                arcade.color.BLACK,
                24)
            self.load = 1
            return

        self.particle_list.draw()

        arcade.draw_text(f"Treta Gunberg:",
                        (SCREEN_WIDTH / 2) - 128,
                        (SCREEN_HEIGHT / 2) + 32,
                        arcade.color.BLACK,
                        32)
        arcade.draw_text(f"The C02 slayer",
                        (SCREEN_WIDTH / 2) - 96,
                        (SCREEN_HEIGHT / 2) - 32,
                        arcade.color.BLACK,
                        24)


        if self.blink:
            arcade.draw_text(f"Press SPACE to play",
                            (SCREEN_WIDTH / 2) - 138,
                            32,
                            arcade.color.WHITE,
                            24)

    def on_update(self, delta_time):
        if self.load == 1:
            self.ass.load_assets()
            self.load = 2

        self.particle_list.on_update(delta_time)

        self.blink_time += delta_time
        if self.blink_time > 0.5:
            self.blink_time = 0
            self.blink = not self.blink
        
        self.explosion_time += delta_time
        if self.explosion_time > self.explosion_max:
            self.explosion_time = 0
            self.explosion_max = random.uniform(0.5, 2)
            particle.flower_explosion(self, random.randrange(64, SCREEN_WIDTH - 64), random.randrange(64, SCREEN_HEIGHT - 64), muted=True)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.SPACE:
            self.window.show_view(Level(STARTING_LEVEL, self.ass, STARTING_SCORE))

    def on_show_view(self):
        """ Called once when view is activated. """
        self.setup()
        arcade.set_background_color(arcade.color.SKY_BLUE)

    def on_hide_view(self):
        pass

    def setup(self):
        """ Set up this view. """
        self.blink_time = 0
        self.blink = True

        self.particle_list = arcade.SpriteList()
        self.explosion_time = 0
        self.explosion_max = 0.5

        self.ass = AssetManager()
        self.load = 0
