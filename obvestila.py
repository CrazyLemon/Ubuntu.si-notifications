#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  obvestila.py - Python script that checks for and shows new posts on Ubuntu.si
#
#  Author: Dražen M. <drazen@ubuntu.si>
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
#       MAYBETODO LIST
#      -> Check whether screen is locked or not by running 'gnome-screensaver-command -q |grep "is active"
#      with os.system("command")
#      -> Check whether monitor is on or off (xset -q doesn't help in this case because it always reports "Monitor is on")
#      -> Add notifications into Ubuntu's messaging menu

from __future__ import absolute_import
from __future__ import print_function
import notify2, sys, os.path, requests, threading, time, six

#disable https warnings about insecure request
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

if __name__ == '__main__':

	global notifications
	global latestID
	latestID = -1

	class TaskThread(threading.Thread):

		global notifications
		global latestID
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
			return six.text_type(os.path.expandvars(path), sys.getdefaultencoding())

		def notifications(category,author,title):
			# sleep is necessary if we use autologin and we do not want to miss notifications
			time.sleep(30)

			# test notifications daemon
			if not notify2.init("Preizkus obvestil"):
				sys.exit(1)

			icon = homepath('$HOME/.UbuntuSi/ubuntusi.png')
			msg = category + " - " + author
			# check if there's an icon and if not just send notifications without
			if ( os.path.exists(icon) ) :
				n = notify2.Notification(msg, title, icon)
				if not n.show():
					print("Napaka pri posiljanju obvestil")
					sys.exit(1)
			else :
				n = notify2.Notification(msg, title)
				if not n.show():
					print("Napaka pri posiljanju obvestil")
					sys.exit(1)

		def task(self):

			global notifications
			global latestID

			#test if we have internet connectivity
			r = requests.get("http://www.gstatic.com/inputtools/images/tia.png")
			if r.status_code == requests.codes.ok:
				try:
					# we need the verify=False because of SSL mismatch
					posts = requests.get("https://www.ubuntu.si/api/get_recent_posts/", verify=False).json()
				except Exception as e:
					pass
                # check for latest post and send it to our notification daemon
				for i in posts["posts"]:
					if i["id"] > latestID:
						latestID = i["id"]
						category =  i["categories"][0]["title"]
						author = i["author"]["name"]
						title = i["title_plain"]
						notifications(category,author,title)
			else :
				#notifications("Napaka pri povezovanju")
				#Optional
				pass

	timer = TaskThread()
	timer.setInterval(7200)
	timer.run()
