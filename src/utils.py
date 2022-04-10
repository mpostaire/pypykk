from src.constants import *

def object_coords_to_game_coords(coordinates, tiled_map):
    return coordinates[0] * tiled_map.scaling, (tiled_map.height * tiled_map.tile_height * tiled_map.scaling) - (coordinates[1] * tiled_map.scaling)

def sprite_collides_with_script_activator(sprite, script_activator, tiled_map):
    script_x, script_y = object_coords_to_game_coords((script_activator.coordinates.x, script_activator.coordinates.y), tiled_map)
    script_y -= script_activator.size.height * 2
    script_width = script_activator.size.width * tiled_map.scaling
    script_height = script_activator.size.height * tiled_map.scaling

    return sprite.left < script_x + script_width \
        and sprite.left + sprite.width > script_x \
        and sprite.bottom < script_y + script_height \
        and sprite.height + sprite.bottom > script_y
