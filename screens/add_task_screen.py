from kivy.uix.screenmanager import Screen 
from kivy.uix.label import Label 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from datetime import datetime
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from models.task import Task 
from models.task_manager import TaskManager
from components.bottom_nav import BottomNav
from kivy.uix.popup import Popup
from kivy.clock import Clock
from components.rounded_button import RoundedButton
from kivy.graphics import Color, Rectangle

class AddTaskScreen(Screen):

    def __init__(self, task_manager, **kw):
        super().__init__(**kw)

        with self.canvas.before:
            Color(0.98, 0.93, 0.95, 1)
            self.bg= Rectangle(pos=self.pos, size= self.size)

        self.bind(pos=self.update_bg, size= self.update_bg)

        layout= BoxLayout(
            orientation= "vertical",
            spacing= 20,
            padding= (50, 25, 50, 0)
        )

        self.title= Label(
            text= "Create Task",
            font_size= 28,
            bold= True,
            color= (0,0,0,1)
        )

        task_label= Label(text="Task",
                          font_size= 18,
                          bold= True,
                          size_hint_y= None,
                          height= 25,
                          halign= "left",
                          valign= "middle",
                          color= (0,0,0,1)
                          )
        task_label.bind(size= task_label.setter("text_size"))
        self.task_name= TextInput(
            hint_text="e.g. Gym",
            size_hint_y= None,
            height= 45,
            font_size= 17,
            padding= (12, 10),
            foreground_color= (0,00,0,1),
            cursor_color= (0.86, 0.28, 0.58, 1),
            selection_color= (0.95, 0.75, 0.85, 0.5),
            
            )

        time_label= Label(
            text="Time",
            font_size= 18,
            bold= True,
            size_hint_y= None,
            height= 25,
            halign= "left",
            valign= "middle",
            color= (0,0,0,1)
            )
        time_label.bind(size= time_label.setter("text_size"))
        current_time= datetime.now().strftime("%H:%M")
        self.time_input= TextInput(
            text=current_time,
            size_hint_y= None,
            height= 45,
            font_size= 17,
            padding= (12, 10),
            foreground_color= (0,00,0,1),
            cursor_color= (0.86, 0.28, 0.58, 1),
            multiline= False,
            selection_color= (0.95, 0.75, 0.85, 0.5)
            )

        notes= Label(
            text="Notes",
            font_size= 18,
            bold= True,
            size_hint_y= None,
            height= 25,
            halign= "left",
            valign= "middle",
            color= (0,0,0,1)
            )
        notes.bind(size= notes.setter("text_size"))
        self.notes_input= TextInput(
            hint_text="e.g. Bring water bottle",
            size_hint_y= None,
            height= 65,
            font_size= 17,
            padding= (12, 10),
            foreground_color= (0,0,0,1),
            cursor_color= (0.86, 0.28, 0.58, 1),
            multiline= True,
            selection_color= (0.95, 0.75, 0.85, 0.5)
            )

        self.reminder_label= Label(
            text="Enable Reminder",
            font_size= 18,
            bold= True,
            size_hint= (0.4, 1),
            width= 170,
            halign= "left",
            valign= "middle",
            color= (0,0,0,1)
            )
        self.reminder_label.bind(
            size= self.reminder_label.setter("text_size"))
        
        self.reminder= CheckBox(
            active=True,
            size_hint= (None, 1),
            size= (30,30),
            width=40
            )

        self.save_button= RoundedButton(
            text="Save",
            background_normal= "",
            background_color= (1.0, 0.08, 0.58, 1),
            color= (1,1,1,1)

        )

        self.save_button.bind(on_press= self.save_task)

        cancel_btn= RoundedButton(
            text="Cancel",
            color= (0,0,0,1),
            background_normal= "",
            background_color= (0.70, 0.72, 0.75, 1 )
        )

        cancel_btn.bind(on_press= self.cancel_task)

        reminder_layout= BoxLayout(
            orientation= "horizontal",
            spacing= 8,
            size_hint_y= None,
            height= 35

        )

        buttons_layout= BoxLayout(
            orientation= "horizontal",
            spacing= 15 
        )

        self.task_manager= task_manager

        self.current_task= None




        layout.add_widget(self.title)
        layout.add_widget(task_label)
        layout.add_widget(self.task_name)
        layout.add_widget(time_label)
        layout.add_widget(self.time_input)
        layout.add_widget(notes)
        layout.add_widget(self.notes_input)
        layout.add_widget(reminder_layout)
        layout.add_widget(buttons_layout)

        
        reminder_layout.add_widget(self.reminder)
        reminder_layout.add_widget(self.reminder_label)

        buttons_layout.add_widget(self.save_button)
        buttons_layout.add_widget(cancel_btn)
        
        self.bottom_nav= BottomNav(
            current_screen="add_task"
            )
        self.bottom_nav.history_button.bind(
            on_press= self.open_history
        )
        self.bottom_nav.home_button.bind(
        on_press= self.open_home
        )

        layout.add_widget(self.bottom_nav)
        self.add_widget(layout)


    def save_task(self, instance):

        name= self.task_name.text
        time= self.time_input.text.strip()
        try: 
            hour, minute= map(int, time.split(":"))

            if not (0<=hour <=23 and 0 <= minute <=59):
                raise ValueError
        except ValueError:
            self.show_feedback()
            return

        notes= self.notes_input.text
        reminder= self.reminder.active

        if self.current_task is None:
            new_task= Task(name, time, notes, reminder)
            self.task_manager.add_task(new_task)
            
        else:
            self.task_manager.cancel_reminder(self.current_task)
            self.current_task.name= name
            self.current_task.time= time 
            self.current_task.notes= notes
            self.current_task.reminder= reminder

            self.task_manager.save_tasks()

            self.task_manager.schedule_reminder(self.current_task)

            self.current_task=None
            self.title.text= "Add Task"
            self.save_button.text= "Save"

            self.manager.current= "welcome"


        self.task_name.text=""
        self.notes_input.text= ""
        self.reminder.active= True


    def cancel_task(self, instance):
        self.manager.current= "welcome"

    def load_task(self, task):
        self.current_task= task

        self.task_name.text= task.name
        self.time_input.text= task.time
        self.notes_input.text= task.notes
        self.reminder.active= task.reminder

        self.title.text= "Edit task"
        self.save_button.text= "Update"

        
    def open_home(self, instance):
        self.manager.current= "welcome"


    def open_history(self, instance):
            self.manager.current= "history"

    def show_feedback(self):

        pop= Popup(
            title= "",
            separator_height= 0,
            size_hint= (None, None), 
            size= (250, 90),
            auto_dismiss= False
        )
        pop.content= Label(
            text= "Invalid time. Use HH:MM",
            halign= "center", 
            valign= "middle"
            )
        pop.open()
        Clock.schedule_once(lambda dt: pop.dismiss(), 0.7)

    def update_bg(self, *args):
        self.bg.pos= self.pos
        self.bg.size= self.size
