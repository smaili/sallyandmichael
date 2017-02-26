#----------------------------------------
# imports
#----------------------------------------
import datetime
import os
import time
from flask import Flask, redirect, render_template, request
from lib.helper import mail, minify, weddingdt, saveRSVP, rsvpAttendingText

#----------------------------------------
# initialization
#----------------------------------------

app = Flask(__name__)

#----------------------------------------
# constants
#----------------------------------------
# May 5, 2016
WEDDING_PROPOSE_DT = weddingdt(5, 1, 2016)
# June 3, 2017
WEDDING_DAY_DT = weddingdt(6, 3, 2017)

MAIL_FROM = 'no-reply@sallyandmichael.com'
MAIL_TO = 'me@smaili.org'
MAIL_SUBJECT = 'Wedding RSVP'

MAX_GUESTS = 5

#----------------------------------------
# routes
#----------------------------------------

@app.route('/')
def home():
  weddingtimes = {
    'start': int(time.mktime(WEDDING_PROPOSE_DT.timetuple())),
    'end': int(time.mktime(WEDDING_DAY_DT.timetuple())),
    'now': int(time.mktime(datetime.datetime.today().timetuple())),
  }

  return minify(render_template('layouts/default.pyhtml', page='home', weddingtimes=weddingtimes))

@app.route('/couple')
def couple():
  return minify(render_template('layouts/default.pyhtml', page='couple'))

@app.route('/story')
def story():
  return minify(render_template('layouts/default.pyhtml', page='story'))

@app.route('/wedding')
def wedding():
  return minify(render_template('layouts/default.pyhtml', page='wedding'))

@app.route('/gifts')
def gifts():
  return minify(render_template('layouts/default.pyhtml', page='gifts'))

@app.route('/rsvp', methods=['GET', 'POST'])
def rsvp():
  targs = {
    'fname': '',
    'lname': '',
    'phone': '',
    'attending': '',
    'errors': {},
    'success': False,
    'MAX_GUESTS': MAX_GUESTS,
    'rsvpAttendingText': rsvpAttendingText,
  }

  if request.method == 'POST':
    targs['fname'] = request.form['fname']
    targs['lname'] = request.form['lname']
    targs['phone'] = request.form['phone']
    targs['attending'] = request.form['attending']
    targs.update(saveRSVP(targs))

    if targs['success']:
      targs['mailfailed'] = mail(MAIL_FROM, MAIL_TO, MAIL_SUBJECT, targs)

  return minify(render_template('layouts/default.pyhtml', page='rsvp', **targs))

@app.errorhandler(404)
def error_404(e):
  return error(404)

@app.errorhandler(Exception)
def error_500(e=None):
  return error(500)

@app.route('/nginxerror.html')
def nginx_error():
  code = int(request.args.get('c'))
  return error(code)

def error(code):
  return redirect('/')

#----------------------------------------
# launch
#----------------------------------------

if __name__ == '__main__':
  app.config.update(DEBUG=True)
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)
