import json
history_file= "storage/history.json"

class HistoryManager:
    def __init__(self):
        self.history= {
            "last_opened": "",
            "history": {}
        }

        self.load_history()


    def save_history(self):
        with open(history_file, "w") as file:
            json.dump(self.history, file, indent=4)

    def load_history(self):
        try:
            with open(history_file, "r") as file:
                self.history= json.load(file)

        except (FileNotFoundError, json.JSONDecodeError):
            self.history= {
                "last_opened": "",
                "history": {}
            }

    def archive_day(self, date, tasks):
        day_tasks= []

        for task in tasks:
            day_tasks.append(task.to_dict())

        self.history["history"][date]= day_tasks
        self.save_history()