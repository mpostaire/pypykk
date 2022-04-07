import arcade
from src.constants import *
from src.ui.components.label import Label

class Title():
    def __init__(self, game):
        self.game = game
        self.camera = arcade.Camera(self.game.window.width, self.game.window.height)

        self.title_label = Label("Treta Gunberg:",
                                    color=arcade.color.BLACK,
                                    font_size=32)
        self.title_label.arcade_text.x = (SCREEN_WIDTH / 2) - self.title_label.arcade_text.content_width / 2
        self.title_label.arcade_text.y = (SCREEN_HEIGHT / 2) + self.title_label.arcade_text.content_height / 2


        self.desc_label = Label("The C02 slayer",
                                        color=arcade.color.BLACK,
                                        font_size=24)
        self.desc_label.arcade_text.x = (SCREEN_WIDTH / 2) - self.desc_label.arcade_text.content_width / 2
        self.desc_label.arcade_text.y = (SCREEN_HEIGHT / 2) - self.desc_label.arcade_text.content_height / 2

        
        self.loading_label = Label("Loading...",
                                    y=32,
                                    color=arcade.color.WHITE,
                                    font_size=24)
        self.loading_label.arcade_text.x = (SCREEN_WIDTH / 2) - self.loading_label.arcade_text.content_width / 2
    

        self.start_label = Label("Press SPACE to play",
                                    y=32,
                                    color=arcade.color.WHITE,
                                    font_size=24,
                                    blink_time=0.5)
        self.start_label.arcade_text.x = (SCREEN_WIDTH / 2) - self.start_label.arcade_text.content_width / 2

    def on_update(self, delta_time):
        self.start_label.on_update(delta_time)

    def draw(self):
        self.camera.use()

        self.title_label.draw()
        self.desc_label.draw()
        if self.game.loaded:
            self.start_label.draw()
        else:
            self.loading_label.draw()
    
