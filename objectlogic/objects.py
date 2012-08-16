import os,sys
from xml.dom.minidom import parse
from operator import itemgetter

#Functions#

class libr:

  def __init__(self,fn,ulist,flogpath):
    self.fn = fn
    self.ulist = ulist
    self.flogpath = flogpath

  def checkme(self,log2chk):
    tester = open(log2chk, 'r')
    for line in tester:
      if '[' and ']' and '(' and ')' in line:
        self.logparsesu(self.fn)
        break
      elif '][' in line:
        self.logparsesmsmtp(self.fn)
        break
      elif '[' and ']' in line:
        self.logparsesmdeliv(self.fn)
        break
      elif '<Events>' in line:
        self.logparseapplog(self.fn)
        break
      else:
        self.logparse(self.fn)
        break

  def filen(self):
    i=0
    for user in self.ulist:
      for log in self.flogpath:
        for line in open(log, 'r'):
          i+=1
    return i

  def logparse(self,fileout):  #function for line-by-line logs
    lparse = open(fileout, 'w')
    i=0
    p=0
    for user in self.ulist:
      lparse.write('#' * (18 + len(user)) + '\n' + '# Logs for user ' + user + ' #\n' + '#' * (18 + len(user)) + '\n\n\n')
      for log in self.flogpath:
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
    for user in self.ulist:
      lparse.write('#' * (18 + len(user)) + '\n' + '# Logs for user ' + user + ' #\n' + '#' * (18 + len(user)) + '\n\n\n')
      loopy = []
      for log in self.flogpath:
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
    for user in self.ulist:
      lparse.write('#' * (18 + len(user)) + '\n' + '# Logs for user ' + user + ' #\n' + '#' * (18 + len(user)) + '\n\n\n')
      loopy = []
      for log in self.flogpath:
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
    if self.ulist is '0':
      for log in self.flogpath:
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
	  if builder.has_key(spamdict[key][0]):
	    builder[spamdict[key][0]].append(spamdict[key][1:])
	  else:
	    builder[spamdict[key][0]] = spamdict[key][1:]
        for key in builder:
	  builder[key] = len(builder[key])
	  i += builder[key]
        count = builder.items()
        count.sort(key = itemgetter(1), reverse = True)
        lparse.write('User / Emails Sent / %\n\n')
        for tup in count:
          lparse.write('%s / %s / ' % (tup[0], str(tup[1])) + str(1.0*(tup[1]*100)/i) + '%\n')
      lparse.close()

  def logparseapplog(self,fileout):
    lparse = open(fileout, 'w')
    for user in self.ulist:
      lparse.write('#' * (18 + len(user)) + '\n' + '# Logs for user ' + user + ' #\n' + '#' * (18 + len(user)) + '\n\n\n')
      for log in self.flogpath:
        xmltree = parse(log)
        for node1 in xmltree.getElementsByTagName('Event'):
	  for node2 in node1.childNodes:
	    if user in node2.toxml():
	      lparse.write('Event:\n\n')
	      lparse.write(node2.toxml())
	      lparse.write('\n\n')
    lparse.close()
