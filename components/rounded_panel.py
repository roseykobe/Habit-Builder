from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color , RoundedRectangle


class RoundedPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.padding= 10
        self.spacing= 5

        with self.canvas.before:
            Color (0.93, 0.68, 0.80, 1)
            self.bg= RoundedRectangle(
                pos= self.pos,
                size= self.size,
                radius= [15]
            )
        self.bind(pos=self.update_bg, size= self.update_bg)

    def update_bg(self, *args):
        self.bg.pos= self.pos
        self.bg.size= self.size
