from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField

# Set your classes here.


class SiteForm(FlaskForm):
    website = StringField('Web Address')
    xpath = StringField('XPath (optional)')
    threads = IntegerField('Max Active Threads')
    time_min = IntegerField('Minimum Time (seconds)')
    time_max = IntegerField('Maximum Time (seconds)')


class ProxyForm(FlaskForm):
    ip = StringField('IP Address')
    port = StringField('Port')
    username = StringField('Username')
    password = StringField('Password')


class ScriptForm(FlaskForm):
    email = StringField('Email')
