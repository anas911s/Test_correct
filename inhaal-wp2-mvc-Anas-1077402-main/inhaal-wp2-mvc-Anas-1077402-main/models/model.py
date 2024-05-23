import sqlite3
import os
from typing import List, Any


class EventCalendarDB:
    def __init__(self, db_path='databases/event_calendar.db'):
        self.db_path = os.path.abspath(db_path)

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def get_gebruiker_by_username(self, username, password):
        conn = self._connect()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        gebruiker = cursor.fetchone()
        conn.close()
        return dict(gebruiker) if gebruiker is not None else None

    def add_user(self, username, password, is_admin=0):
        conn = self._connect()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)", (username, password, is_admin))
        conn.commit()
        conn.close()

    def get_all_users(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        print(users)
        users_list = [{'id': user[0], 'username': user[1], 'password': user[2], 'is_admin': user[3]} for user in users]

        return users_list
    def get_all_events(self):
        conn = self._connect()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        query = 'SELECT * FROM events'
        print(f"Query: {query}")
        try:
            events = cursor.execute(query).fetchall()
        except Exception as e:
            print(f"Error executing query: {e}")
            return []

        conn.close()

        print(events)

        return events

    def get_all_agendas(self):
        conn = self._connect()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        query = 'SELECT * FROM agendas'
        try:
            agendas = cursor.execute(query).fetchall()
        except Exception as e:
            print(f"Error executing query: {e}")
            return []
        conn.close()

        return agendas

    def get_agenda_by_name(self, agenda_naam):
        agendas = self.get_all_agendas()
        for agenda in agendas:
            if agenda['url_name'] == agenda_naam:
                return agenda
        return None

    def get_events_by_agenda_id(self, agenda_id):
        conn = self._connect()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events WHERE agenda_id = ?", (agenda_id,))
        events = cursor.fetchall()
        conn.close()

        return events

    def get_more_events(self, num_to_show):
        conn = self._connect()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events LIMIT ?", (num_to_show,))
        more_events = cursor.fetchall()
        conn.close()
        return more_events

    def opslaan_agenda(self, titel, url_name, external_stylesheet):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO agendas (title, url_name, external_stylesheet) VALUES (?, ?, ?)",
                       (titel, url_name, external_stylesheet))

        conn.commit()
        conn.close()

    def opslaan_event(self, agenda_id, name, event_date, start_time, end_time, location, beschrijving):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO events (agenda_id,name, event_date, start_time, end_time, location, description) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (agenda_id, name, event_date, start_time, end_time, location, beschrijving))

        conn.commit()
        conn.close()

    def delete_event(self, event_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
        conn.commit()
        conn.close()

    # model.py
    def update_event_in_database(self, event_id, updated_name, updated_date, updated_start_time, updated_end_time,
                                 updated_location, updated_description):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE events
            SET name = ?, event_date = ?, start_time = ?, end_time = ?, location = ?, description = ?
            WHERE id = ?
        """, (updated_name, updated_date, updated_start_time, updated_end_time, updated_location, updated_description,
              event_id))

        conn.commit()
        conn.close()

    def delete_user(self, user_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()

