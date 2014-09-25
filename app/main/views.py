from flask import render_template, session, redirect, url_for, current_app
from ..email import send_email
from . import main
from .forms import NameForm
from .. import flash
from flask.ext.babel import gettext as _
from app.auth.models import User

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash(_('Looks like you have changed your name'))
        session['name'] = form.name.data
    form.name.data = ''
    return render_template('index.html', form=form, name=session.get('name'))

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    return render_template('user.html', user=user)

