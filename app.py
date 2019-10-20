#----------------------------------------
# imports
#----------------------------------------
import datetime
import json
import functools
import os
import time

from flask import Flask, redirect, render_template, request, Response, url_for

from lib.helper import loadGuestList, mailRSVP, minify, todatetime, tolocaldt, saveRSVP, rsvpAttendingText, getGuestStats, mailInvite, saveInvite, storeInvite

#----------------------------------------
# initialization
#----------------------------------------

app = Flask(__name__)

#----------------------------------------
# constants
#----------------------------------------
# guest list path
TZ = 'US/Pacific'
HERE = os.path.dirname(os.path.realpath(__file__))
LIST_PATH = os.path.join(HERE, 'config', 'list.json')
GUESTS_CONFIG = loadGuestList(LIST_PATH)

# May 5, 2016
WEDDING_PROPOSE_DT = tolocaldt(todatetime(5, 1, 2016, tz=TZ))
# June 3, 2017
WEDDING_DAY_DT = tolocaldt(todatetime(6, 3, 2017, hour=10, minutes=0, seconds=0, tz=TZ))

# Mail
MAIL_FROM = 'no-reply@sallyandmichael.com'
MAIL_TO = 'me@smaili.org'

WEDDING_RSVP_MAIL_SUBJECT = 'Wedding RSVP'
BABY_SHOWER_RSVP_MAIL_SUBJECT = 'Baby Shower RSVP'

WEDDING_INVITE_MAIL_SUBJECT = 'Subject'
BABY_SHOWER_INVITE_MAIL_SUBJECT = 'Sally Smaili\'s Baby Shower (Women Only)'

# RSVP
MAX_GUESTS = 5
# May 20, 2017
RSVP_BY_DT = tolocaldt(todatetime(5, 15, 2017, tz=TZ))
CONTACT_PHONE = '(408) 605-4636'

# Baby Shower
BABY_SHOWER_MAX_GUESTS = 5
# November 5, 2019
BABY_SHOWER_RSVP_BY_DT = tolocaldt(todatetime(11, 1, 2019, tz=TZ))
BABY_SHOWER_DAY_DT = tolocaldt(todatetime(11, 16, 2019, hour=10, minutes=0, seconds=0, tz=TZ))
BABY_SHOWER_CONTACT_PHONE = '(408) 605-4636'

# guest list path
BABY_SHOWER_LIST_PATH = os.path.join(HERE, 'config', 'list-babyshower.json')
BABY_SHOWER_GUESTS_CONFIG = loadGuestList(BABY_SHOWER_LIST_PATH)

#----------------------------------------
# helpers
#----------------------------------------
def check_auth(username, password, guest_config):
  guests_login = guest_config['login']
  return username == guests_login['username'] and password == guests_login['password']

