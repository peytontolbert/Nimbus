class eventmanagement:
    def __init__(self):
        # Dictionary to hold events with event_name as the key
        self.events = {}

    def eventscheduler(self, event_name, date, location, invitees, user_permission):
        """
        Aids in planning and scheduling events, sending invites, and managing RSVPs.

        Args:
            event_name (str): The name of the event.
            date (str): The date of the event.
            location (str): The location of the event.
            invitees (list of str): A list of invitees' names.
            user_permission (bool): User permission required to schedule the event.

        Returns:
            str: Confirmation message about the event scheduling.
        """
        if not user_permission:
            return "User permission is required to schedule an event."

        if event_name in self.events:
            return f"Event '{event_name}' is already scheduled."

        # Schedule the event
        self.events[event_name] = {
            'date': date,
            'location': location,
            'invitees': {invitee: 'Pending' for invitee in invitees}
        }

        # Simulate sending invites
        self.send_invites(event_name)

        return f"Event '{event_name}' scheduled successfully on {date} at {location}."

    def send_invites(self, event_name):
        """
        Simulates sending invites to all invitees for a given event.

        Args:
            event_name (str): The name of the event.
        """
        event = self.events.get(event_name)
        if not event:
            print(f"No event found with the name '{event_name}'.")
            return

        print(f"Sending invites for '{event_name}'...")
        for invitee in event['invitees']:
            print(f"Invite sent to {invitee}. RSVP status: {event['invitees'][invitee]}")

    def update_rsvp(self, event_name, invitee, rsvp_status):
        """
        Updates the RSVP status for a given invitee.

        Args:
            event_name (str): The name of the event.
            invitee (str): The name of the invitee.
            rsvp_status (str): The RSVP status ('Accepted', 'Declined', or 'Pending').
        """
        event = self.events.get(event_name)
        if not event:
            print(f"No event found with the name '{event_name}'.")
            return

        if invitee not in event['invitees']:
            print(f"No invitee found with the name '{invitee}'.")
            return

        event['invitees'][invitee] = rsvp_status
        print(f"RSVP status for {invitee} updated to '{rsvp_status}' for event '{event_name}'.")