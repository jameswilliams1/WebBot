#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, flash, redirect, url_for
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
import random, threading, webbrowser
from logging import Formatter, FileHandler
from forms import *
import os
import OpenSite
from threading import Thread

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.secret_key = "12345678910"

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/', methods=('GET', 'POST'))
def home():
    form = SiteForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            OpenSite.update_site(form.website.data)
            OpenSite.update_target(form.xpath.data)
            OpenSite.update_threads(form.threads.data)
            OpenSite.update_startup_threads(form.start_threads.data)
            OpenSite.update_min(form.time_min.data)
            OpenSite.update_max(form.time_max.data)
            OpenSite.show_windows(form.display_windows.data)
            total_number_bots = form.total_bots.data
            if total_number_bots == 0:
                total_number_bots = 999999999
            OpenSite.update_total_bots(int(total_number_bots))
            flash("Website details saved")
            return redirect('/proxy')
        else:
            flash("There was a problem with the details submitted")
    return render_template('pages/home.html', form=form)


@app.route('/proxy', methods=('GET', 'POST'))
def proxy():
    form = ProxyForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        choice = form.proxy_type.data
        OpenSite.update_proxy(choice)
        if choice == 'none':
            OpenSite.clear_proxy()
            flash('Proxy details saved')
            return redirect('/script')
        if choice == 'list':
            return redirect('/list')
        if choice == 'rotating':
            return redirect('/rotating')
    return render_template('pages/proxy.html', form=form)


@app.route('/list', methods=('GET', 'POST'))
def listp():
    form = ListForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        OpenSite.make_proxy_list(form.list_file.data)
        flash('Proxy details saved')
        return redirect('/script')
    return render_template('pages/list.html', form=form)


@app.route('/rotating', methods=('GET', 'POST'))
def rotating():
    form = RotatingForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        OpenSite.change_proxy(form.ip.data, form.port.data)
        flash('Proxy details saved')
        return redirect('/script')
    return render_template('pages/rotating.html', form=form)


@app.route('/script', methods=('GET', 'POST'))
def script():
    form = ScriptForm(request.form)
    if request.form.get("submit") == "Add item":
        if len(form.script_items.data) == form.script_items.max_entries:
            flash("Maximum number of items is %d" %form.script_items.max_entries)
            return render_template('pages/script.html', form=form)
        form.script_items.append_entry()
        return render_template('pages/script.html', form=form)
    elif request.form.get("submit") == 'Save' and form.validate_on_submit():
        key_to_press = form.key_press.data
        if len(key_to_press) == 0:
            key_to_press = OpenSite.random_key()
        OpenSite.set_parameters(int(form.pause_time_min.data), int(form.pause_time_max.data), int(form.min_scroll_count.data), int(form.max_scroll_count.data), str(key_to_press), int(form.min_click_count.data), int(form.max_click_count.data))
        OpenSite.update_script(form.script_items.data)
        OpenSite.update_xpath_time(int(form.min_xpath.data), int(form.max_xpath.data))
        flash("Settings saved")
    return render_template('pages/script.html', form=form)


@app.route('/run')
def run():
    try:
        OpenSite.run_threads()
    except:
        pass
    return redirect("/")


# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


log = logging.getLogger('werkzeug')
if not app.debug:
    app.logger.disabled = True
    log.disabled = True

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

if __name__ == '__main__':
    port = 5000 + random.randint(0, 999)
    url = "http://127.0.0.1:{0}".format(port)
    threading.Timer(2.0, lambda: webbrowser.open(url)).start()
    print("Bot server running on %s" % url)
    app.run(port=port, debug=False)