def authenticate():
  return Response(
  'Please login', 401,
  {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(guest_config):
  def requires_auth_inner(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password, guest_config):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
  return requires_auth_inner


#----------------------------------------
# routes
#----------------------------------------

@app.route('/')
def home():
  weddingtimes = {
    'start': int(time.mktime(WEDDING_PROPOSE_DT.timetuple())),
    'end': int(time.mktime(WEDDING_DAY_DT.timetuple())),
    'now': int(time.mktime(tolocaldt(tz=TZ).timetuple())),
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
    'CONTACT_PHONE': CONTACT_PHONE,
    'rsvpAttendingText': rsvpAttendingText,
    'rsvpByDate': '{d:%A}, {d:%B} {d.day}'.format(d=RSVP_BY_DT),
    'rsvpEnabled': tolocaldt(tz=TZ) <= RSVP_BY_DT,
    'rsvpEventDate': '{d:%A}, {d:%b} {d.day}'.format(d=WEDDING_DAY_DT),
  }

  if targs['rsvpEnabled'] and request.method == 'POST':
    targs['fname'] = request.form['fname']
    targs['lname'] = request.form['lname']
    targs['phone'] = request.form['phone']
    targs['attending'] = request.form['attending']
    targs.update(saveRSVP(targs))

    if targs['success']:
      targs['mailfailed'] = mailRSVP(MAIL_FROM, MAIL_TO, WEDDING_RSVP_MAIL_SUBJECT, targs)

  targs['page'] = 'rsvp'
  targs['rsvpFormHref'] = url_for('rsvp')

  return minify(render_template('layouts/default.pyhtml', **targs))


@app.route('/guests')
@requires_auth(GUESTS_CONFIG)
def guests():
  targs = {}

  targs['guests'] = loadGuestList(LIST_PATH)
  targs['stats'] = getGuestStats(targs['guests'])
  targs['guestTitle'] = 'Sally & Michael'

  return minify(render_template('layouts/guests.pyhtml', **targs))


@app.route('/babyshower')
def babyshower():
  return redirect(url_for('babyshower_rsvp'))


@app.route('/babyshower/rsvp', methods=['GET', 'POST'])
def babyshower_rsvp():
  targs = {
    'fname': '',
    'lname': '',
    'phone': '',
    'attending': '',
    'errors': {},
    'success': False,
    'MAX_GUESTS': BABY_SHOWER_MAX_GUESTS,
    'CONTACT_PHONE': BABY_SHOWER_CONTACT_PHONE,
    'rsvpAttendingText': rsvpAttendingText,
    'rsvpByDate': '{d:%A}, {d:%b} {d.day}'.format(d=BABY_SHOWER_RSVP_BY_DT),
    'rsvpEnabled': tolocaldt(tz=TZ) <= BABY_SHOWER_RSVP_BY_DT,
    'rsvpEventDate': '{d:%A}, {d:%b} {d.day}'.format(d=BABY_SHOWER_DAY_DT),
  }

  if targs['rsvpEnabled'] and request.method == 'POST':
    targs['fname'] = request.form['fname']
    targs['lname'] = request.form['lname']
    targs['phone'] = request.form['phone']
    targs['attending'] = request.form['attending']
    targs.update(saveRSVP(targs))

    if targs['success']:
      targs['mailfailed'] = mailRSVP(MAIL_FROM, MAIL_TO, BABY_SHOWER_RSVP_MAIL_SUBJECT, targs)

  targs['page'] = 'babyshower'
  targs['section'] = 'rsvp'
  targs['rsvpFormHref'] = url_for('babyshower_rsvp')

  return minify(render_template('layouts/default.pyhtml', **targs))


@app.route('/babyshower/whenwhere')
def babyshower_whenwhere():
  targs = {
    'eventDate': '{d:%A}, {d:%b} {d.day}'.format(d=BABY_SHOWER_DAY_DT),
  }

  targs['page'] = 'babyshower'
  targs['section'] = 'whenwhere'

  return minify(render_template('layouts/default.pyhtml', **targs))


@app.route('/babyshower/registry')
def babyshower_registry():
  targs = {}

  targs['page'] = 'babyshower'
  targs['section'] = 'registry'

  return minify(render_template('layouts/default.pyhtml', **targs))


@app.route('/babyshower/guests', methods=['GET', 'POST'])
@requires_auth(BABY_SHOWER_GUESTS_CONFIG)
def babyshower_guests():
  targs = {}

  inviteargs = {
    'date': '{d:%A}, {d:%b} {d.day}'.format(d=BABY_SHOWER_DAY_DT),
    'website': 'http://www.sallyandmichael.com/babyshower',
  }
  targs['invitations'] = {
    'name': '',
    'email': '',
    'cc': '',
    'bcc': '',
    'subject': BABY_SHOWER_INVITE_MAIL_SUBJECT,
    'message': render_template('email/babyshower-invite.pyhtml', **inviteargs),
  }
  targs['invitations']['inviteFormHref'] = url_for('babyshower_guests')

  if request.method == 'POST':
    targs['invitations']['name'] = request.form['name']
    targs['invitations']['email'] = request.form['email']
    targs['invitations']['cc'] = request.form['cc']
    targs['invitations']['bcc'] = request.form['bcc']
    targs['invitations']['subject'] = request.form['subject']
    targs['invitations']['message'] = request.form['message']

    targs.update(saveInvite(targs['invitations']))

    if targs['success']:
      targs['mailfailed'] = mailInvite(MAIL_FROM, targs['invitations']['email'], targs['invitations'])

    targs['status'] = 'success' if targs['success'] and not targs['mailfailed'] else 'error'

    if targs['status'] == 'success':
      data = loadGuestList(BABY_SHOWER_LIST_PATH)
      data['invitations'].append({
        'name': targs['invitations']['name'],
        'email': targs['invitations']['email'],
      })
      success = storeInvite(BABY_SHOWER_LIST_PATH, data)
      if not success:
        targs['status'] = 'error'
        targs['savefailed'] = 'Invitation sent but unable to save changes to %s' % BABY_SHOWER_LIST_PATH
      else:
        targs['success'] = 'Invitation has been sent and changes saved.'


    return json.dumps(targs)

  targs['guests'] = loadGuestList(BABY_SHOWER_LIST_PATH)
  targs['stats'] = getGuestStats(targs['guests'])
  targs['guestTitle'] = 'Baby Shower'

  return minify(render_template('layouts/guests.pyhtml', **targs))


@app.errorhandler(404)
def error_404(e):
  return error(404)


@app.errorhandler(Exception)
def error_500(e=None):
  print e
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
