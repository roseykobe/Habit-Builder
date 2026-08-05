from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class BottomNav(BoxLayout):
    def __init__(self, current_screen, **kwargs):
        super().__init__(**kwargs)

        self.orientation= "horizontal"
        self.size_hint_y= None
        self.height= 50
        self.spacing= 0
        self.padding= 0

        self.home_button= Button(
            text="Home",
            size_hint_x= 0.5
        )
        self.history_button= Button(
            text="History",
            size_hint_x= 0.5
        )

        if current_screen == "welcome":
            self.home_button.background_normal= ""
            self.home_button.background_color= (0.93, 0.20, 0.53, 1)
            self.home_button.color= (0,0,0,1)

            self.history_button.background_normal= ""
            self.history_button.background_color= (0.99, 0.56, 0.67, 1)
            self.history_button.color= (0,0,0,1)

        elif current_screen == "history":
            self.history_button.background_normal= ""
            self.history_button.background_color= (0.93, 0.20, 0.53, 1)
            self.history_button.color= (0,0,0,1)

            self.home_button.background_normal= ""
            self.home_button.background_color= (0.99, 0.56, 0.67, 1)
            self.home_button.color= (0,0,0,1)

        elif current_screen== "add_task":
            self.home_button.background_normal= ""
            self.history_button.background_normal= ""

            self.home_button.background_color= (0.99, 0.56, 0.67, 1)
            self.history_button.background_color= (0.99, 0.56, 0.67, 1)

            self.home_button.color= (0,0,0,1)
            self.history_button.color= (0,0,0,1)


        self.add_widget(self.home_button)
        self.add_widget(self.history_button)
