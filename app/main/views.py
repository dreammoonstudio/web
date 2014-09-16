from flask import render_template, session, redirect, url_for, current_app
from ..email import send_email
from . import main
from .forms import NameForm
from .. import flash
from flask.ext.babel import gettext as _

@main.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash(_('Looks like you have changed your name'))
    return render_template('index.html', form=form, name=name)

@main.route('/user/<username>')
def user(username):
    return render_template('user.html', name=username)

