#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  obvestila.py - Python script that checks for and shows new articles on Ubuntu.si
#  
#  Copyright 2013 Drazen M. <drazen@ubuntu.si>
#  Idea by dz0ny
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
# MAYBETODO LIST
# 	-> Check whether screen is locked or not by running 'gnome-screensaver-command -q |grep "is active"
# 	with os.system("command")
#	-> Add notifications into Ubuntu's messaging menu
# MUST DO LIST
#         -> Fix bug when you receive a title with a comma. Displays only first set of string till comma and nothing beyond that
 
import pynotify
import sys
import os.path
import json
from urllib2 import Request , urlopen
import threading
import HTMLParser
import time

if __name__ == '__main__':

	global notifications
	global latestID
	latestID = -1

	class TaskThread(threading.Thread):

		global notifications
		global latestID
		global internet_con
		global homepath

		def __init__(self):
			threading.Thread.__init__(self)
			self._finished = threading.Event()
			self._interval = 15.0

		def setInterval(self, interval):
			self._interval = interval

		def shutdown(self):
			self._finished.set()
		
		def run(self):
			while 1:
				if self._finished.isSet(): return
				self.task()
				self._finished.wait(self._interval)
				
		def homepath(path):
			return unicode(os.path.expandvars(path), sys.getdefaultencoding())

		def notifications(novica):
			#we should wait a few seconds to load all the stuff in case we have autologin enabled
			time.sleep(30)
			if not pynotify.init("Preizkus obvestil"):
				sys.exit(1)

			icon = homepath('$HOME/.UbuntuSi/ubuntusi.png')

			if ( os.path.exists(icon) ) :
				n = pynotify.Notification("Novica", novica , icon)
				if not n.show():
					print "Napaka pri posiljanju obvestil"
					sys.exit(1)
			else :
				n = pynotify.Notification("Novica", novica)
				if not n.show():
					print "Napaka pri posiljanju obvestil"
					sys.exit(1)

		def internet_con(test_url):

			global latestID
			#preverimo ce nam odpre googlov link i.e. ali dela internet 
			try:
				response = Request(test_url)
				return True
			except Exception as err: 
				pass
			return False

		def task(self):

			global notifications
			global latestID
			global internet_con
			test_url = "http://www.gstatic.com/inputtools/images/tia.png"

			if ( internet_con(test_url) ):
				getRecentPosts = Request("https://www.ubuntu.si/api/get_recent_posts/")

				try: 
					recentPostsOutput = json.load(urlopen(getRecentPosts))
				except Exception as e: 
					pass

				idlist = json.dumps([s['id'] for s in recentPostsOutput['posts']]).strip('[ ]').split()
				getTitleList = json.dumps([s['title_plain'] for s in recentPostsOutput['posts']], ensure_ascii=False).strip('[ ]')
				tmp = getTitleList.replace('"','').split(',')
				n=0

				for i in idlist:
					idlistItem = i.strip(',')
					getTitleListItem = tmp[n].strip('"')
					n=n+1
					if ( idlistItem > latestID ):
						latestID = idlistItem
						parser = HTMLParser.HTMLParser()
						notifications(parser.unescape(getTitleListItem))
			else :
				#notifications("Napaka pri povezovanju")
				#Optional notifications
				pass

	timer = TaskThread()
	timer.setInterval(7200)
	timer.run()