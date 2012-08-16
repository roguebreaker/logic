#!/usr/bin/env python

#~*~*~*~ Use the following command or quick shell execution:

#~*~*~*~ wget http://bashbits.net/tools/autologic.py && chmod +x ./autologic.py && ./autologic.py

#Imports#

import os,sys
from xml.dom.minidom import parse
from operator import itemgetter

#Functions#

class libr:

  def progress(self):
    sys.stdout.write('\rScan Progress: [' + '#'*p + '-'*(50-p) + ']' )
    sys.stdout.flush()
    p+=1

  def checkme(self,log2chk):
    tester = open(log2chk, 'r')
    for line in tester:
      if '[' and ']' and '(' and ')' in line:
        self.logparsesu(fn)
        break
      elif '][' in line:
        self.logparsesmsmtp(fn)
        break
      elif '[' and ']' in line:
        self.logparsesmdeliv(fn)
        break
      elif '<Events>' in line:
        self.logparseapplog(fn)
        break
      else:
        self.logparse(fn)
        break

  def filen(self):
    i=0
    for user in ulist:
      for log in flogpath:
        for line in open(log, 'r'):
          i+=1
    return i

  def logparse(self,fileout):  #function for line-by-line logs
    lparse = open(fileout, 'w')
    i=0
    p=0
    for user in ulist:
      lparse.write('#' * (18 + len(user)) + '\n' + '# Logs for user ' + user + ' #\n' + '#' * (18 + len(user)) + '\n\n\n')
      for log in flogpath:
        for line in open(log, 'r'):  #loop for finding all occurrences of unique user transaction IDs
          if i in enume:
            sys.stdout.write('\rScan Progress: [' + '#'*p + '-'*(50-p) + ']' )
            sys.stdout.flush()
            p+=1
          i+=1
          if user in line:
            lparse.write(line + "\n")
      lparse.write('\n')
    lparse.close()

  def logparsesu(self,fileout):  #function for serv-u logs
    lparse = open(fileout, 'w')
    i=0
    p=0
    for user in ulist:
      lparse.write('#' * (18 + len(user)) + '\n' + '# Logs for user ' + user + ' #\n' + '#' * (18 + len(user)) + '\n\n\n')
      loopy = []
      for log in flogpath:
        for line in open(log, 'r'): #nested loops: for each defined user - for each log - search line in log for...
          if ') User %s logged in\r'%user.upper() in line:
	    loopy.append(line[line.find('('):line.find(')')+1])  #transaction ID search and append to new list
        loopy = list(set(loopy))  #remove duplicates in list
        loopy.sort()
        for line in open(log, 'r'):  #loop for finding all occurrences of unique user transaction IDs
          if i in enume:
            sys.stdout.write('\rScan Progress: [' + '#'*p + '-'*(50-p) + ']' )
            sys.stdout.flush()
            p+=1
          i+=1
          for id in loopy:
            if id in line:
              lparse.write(line)  #write each line containing transaction ID sequentially
      lparse.write('\n')
    lparse.close()

  def logparsesmdeliv(self,fileout):  #function for serv-u logs
    lparse = open(fileout, 'w')
    i=0
    p=0
    enumm = []
    for user in ulist:
      lparse.write('#' * (18 + len(user)) + '\n' + '# Logs for user ' + user + ' #\n' + '#' * (18 + len(user)) + '\n\n\n')
      loopy = []
      for log in flogpath:
        for line in open(log, 'r'): #nested loops: for each defined user - for each log - search line in log$
          if user in line:
            loopy.append(line[line.find('['):line.find(']')+1])  #transaction ID search and append to new li$
        loopy = list(set(loopy))  #remove duplicates in list
        loopy.sort()
        for x in enume:
          enumm.append(x*len(loopy))
        for id in loopy:
          for line in open(log, 'r'):
            if i in enumm:
              sys.stdout.write('\rScan Progress: [' + '#'*p + '-'*(50-p) + ']' )
              sys.stdout.flush()
              p+=1
            i+=1
            if id in line:
              lparse.write(line)  #write each line containing transaction ID sequentially
          lparse.write('\n')
      lparse.write('\n')
    lparse.close()

  def logparsesmsmtp(self,fileout):
    if ulist is '0':
      for log in flogpath:
        i = 0
        id = []
        rcptall = []
        spamdict = {}
        newfn = log + "." + fileout
        lparse = open(newfn, 'w')
        for line in open(log, 'r'):
          if 'MAIL FROM:' in line:
	    rcptall.append(line)
	  if 'RCPT TO:' in line:
	    rcptall.append(line)
        for line in rcptall:
	  id.append(line[line.find('['):line.find('] ')+1])
        id = set(id)
        for sess in id:
	  for line in rcptall:
	    if sess in line:
	      if 'MAIL FROM:' in line:
	        emailer = line[line.find('<'):line.find('>')+1]
	        if '<>' in emailer:
	          emailer = line[line.find('['):line.find(']')+1]
	        elif emailer is '':
	          emailer = line[line.find('['):line.find(']')+1]
	      spamdict[sess] = [emailer]
	      print spamdict[sess]
              if 'RCPT TO:' in line:
	        emailer = line[line.find('<'):line.find('>')+1]
	      spamdict[sess].append(emailer)
	      print spamdict[sess]
        builder = {}
        for key in spamdict:
