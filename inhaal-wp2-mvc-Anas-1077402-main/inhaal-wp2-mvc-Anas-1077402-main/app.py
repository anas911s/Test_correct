from flask import Flask, render_template, url_for, session
from routes.routes import bp as routes_bp
from routes.auth_route import auth_bp
from controllers.auth_controllers import get_events

app = Flask(__name__)
app.secret_key = "conquer_the_world"
app.register_blueprint(routes_bp)
app.register_blueprint(auth_bp)


@app.route('/')
def index():
    is_logged_in = 'username' in session
    is_admin = session.get("is_admin", False) if is_logged_in else False
    user_id = session.get("user_id", None) if is_logged_in else None
    events = get_events()
    return render_template('index.html', newData=['name1', 'name2'], events=events, user_id=user_id if not None else None,
                           is_admin=is_admin, is_logged_in=is_logged_in)

if __name__ == "__main__":
    app.run(debug=True)
