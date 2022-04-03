from arcade import TileMap
from src.constants import *

def object_coords_to_game_coords(coordinates, tiled_map):
    return coordinates[0] * TILE_SCALING, ((tiled_map.height * tiled_map.tile_height) - coordinates[1]) * TILE_SCALING
