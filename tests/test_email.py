from flask.ext.mail import Message
from app import mail, create_app
from flask import current_app
import unittest

class TestEmailSend(unittest.TestCase):

    def setup(self):
        self.app = create_app('test')
        msg = Message('test', sender='admin@dreammoonstudio.com', recipients=['charixandra@hotmail.com'])
        msg.body = 'text body'
        msg.html = '<b>HTML</b> body'
        with self.app.app_context():
            mail.send(msg)

    def test_app_is_testing(self):
        self.setup()
