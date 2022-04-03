from arcade import TileMap
from src.constants import *
import random
import arcade

played_sounds = {
    "effects": [],
    "music": None
}

def object_coords_to_game_coords(coordinates, tiled_map):
    return coordinates[0] * TILE_SCALING, ((tiled_map.height * tiled_map.tile_height) - coordinates[1]) * TILE_SCALING

def play_sound(sound, repeat=False):
    if sound == "music" and played_sounds["music"] is not None:
        return

    player = None
    if isinstance(sounds[sound], list):
        player = arcade.play_sound(random.choice(sounds[sound]), looping=repeat)
    else:
        player = arcade.play_sound(sounds[sound], looping=repeat)

    if sound == "music":
        played_sounds["music"] = player
    else:
        played_sounds["effects"].append(player)

def stop_sounds(also_stop_music=False):
    for p in played_sounds["effects"]:
        arcade.stop_sound(p)
        played_sounds["effects"] = []

    if also_stop_music:
        arcade.stop_sound(played_sounds["music"])
        played_sounds["music"] = None
