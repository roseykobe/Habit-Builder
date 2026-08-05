from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from components.bottom_nav import BottomNav
from models.history_manager import HistoryManager
from kivy.uix.scrollview import ScrollView
from components.history_card import HistoryCard
from kivy.graphics import Color, Rectangle



class HistoryScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        with self.canvas.before:
            Color(0.82, 0.76, 0.92, 1)
            self.bg= Rectangle(pos= self.pos, size= self.size)

        self.bind(pos=self.update_bg, size= self.update_bg)

        self.history_manager= HistoryManager()

        self.layout= BoxLayout(
            orientation= "vertical",
            padding= (40, 25, 40, 25),
            spacing= 15
        )
        self.title= Label(
            text="Task History", 
            size_hint_y= None,
            height= 60,
            font_size= 28,
            bold= True,
            color= (0,0,0,1)
        )
        self.layout.add_widget(self.title)


        self.bottom_nav= BottomNav(
            current_screen="history"
        )
        self.bottom_nav.home_button.bind(
            on_press= self.open_home
        )
        
        self.history_layout= BoxLayout(
            orientation= "vertical",
            size_hint_y= None,
            spacing= 20,
            padding= (0, 20, 0, 0)
        )
        self.history_layout.bind(
            minimum_height= self.history_layout.setter("height")
        )
        self.scroll= ScrollView(
            size_hint= (1, 1)
        )
        self.scroll.add_widget(self.history_layout)
        self.layout.add_widget(self.scroll)

        self.layout.add_widget(self.bottom_nav)

        self.load_history()
        from kivy.clock import Clock
        Clock.schedule_once(self.reset_scroll, 1)

        self.add_widget(self.layout)



    def open_home(self, instance):
        self.manager.current= "welcome"


    def load_history(self):
        self.history_layout.clear_widgets()

        history= self.history_manager.history["history"]

        for day, tasks in reversed( history.items()):
            card= HistoryCard(day, tasks)

            self.history_layout.add_widget(card)

            self.history_layout.do_layout()
            

    def reset_scroll(self, dt):
        self.scroll.scroll_y=1      

    def update_bg(self, *args):
        self.bg.pos= self.pos
        self.bg.size= self.size
