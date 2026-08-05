from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle


class RoundedButton(Button):
    def __init__(self, **kwargs):
        fill_color= kwargs.pop("background_color", (1,1,1,1))
        super().__init__(**kwargs)

        self.background_normal= ""
        self.background_down= ""
        self.background_color= (0,0,0,0)

        self._fill_color= fill_color

        with self.canvas.before:
            self._color= Color(*self._fill_color)
            

            self._bg= RoundedRectangle(
                pos= self.pos,
                size= self.size,
                radius= [(20,20),  (20,20), (20,20), (20, 20)]
            )
        self.bind(
            pos= self.update_canvas,
            size= self.update_canvas
            )

    def update_canvas(self, *args):
        self._bg.pos= self.pos
        self._bg.size= self.size

    def update_color(self, *args):
        self.bg_color.rgba= self.background_color

    def on_press(self):
        r, g, b, a = self._fill_color
        self._color.rgba= (
            max(0, r - 0.12),
            max(0, g - 0.12),
            max(0, b - 0.12),
            a
        )

    def on_release(self):
        self._color.rgba= self._fill_color
