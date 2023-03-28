import functools
import hashlib
from Database import Database
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)


bp = Blueprint('auth', __name__, url_prefix='/auth')
dataBase = Database()
db = dataBase.get_db()

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            usernameDB = db['users'].find({'username': username}).limit(1)
            if usernameDB.count_documents() > 0:
                error = 'User {} is already registered.'.format(username)
            else:
                db['users'].insert_one({'username': username, 'password': password})
                return redirect(url_for('auth.login'))
        flash(error)
    return render_template('register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        error = None

        cursor = db.users.find({'username': username, 'password': password}).limit(1)
        user = next(cursor, None)
        if len(list(cursor.clone())) == 0:
            error = 'Incorrect username or password.'
        else:
            session.clear()
            session['user_id'] = user['username']
            return redirect(url_for('index'))
        flash(error)
    return render_template('login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = db['users'].find({'username': user_id}).limit(1)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