#	lparse.write(str(spamdict[key][0]) + ": " + str(spamdict[key][1:]) + "\n")
	  if builder.has_key(spamdict[key][0]):
	    builder[spamdict[key][0]].append(spamdict[key][1:])
	  else:
	    builder[spamdict[key][0]] = spamdict[key][1:]
        for key in builder:
	  builder[key] = len(builder[key])
	  i += builder[key]
      
#	if 'MAIL FROM:' in line:
#	  emailer = line[line.find('<'):line.find('>')+1]
#	  if '<>' in emailer:
#	    emailer = line[line.find('['):line.find(']')+1]
#	  elif emailer is '':
#	    emailer = line[line.find('['):line.find(']')+1]
#	    rcpt.append(line[line.find('<'):line.find('>')+1])
#	spamdict[emailer] = rcpt
#      for line in rcptall:
#        lparse.write(line)
	
	

#      for user in spammers:
#	i=i+1
#	spamdict[user] = spamdict.get(user,0)+1
        count = builder.items()
        count.sort(key = itemgetter(1), reverse = True)
        lparse.write('User / Emails Sent / %\n\n')
        for tup in count:
          lparse.write('%s / %s / ' % (tup[0], str(tup[1])) + str(1.0*(tup[1]*100)/i) + '%\n')
      lparse.close()

  def logparseapplog(self,fileout):
    lparse = open(fileout, 'w')
    for user in ulist:
      lparse.write('#' * (18 + len(user)) + '\n' + '# Logs for user ' + user + ' #\n' + '#' * (18 + len(user)) + '\n\n\n')
      for log in flogpath:
        xmltree = parse(log)
        for node1 in xmltree.getElementsByTagName('Event'):
	  for node2 in node1.childNodes:
	    if user in node2.toxml():
	      lparse.write('Event:\n\n')
	      lparse.write(node2.toxml())
	      lparse.write('\n\n')
    lparse.close()

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

tested = open(flogpath[0], 'r')
for line in  tested:
  if '][' in line:
    fspam = raw_input('These appear to be SMTP logs, find the spammers? [y/n]: ')
    if fspam is 'y':
      fn = 'spammers.txt'
      ulist = '0'
      newins = libr()
      newins.checkme(flogpath[0])
#      cont = raw_input('Continue with parsing? [y/n]: ')
#      if cont is 'n':
      print 'Bye!\n'
      sys.exit()
#      else:
#        break
  else:
    break

users = <http request> # Please input the file listing your desired search strings, a search string, or any mix of the two separated by commas:
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

fn = 'logoutput' # Please specify the file you would like to output the results to:

newins = libr()

linecount = newins.filen()  #codeblock for getting counter numbers for progress bar
increment = linecount / 50
enume = []
j = 0
while j <= 50:
  enume.append(increment * j)
  j+=1
enume.sort() #end codeblock

sys.stdout.write('\nScan Progress: [' + '-'*50 + ']')  #begin progress bar
sys.stdout.flush()

newins.checkme(flogpath[0])

sys.stdout.write('\rScan Progress: [' + '#'*50 + ']' )
sys.stdout.write('\r\r\n')
sys.stdout.write('\r\r\nLogs have been parsed to %s\n' %  fn)
sys.stdout.flush()
print ''
