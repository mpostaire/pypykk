from os import listdir
import arcade
from src.actors.player import Player
from src.actors.evil_car import EvilCar
from src.actors.junk import Junk
from src.actors.boss import Boss
from src.actors.gun import Gun
from src.utils import object_coords_to_game_coords, sprite_collides_with_script_activator
from src.constants import *
from src.ui.hud import HUD
from src.ui.components.label import Label

class Level(arcade.View):
    """
    Main application class.
    """

    def __init__(self, id, ass, score, player_init_hp=PLAYER_HP):
        """
        Initializer
        """
        # Call the parent class initializer
        super().__init__()
        self.id = id % (len(listdir("assets/levels")) - 1)
        self.ass = ass
        self.score = score
        self.init_score = score
        self.player_init_hp = player_init_hp

    
    def on_show_view(self):
        """ Called once when view is activated. """
        self.setup()

    def on_hide_view(self):
        self.ass.stop_sounds()

    def next_level(self):
        self.window.show_view(Level(self.id + 1, self.ass, self.score, player_init_hp=self.player.hp))
    
    def restart_level(self):
        self.window.show_view(Level(self.id, self.ass, self.init_score, player_init_hp=self.player_init_hp))

    def restart_game(self):
        self.window.show_view(Level(STARTING_LEVEL, self.ass, STARTING_SCORE))

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.shoot_left_pressed = False
        self.shoot_right_pressed = False
        self.shoot_up_pressed = False
        self.shoot_down_pressed = False

        self.over_exit_door = False

        self.paused = False
        self.game_over = False
        self.win = False

        self.boss = None

        # Set the background color
        arcade.set_background_color(arcade.color.SKY_BLUE)

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
            "water": {
                "hitbox_algorithm": "Simple"
            }
        }
        self.level_tile_map = arcade.tilemap.load_tilemap(f"assets/levels/level{self.id}.json", TILE_SCALING, layer_options=options)
        self.scene = arcade.Scene.from_tilemap(self.level_tile_map)

        # A Camera that can be used for scrolling the screen
        self.camera = arcade.Camera(self.window.width, self.window.height)

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.gun_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.particle_list = arcade.SpriteList()

        # Set up the player
        self.player = Player(self, hp=self.player_init_hp, center_x=SCREEN_WIDTH / 2, center_y=SCREEN_HEIGHT / 2)
        self.player_list.append(self.player)

        self.ui = HUD(self)

        #Spawn enemies
        info_layer = self.level_tile_map.get_tilemap_layer('info').tiled_objects
        self.exit_door = list(filter(lambda x: x.name == 'exit_door', info_layer))
        if self.exit_door:
            self.exit_door = self.exit_door[0]
            cx, cy = object_coords_to_game_coords(self.exit_door.coordinates, self.level_tile_map)
            cy -= self.exit_door.size.height * 2
            self.exit_door_label = Label(
                "[S] Exit door",
                color=arcade.color.WHITE,
                font_size=14,
                draw_background=True,
                background_color=arcade.color.BLACK)
            self.exit_door_label.x = cx - self.exit_door_label.content_width // 3
            self.exit_door_label.y = cy + (self.exit_door.size.height * self.level_tile_map.scaling) + 8

        enemy_spawn_list = list(filter(lambda x: 'enemy' in x.name and 'spawn' in x.name, info_layer))
        for point in enemy_spawn_list:
            cx, cy = object_coords_to_game_coords(point.coordinates, self.level_tile_map)
            if 'car' in point.name:
                enemy = EvilCar(self, 'walls', center_x=cx)
            elif 'junk' in point.name:
                enemy = Junk(self, center_x=cx)
                enemy.base_y = cy + enemy.height // 2
            elif 'boss' in point.name:
                enemy = Boss(self, 'invis_walls', center_x=cx)
                self.boss = enemy
            enemy.center_y = cy + enemy.height // 2
            self.enemy_list.append(enemy)
        
        self.scene.add_sprite_list_before('enemies', 'water',self.enemy_list)
        self.scene.add_sprite_list_before('player', 'water',self.player_list)
        self.scene.add_sprite_list_before('bullets', 'water',self.bullet_list)
        self.scene.add_sprite_list_before('enemy_bullets', 'water',self.enemy_bullet_list)
        self.scene.add_sprite_list_before('gun', 'water',self.gun_list)
        self.scene.add_sprite_list_before('particles', 'water', self.particle_list)
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, gravity_constant=GRAVITY, walls=[self.scene["walls"], self.scene["invis_walls"]]
        )
        spawn_point = list(filter(lambda x: x.name == 'player_spawn', self.level_tile_map.get_tilemap_layer('info').tiled_objects))[0]
        self.player.center_x, self.player.center_y = object_coords_to_game_coords(spawn_point.coordinates, self.level_tile_map)

        self.gun_sprite = Gun(self, center_x=self.player.center_x, center_y=self.player.center_y)
        self.gun_list.append(self.gun_sprite)

        self.ass.play_sound("music", repeat=True)


    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()

        # Activate our Camera
        self.camera.use()
        for name, list in self.scene.name_mapping.items():
            if name not in ['water', 'enemies', 'player', 'bullets', 'gun', 'enemy_bullets']:
                self.scene[name].draw(pixelated=True)


        # Draw all the sprites.

        if self.over_exit_door:
            self.exit_door_label.draw()

            script_x, script_y = object_coords_to_game_coords(self.exit_door.coordinates, self.level_tile_map)
            script_width = self.exit_door.size.width * self.level_tile_map.scaling
            script_height = self.exit_door.size.height * self.level_tile_map.scaling

            arcade.draw_rectangle_outline(
                script_x + script_width / 2,
                script_y - script_height / 2,
                script_width, script_height, arcade.color.BLACK,
                border_width=3)

        self.player_list.draw(pixelated=True)
        self.gun_list.draw(pixelated=True)
        self.enemy_list.draw(pixelated=True)
        self.particle_list.draw(pixelated=True)
        self.enemy_bullet_list.draw(pixelated=True)
        self.bullet_list.draw(pixelated=True)

        self.scene['water'].draw(pixelated=True)

        self.ui.draw()


    def center_camera_to_player(self):
        screen_center_x = self.player.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player.center_y - (
            self.camera.viewport_height / 2
        )

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered, CAMERA_MOVE_SPEED)

    def on_update(self, delta_time):
        """ Movement and game logic """
        if self.paused and not self.game_over and not self.win:
            self.ui.on_update(delta_time)
            return
        if self.game_over or self.win:
            self.particle_list.on_update(delta_time)
            return

        self.physics_engine.update()

        self.enemy_list.on_update(delta_time)
        self.particle_list.on_update(delta_time)
        self.player_list.on_update(delta_time)
        self.gun_list.on_update(self.player)
        self.bullet_list.on_update(delta_time)
        self.enemy_bullet_list.on_update(delta_time)
        self.enemy_list.on_update(delta_time)
        self.particle_list.on_update(delta_time)

        if self.exit_door and sprite_collides_with_script_activator(self.player, self.exit_door, self.level_tile_map):
            self.over_exit_door = True
        else:
            self.over_exit_door = False
        
        if self.player.collides_with_list(self.scene['water']):
            self.player.hit(4)

        # entities collision logic
        # collision on player's bullet
        for b in self.bullet_list:
            enemies_collided = b.collides_with_list(self.enemy_list)
            if enemies_collided:
                if enemies_collided[0].hit(b.damage):
                    if self.boss and not isinstance(enemies_collided[0], Boss) and enemies_collided[0].hp <= 0:
                        self.boss.hp = max(5, self.boss.hp - enemies_collided[0].score)
                    self.bullet_list.remove(b)
            elif b.collides_with_list(self.scene["walls"]):
                self.bullet_list.remove(b)
        
        # collision on player
        enemies_collided = self.player.collides_with_list(self.enemy_list)
        if enemies_collided:
            self.player.hit(enemies_collided[0].damage)
            self.health_label = f"Gunberg's health: {int(self.player.hp)}"
        
        bullets_collided = self.player.collides_with_list(self.enemy_bullet_list)
        if bullets_collided:
            if self.player.hit(bullets_collided[0].damage):
                self.enemy_bullet_list.remove(bullets_collided[0])

        # Position the camera
        self.center_camera_to_player()

        self.ui.on_update(delta_time)


    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.Z or key == arcade.key.SPACE:
            self.up_pressed = True
        elif key == arcade.key.S:
            if self.exit_door and self.over_exit_door:
                self.next_level()
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
        elif key == arcade.key.R:
            if modifiers & arcade.key.MOD_SHIFT:
                self.restart_game()
            else:
                self.restart_level()
        elif key == arcade.key.M:
            self.ass.toggle_mute()
        elif key == arcade.key.ESCAPE or key == arcade.key.P:
            self.paused = not self.paused

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
