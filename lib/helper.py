#----------------------------------------
# imports
#----------------------------------------
import datetime
import smtplib
import email.utils
import json
import io
import pytz
import cStringIO, mimetools, MimeWriter
import re
import StringIO
from email.mime.text import MIMEText
from flask import render_template

# constants
#------------------------------------------------------------------------
JSON_ENCODING = 'utf-8'
JSON_ARGS = {
  'ensure_ascii': False,
  'indent': 2,
}

#----------------------------------------
# helpers
#----------------------------------------
def loadGuestList(path):
  j = None
  with io.open(path, 'r', encoding='utf-8') as f:
    j = json.load(f)
  return j


def saveJSON(file, data):
  with io.open(file, 'w', encoding=JSON_ENCODING) as f:
    # there's a strange bug where commas have a space, so this is to help fix that
    tostr = json.dumps(data, **JSON_ARGS)

    # since some content may have the newline, we need to do line by line to be safe
    lines = StringIO.StringIO(tostr).readlines()
    jsonbug = ', \n'
    jsonfix = ',\n'
    for i, line in enumerate(lines):
      # we make sure we only do this if it ends with it since there's always a chance
      # actual content may contain these characters
      if line.endswith(jsonbug):
        #  we replace the last occurrence
        lines[i] = line[:-len(jsonbug)] + jsonfix

    tostr = ''.join(lines)
    f.write(tostr)


def todatetime(month, day, year, hour = 0, minutes = 0, seconds = 0, tz=None):
  dt = datetime.datetime(year, month, day, hour, minutes, seconds, tzinfo=pytz.timezone(tz))
  return dt


def tolocaldt(dt=None, tz=None):
  if dt is None:
    dt = datetime.datetime.now(pytz.timezone(tz))
  return dt


def minify(html):
  html = html.replace("\r\n", "\n")
  html = html.replace("\n", "")
  html = re.sub(r"<p>\s+", "<p>", html)
  html = re.sub(r"\s+</p>", "</p>", html)
  html = re.sub(r">\s{2,}<", "><", html)
  html = re.sub(r"(>)\s{2,}(.)", r"\1 \2", html)

  return html


def mail(mail_from, mail_to, subject, targs):
  error = ''
  server = None
  try:
    # prep
    sender = email.utils.formataddr(('No Reply', mail_from))
    recipients = email.utils.formataddr(('Michael Smaili', mail_to))

    html = targs['html']
    text = targs['text']

    # init
    out = cStringIO.StringIO()
    htmlin = cStringIO.StringIO(html)
    txtin = cStringIO.StringIO(text)
    writer = MimeWriter.MimeWriter(out)

    # headers
    writer.addheader("From", sender)
    writer.addheader("To", recipients)

    if 'cc' in targs and len(targs['cc']) > 0:
      if type(targs['cc']) == str:
        targs['cc'] = list(targs['cc'])
      for cc in targs['cc']:
        writer.addheader('Cc', cc)

    if 'bcc' in targs and len(targs['bcc']) > 0:
      if type(targs['bcc']) == str:
        targs['bcc'] = list(targs['bcc'])
      for bcc in targs['bcc']:
        writer.addheader('Bcc', bcc)

    writer.addheader("Subject", subject)
    writer.addheader("X-Mailer", "SmailiMail [version 1.0]")
    writer.addheader("MIME-Version", "1.0")
    writer.startmultipartbody("alternative")
    writer.flushheaders()

    # text
    subpart = writer.nextpart()
    subpart.addheader("Content-Transfer-Encoding", "quoted-printable")
    pout = subpart.startbody("text/plain", [("charset", 'UTF-8')])
    mimetools.encode(txtin, pout, 'quoted-printable')
    txtin.close()

    # html
    subpart = writer.nextpart()
    subpart.addheader("Content-Transfer-Encoding", "quoted-printable")
    pout = subpart.startbody("text/html", [("charset", 'UTF-8')])
    mimetools.encode(htmlin, pout, 'quoted-printable')
    htmlin.close()

    # to string
    writer.lastpart()
    msg = out.getvalue()
    out.close()

    # send out
    server = smtplib.SMTP('localhost', 25, timeout=1)
    server.sendmail(sender, recipients, msg)
  except Exception, e:
    print e
    error = 'Error trying to save your RSVP.'
  finally:
    if server:
      server.quit()

  return error


def mailRSVP(mail_from, mail_to, title, targs):
  subject = '%s - %s %s' % (title, targs['fname'], targs['lname'])

  targs['html'] = render_template('email/rsvp.pyhtml', format='html', **targs)
  targs['text'] = render_template('email/rsvp.pyhtml', format='text', **targs)

  return mail(mail_from, mail_to, subject, targs)


def rsvpAttendingText(headcount, MAX_GUESTS):
  if headcount == 0:
    return 'No'

  suffix = '+' if headcount == MAX_GUESTS else ''
  return 'YES, attending as party of %s%s' % (headcount, suffix)


