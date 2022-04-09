from src.constants import *

def object_coords_to_game_coords(coordinates, tiled_map):
    return coordinates[0] * tiled_map.scaling, (tiled_map.height * tiled_map.tile_height * tiled_map.scaling) - (coordinates[1] * tiled_map.scaling)
