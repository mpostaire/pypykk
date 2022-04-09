import arcade

class Label():

    def __init__(self, text, x=0, y=0, color=arcade.color.BLACK, font_size=12, draw_background=False, blink_time=0):
        self.color = color
        self.font_size = font_size
        self.draw_background = draw_background

        # if we change its text after creation it breaks water hitboxes (very strange), so we only use this to compute size
        arcade_text = arcade.Text(text, x, y, color=self.color, font_size=self.font_size)

        self.x = x
        self.y = y
        self.content_width = arcade_text.content_width
        self.content_height = arcade_text.content_height
        self.margin = 4
        self.text = text

        self.blink_elapsed = 0
        self.blink_time = blink_time
        self.blink = True

    def on_update(self, delta_time):
        self.blink_elapsed += delta_time

        if not self.blink_time == 0 and self.blink_elapsed > self.blink_time:
            self.blink_elapsed = 0
            self.blink = not self.blink

    def draw(self):
        if self.draw_background:
            arcade.draw_rectangle_filled(
                self.x + self.content_width // 2,
                (self.y + self.content_height // 2) - self.margin,
                self.content_width + self.margin * 4,
                self.content_height + self.margin * 2,
                (255, 255, 255, 200))

        if self.blink:
            arcade.draw_text(self.text, self.x, self.y, font_size=self.font_size, color=self.color)
