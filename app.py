#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, flash, redirect, url_for
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os
import OpenSite
from threading import Thread

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config["SECRET_KEY"] = "12345678910"
app.config.from_object('config')
#db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
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
            OpenSite.update_min(form.time_min.data)
            OpenSite.update_max(form.time_max.data)
            flash("Details saved")
        else:
            flash("There was a problem with the details submitted")
    return render_template('pages/home.html', form=form)


@app.route('/proxy')
def proxy():
    return render_template('pages/proxy.html')


@app.route('/script')
def script():
    return render_template('pages/script.html')


@app.route('/run')
def run():
    try:
        bg = Thread(OpenSite.run_threads())

    except:
        pass
    return redirect("/")


# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
