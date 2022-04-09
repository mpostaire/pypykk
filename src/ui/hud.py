import arcade
from src.constants import *
from src.ui.components.label import Label

class HUD():
    def __init__(self, game):
        self.game = game
        self.camera = arcade.Camera(self.game.window.width, self.game.window.height)

        self.hp = int(self.game.player.hp)
        self.health_label = Label(f"Gunberg's health: {self.hp}",
                                    x=16,
                                    y=SCREEN_HEIGHT - 32,
                                    color=arcade.color.BLACK,
                                    font_size=18,
                                    draw_background=True)

        self.score = int(self.game.score)
        self.score_label = Label(f"Global warming: {self.score}°C",
                                    x=SCREEN_WIDTH - 256,
                                    y=SCREEN_HEIGHT - 32,
                                    color=arcade.color.BLACK,
                                    font_size=18,
                                    draw_background=True)


        self.game_over_label = Label("GAME OVER",
                                        color=arcade.color.BLACK,
                                        font_size=24,
                                        draw_background=True)
        self.game_over_label.arcade_text.x = (SCREEN_WIDTH / 2) - self.game_over_label.arcade_text.content_width / 2
        self.game_over_label.arcade_text.y = (SCREEN_HEIGHT / 2) + self.game_over_label.arcade_text.content_height
        
        self.game_over_desc_label = Label("All hope is forever lost :'(",
                                        color=arcade.color.BLACK,
                                        font_size=18,
                                        draw_background=True)
        self.game_over_desc_label.arcade_text.x = (SCREEN_WIDTH / 2) - self.game_over_desc_label.arcade_text.content_width / 2
        self.game_over_desc_label.arcade_text.y = (SCREEN_HEIGHT / 2) - self.game_over_desc_label.arcade_text.content_height


        self.game_win_label = Label("YOU WON!",
                                        color=arcade.color.BLACK,
                                        font_size=24,
                                        draw_background=True)
        self.game_win_label.arcade_text.x = (SCREEN_WIDTH / 2) - self.game_win_label.arcade_text.content_width / 2
        self.game_win_label.arcade_text.y = (SCREEN_HEIGHT / 2) + self.game_win_label.arcade_text.content_height
        
        self.game_win_desc_label = Label("Global warming ended :D",
                                        color=arcade.color.BLACK,
                                        font_size=18,
                                        draw_background=True)
        self.game_win_desc_label.arcade_text.x = (SCREEN_WIDTH / 2) - self.game_win_desc_label.arcade_text.content_width / 2
        self.game_win_desc_label.arcade_text.y = (SCREEN_HEIGHT / 2) - self.game_win_desc_label.arcade_text.content_height

        self.paused = self.game.paused
        self.paused_label = Label("PAUSE: press P to resume",
                                    color=arcade.color.BLACK,
                                    font_size=18,
                                    draw_background=True,
                                    blink_time=0.5)
        self.paused_label.arcade_text.x = (SCREEN_WIDTH / 2) - self.paused_label.arcade_text.content_width / 2
        self.paused_label.arcade_text.y = (SCREEN_HEIGHT / 2) + self.paused_label.arcade_text.content_height / 2

    def on_update(self, delta_time):
        if int(self.game.player.hp) != self.hp:
            self.hp = int(self.game.player.hp)
            self.health_label.text = f"Gunberg's health: {self.hp}"
        
        if int(self.game.score) != self.score:
            self.score = int(self.game.score)
            self.score_label.text = f"Global warming: {self.score}°C"
        
        if self.game.paused != self.paused:
            self.paused_label.blink_elapsed = 0
            self.paused_label.blink = True
            self.paused = self.game.paused

        self.paused_label.on_update(delta_time)

    def draw(self):
        self.camera.use()

        self.health_label.draw()
        self.score_label.draw()

        if self.game.game_over:
            self.game_over_label.draw()
            self.game_over_desc_label.draw()
        elif self.game.win:
            self.game_win_label.draw()
            self.game_win_desc_label.draw()
        elif self.game.paused:
            self.paused_label.draw()
    
