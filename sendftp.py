import os, ftplib

DEBUG=True
REMOTE_HOST='somehost'
FTP_USER='someuser'
FTP_PASS=''
MAIL_HOST='localhost'
MAIL_FROM='robot@domain.com'
MAIL_TO=['admin@mydom.com']
FILE_PATH='/home/androme/incoming'
ARCHIVE_FILE_TO='/home/androme/archive'
FILE1_TO_SEND='*.csv'
FILE1_REMOTE_FOLDER='csvfile'
FILE2_TO_SEND='*.txt'
FILE2_REMOTE_FOLDER='textfile'
FILE3_TO_SEND='*.pdf'
FILE3_REMOTE_FOLDER='pdffile'

MAIL_ALERT_TO=['alert@sys.com']
ALERT_SUBJECT='[Alert]SFTP Transfer Failed !!!'

def send_files(hostname=REMOTE_HOST,port=22):
    import paramiko 
    import sys
    import traceback
    log_msg=''
    # get host key, if we know one
    hostkeytype = None
    hostkey = None
    try:
        host_keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
    except IOError:
        try:
            # try ~/ssh/ too, because windows can't have a folder named ~/.ssh/
            host_keys = paramiko.util.load_host_keys(os.path.expanduser('~/ssh/known_hosts'))
        except IOError:
            print '*** Unable to open host keys file'
            host_keys = {}

    if host_keys.has_key(REMOTE_HOST):
        hostkeytype = host_keys[REMOTE_HOST].keys()[0]
        hostkey = host_keys[REMOTE_HOST][hostkeytype]
        print 'Using host key of type %s' % hostkeytype

    # now, connect and use paramiko Transport to negotiate SSH2 across the connection
    try:
        ##t = paramiko.Transport((REMOTE_HOST, port))
        #t.connect(username=username, password=password, hostkey=hostkey)
        #t.connect(username=FTP_USER, password=FTP_PASS,hostkey=hostkey)
        ##t.connect(username=FTP_USER,hostkey=hostkey)
        ##sftp = paramiko.SFTPClient.from_transport(t)
        ssh=paramiko.SSHClient()
        ssh.load_host_keys(os.path.expanduser(os.path.join("~",".ssh","known_hosts")))
        ssh.connect(hostname,username=FTP_USER,look_for_keys=True)
        sftp=ssh.open_sftp()

        files=get_file(FILE_PATH+'/'+FILE1_TO_SEND)
        if len(files)==0:
            if DEBUG==True:
                print 'No File detected. Exit Cleanly'
            #sys.exit(1)
        else:
		    if DEBUG==True:
				print 'Files detected. Prepare uploading to SFTP Server'
        import string
        attach=[]
        for f in files:
            s1=string.replace(f,'\\','/')
            
            s=string.split(s1,'/')
            if DEBUG==True:
                print 'The File name is : %s' % s[5]

            log_msg+=' The File Name is : %s' %s[5]
            sftp.put(f, FILE1_REMOTE_FOLDER+'/'+s[5])
            
            if DEBUG==True:
                print 'Upload '+ f +' to server '
            log_msg+= 'Upload '+ f +' to server '
            attach.append(s1)
        '''
        process second files type
        '''
        files=get_file(FILE_PATH+'/'+FILE2_TO_SEND)
        if len(files)==0:
            if DEBUG==True:
                print 'No File detected. Exit Cleanly'
            #sys.exit(1)
        else:
		    if DEBUG==True:
				print 'Files detected. Prepare uploading to SFTP Server'
        
        for f in files:
            s1=string.replace(f,'\\','/')
            
            s=string.split(s1,'/')
            if DEBUG==True:
                print 'The File name is : %s' % s[5]

            log_msg+=' The File Name is : %s' %s[5]
            sftp.put(f, FILE2_REMOTE_FOLDER+'/'+s[5])
            
            if DEBUG==True:
                print 'Upload '+ f +' to server '
            log_msg+= 'Upload '+ f +' to server '
            attach.append(s1)
			
        '''
	files 3 types
        '''
        files=get_file(FILE_PATH+'/'+FILE3_TO_SEND)
        if len(files)==0:
            if DEBUG==True:
                print 'No File detected. Exit Cleanly'
            #sys.exit(1)
        else:
		    if DEBUG==True:
				print 'Files detected. Prepare uploading to SFTP Server'
        
        
        for f in files:
            s1=string.replace(f,'\\','/')
            
            s=string.split(s1,'/')
            if DEBUG==True:
                print 'The File name is : %s' % s[5]

            log_msg+=' The File Name is : %s' %s[5]
            sftp.put(f, FILE3_REMOTE_FOLDER+'/'+s[5])
            
            if DEBUG==True:
                print 'Upload '+ f +' to server '
            log_msg+= 'Upload '+ f +' to server '
            attach.append(s1)


        if DEBUG==True:
           print 'Prepare send the file to email.The file to attach %s' % attach
        log_msg+='Prepare send the file to email.The file to attach %s' % attach

        subject='The Transfered Files'		
        text='The files '   
        if len(attach)!=0:
           send_mail(MAIL_FROM, MAIL_TO, subject, text, attach, MAIL_HOST)
        move_file(FILE_PATH+'/'+FILE1_TO_SEND)
        move_file(FILE_PATH+'/'+FILE2_TO_SEND)
        move_file(FILE_PATH+'/'+FILE3_TO_SEND)
		# BETTER: use the get() and put() methods
		
		#sftp.put('demo_sftp.py', 'tes/demo_sftp.py')
		
		#sftp.get('demo_sftp_folder/README', 'README_demo_sftp')

        sftp.close()

    except Exception, e:
        print '*** Caught exception: %s: %s' % (e.__class__, e)
        log_msg+='\nSomething Wrong \n\n'
        log_msg+='Caugh Exception: %s \n\n' % ( e)
        log_msg+='Alert !!! Error in uploading to SFPT server : %s ' % REMOTE_HOST
        
        send_mail(MAIL_FROM,MAIL_ALERT_TO,ALERT_SUBJECT,log_msg,[],MAIL_HOST)
    	
        try:
            sftp.close()
        except:
            pass
        sys.exit(1)

