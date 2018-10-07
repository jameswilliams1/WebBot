from flask_wtf import Form
from wtforms import TextField, RadioField
from wtforms.validators import DataRequired, EqualTo, Length, Optional

# Set your classes here.


class SiteForm(Form):
    website = TextField(
        'Web Address', validators=[DataRequired()]
    )
    xpath = TextField(
        'XPath (optional)', validators=[Optional()]
    )
    threads = TextField(
        'Max Active Threads', validators=[DataRequired()]
    )


class ProxyForm(Form):
    ip = TextField('IP Address', [DataRequired()])
    port = TextField('Port', [DataRequired()])


class ScriptForm(Form):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
