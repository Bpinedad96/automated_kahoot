#!/usr/bin/env python2

import sys
import time
import re
import os
import selenium
import openpyxl
import gtk, pygtk
import rospy

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from std_msgs.msg import Float32MultiArray

driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
# Open camera ip page
driver.get("https://kahoot.it/")
actions=ActionChains(driver)
info=None

if sys.argv[2]=='1':
	#relocate window
	driver.set_window_size(gtk.gdk.screen_width()/2, gtk.gdk.screen_height()/2)
	driver.set_window_position(gtk.gdk.screen_width()/2+10, 0)
elif sys.argv[2]=='0':
	#relocate window
	driver.set_window_size(gtk.gdk.screen_width()/2, gtk.gdk.screen_height()/2)
	driver.set_window_position(gtk.gdk.screen_width()/2+10, gtk.gdk.screen_height()/2)

def check_exists_by_xpath(xpath):
	try:
		driver.find_element_by_xpath(xpath)
	except NoSuchElementException:
		return False
	return True

def callback(data):
	global info
	info=data.data
	
def main():
	#Enter quiz
	time.sleep(5)
	room=driver.find_element_by_xpath('//*[@id="mainView"]/div[1]/div[2]/div/div/form/input')
	room.send_keys(str(sys.argv[1]))
	button=driver.find_element_by_xpath('//*[@id="mainView"]/div[1]/div[2]/div/div/form/button')
	button.click()
	time.sleep(2)
	usr=driver.find_element_by_xpath('//*[@id="mainView"]/div[1]/div[2]/div/div/form/input')
	usr.send_keys("Player "+str(sys.argv[2]))
	button=driver.find_element_by_xpath('//*[@id="mainView"]/div[1]/div[2]/div/div/form/button')
	button.click()

	rospy.init_node('listener', anonymous=True)
	i=0
	while (i < int(sys.argv[3])):
		rospy.Subscriber("objects", Float32MultiArray, callback)
		rospy.spin()
		print (info)
		if str(driver.current_url)=='https://kahoot.it/getready':
			solved=False
		try:
			iframe=driver.find_element_by_id('gameBlockIframe')
			driver.switch_to_frame(iframe)
			if len(info)>1 and len(info)<12:
				if sys.argv[2]=='0' and info[0]<5:
					button=driver.find_element_by_xpath('//*[@id="app"]/main/div[1]/button['+str(info[0])+']')
					button.click()
					solved=True
				elif sys.argv[2]=='1' and info[0]>4:
					button=driver.find_element_by_xpath('//*[@id="app"]/main/div[1]/button['+str(info[0]-4)+']')
					button.click()
					solved=True

			elif len(info)>12:
				if sys.argv[2]=='0' and info[12]<5:
					button=driver.find_element_by_xpath('//*[@id="app"]/main/div[1]/button['+str(info[0])+']')
					button.click()
					solved=True
				elif sys.argv[2]=='1' and info[12]>4:
					button=driver.find_element_by_xpath('//*[@id="app"]/main/div[1]/button['+str(info[0]-4)+']')
					button.click()
					solved=True
			
			driver.switch_to_default_content()
		except:
			pass
		if driver.current_url=='https://kahoot.it/answer/result':
			solved=True
			time.sleep(5)
		if (solved):
			i+=1

		print (info)
		time.sleep(5)
		return

if __name__ == '__main__':
    main()
