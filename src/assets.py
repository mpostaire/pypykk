import arcade
import random
from src.constants import *

class AssetManager():

    def __init__(self):
        self.sounds = {}
        self.textures = {}
        
        self.muted = MUTED_STATUS

        self.played_sounds = {
            "effects": [],
            "music": None
        }

    def play_sound(self, sound, repeat=False):
        if sound == "music" and self.played_sounds["music"] is not None:
            return

        player = None
        if isinstance(self.sounds[sound], list):
            player = arcade.play_sound(random.choice(self.sounds[sound]), volume=0 if self.muted else 1, looping=repeat)
        else:
            player = arcade.play_sound(self.sounds[sound], volume=0 if self.muted else 1, looping=repeat)

        if sound == "music":
            self.played_sounds["music"] = player
        else:
            self.played_sounds["effects"].append(player)

    def stop_sounds(self, also_stop_music=False):
        for p in self.played_sounds["effects"]:
            arcade.stop_sound(p)
        self.played_sounds["effects"] = []

        if also_stop_music:
            arcade.stop_sound(self.played_sounds["music"])
            self.played_sounds["music"] = None

    def toggle_mute(self):
        self.muted = not self.muted

        for p in self.played_sounds["effects"]:
            p.volume = 0 if self.muted else 1

        self.played_sounds["music"].volume = 0 if self.muted else 1

    def load_assets(self):
        self.sounds = {
            "game_over": arcade.load_sound("assets/audio/yaaaoooow.ogg"),
            "pew": [arcade.load_sound(f"assets/audio/pew_0{x}.ogg") for x in range(3)],
            "ploof": [arcade.load_sound(f"assets/audio/ploof_0{x}.ogg") for x in range(3)],
            "vroom": [arcade.load_sound(f"assets/audio/vroom_0{x}.ogg") for x in range(3)],
            "step": arcade.load_sound("assets/audio/step.ogg"),  # FIXME this sound is horrible for the ears in game
            "oof": [arcade.load_sound(f"assets/audio/oof_0{x}.ogg") for x in range(2)],
            "boom": arcade.load_sound("assets/audio/boom_00.ogg"),
            "music": arcade.load_sound("assets/audio/Gilles Stella - Libre de droit.ogg")
        }

        dims = [
            (16, 45),
            (39, 55),
            (36, 44),
            (51, 48)
        ]
        self.textures = {
            "flowers": arcade.load_spritesheet("assets/textures/flowers.png", 32, 32, 15, 45),
            "smoke": arcade.load_spritesheet("assets/textures/smoke.png", 16, 16, 2, 3),
            "evil_car_right": arcade.load_spritesheet("assets/textures/evil_car_right.png", 576 // 2, 118, 2, 2),
            "evil_car_left": arcade.load_spritesheet("assets/textures/evil_car_left.png", 576 // 2, 118, 2, 2),
            "boss_car_right": arcade.load_spritesheet("assets/textures/very_evil_car_right.png", 576 // 2, 84, 2, 2),
            "boss_car_left": arcade.load_spritesheet("assets/textures/very_evil_car_left.png", 576 // 2, 84, 2, 2),
            "gunberg_right": arcade.load_spritesheet("assets/textures/gunberg_right.png", 16, 16, 5, 9),
            "gunberg_left": arcade.load_spritesheet("assets/textures/gunberg_left.png", 16, 16, 5, 9),
            "gun_right": arcade.load_texture("assets/textures/gun.png"),
            "gun_left": arcade.load_texture("assets/textures/gun.png", flipped_horizontally=True),
            "junk": [
                arcade.load_texture(f'assets/textures/junk_0{i}.png', width=dims[i][0], height=dims[i][1])
                for i in range(3)
            ]
        }
