#----------------------------------------
# imports
#----------------------------------------
import datetime
import smtplib
import email.utils
import json
import io
import cStringIO, mimetools, MimeWriter
import re
from email.mime.text import MIMEText
from flask import render_template

#----------------------------------------
# helpers
#----------------------------------------
def loadGuestList(path):
  j = None
  with io.open(path, 'r', encoding='utf-8') as f:
    j = json.load(f)
  return j


def todatetime(month, day, year, hour = 0, minutes = 0, seconds = 0):
  dt = datetime.datetime(year, month, day, hour, minutes, seconds)
  return dt


def minify(html):
  html = html.replace("\r\n", "\n")
  html = html.replace("\n", "")
  html = re.sub(r"<p>\s+", "<p>", html)
  html = re.sub(r"\s+</p>", "</p>", html)
  html = re.sub(r">\s{2,}<", "><", html)
  html = re.sub(r"(>)\s{2,}(.)", r"\1 \2", html)

  return html


def mail(mail_from, mail_to, title, targs):
  error = ''
  server = None
  try:
    # prep
    sender = email.utils.formataddr(('No Reply', mail_from))
    recipients = email.utils.formataddr(('Michael Smaili', mail_to))
    subject = '%s - %s %s' % (title, targs['fname'], targs['lname'])

    html = render_template('email/rsvp.pyhtml', format='html', **targs)
    text = render_template('email/rsvp.pyhtml', format='text', **targs)

    # init
    out = cStringIO.StringIO()
    htmlin = cStringIO.StringIO(html)
    txtin = cStringIO.StringIO(text)
    writer = MimeWriter.MimeWriter(out)

    # headers
    writer.addheader("From", sender)
    writer.addheader("To", recipients)
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


def rsvpAttendingText(headcount, MAX_GUESTS):
  if headcount == 0:
    return 'No'

  suffix = '+' if headcount == MAX_GUESTS else ''
  return 'YES, attending as party of %s%s' % (headcount, suffix)


def validateText(text, minlen, maxlen):
  error = ''
  if len(text) == 0:
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