import arcade
import random

class AssetManager():

    def __init__(self):
        self.sounds = {}
        self.textures = {}
        
        self.played_sounds = {
            "effects": [],
            "music": None
        }

    def play_sound(self, sound, repeat=False):
        if sound == "music" and self.played_sounds["music"] is not None:
            return

        player = None
        if isinstance(self.sounds[sound], list):
            player = arcade.play_sound(random.choice(self.sounds[sound]), looping=repeat)
        else:
            player = arcade.play_sound(self.sounds[sound], looping=repeat)

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


    def load_assets(self):
        # TODO add explosion sound
        self.sounds = {
            "game_over": arcade.load_sound("assets/yaaaoooow.wav"),
            "pew": [
                arcade.load_sound("assets/pew_00.mp3"),
                arcade.load_sound("assets/pew_01.mp3"),
                arcade.load_sound("assets/pew_02.mp3")
            ],
            "ploof": [
                arcade.load_sound("assets/ploof_00.wav"),
                arcade.load_sound("assets/ploof_01.wav"),
                arcade.load_sound("assets/ploof_02.wav")
            ],
            "vroom": [
                arcade.load_sound("assets/vroom_00.mp3"),
                arcade.load_sound("assets/vroom_01.mp3"),
                arcade.load_sound("assets/vroom_02.mp3")
            ],
            "step": arcade.load_sound("assets/step.wav"),  # FIXME this sound is horrible for the ears in game
            "oof": [
                arcade.load_sound("assets/oof_00.wav"),
                arcade.load_sound("assets/oof_01.wav")
            ],
            "music": arcade.load_sound("assets/Gilles Stella - Libre de droit.m4a")
        }

        dims = [
            (16, 45),
            (39, 55),
            (36, 44),
            (51, 48)
        ]
        self.textures = {
            "flower": arcade.load_spritesheet("assets/flowers.png", 32, 32, 15, 45),
            "smoke": arcade.load_spritesheet("assets/smoke.png", 16, 16, 2, 3),
            "evil_car_right": arcade.load_spritesheet("assets/evil_car_0_right.png", 576//2, 118, 2, 2),
            "evil_car_left": arcade.load_spritesheet("assets/evil_car_0_left.png", 576//2, 118, 2, 2),
            "boss_car_right": arcade.load_spritesheet("assets/very_evil_car_0_right.png", 576//2, 84, 2, 2),
            "boss_car_left": arcade.load_spritesheet("assets/very_evil_car_0_left.png", 576//2, 84, 2, 2),
            "gunberg_right": arcade.load_spritesheet("assets/GirlyGirl_walkcycle_right.png", 240, 240, 5, 9),
            "gunberg_left": arcade.load_spritesheet("assets/GirlyGirl_walkcycle_left.png", 240, 240, 5, 9),
            "gun_right": arcade.load_texture("assets/gun.png"),
            "gun_left": arcade.load_texture("assets/gun.png", flipped_horizontally=True),
            "junk": [
                arcade.load_texture(f'assets/junk_0{i}.png', width=dims[i][0], height=dims[i][1])
                for i in range(3)
            ]
        }
