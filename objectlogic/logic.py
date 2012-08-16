#!/usr/bin/env python

#Imports#

import os,sys
from objects import libr

#Main Logic#

while True:

  logdir = raw_input('\nPlease input logs to parse (this can be a file, directory, or any mix of the two separated by commas): ')

  loglist = []
  ilogdir = []

  if ',' in logdir:
    jlogdir = logdir.split(',')
    for x in jlogdir:
      ilogdir.append(x.strip())
    for x in ilogdir:
      if os.path.isfile(x) is True:
        loglist.append(os.path.abspath(x))
      elif os.path.isdir(x) is True:
        j = os.listdir(x)
        i = 0
        for a in j:
          loglist.append(os.path.join(os.path.abspath(x), a))
  else:
    ilogdir = logdir.strip()
    if os.path.isfile(ilogdir) is True:
      loglist.append(os.path.abspath(ilogdir))
    elif os.path.isdir(ilogdir) is True:
      j = os.listdir(ilogdir)
      for a in j:
        loglist.append(os.path.join(os.path.abspath(ilogdir), a))

  flogpath = []

  for logfile in loglist:	#loop in order to optain full path for all files listed in defined directory
    flogpath.append(os.path.join(os.path.abspath(logdir), logfile))
  flogpath.sort()
  flogpath = tuple(flogpath)

  try:
    test = open(flogpath[0], 'r')
    break

  except:
    print 'That was an incorrect path. Please try again.'

users = raw_input('\nPlease input the file listing your desired search strings, a search string, or any mix of the two separated by commas: ')
ulist = []

if ',' in users:
  tranulist = users.split(',')
  t2list = []
  for x in tranulist:
    t2list.append(x.strip())
  for x in t2list:
    if os.path.isfile(x) is True:
      fi = open(x).readlines()
      for i in fi:
        ulist.append(i.strip())
    else:
      ulist.append(x.strip())
else:
  if os.path.isfile(users) is True:
    fi = open(users).readlines()
    for i in fi:
      ulist.append(i.strip())
  else:
    ulist.append(users.strip())

fn = raw_input('\nPlease specify the file you would like to output the results to: ')

while True:
  if os.path.isfile(fn) is True:
    q = raw_input('*!* This is already a file, would you like to overwrite it? (y/n): ')
    if q is 'y':
      break
    elif q is 'n':
      fn = raw_input('Please specify the file you would like to output the results to: ')
  else:
    break

newins = libr(fn,ulist,flogpath)


sys.stdout.write('\nScan Progress: [' + '-'*50 + ']')  #begin progress bar
sys.stdout.flush()

newins.checkme(flogpath[0])

sys.stdout.write('\rScan Progress: [' + '#'*50 + ']' )
sys.stdout.write('\r\r\n')
sys.stdout.write('\r\r\nLogs have been parsed to %s\n' %  fn)
sys.stdout.flush()
print ''
