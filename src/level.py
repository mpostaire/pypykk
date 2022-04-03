from os import listdir
import arcade
from src.actors.player import Player
from src.actors.evil_car import EvilCar
from src.actors.junk import Junk
from src.actors.boss import Boss

from src.actors.gun import Gun
from src.actors.bullet import Bullet
from src.utils import object_coords_to_game_coords
from src.constants import *
from arcade import gui
from src.particles.particle import flower_explosion

class Level(arcade.View):
    """
    Main application class.
    """

    def __init__(self, id, ass, score):
        """
        Initializer
        """
        # Call the parent class initializer
        super().__init__()
        self.id = id % len(listdir("assets/levels"))
        self.ass = ass

        # A Camera that can be used for scrolling the screen
        self.camera = None

        # TODO edit this following the total number of enemies in all the levels
        self.score = score

        # Variables that will hold sprite lists
        self.player_list = None

        # Set up the player info
        self.player_sprite = None

        self.gun_list = None
        self.gun_sprite = None

        # Variables that will hold bullet lists
        self.bullet_list = None

        self.particle_list = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.shoot_left_pressed = False
        self.shoot_right_pressed = False
        self.shoot_up_pressed = False
        self.shoot_down_pressed = False
        
        self.jump_duration = PLAYER_JUMP_DURATION

        self.bullet_time = 0
        self.level_idx = 0
        self.max_air_jumps = 1
        self.n_jumps = 0
        self.air_jump_ready = False

        self.game_over = False

        # Set the background color
        arcade.set_background_color(arcade.color.SKY_BLUE)
    
    def on_show_view(self):
        """ Called once when view is activated. """
        self.setup()

    def on_hide_view(self):
        self.ass.stop_sounds()

    def next_level(self):
        self.window.show_view(Level(self.id + 1, self.ass, self.score))

    def setup(self):
        """ Set up the game and initialize the variables. """
        options = {
            "walls": {
                "use_spatial_hash": True,
                "hitbox_algorithm": "Simple"
            },
            "invis_walls": {
                "use_spatial_hash": True,
                "hitbox_algorithm": "Simple"
            },
            "deco":{
                "hitbox_algorithm": "None"
            },
            "objects": {
                "hitbox_algorithm": "None"
            },
            "water": {
                "hitbox_algorithm": "Simple"
            }
        }
        self.level_tile_map = arcade.tilemap.load_tilemap(f"assets/levels/level{self.id}.json", TILE_SCALING, layer_options=options)
        self.scene = arcade.Scene.from_tilemap(self.level_tile_map)

        # Set up the Camera
        self.camera = arcade.Camera(self.window.width, self.window.height)

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.gun_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.particle_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Player(self, center_x=SCREEN_WIDTH / 2, center_y=SCREEN_HEIGHT / 2)
        self.player_list.append(self.player_sprite)

        enemy_spawn_list = list(filter(lambda x: 'enemy' in x.name and 'spawn' in x.name, self.level_tile_map.get_tilemap_layer('info').tiled_objects))
        for point in enemy_spawn_list:
            cx, cy = object_coords_to_game_coords(point.coordinates, self.level_tile_map)
            if 'car' in point.name:
                enemy = EvilCar(self, center_x=cx, center_y=cy)
            elif 'junk' in point.name:
                enemy = Junk(self, center_x=cx, center_y=cy)
            elif 'boss' in point.name:
                enemy = Boss(self, center_x=cx, center_y=cy)
            self.enemy_list.append(enemy)
        self.scene.add_sprite_list_before('enemies', 'water',self.enemy_list)
        self.scene.add_sprite_list_before('player', 'water',self.player_list)
        self.scene.add_sprite_list_before('bullets', 'water',self.bullet_list)
        self.scene.add_sprite_list_before('gun', 'water',self.gun_list)
        self.scene.add_sprite_list_before('particles', 'water', self.particle_list)
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=[self.scene["walls"], self.scene["invis_walls"]]
        )
        spawn_point = list(filter(lambda x: x.name == 'player_spawn', self.level_tile_map.get_tilemap_layer('info').tiled_objects))[0]
        self.player_sprite.center_x, self.player_sprite.center_y = object_coords_to_game_coords(spawn_point.coordinates, self.level_tile_map)

        self.gun_sprite = Gun(self, center_x=self.player_sprite.center_x, center_y=self.player_sprite.center_y)
        self.gun_list.append(self.gun_sprite)

        self.ass.play_sound("music", repeat=True)

        #Spawn enemies


    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()

        # Activate our Camera
        self.camera.use()
        for name, list in self.scene.name_mapping.items():
            if name not in ['water', 'enemies', 'player', 'bullets', 'gun']:
                self.scene[name].draw(pixelated=True)


        # Draw all the sprites.

        self.player_list.draw(pixelated=True)
        self.gun_list.draw(pixelated=True)
        self.enemy_list.draw(pixelated=True)
        self.particle_list.draw(pixelated=True)
        self.bullet_list.draw(pixelated=True)

        self.scene['water'].draw(pixelated=True)

        # draw UI
        arcade.draw_rectangle_filled(
                self.camera.position[0] + 120,
                self.camera.position[1] + SCREEN_HEIGHT - 25,
                220, 32, (255, 255, 255, 200))
        arcade.draw_text(f"Gunberg's health: {int(self.player_sprite.hp)}",
                        self.camera.position[0] + 16,
                        self.camera.position[1] + SCREEN_HEIGHT - 32,
                        arcade.color.BLACK,
                        18)
        arcade.draw_rectangle_filled(
                self.camera.position[0] + SCREEN_WIDTH - 140,
                self.camera.position[1] + SCREEN_HEIGHT - 25,
                246, 32, (255, 255, 255, 200))
        arcade.draw_text(f"Global warming: {int(self.score)}°C",
                        self.camera.position[0] + SCREEN_WIDTH - 256,
                        self.camera.position[1] + SCREEN_HEIGHT - 32,
                        arcade.color.BLACK,
                        18)

        if self.game_over:
            arcade.draw_rectangle_filled(
                self.camera.position[0] + (SCREEN_WIDTH / 2) + 64,
                self.camera.position[1] + (SCREEN_HEIGHT / 2) + 32,
                300, 64, (255, 255, 255, 200))
            arcade.draw_text(f"GAME OVER",
                            self.camera.position[0] + (SCREEN_WIDTH / 2) - 32,
                            self.camera.position[1] + (SCREEN_HEIGHT / 2) + 32,
                            arcade.color.BLACK,
                            24)
            arcade.draw_text(f"All hope is forever lost :'(",
                            self.camera.position[0] + (SCREEN_WIDTH / 2) - 64,
                            self.camera.position[1] + (SCREEN_HEIGHT / 2) + 8,
                            arcade.color.BLACK,
                            18)


    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def update_player_speed(self, dt):
        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        #self.player_sprite.change_y = 0
        flower_coordinates = (
            self.player_sprite.center_x + (self.player_sprite.width//2),
            self.player_sprite.center_y - self.player_sprite.height//2
        )
        if self.physics_engine.can_jump():
            self.air_jump_ready = False
            self.n_jumps = 0
            self.jump_duration = PLAYER_JUMP_DURATION
            if self.up_pressed and not self.down_pressed:
                self.player_sprite.change_y = PLAYER_JUMP_SPEED

        elif self.jump_duration > 0 and self.up_pressed:
            self.jump_duration -= dt
            self.player_sprite.change_y = PLAYER_JUMP_SPEED

        elif not self.air_jump_ready and not self.up_pressed and self.n_jumps < self.max_air_jumps:
            self.air_jump_ready = True
            self.n_jumps += 1

        elif self.air_jump_ready and self.up_pressed:

            flower_explosion(self, flower_coordinates[0], flower_coordinates[1], n_flowers=3)
            self.player_sprite.change_y = PLAYER_JUMP_SPEED
            self.air_jump_ready = False

        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED * dt
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED * dt

    def shoot(self, delta_time):
        if self.bullet_time < BULLET_RATE:
            return

        direction = None
        if self.shoot_up_pressed:
            if self.shoot_left_pressed:
                direction = Direction.UP_LEFT
            elif self.shoot_right_pressed:
                direction = Direction.UP_RIGHT
            else:
                direction = Direction.UP
        elif self.shoot_down_pressed:
            if self.shoot_left_pressed:
                direction = Direction.DOWN_LEFT
            elif self.shoot_right_pressed:
                direction = Direction.DOWN_RIGHT
            else:
                direction = Direction.DOWN
        elif self.shoot_left_pressed:
            direction = Direction.LEFT
        elif self.shoot_right_pressed:
            direction = Direction.RIGHT
        else:
            return

        self.bullet_time = 0

        bullet_x = 0
        if self.player_sprite.facing_direction == Direction.LEFT:
            bullet_x = self.gun_sprite.center_x - self.gun_sprite.width / 2
        else:
            bullet_x = self.gun_sprite.center_x + self.gun_sprite.width / 2

        bullet_y = self.gun_sprite.center_y + self.gun_sprite.height / 4
        self.bullet_list.append(Bullet(direction, self, center_x=bullet_x, center_y=bullet_y))
        self.ass.play_sound("pew")


    def on_update(self, delta_time):
        """ Movement and game logic """
        if self.game_over:
            return

        self.physics_engine.update()
        self.update_player_speed(delta_time)
        self.bullet_time += delta_time

        self.enemy_list.on_update(delta_time)
        self.particle_list.on_update(delta_time)
        self.player_list.on_update(delta_time)
        self.gun_list.on_update(self.player_sprite)
        self.bullet_list.on_update(delta_time)
        self.enemy_list.on_update(delta_time)
        self.particle_list.on_update(delta_time)
        
        water_collided = arcade.check_for_collision_with_list(self.player_sprite, self.scene['water'])
        if len(water_collided) > 0:
            self.player_sprite.hit(4)

        # entities collision logic
        # collision on player's bullet
        for b in self.bullet_list:
            enemies_collided = arcade.check_for_collision_with_list(b, self.enemy_list)
            if enemies_collided:
                if enemies_collided[0].hit(b.damage):
                    self.bullet_list.remove(b)
            elif arcade.check_for_collision_with_list(b, self.scene["walls"]):
                self.bullet_list.remove(b)
        
        # collision on player
        enemies_collided = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)
        if enemies_collided:
            self.player_sprite.hit(enemies_collided[0].damage)

        # update player facing direction in function of shoot direction and movement direction
        if self.shoot_left_pressed:
            self.player_sprite.facing_direction = Direction.LEFT
        elif self.shoot_right_pressed:
            self.player_sprite.facing_direction = Direction.RIGHT
        elif self.left_pressed:
            self.player_sprite.facing_direction = Direction.LEFT
        elif self.right_pressed:
            self.player_sprite.facing_direction = Direction.RIGHT

        self.shoot(delta_time)

        # Position the camera
        self.center_camera_to_player()


    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.Z or key == arcade.key.SPACE:
            self.up_pressed = True
        elif key == arcade.key.Q:
            self.left_pressed = True
        elif key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.UP:
            self.shoot_up_pressed = True
        elif key == arcade.key.DOWN:
            self.shoot_down_pressed = True
        elif key == arcade.key.LEFT:
            self.shoot_left_pressed = True
        elif key == arcade.key.RIGHT:
            self.shoot_right_pressed = True

        elif key == arcade.key.N:
            # skip to next level (this is a cheat used for debugging purposes)
            self.next_level()


    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.Z or key == arcade.key.SPACE:
            self.up_pressed = False
        elif key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.Q:
            self.left_pressed = False
        elif key == arcade.key.D:
            self.right_pressed = False
        elif key == arcade.key.UP:
            self.shoot_up_pressed = False
        elif key == arcade.key.DOWN:
            self.shoot_down_pressed = False
        elif key == arcade.key.LEFT:
            self.shoot_left_pressed = False
        elif key == arcade.key.RIGHT:
            self.shoot_right_pressed = False
