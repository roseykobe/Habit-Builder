from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from datetime import datetime
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from components.rounded_panel import RoundedPanel



class HistoryCard(BoxLayout):
    def __init__(self, date, tasks, **kwargs):
        super().__init__(**kwargs)

        self.orientation= "vertical"
        self.size_hint_y= None
        self.height= 80
        self.spacing=5

        self.date= date
        self.tasks= tasks
        self.expanded= False

        completed= 0
        for task in self.tasks:
            if task["status"]== "completed":
                completed+= 1

        total= len(self.tasks)

        if total>0:
            percentage= round((completed/total)* 100)
        else:
            percentage=0

        formatted_date= datetime.strptime(self.date, "%Y-%m-%d").strftime("%d %B %Y")
        self.day_button= Button(
            text= f'[b]{formatted_date}[/b]\n{percentage}% Complete - {completed} of {total} Tasks',
            size_hint_y= None,
            height= 80,
            halign= "center",
            valign= "middle",
            background_normal= "",
            background_color= (0.58, 0.40, 0.78, 1),
            color= (0, 0, 0, 1),
            markup= True
        )
        self.day_button.bind(
            size=lambda instance, value: setattr(instance, "text_size", (instance.size))
        )
        self.add_widget(self.day_button)
    
        
        self.day_button.bind(
            on_press= self.toggle
        )
        self.content= BoxLayout(
            orientation= "vertical",
            size_hint_y= None,
            spacing= 5, 
            padding= (15, 10, 15, 10)
        )
        

        self.add_widget(self.content)


        self.content.bind(minimum_height= self.content.setter("height"))

    
    def toggle(self, instance):

        if self.expanded:
            self.content.clear_widgets()
            self.content.height= 0
            self.height= self.day_button.height
            self.expanded= False

        else:
            self.content.clear_widgets()

            for task in self.tasks:
                label= Label(
                    text= f"[b]Task:[/b] {task["name"]}\n[b]Time:[/b] {task["time"]}\n[b]Notes:[/b] {task["notes"]}\n[b]Status:[/b] {task["status"]}",
                    size_hint_y= None,
                    markup= True,
                    height= 80,
                    color= (0,0,0,1)
                    )
                taskpanel= RoundedPanel(
                    orientation= "vertical",
                    size_hint_y= None,
                    height= 90
                )
                label.bind(size=label.setter("text_size"))
                taskpanel.add_widget(label)

                self.content.add_widget(taskpanel)

            self.content.do_layout()
            self.content.height= self.content.minimum_height
            self.height= self.day_button.height + self.content.minimum_height + 20
            self.expanded= True





