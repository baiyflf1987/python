#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from ftplib import FTP
import os
import sys
import glob


device = ''
filename = ''
local_path='/homes/ssd-builder/ngsrx-yocto-daily/DEV_X_151_X49_BRANCH/LATEST/srx-mr/ship/cli/'
#local_path='/homes/ssd-builder/ngsrx-yocto-daily/DEV_X_151_X49_BRANCH/LATEST/srx-ffp/ship/cli/'
#local_path='/homes/ssd-builder/ngsrx-yocto-daily/JUNOS_151_X49_D50_BRANCH/LATEST/srx-ffp/ship/cli/'
remote_path='/var/crash/corefiles/'


def filename():
		global filename
		path = glob.glob(local_path+"/"+'*.tgz')
		#print 'file path is :'+ path[0]
		filename = path[0].split('/')[-1]
		#print 'The lateset daily build is : '+filename
		return filename

def sysarg():

		global device
		global filename
		global local_path
		global remote_path

		s=sys.argv
		if len(s)==2 and s[1]== '--help':
				print "Please use -d device -f filename -l local_path -r remote_path"
				print '+'*30
				print "You can use './ftp_up.py -d device default' to use default value !"
				sys.exit()
		elif not s[1].startswith('-d'):
		        print "Please use -d device -f filename -l local_path -r remote_path"
		        sys.exit()
		elif s[1] == '-d':
				device = s[2]
				if s[3] == 'default':
						print "device is : "+device
						print "filename is : "+filename
						print "local_path is : "+local_path
						print "remote_path is : "+remote_path
	#					sys.exit()
				elif s[3] == '-f':
					   filename = s[4]
					   if not s[5].startswith('-l'):
							   print "Please use -d device -f filename -l local_path -r remote_path"
							   sys.exit()
					   elif s[5] == '-l':
							   local_path = s[6]
							   if not s[7].startswith('-r'):
									   print "Please use -d device -f filename -l local_path -r remote_path"
									   sys.exit()
							   elif s[7] == '-r':
									   remote_path = s[8]
									   print "device is : "+device
									   print "filename is : "+filename
									   print "local_path is : "+local_path
									   print "remote_path is : "+remote_path
		return device,filename,local_path,remote_path

def ftp_up():
		global device
		global filename
		global local_path
		global remote_path
		ftp=FTP()
		f=local_path+ "/" +filename
		ftp.set_debuglevel(1)
		ftp.connect(device,'21')
		ftp.login('root','Embe1mpls')
		print ftp.getwelcome()
		ftp.cwd(remote_path)
		bufsize = 1024
		file_handler = open(f,'rb')
		lsize = os.path.getsize(f)
		print 'The file\'s size is :'+ str(lsize)
		ftp.storbinary('STOR %s' % os.path.basename(f),file_handler,bufsize)
		ftp.set_debuglevel(0)
		#rsize = ftp.size(filename)
		#print 'file_size is :'+str(rsize)
		ftp.quit
		print "ftp up completed"




if __name__ == '__main__':
		filename()
		sysarg()
		ftp_up()
