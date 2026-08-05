from kivy.config import Config
Config.set("kivy","window_icon", "assets/icon.png" )
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens.splash_screen import SplashScreen
from screens.welcome_screen import WelcomeScreen
from screens.add_task_screen import AddTaskScreen
from models.task_manager import TaskManager
from models.history_manager import HistoryManager
from screens.history_screen import HistoryScreen 


class HabitBuilderApp(App):

    def build(self):


        sm= ScreenManager()

        task_manager= TaskManager()

        task_manager.load_tasks()
    
        welcome_screen= WelcomeScreen(task_manager= task_manager, name= "welcome")
        sm.add_widget(SplashScreen(task_manager= task_manager, name="splash"))
        sm.add_widget(welcome_screen)
        task_manager.welcome_screen= sm.get_screen("welcome")
        sm.add_widget(AddTaskScreen(task_manager= task_manager, name="add_task"))
        sm.add_widget(HistoryScreen(name= "history"))
        

        sm.current = "splash"

        return sm

HabitBuilderApp().run()