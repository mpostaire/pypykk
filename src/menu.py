import arcade
import random
from src.constants import *
from src.assets import AssetManager
from src.particles import particle
from src.level import Level
from src.ui.title import Title

class Menu(arcade.View):

    def setup(self):
        """ Set up this view. """
        self.particle_list = arcade.SpriteList()
        self.explosion_time = 0
        self.explosion_max = 0.5

        self.ass = AssetManager()
        self.loaded = False
        self.first_frame_drawn = False

        self.ui = Title(self)

    def on_draw(self):
        self.clear()
        self.particle_list.draw()
        self.ui.draw()
        self.first_frame_drawn = True

    def on_update(self, delta_time):
        if not self.first_frame_drawn:
            return
        if not self.loaded:
            self.ass.load_assets()
            self.loaded = True
    
        self.particle_list.on_update(delta_time)

        self.explosion_time += delta_time
        if self.explosion_time > self.explosion_max:
            self.explosion_time = 0
            self.explosion_max = random.uniform(0.5, 2)
            for i in range(random.randrange(1, 4)):
                particle.flower_explosion(self, random.randrange(64, SCREEN_WIDTH - 64), random.randrange(64, SCREEN_HEIGHT - 64), muted=True)

        self.ui.on_update(delta_time)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.SPACE:
            self.window.show_view(Level(STARTING_LEVEL, self.ass, STARTING_SCORE))

    def on_show_view(self):
        """ Called once when view is activated. """
        self.setup()
        arcade.set_background_color(arcade.color.SKY_BLUE)

    def on_hide_view(self):
        pass
