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
		print('pkg test error: %s',e)


def connection_test():
	try:
		options = Options()
		options.add_argument('--headless')
		driver = webdriver.Chrome(chrome_options=options,executable_path="/home/kotetsu219specialpartner/bin/chromedriver")
		driver.get('https://www.google.co.jp/')
		print(driver.title) #=> Google
		print('[OK]connection test')
	except Exception as e:
		print('connection test error: %s',e)


if __name__ == '__main__':
	pkg_test()
	connection_test()
