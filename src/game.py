import arcade
from src.actors.player import Player
from src.actors.evil_car import EvilCar
from src.actors.gun import Gun
from src.actors.bullet import Bullet
from src.utils import object_coords_to_game_coords
from src.constants import *
from arcade import gui

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """
        # Call the parent class initializer
        super().__init__(width, height, title)

        # A Camera that can be used for scrolling the screen
        self.camera = None

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

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()

        # Set the background color
        arcade.set_background_color(arcade.color.SKY_BLUE)

    def setup(self):
        """ Set up the game and initialize the variables. """
        options = {
            "walls": {
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
        self.level_tile_map = arcade.tilemap.load_tilemap("assets/levels/level0.json", TILE_SCALING, layer_options=options)
        self.scene = arcade.Scene.from_tilemap(self.level_tile_map)

        # Set up the Camera
        self.camera = arcade.Camera(self.width, self.height)

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.gun_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.particle_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Player(self, center_x=SCREEN_WIDTH / 2, center_y=SCREEN_HEIGHT / 2)
        self.player_list.append(self.player_sprite)
        self.gun_sprite = Gun("assets/gun.png", center_x=self.player_sprite.center_x, center_y=self.player_sprite.center_y)
        self.gun_list.append(self.gun_sprite)

        enemy_spawn_list = list(filter(lambda x: 'enemy' in x.name and 'spawn' in x.name, self.level_tile_map.get_tilemap_layer('info').tiled_objects))
        for point in enemy_spawn_list:
            enemy = EvilCar(self)
            enemy.center_x, enemy.center_y = object_coords_to_game_coords(point.coordinates, self.level_tile_map)
            self.enemy_list.append(enemy)
        self.scene.add_sprite_list_before('enemies', 'water',self.enemy_list)
        self.scene.add_sprite_list_before('player', 'water',self.player_list)
        self.scene.add_sprite_list_before('bullets', 'water',self.bullet_list)
        self.scene.add_sprite_list_before('gun', 'water',self.gun_list)
        self.scene.add_sprite_list_before('particles', 'water', self.particle_list)
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["walls"]
        )
        spawn_point = list(filter(lambda x: x.name == 'player_spawn', self.level_tile_map.get_tilemap_layer('info').tiled_objects))[0]
        self.player_sprite.center_x, self.player_sprite.center_y = object_coords_to_game_coords(spawn_point.coordinates, self.level_tile_map)

        # UI
        self.health_label = arcade.gui.UITextArea(text=f"Health: {self.player_sprite.hp}",
                                            x=16,
                                            y=SCREEN_HEIGHT - 48,
                                            width=450,
                                            height=40,
                                            font_size=18,
                                            font_name="Kenney Future")

        self.ui_manager.add(self.health_label)

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

        self.ui_manager.draw()


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
        self.bullet_list.append(Bullet(direction, self.camera, self.player_sprite,
                                        center_x=bullet_x, center_y=bullet_y))


    def on_update(self, delta_time):
        """ Movement and game logic """
        self.physics_engine.update()
        self.update_player_speed(delta_time)
        self.bullet_time += delta_time

        self.enemy_list.on_update(delta_time)
        self.particle_list.on_update(delta_time)
        self.player_list.on_update(delta_time)
        self.gun_list.on_update(self.player_sprite)
        self.bullet_list.on_update(delta_time)

        # entities collision logic
        # collision on player's bullet
        for b in self.bullet_list:
            enemies_collided = arcade.check_for_collision_with_list(b, self.enemy_list)
            if enemies_collided:
                if enemies_collided[0].hit(b):
                    self.bullet_list.remove(b)
            elif arcade.check_for_collision_with_list(b, self.scene["walls"]):
                self.bullet_list.remove(b)
        
        # collision on player
        enemies_collided = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)
        if enemies_collided:
            self.player_sprite.hit(enemies_collided[0])

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
        if key == arcade.key.Z:
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


    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.Z:
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
