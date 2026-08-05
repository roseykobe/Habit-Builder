from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class ReminderPopup(Popup):
    def __init__(self, task, task_manager,**kwargs):
        super().__init__(**kwargs)

        self.task= task
        self.task_manager= task_manager 
        

        self.title= "Reminder"
        self.size_hint= (0.8, 0.4)
        self.auto_dismiss= False

        layout= BoxLayout(
            orientation= "vertical",
            spacing= 10,
            padding= 10
        )

        task_label= Label(
            text= f"[b]{self.task.name}[/b]",
            markup= True
        )
        layout.add_widget(task_label)

        if self.task.notes.strip():
            notes_label= Label(
                text= f"{self.task.notes}:-"
            )
            layout.add_widget(notes_label)

        button_layout= BoxLayout(
            orientation= "horizontal",
            spacing= 10,
            size_hint_y= None,
            height= 50
        )

        complete_btn= Button(text="Complete")
        snooze_btn= Button(text="Snooze")
        close_btn= Button(text="Dismiss")

        complete_btn.bind(on_press=self.complete_task)
        snooze_btn.bind(on_press= self.snooze_task)
        close_btn.bind(on_press= self.close_popup)

        button_layout.add_widget(complete_btn)
        button_layout.add_widget(snooze_btn)
        button_layout.add_widget(close_btn)

        layout.add_widget(button_layout)

        self.content= layout

    def complete_task(self, instance):
        self.task_manager.complete_task(self.task)

        if self.task_manager.welcome_screen:

            self.task_manager.welcome_screen.load_tasks()
        self.dismiss()

    def snooze_task(self, instance):
        self.task_manager.snooze_task(self.task)

        if self.task_manager.welcome_screen:
            self.task_manager.welcome_screen.load_tasks()
        self.dismiss()

    def close_popup(self, instance):
        self.dismiss()