def validateText(text, minlen, maxlen):
  error = ''
  if len(text) == 0 and minlen > 0:
    error = 'This field is required.'
  elif len(text) < minlen:
    error = 'Please enter at least %s characters.' % minlen

  return error


def validateSelect(value, minval, maxval):
  error = ''
  if len(value) == 0:
    error = 'This field is required.'
  elif not value.isdigit():
    error = 'This field must be a number.'
  elif int(value) < minval or int(value) > maxval:
    error = 'This field must be between %s and %s.' % (minval, maxval)

  return error


def saveRSVP(targs):
  errors = {
    'fname': '',
    'lname': '',
    'phone': '',
    'attending': '',
  }
  success = True

  errors['fname'] = validateText(targs['fname'], 2, 50)
  errors['lname'] = validateText(targs['lname'], 2, 50)
  errors['phone'] = validateText(targs['phone'], 1, 50)
  errors['attending'] = validateSelect(targs['attending'], 0, targs['MAX_GUESTS'])

  if errors['fname'] or errors['lname'] or errors['phone'] or errors['attending']:
    success = False

  return {'errors': errors, 'success': success}


def getGuestStats(guests_config):
  stats = {}
  stats['parties'] = sum([len(guests_config['invites'][key]) for key in guests_config['invites']])
  stats['gross'] = sum([sum([int(party['attending'] if '+' not in party['attending'] else party['attending'][:-1]) for party in guests_config['invites'][key]]) for key in guests_config['invites']])
  stats['net'] = sum([sum([int(party['attending'] if '+' not in party['attending'] else party['attending'][:-1]) - int(party.get('exclude', 0)) for party in guests_config['invites'][key]]) for key in guests_config['invites']])
  stats['rejections'] = sum([sum([1 if party['attending'] == '0' else 0 for party in guests_config['invites'][key]]) for key in guests_config['invites']])
  stats['capacity'] = guests_config['capacity']
  stats['available'] = stats['capacity'] - stats['net']
  stats['headcountbreakdown'] = {}
  for category in guests_config['invites']:
    stats['headcountbreakdown'][category] = sum([int(party['attending'] if '+' not in party['attending'] else party['attending'][:-1]) for party in guests_config['invites'][category]])

  def parseGift(gift, type):
    value = 0
    if gift.startswith('$'):
      split = gift.split(' ')
      splitValue = int(split[0][1:])
      splitType = split[len(split) - 1]
      addValue = False
      if type == 'all':
        addValue = True
      elif splitType == 'Cash' and (type == 'cash' or type == 'money'):
        addValue = True
      elif splitType == 'Check' and (type == 'check' or type == 'money'):
        addValue = True
      elif splitType == 'Card' and type == 'card':
        addValue = True

      if addValue:
        value = value + splitValue
    else:
      if type == 'item':
        value = len(gift.split(','))

    return value

  stats['giftcash'] = sum([parseGift(guest['gifts'], 'cash') for guest in guests_config['gifts']])
  stats['giftcheck'] = sum([parseGift(guest['gifts'], 'check') for guest in guests_config['gifts']])
  stats['giftcard'] = sum([parseGift(guest['gifts'], 'card') for guest in guests_config['gifts']])
  stats['giftallmoney'] = sum([parseGift(guest['gifts'], 'money') for guest in guests_config['gifts']])
  stats['giftall'] = sum([parseGift(guest['gifts'], 'all') for guest in guests_config['gifts']])
  stats['giftitem'] = sum([parseGift(guest['gifts'], 'item') for guest in guests_config['gifts']])

  return stats


def saveInvite(targs):
  errors = {
    'name': '',
    'email': '',
    'cc': '',
    'bcc': '',
    'subject': '',
    'message': '',
  }
  success = True

  errors['name'] = validateText(targs['name'], 2, 50)
  errors['email'] = validateText(targs['email'], 5, 50)
  errors['cc'] = validateText(targs['cc'], 0, 50)
  errors['bcc'] = validateText(targs['bcc'], 0, 50)
  errors['subject'] = validateText(targs['subject'], 1, 100)
  errors['message'] = validateText(targs['message'], 1, 1000)

  if errors['name'] or errors['email'] or errors['cc'] or errors['bcc'] or errors['subject'] or errors['message']:
    success = False

  return {'errors': errors, 'success': success}


def mailInvite(mail_from, mail_to, targs):
  targs['html'] = targs['text'] = targs['message']

  if len(targs['cc']) > 0:
    targs['cc'] = targs['cc'].replace(' ').split(',')

  if len(targs['bcc']) > 0:
    targs['bcc'] = targs['bcc'].replace(' ').split(',')

  # need to wrap the error message since the one from mail is rsvp related
  error = mail(mail_from, mail_to, targs['subject'], targs)
  if error:
    error = 'Error trying to send your invite.'

  return error


def storeInvite(file, data):
  success = True

  try:
    saveJSON(file, data)
  except Exception, e:
    print e
    success = False

  return success