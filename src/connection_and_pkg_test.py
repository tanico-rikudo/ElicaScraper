from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def pkg_test():
	try:
		#basis
		import datetime
		from  datetime import datetime as dt
		import time

		#debug
		import pickle

		#util
		import subprocess
		import configparser
		import logging
		import csv
		import socket

		#crawl
		from selenium import webdriver
		from selenium.webdriver.common.action_chains import ActionChains

		# mail 
		import smtplib
		from email.mime.text import MIMEText
		from email.mime.multipart import MIMEMultipart
		from email.utils import formatdate

		from timeout_decorator import timeout, TimeoutError
		print('[OK]pkg test')
	except Exception as e:
		print('pkg test error: ',e)


def connection_test():
	try:
		options = Options()
		import socket
		hostname = socket.gethostname()

		if hostname == 'elica03':
			driver = webdriver.Chrome(options=options,executable_path="/home/kotetsu219specialpartner/bin/chromedriver")
		if hostname == 'Macico.local':
			driver = webdriver.Chrome(options=options)

		options.add_argument('--headless')
		options.add_argument('--disable-gpu')
		options.add_argument('--disable-infobars')
		
		driver.get('https://www.google.co.jp/')
		print(driver.title) #=> Google
		print('[OK]connection test')
		driver.quit()
	except Exception as e:
		print('connection test error: ',e)
		driver.quit()


if __name__ == '__main__':
	pkg_test()
	connection_test()
