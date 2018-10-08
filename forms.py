from flask_wtf import FlaskForm
from wtforms import StringField

# Set your classes here.


class SiteForm(FlaskForm):
    website = StringField('Web Address')
    xpath = StringField('XPath (optional)')
    threads = StringField('Max Active Threads')


class ProxyForm(FlaskForm):
    ip = StringField('IP Address')
    port = StringField('Port')


class ScriptForm(FlaskForm):
    email = StringField('Email')
