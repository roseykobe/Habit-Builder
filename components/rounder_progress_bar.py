from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle
from kivy.animation import Animation


class RoundedProgressBar(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.max= 100
        self.value= 0

        with self.canvas:
            Color(0.9, 0.9, 0.9, 1)
            self.bg= RoundedRectangle(
                pos= self.pos,
                size= self.size,
                radius= [15, 15, 15, 15]
            )

            Color(0.20, 0.75, 0.45, 1)
            self.fill= RoundedRectangle(
                pos= self.pos, 
                size= (0, self.height),
                radius= [15, 15, 15, 15]
            )

        self.bind(
            pos= self.update_bar, size= self.update_bar
        )

    def update_bar (self, *args):

        percentage= self.value/self.max

        self.bg.pos= self.pos
        self.bg.size= self.size

        self.fill.pos= self.pos

        target_width= self.width * percentage

        Animation.cancel_all(self.fill)

        anim= Animation(
            size= (target_width, self.height), 
            duration= 0.25
        )
        anim.start(self.fill)

