import tweepy
#from ipdb import set_trace
from os import path
import sys
import os
import webbrowser 
import sqlite3
import datetime
import argparse
import time


def add_to_buffer(user):

	while True:
		tweeter = raw_input("enter your tweet: ")
		
		if tweeter!="":
			date=datetime.date.today().strftime("%d %m %Y")
			time=datetime.datetime.now().time().strftime("%H %M %S")
			buffer_path='dbase/'+user+'_buff.db'
	
			conn = sqlite3.connect(buffer_path)
			c = conn.cursor()
	#set_trace()	
	# Insert a row of data
			c.execute("INSERT INTO tweets VALUES (null,?,?,?)",(tweeter,date,time))
	
	# Save (commit) the changes
			conn.commit()

	# We can also close the connection if we are done with it.
	# Just be sure any changes have been committed or they will be lost.
			conn.close()
	#return buffer_path
	## If it doesn't, we will create one.
		else:
			break


def get_last():
	conn = sqlite3.connect('dbase/cred.db')
	c = conn.cursor()
	

	t = (1,)
	c.execute('SELECT * FROM tweets WHERE Id=?', t)
	print c.fetchone()

def del_post(t):
	conn = sqlite3.connect('dbase/subho_buff.db')
	c = conn.cursor()
	
	c.execute('DELETE FROM tweets WHERE tweet=?',t)

	conn.commit()
	#print "post deleted"
	conn.close()

def post():
	conn = sqlite3.connect('dbase/subho_buff.db')
	c = conn.cursor()
	
	
	c.execute('SELECT tweet FROM tweets')
	j= c.fetchone()
	conn.close()
	return j
	

def getuser():
	conn = sqlite3.connect('dbase/cred.db')
	c = conn.cursor()
	
	t='1'
	c.execute('SELECT author FROM credentials WHERE Id=?',t)
	for row in c.fetchone():
		return row
	#print b

def get_cred():
	conn = sqlite3.connect('dbase/cred.db')
	c = conn.cursor()
	
	t='1'
	c.execute('SELECT author,consumer_key,consumer_secret,auth_key,auth_secret FROM credentials WHERE Id=?',t)
	for user,con_key,con_secret,auth_key,auth_sec in c.fetchmany():
		return user,con_key,con_secret,auth_key,auth_sec


def login(consumer_key,consumer_secret,auth_key,auth_secret,token):
	auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
	auth.set_access_token(auth_key,auth_secret)
	api=tweepy.API(auth)
	#print "Authenticated!!"
	return api
	'''
	update=post()
	else:
		update=if(bool(api.update_status(update))):
		print "Status updated successfully!!!"
	'''
#def updater(api):
	
def buff_disp():
	conn = sqlite3.connect('dbase/subho_buff.db')
	c = conn.cursor()
	
	t=('1',)
	c.execute('SELECT * FROM tweets')
	for i in c.fetchall():
		print i
	conn.close()

        
def createDaemon(choice):
    if choice=="start":
    	
		try:
			pid = os.fork()
			if pid > 0:
				print 'PID: %s Daemon started successfully' % pid
				with open('pidinfo', 'w') as piddata:
					piddata.write("%d" %pid)
				os._exit(0)
		except OSError, error:
			print 'Unable to fork. Error: %d (%s)' % (error.errno, error.strerror)
			os._exit(1)
		posting()
    
    elif choice == 'stop':
        with open('pidinfo', 'r') as pid:
            os.kill(int(pid.read()), 15)
        print "Daemon killed succesfully"
    else:
        pass


def posting():
    while True:
		user,con_key,con_secret,auth_key,auth_sec=get_cred()
		user=user.encode("utf-8")
		#print user 
		auth_key=auth_key.encode("utf-8")
		auth_sec=auth_sec.encode("utf-8")
		con_key=con_key.encode("utf-8")
		con_secret==con_secret.encode("utf-8")
		token="daemon"
		j=post()
			
		
		api=login(con_key,con_secret,auth_key,auth_sec,token)
		api.update_status(j[0].encode("utf-8"))

		del_post(post())
	


		time.sleep(60)




def main():
	
	
	parser = argparse.ArgumentParser(prog='Buff_tweet',usage='%(prog)s is used to buffer your tweets [options]')
	parser.add_argument('-b', '--store' , action="store_true", help="store your tweet")
	parser.add_argument('-on','--start',action='store_true', help="start posting")
	parser.add_argument('-off', '--stop', action='store_true', help="stop posting")
	parser.add_argument('-p', '--post' , help="posts tweets instantly")
	parser.add_argument('-d', '--display' , action="store_true", help="menu mode")

	
	args = parser.parse_args()

	if args.start==True:
		createDaemon("start")
	
	elif args.stop==True:
		createDaemon("stop")
		#if daemon off
		#	error
		#else:
		#	stop daemon
	elif args.post!=None:
		print "start"#if daemon on
		#authenticate then post
	
	elif args.store==True:
		add_to_buffer('subho')
		buff_disp()
	
	elif args.display==True:
		buff_disp()
		#display menu
	else:

		os.system("python bufftweet.py -h")
		






if __name__=='__main__':
	
	main()
	


	#main()#user=raw_input("enter your name: ")
	#ip='y'
	
	
	#print user,auth_key,auth_sec,con_key,con_secret
	#dbname=add_to_buffer(user)
	#print dbname
	