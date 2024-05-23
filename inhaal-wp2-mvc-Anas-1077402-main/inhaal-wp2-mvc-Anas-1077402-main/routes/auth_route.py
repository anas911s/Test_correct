from typing import Dict, Any

from flask import Blueprint, render_template, request, redirect, url_for, session
from controllers.auth_controllers import add_user, get_gebruiker_by_username

auth_bp: Blueprint = Blueprint('auth', __name__)


@auth_bp.route('/auth/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('routes.index_session'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        gebruiker = get_gebruiker_by_username(username, password)
        print(gebruiker)
        if gebruiker:
            session['username'] = username
            session['user_id'] = gebruiker["id"]
            session['is_admin'] = gebruiker["is_admin"]
            session.permanent = True
            return redirect(url_for("routes.index_session"))
        else:
            return render_template('login.html', error='Gebruikersnaam of wachtwoord komen niet overeen.')
    return render_template('login.html', error=None)


@auth_bp.route('/auth/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('index'))

    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']

        gebruiker = get_gebruiker_by_username(username, password)

        if not username or not password or not password2:
            error = 'Alle velden zijn verplicht'
        elif gebruiker:
            error = 'Gebruikersnaam bestaat al. Probeer het opnieuw.'
        elif password != password2:
            error = 'De herhaalde wachtwoord invoer komt niet overeen. Probeer het opnieuw.'
        else:
            add_user(username, password)
            print('Succesvol geregistreerd, u kunt nu inloggen', 'success')
            return redirect(url_for('auth.login'))

    return render_template('register.html', error=error)


@auth_bp.route('/auth/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('auth.login'))
