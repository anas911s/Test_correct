from models.model import EventCalendarDB


def get_gebruiker_by_username(username, password):
    event_db = EventCalendarDB()
    print(username, password)
    return event_db.get_gebruiker_by_username(username, password)


def add_user(username, password):
    event_db = EventCalendarDB()
    print(username, password)
    return event_db.add_user(username, password)


def all_users():
    users = EventCalendarDB()
    return users.get_all_users()

def get_events():
    event_model = EventCalendarDB()
    return event_model.get_all_events()


def get_agenda():
    agenda_model = EventCalendarDB()
    return agenda_model.get_all_agendas()


def get_agenda_by_name():
    agenda_name = EventCalendarDB()
    return agenda_name.get_agenda_by_name()


def get_events_by_agenda_id(agenda_id):
    event_calendar = EventCalendarDB()
    return event_calendar.get_events_by_agenda_id(agenda_id)

def get_more_events():
    event_calendar = EventCalendarDB()
    return event_calendar.get_more_events()

from models.model import EventCalendarDB


def get_event_by_id(event_id, agenda_id):
    event_calendar = EventCalendarDB()
    events = event_calendar.get_events_by_agenda_id(agenda_id)

    for event in events:
        if event['id'] == event_id:
            return event

    return None


def update_event_in_database(event_id, agenda_id, updated_name, updated_date, updated_start_time, updated_end_time, updated_location, updated_description):
    event_calendar = EventCalendarDB()
    event_calendar.update_event_in_database(event_id, agenda_id, updated_name, updated_date, updated_start_time, updated_end_time, updated_location, updated_description)