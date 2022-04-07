import arcade

class Label():

    def __init__(self, text, x=0, y=0, color=arcade.color.BLACK, font_size=12, draw_background=False, blink_time=0):
        self.color = color
        self.font_size = font_size
        self.draw_background = draw_background
        self.arcade_text = arcade.Text(text, x, y, color=self.color, font_size=self.font_size)

        self.margin = 4

        self.blink_elapsed = 0
        self.blink_time = blink_time
        self.blink = True

    @property
    def text(self):
        return self.arcade_text.text
    
    @text.setter
    def text(self, text):
        self.arcade_text.text = text
    
    @property
    def x(self):
        return self.arcade_text.x
    
    @x.setter
    def x(self, x):
        self.arcade_text.x = x

    @property
    def y(self):
        return self.arcade_text.y
    
    @y.setter
    def y(self, y):
        self.arcade_text.y = y

    def on_update(self, delta_time):
        self.blink_elapsed += delta_time

        if not self.blink_time == 0 and self.blink_elapsed > self.blink_time:
            self.blink_elapsed = 0
            self.blink = not self.blink

        if self.text != self.arcade_text.text:
            self.arcade_text.text = self.text

    def draw(self):
        if self.draw_background:
            arcade.draw_rectangle_filled(
                self.x + self.arcade_text.content_width // 2,
                (self.y + self.arcade_text.content_height // 2) - self.margin,
                self.arcade_text.content_width + self.margin * 4,
                self.arcade_text.content_height + self.margin * 2,
                (255, 255, 255, 200))

        if self.blink:
            self.arcade_text.draw()
