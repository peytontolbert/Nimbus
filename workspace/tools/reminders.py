from datetime import datetime, timedelta

class reminders:
    def __init__(self):
        self.reminders = {}

    def create_reminder(self, reminder: str, time: str):
        self.reminders[reminder] = time
        return f"Reminder set for {time}"

    def get_reminders(self):
        return self.reminders

    def update_reminder(self, reminder_id: str, new_name: str, new_time: str):
        """
        This tool allows you to update the details of an existing reminder. It is useful for changing the time or name of a reminder if your plans change.
        """
        if reminder_id in self.reminders:
            self.reminders[new_name] = self.reminders.pop(reminder_id)
            self.reminders[new_name]["time"] = new_time
            return f"Reminder updated: {new_name} set for {new_time}"
        else:
            return f"Reminder '{reminder_id}' not found."

    def delete_reminder(self, reminder_id: str):
        """
        This tool enables you to delete a reminder that is no longer needed. It helps keep your reminder list organized by removing outdated or unnecessary entries.
        """
        if reminder_id in self.reminders:
            del self.reminders[reminder_id]
            return f"Reminder '{reminder_id}' deleted."
        else:
            return f"Reminder '{reminder_id}' not found."

    def snooze_reminder(self, reminder_id: str, snooze_duration: int):
        """
        This tool allows you to snooze a reminder for a specified duration. It is helpful if you are unable to attend to the reminder at the scheduled time and need a short delay.
        """
        if reminder_id in self.reminders:
            reminder_time = datetime.strptime(self.reminders[reminder_id]["time"], "%Y-%m-%d %H:%M:%S")
            snoozed_time = reminder_time + timedelta(minutes=snooze_duration)
            self.reminders[reminder_id]["time"] = snoozed_time.strftime("%Y-%m-%d %H:%M:%S")
            self.reminders[reminder_id]["snoozed"] = True
            return f"Reminder '{reminder_id}' snoozed for {snooze_duration} minutes."
        else:
            return f"Reminder '{reminder_id}' not found."

    def recurring_reminder(self, name: str, time: str, interval: str):
        """
        This tool lets you set up recurring reminders that repeat at specified intervals. It is ideal for tasks or events that occur regularly, such as weekly meetings or daily workouts.
        """
        self.reminders[name] = {"time": time, "snoozed": False, "interval": interval}
        return f"Recurring reminder '{name}' set for {time} with interval {interval}."

    def reminder_summary(self):
        """
        This tool provides a summary of all your reminders, including upcoming and past reminders. It helps you quickly assess your schedule and plan accordingly.
        """
        if not self.reminders:
            return "No reminders set."
        summary = "Reminder Summary:\n"
        for reminder, details in self.reminders.items():
            summary += f"Name: {reminder}, Time: {details['time']}, Snoozed: {details['snoozed']}, Interval: {details['interval']}\n"
        return summary