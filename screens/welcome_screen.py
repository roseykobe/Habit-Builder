from kivy.uix.screenmanager import Screen 
from kivy.uix.button import Button  
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.label import Label
from models.task_manager import TaskManager
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView 
from components.bottom_nav import BottomNav
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from components.rounded_button import RoundedButton
from components.rounder_progress_bar import RoundedProgressBar


class WelcomeScreen(Screen):

    def __init__(self, task_manager, **kw):
        super().__init__(**kw)

        self.layout= BoxLayout(
            orientation= "vertical",
            spacing= 20, 
            padding= (25, 25, 25, 0) 
        )
        with self.layout.canvas.before:
            Color (1.0, 0.80, 0.87, 1)
            self.bg_rect= Rectangle(pos= self.layout.pos, size= self.layout.size)

        self.layout.bind (pos= self.update_bg, size= self.update_bg)

        self.title= Label(
            text="Welcome to Habit Builder",
            size_hint= (1, 0.2),
            font_size= 32,
            color= (0,0,0,1),
            bold= True
        )

        self.slogan= Label(
            text= "Every habit starts with one task" ,
            font_size= 15,
            size_hint= (1, 0.1),
            color= (0,0,0,1)
        )

        self.button= RoundedButton(
            text="Create My First Task",
            size_hint= (0.9, None), 
            height= 55,
            color= (1,1,1,1), 
            background_normal= "",
            background_color= (1.0, 0.08, 0.58, 1), 
            pos_hint= {"center_x": 0.5}
        )

        self.button.bind(on_press=self.button_clicked)

        self.copy_button= Button(
            text="Copy Yesterday's Schedule",
            size_hint= (1, None),
            height= 50,
            color= (1,1,1,1),
            background_normal= "",
            background_color= (0.86, 0.28, 0.58, 1)
        )
        self.copy_button.bind(on_press= self.copy_last_schedule)

        self.or_label= Label(
            text= "or",
            size_hint= (1, None),
            height= 30,
            color= (0,0,0,1)
        )

        self.progress_layout= BoxLayout(
            orientation= "horizontal",
            size_hint= (1, 0.05)
        )

        self.progress_bar= RoundedProgressBar(
            size_hint= (0.9, None),
            height= 25
        )
        self.progress_label= Label(
            text="0/0",
            size_hint= (None, 0.05),
            width= 55,
            color= (0, 0, 0, 1)
        )

        self.pending_label= Label(text="Pending Tasks",
        size_hint= (1, 0.1), 
        color= (0,0,0,1),
        bold= True
        )
        self.complete_label= Label(text="Completed Tasks",
        size_hint= (1, 0.1),
        color= (0,0,0,1),
        bold= True
        )
        self.pending_layout= BoxLayout(
            orientation= "vertical",
            spacing=10,
            size_hint_y= None,
            padding= 20
        )
        self.pending_layout.bind(
            minimum_height=self.pending_layout.setter("height")
        )
        self.completed_layout= BoxLayout(
            orientation= "vertical",
            spacing=10,
            size_hint_y= None,
            padding= 20
        )
        self.completed_layout.bind(
            minimum_height= self.completed_layout.setter("height")
        )
        self.content_layout= BoxLayout(
            orientation= "vertical",
            spacing= 10,
            size_hint_y= None,
            padding= (0, 20, 0, 20)
        )
        self.content_layout.bind(
            minimum_height=self.content_layout.setter("height")
        )
        self.scroll= ScrollView(
            size_hint= (1, 1)
        )
        self.scroll.add_widget(self.content_layout)

        self.task_manager= task_manager

        self.layout.add_widget(self.title)
        self.layout.add_widget(self.slogan)

        self.layout.add_widget(self.progress_layout)
        self.progress_layout.add_widget(self.progress_bar)
        self.progress_layout.add_widget(self.progress_label)

        self.content_layout.add_widget(self.pending_label)
        self.content_layout.add_widget(self.pending_layout)

        self.content_layout.add_widget(self.complete_label)
        self.content_layout.add_widget(self.completed_layout)

        self.layout.add_widget(self.scroll)
        self.layout.add_widget(self.button)

        
        self.bottom_nav= BottomNav(current_screen="welcome")
        self.bottom_nav.history_button.bind(
            on_press= self.open_history
        )
        self.layout.add_widget(self.bottom_nav)

        self.add_widget(self.layout)
        
        self.load_tasks()

        
    def button_clicked(self, instance):
        self.manager.current= "add_task"

    def load_tasks(self):
        self.pending_layout.clear_widgets()
        self.completed_layout.clear_widgets()

        tasks= self.task_manager.get_tasks()
        pending_tasks= self.task_manager.get_pending_tasks()
        completed_tasks= self.task_manager.get_completed_tasks()

        total_tasks= len(tasks)
        completed_count= len(completed_tasks)
        self.progress_label.text= f"{completed_count}/{total_tasks}"

        if len(pending_tasks)>0:
            self.pending_label.opacity=1
            self.pending_label.height= 30
            self.pending_layout.opacity=1
            self.pending_layout.height= self.pending_layout.minimum_height
        else:
            self.pending_label.opacity= 0
            self.pending_label.height=0
            self.pending_layout.opacity= 0
            self.pending_layout.height= 0

        if len(completed_tasks) >0:
            self.complete_label.opacity= 1
            self.complete_label.height= 30
            self.completed_layout.opacity=1
            self.completed_layout.height= self.completed_layout.minimum_height
        else:
            self.complete_label.opacity= 0
            self.complete_label.height=0
            self.completed_layout.opacity=0
            self.completed_layout.height= 0

        if total_tasks== 0:
            self.progress_bar.max = 1
            self.progress_bar.value= 0
        else:
            self.progress_bar.max = total_tasks
            self.progress_bar.value= completed_count 
        self.progress_bar.update_bar()

        if len(tasks) >0:
            self.title.text= "Today's Tasks"
            self.layout.remove_widget(self.slogan)
            self.button.text= "+ Add Task"
        else:
            self.title.text= "Welcome to Habit Builder"
            self.slogan.text= "Every habit starts with one task."
            self.button.text= "Create My First Task"

        for task in pending_tasks:
            self.task_button= RoundedButton(
                text= f"{task.time} - {task.name}",
                size_hint_y= None,
                background_normal= "",
                background_color= (0.99, 0.56, 0.67, 1),
                color= (0,0,0,1),
                height= 70
                )
            self.pending_label.text= f"Pending ({len(pending_tasks)})"
            self.task_button.halign= "left"
            self.task_button.valign= "middle"
            self.task_button.bind(
                width= lambda instance, value:
                setattr(instance, "text_size", (value - 20, None))
            )
            self.task_button.texture_update()
            self.task_button.height= self.task_button.texture_size[1]+25
            self.task_button.task= task
            self.task_button.bind(on_press= self.task_clicked)
            self.pending_layout.add_widget(self.task_button)

        for task in completed_tasks:
            self.task_button= Button(
                text=f"Done - {task.time} - {task.name}",
                size_hint_y= None,
                background_normal= "",
                background_color= (0.18, 0.80, 0.44, 1),
                color= (0,0,0,1)
            )
            
            self.complete_label.text= f"Completed ({len(completed_tasks)})"
            self.task_button.halign= "left"
            self.task_button.valign= "middle"
            self.task_button.bind(
            width= lambda instance, value:
            setattr(instance, "text_size", (value - 20, None))
            )
            self.task_button.texture_update()
            self.task_button.height= self.task_button.texture_size[1]+25
            self.task_button.task=task 
            self.task_button.bind(on_press=self.task_clicked)
            self.completed_layout.add_widget(self.task_button)

            if total_tasks >0 and len(completed_tasks) == total_tasks:
                self.complete_label.text= f"All Tasks Completed ({len(completed_tasks)})"

        if len(tasks)== 0 and self.task_manager.can_restore_last_schedule():
                button_index= self.layout.children.index(self.button)

                if self.copy_button.parent is None:
                    self.layout.add_widget(self.copy_button, index= button_index)

                button_index= self.layout.children.index(self.button)

                if self.or_label.parent is None:
                    self.layout.add_widget(self.or_label, index= button_index)

        else:
            if self.copy_button.parent:
                self.layout.remove_widget(self.copy_button)

            if self.or_label.parent:
                self.layout.remove_widget(self.or_label)

    def on_pre_enter(self):
        self.load_tasks()

    def task_clicked(self, button):
        task= button.task
        self.show_task_menu(task)

    def show_task_menu(self, task):
        self.popup_layout= BoxLayout(
            orientation= "vertical",
            spacing= 10,
            padding= 10
        )

        complete_btn= Button(text="Complete")
        edit_btn= Button(text="Edit")
        self.delete_btn= Button(text="Delete")
        snooze_btn= Button(text="Snooze")
        cancel_btn= Button(text="Cancel")
        mark_pending_button= Button(text="Mark as pending")

        if task.status == "completed":
            self.popup_layout.add_widget(mark_pending_button)
            self.popup_layout.add_widget(edit_btn)
            self.popup_layout.add_widget(self.delete_btn)
            self.popup_layout.add_widget(cancel_btn)
        else:
            self.popup_layout.add_widget(complete_btn)
            self.popup_layout.add_widget(snooze_btn)
            self.popup_layout.add_widget(edit_btn)
            self.popup_layout.add_widget(self.delete_btn)
            self.popup_layout.add_widget(cancel_btn)

        self.popup= Popup(
            title="Task Options",
            content=self.popup_layout,
            size_hint= (0.7, 0.6),
            auto_dismiss=False
        )

        cancel_btn.bind(
            on_press=lambda instance: self.popup.dismiss()
        )
        self.delete_btn.bind(
            on_press= lambda instance: self.delete_task_confirm(task)
        )
        edit_btn.bind(
            on_press= lambda instance: self.edit_task(task))

        complete_btn.bind(
            on_press= lambda instance: self.complete_task(task)
        )

        snooze_btn.bind(
            on_press= lambda instance: self.snooze_task(task)
        )
        mark_pending_button.bind(
            on_press= lambda instance: self.mark_as_pending(task)
        )
        self.popup.open()

    def popup_dismiss(self, instance):
        self.popup.dismiss()

    def complete_task(self, task):
        self.task_manager.complete_task(task)
        self.popup.dismiss()
        Clock.schedule_once(lambda dt: self.load_tasks(), 0)
        self.load_tasks()
        

    def snooze_task(self, task):
        self.task_manager.snooze_task(task)
        self.popup.dismiss()

        self.popup.dismiss()
        self.load_tasks()
        self.show_feedback ("Snoozed for 10 minutes")

    def delete_task_confirm(self, task):
        self.popup.dismiss()

        self.delete_confirm= BoxLayout(
            orientation= "vertical",
            spacing= 10,
            padding= 10
        )
        
        self.confirmation_message= Label(text=f"Are you sure you want to\ndelete {task.name}")
        self.yes_btn= Button(text="Yes")
        self.no_btn= Button(text="No")

        self.delete_confirm.add_widget(self.confirmation_message)
        self.delete_confirm.add_widget(self.yes_btn)
        self.delete_confirm.add_widget(self.no_btn)

        self.delete_popup= Popup(
            title= "Delete Task?",
            content= self.delete_confirm,
            size_hint= (0.7, 0.4)
        )

        
        self.yes_btn.bind(
            on_press= lambda instance: self.delete_task(task) 
        )
        self.no_btn.bind(on_press= self.cancel_deletion)

        self.delete_popup.open()
        

    def delete_task(self, task):
        self.task_manager.delete_tasks(task)
        self.delete_popup.dismiss()
        self.load_tasks()
        self.show_feedback ("Task deleted.")



    def cancel_deletion(self, instance):
        self.delete_popup.dismiss() 

    def edit_task(self, task):
        add_task_screen= self.manager.get_screen("add_task")

        add_task_screen.load_task(task)
        self.manager.current= "add_task"

        self.popup.dismiss()
        

    def open_history(self, instance):
        self.manager.current= "history"

    def copy_last_schedule(self, instance):
        self.task_manager.restore_last_schedule()
        self.show_feedback(f"Yesterday copied!")

        self.load_tasks()
        

    def mark_as_pending(self, task):
        task.status= "pending"
        self.task_manager.schedule_reminder(task)
        self.task_manager.save_tasks()
        self.load_tasks()
        self.popup.dismiss()

    def show_feedback(self, message):

        feedback_popup= Popup(
            title= "",
            separator_height= 0,
            size_hint= (None, None), 
            size= (250, 90),
            auto_dismiss= False
        )
        feedback_popup.content= Label(
            text= message,
            halign= "center", 
            valign= "middle"
            )

        feedback_popup.open()
        Clock.schedule_once(lambda dt: feedback_popup.dismiss(), 0.4)

    def update_bg(self, *args):
        self.bg_rect.pos= self.layout.pos
        self.bg_rect.size= self.layout.size


    