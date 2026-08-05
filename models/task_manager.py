import json 
from models.task import Task
from kivy.clock import Clock
from datetime import datetime, timedelta
from screens.reminder_popup import ReminderPopup
from models.history_manager import HistoryManager
from datetime import date


class TaskManager:
    def __init__(self):
        
        self.welcome_screen= None 
        
        self.tasks= []
        self.history_manager= HistoryManager()

        self.load_tasks()
        self.check_new_day()
    

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

        self.schedule_reminder(task)

    def get_tasks(self):
        return self.tasks
    
    def delete_tasks(self, task):
        self.cancel_reminder(task)
        self.tasks.remove(task)
        self.save_tasks()

    def complete_task(self, task):
        self.cancel_reminder(task)
        task.status= "completed"
        self.save_tasks()

    def save_tasks(self):
        task_data= []

        for task in self.tasks:
            task_data.append(task.to_dict())

        with open("storage/tasks.json", "w") as file:
            json.dump(task_data, file, indent=4)


    def load_tasks(self):
        try:
            with open("storage/tasks.json", "r") as file:
                task_data= json.load(file)

            self.tasks.clear()

            for data in task_data:
                task= Task.from_dict(data)
                self.tasks.append(task)
                self.schedule_reminder(task)

        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks= []


    def schedule_at(self, task, reminder_time):
        now= datetime.now()  

        if reminder_time<= now:
            return

        seconds = (reminder_time-now).total_seconds()

        task.reminder_event= Clock.schedule_once(
            lambda dt: self.show_reminder(task),
            seconds
        )


    def schedule_reminder(self, task):

        if not task.reminder:
            return

        now= datetime.now()
        reminder_time= datetime.strptime(task.time, "%H:%M")
        reminder_time=reminder_time.replace(
            year=now.year,
            month=now.month,
            day=now.day
        )

        if reminder_time < now:
            reminder_time+=timedelta(days=1)

        self.schedule_at(task, reminder_time)
        

    def show_reminder(self, task):
        task.reminder_event= None

        popup= ReminderPopup(task, self)
        popup.open()
    

    def cancel_reminder(self, task):
        if task.reminder_event is not None:
            task.reminder_event.cancel()
            task.reminder_event= None

    def snooze_task(self, task):
        self.cancel_reminder(task)

        reminder_time = datetime.now() + timedelta(minutes=10)

        self.schedule_at(task, reminder_time)

    def get_pending_tasks(self):
        return [task for task in self.tasks if task.status == "pending"]

    def get_completed_tasks(self):
        return [task for task in self.tasks if task.status == "completed"]


    def check_new_day(self):
    
        today= date.today().isoformat()
        last_opened= self.history_manager.history["last_opened"]

        if last_opened=="":
            self.history_manager.history["last_opened"] = today
            self.history_manager.save_history()
            return

        if today != last_opened:
            self.history_manager.archive_day(last_opened, self.tasks)

            self.tasks.clear()
            self.save_tasks()

            self.history_manager.history["last_opened"] = today
            self.history_manager.save_history()


    def restore_last_schedule(self):

        last_date= self.get_last_schedule_date()

        if last_date is None:
            return False

        schedule = self.get_schedule(last_date)

        restored_tasks= self.prepare_tasks_for_today(schedule)


        self.replace_today_schedule(restored_tasks)

        return True
        

    def get_last_schedule_date(self): 
        history= self.history_manager.history["history"]

        if not history:
            return None
        return max(history.keys())

    def get_schedule(self, date):
        history= self.history_manager.history["history"]
        
        schedule= history.get(date, [])
        return schedule

    def prepare_tasks_for_today(self, tasks):
        restored_tasks= []

        for task in tasks:
            new_data= task.copy()
            new_data["status"] = "pending"
            new_task= Task.from_dict(new_data)
            restored_tasks.append(new_task)

        return restored_tasks

    def replace_today_schedule(self, tasks):
        
        self.tasks.clear()

        self.tasks.extend(tasks)

        self.save_tasks()

    def can_restore_last_schedule(self):
        return self.get_last_schedule_date() is not None


