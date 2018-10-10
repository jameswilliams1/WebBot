from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, FileField, BooleanField

# Set your classes here.


class SiteForm(FlaskForm):
    website = StringField('Web address')
    xpath = StringField('Target Xpath (optional)')
    threads = IntegerField('Max active threads')
    time_min = IntegerField('Minimum thread time (seconds)')
    time_max = IntegerField('Maximum thread time (seconds)')
    display_windows = BooleanField("Display browser windows? ")


class ProxyForm(FlaskForm):
    proxy_type = SelectField('Proxy type', choices=[('none', 'None'), ('list', 'Use proxy list'), ('rotating', 'Use rotating proxy')])


class RotatingForm(FlaskForm):
    ip = StringField('IP Address/host (including http://)')
    port = IntegerField('Port')


class ListForm(FlaskForm):
    list_file = StringField("File path to proxy list")


class ScriptForm(FlaskForm):
    email = StringField('Email')
