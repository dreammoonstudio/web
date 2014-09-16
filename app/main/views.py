from flask import render_template, session, redirect, url_for, current_app
from ..email import send_email
from . import main
from .forms import NameForm

@main.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html', form=form, name=name)

@main.route('/user/<username>')
def user(username):
    return render_template('user.html', name=username)

