import arcade
from src.menu import Menu
from src.constants import *

def main():
    """ Main function """
    window = arcade.Window(title=SCREEN_TITLE, height=SCREEN_HEIGHT, width=SCREEN_WIDTH)
    window.show_view(Menu())
    arcade.run()


if __name__ == "__main__":
    main()
