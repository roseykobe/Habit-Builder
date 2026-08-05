class Task:
    def __init__(self, name, time, notes, reminder, status= "pending"):
        self.name= name
        self.time= time 
        self.notes= notes 
        self.reminder= reminder
        self.reminder_event= None
        self.status= status

    def to_dict(self):

        return {
            "name": self.name,
            "time": self.time,
            "notes": self.notes,
            "reminder": self.reminder,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):

        return cls(
            data["name"],
            data["time"],
            data["notes"],
            data["reminder"],
            data.get("status", "pending")
        )
        