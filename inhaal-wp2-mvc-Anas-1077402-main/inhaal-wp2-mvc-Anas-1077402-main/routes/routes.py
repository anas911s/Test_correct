from os import abort
from flask import Blueprint, render_template, request, redirect, url_for, session

import routes.routes
from controllers.auth_controllers import add_user, all_users, get_events, get_agenda, get_agenda_by_name, get_more_events, get_events_by_agenda_id, update_event_in_database, get_event_by_id
from models.model import EventCalendarDB

bp = Blueprint("routes", __name__)
event_calendar = EventCalendarDB()


@bp.route("/")
def index():
    agenda_data = get_agenda()
    events_data = get_events()
    return render_template("index.html", events=events_data, agendas=agenda_data)


@bp.route("/index")
def index_session():
    if 'username' in session:
        agenda_data = get_agenda()
        events_data = get_events()
        return render_template('index_session.html', events=events_data, agendas=agenda_data)
    else:
            return render_template('login.html', error='U moet inloggen om hier te komen.')
    return render_template('login.html', error=None)


@bp.route("/register")
def register():
    return render_template("register.html")


@bp.route("/agenda")
def agenda():
    agenda = get_agenda()
    events = get_events()
    return render_template("index.html", agendas=agenda, events=events)


@bp.route("/agenda/<url_name>")
def agenda_naam(url_name):
    event_calendar = EventCalendarDB()
    result = event_calendar.get_agenda_by_name(url_name)
    if result:
        agenda_id = result['id']

        events = get_events_by_agenda_id(agenda_id)
        return render_template("agenda.html", agenda=result, events=events, agenda_id=agenda_id)
    else:
        return render_template("404_not_found.html")

@bp.route("/agenda/create")
def agenda_create():
    if 'username' not in session:
        return render_template('login.html', error='U moet inloggen om hier te komen.')
    return render_template("agenda_create.html")

@bp.route("/event/create/<int:agenda_id>")
def event_create(agenda_id):
    if 'username' not in session:
        return render_template('login.html', error='U moet inloggen om hier te komen.')
    else:
        return render_template("event_create.html", agenda_id=agenda_id)

@bp.route("/event/<int:event_id>")
def event_detail(event_id):
    events = get_events()

    selected_event = None
    for event in events:
        if event['id'] == event_id:
            selected_event = event

    if selected_event:
        return render_template("event.html", events=selected_event)
    else:
        return render_template("404_not_found.html")



@bp.route("/agenda/show_more_events/<int:num_to_show>")
def show_more_events(num_to_show):

    agenda_id = request.args.get('agenda_id')
    more_events = event_calendar.get_more_events(num_to_show)
    if not more_events:
        return render_template("404_not_found.html")
    else:
        return render_template("agenda.html", events=more_events, agenda=agenda_id)


@bp.route("/opslaan_agenda", methods=["POST"])
def opslaan_agenda():
    titel = request.form.get("titel")
    url_naam = request.form.get("url_naam")
    stylesheet_select = request.form.get("stylesheet_select")
    event_calendar.opslaan_agenda(titel, url_naam, stylesheet_select)

    return redirect(url_for("routes.index"))

@bp.route("/opslaan_event/<int:agenda_id>", methods=["POST"])
def opslaan_event(agenda_id):
    name = request.form.get("name")
    event_date = request.form.get("event_date")
    start_time = request.form.get("start_time")
    end_time = request.form.get("end_time")
    location = request.form.get("location")
    beschrijving = request.form.get("beschrijving")

    event_calendar.opslaan_event(agenda_id, name, event_date, start_time, end_time, location, beschrijving)
    return redirect(url_for("routes.index"))

@bp.route("/event/delete/<int:event_id>", methods=["GET", "POST"])
def delete_event(event_id):
    if 'username' not in session:
        return render_template('login.html', error='U moet inloggen om hier te komen.')
    agenda_url_name = request.args.get('url_name')

    event_calendar.delete_event(event_id)

    return redirect(url_for("routes.index", url_name=agenda_url_name))


@bp.route("/event/update/<int:event_id>/<int:agenda_id>", methods=["GET", "POST"])
def update_event_form(event_id, agenda_id):
    if 'username' not in session:
        return render_template('login.html', error='U moet inloggen om hier te komen.')
    event = get_event_by_id(event_id, agenda_id)
    if not event:
        return render_template("404_not_found.html")

    if request.method == "GET":
            return render_template("update_event.html", event=event)
    elif request.method == "POST":
        updated_name = request.form.get("name")
        updated_date = request.form.get("event_date")
        updated_start_time = request.form.get("start_time")
        updated_end_time = request.form.get("end_time")
        updated_location = request.form.get("location")
        updated_description = request.form.get("beschrijving")

        success = event_calendar.update_event_in_database(event_id, updated_name, updated_date, updated_start_time, updated_end_time, updated_location, updated_description)

        if success:
            return redirect(url_for("routes.index"))
        else:
            return redirect(url_for("routes.index"))


@bp.route("/admin_panel", methods=["GET", "POST"])
def admin_panel():
    if request.method == "POST":
        username = request.form.get("new_username")
        password = request.form.get("new_password")
        is_admin = request.form.get("is_admin")

        is_admin = 1 if is_admin else 0

        event_calendar.add_user(username, password, is_admin)

        return redirect(url_for('routes.admin_panel'))

    existing_users = all_users()
    print(existing_users)

    return render_template("admin_panel.html", users=existing_users)

@bp.route("/delete_user/<int:user_id>")
def delete_user(user_id):
    event_calendar = EventCalendarDB()
    event_calendar.delete_user(user_id)

    return redirect(url_for("routes.admin_panel"))