def get_file(dir='.'):
    '''
    Get the content of directory 
    return list of file name
    '''
    import glob
    if dir=='.':
        f=glob.glob(dir)
    else:
        f=glob.glob(dir)
	
    if DEBUG==True:
       print 'Getting the File List...'
       print 'The file list : %s' % f
    return f

def move_file(dir='.'):
   '''
   Move file to the ARCHIVE_FILE_TO variable from the FILE_PATH variable contents listing
   '''
   import shutil
   import string
   import os
   
   f=shutil
   list=get_file(dir)
   for dat in list:
      s1=string.replace(dat,'\\','/')
     
      res=f.copy(s1,ARCHIVE_FILE_TO)
      if res == None:
        r=os.remove(s1)
      if DEBUG==True:
        print 'Removing Files...'
        print 'File %s removed' % s1	  
   return
   
   
import smtplib
import os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

def send_mail(send_from, send_to, subject, text, files=[], server="localhost"):
  '''
  Send email with attachment from file system
  '''
  assert type(send_to)==list
  assert type(files)==list

  msg = MIMEMultipart()
  msg['From'] = send_from
  msg['To'] = COMMASPACE.join(send_to)
  msg['Date'] = formatdate(localtime=True)
  msg['Subject'] = subject

  msg.attach( MIMEText(text) )
  
  if len(files)==0:
     pass
  else:
     for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(f,"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)

  smtp = smtplib.SMTP(server)
  smtp.sendmail(send_from, send_to, msg.as_string())
  smtp.close()

send_files()
