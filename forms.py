from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, FileField, BooleanField, FieldList

# Set your classes here.


class SiteForm(FlaskForm):
    website = StringField('Web address')
    xpath = StringField('Target Xpath (optional)')
    threads = IntegerField('Max active threads for main program')
    start_threads = IntegerField('Max active threads while gathering page links at startup')
    time_min = IntegerField('Minimum thread time (seconds)')
    time_max = IntegerField('Maximum thread time (seconds)')
    display_windows = BooleanField("Display browser windows? ")
    total_bots = IntegerField("Total bots to run (0 for infinite)")


class ProxyForm(FlaskForm):
    proxy_type = SelectField('Proxy type', choices=[('none', 'None'), ('list', 'Use proxy list'), ('rotating', 'Use rotating proxy')])


class RotatingForm(FlaskForm):
    ip = StringField('IP Address/host (including http://)')
    port = IntegerField('Port')


class ListForm(FlaskForm):
    list_file = StringField("File path to proxy list")


class ScriptForm(FlaskForm):
    script_items = FieldList(SelectField("Choose action: ", choices=[('none', ''), ('sleep', 'Pause'), ('scroll_up', 'Scroll up'), ('scroll_down', 'Scroll down'), ('press_key', 'Press key'), ('left_click', 'Left click')]), min_entries=1, max_entries=25)
    pause_time_min = IntegerField("Minimum pause time (seconds)")
    pause_time_max = IntegerField("Maximum pause time (seconds)")
    min_scroll_count = IntegerField("Minimum number of scroll actions to perform")
    max_scroll_count = IntegerField("Maximum number of scroll actions to perform")
    key_press = StringField("Enter key to press (leave blank for random)")
    min_click_count = IntegerField("Minimum number of left click actions to perform")
    max_click_count = IntegerField("Maximum number of left click actions to perform")
    min_xpath = IntegerField("Minimum time after which to click target XPath")
    max_xpath = IntegerField("Maximum time before which to click target XPath")
