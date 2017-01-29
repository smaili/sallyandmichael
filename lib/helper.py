#----------------------------------------
# imports
#----------------------------------------
import datetime
import smtplib
import email.utils
import re
from email.mime.text import MIMEText
from flask import render_template

#----------------------------------------
# helpers
#----------------------------------------
def weddingdt(month, day, year, hour = 0, minutes = 0, seconds = 0):
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
    body = render_template('email/rsvp.pyhtml', **targs)
    mail_subject = '%s - %s %s' % (title, targs['fname'], targs['lname'])

    server = smtplib.SMTP('localhost', 25)
    server.set_debuglevel(True)

    msg = MIMEText(body, 'plain')
    msg['To'] = email.utils.formataddr(('Michael Smaili', mail_to))
    msg['From'] = email.utils.formataddr(('No Reply', mail_from))
    msg['Subject'] = mail_subject

    print msg['To']
    print msg['From']
    print msg['Subject']

    server.sendmail(mail_from, [mail_to], msg.as_string())
  except Exception, e:
    print e
    error = 'Error trying to save your RSVP!'
  finally:
    if server:
      server.quit()

  return error


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


def saveRSVP(fname, lname, phone, attending):
  errors = {
    'fname': '',
    'lname': '',
    'phone': '',
    'attending': '',
  }
  success = True

  errors['fname'] = validateText(fname, 2, 50)
  errors['lname'] = validateText(lname, 2, 50)
  errors['phone'] = validateText(phone, 1, 50)
  errors['attending'] = validateSelect(attending, 0, 11)

  if errors['fname'] or errors['lname'] or errors['phone'] or errors['attending']:
    success = False

  return {'errors': errors, 'success': success}