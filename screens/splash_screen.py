from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation
from kivy.uix.image import Image

class SplashScreen(Screen):

    def __init__(self, task_manager, **kw):
        super().__init__(**kw)

        with self.canvas.before:
            Color(0.82, 0.76, 0.92, 1)
            self.bg= Rectangle(pos= self.pos, size= self.size)

        self.bind(pos=self.update_bg, size=self.update_bg)

        self.logo= Image(
            source= "assets/icon.png",
            size_hint=(None, None),
            size= (170, 170),
            pos_hint= {
                "center_x": 0.5,
                "center_y": 0.75
            }
        )

        self.title= Label(
                text="[b]Habit Builder[/b]\n\n[size=18][i] Every Habit starts with one task.[/i][/size] ",
                markup= True,
                font_size= 38,
                bold= True,
                color= (1,1,1,1),
                halign= "center",
                valign= "middle",
                opacity= 0,
                pos_hint= {
                    "center_x": 0.5,
                    "center_y": 0.43
                }
            )

        self.add_widget(self.logo)
        self.title.bind(size=self.title.setter("text_size"))
        self.add_widget(self.title)

        Animation(
            opacity=1,
            pos_hint= {
                "center_x":0.5,
                "center_y": 0.5
            },
            duration= 1.5
        ).start(self.title)

        self.task_manager= task_manager


    def on_enter(self):
        Clock.schedule_once(self.change_screen, 10)

    def change_screen(self, dt):
        self.manager.current = "welcome"

    def update_bg(self, *args):
        self.bg.pos= self.pos
        self.bg.size= self.size

