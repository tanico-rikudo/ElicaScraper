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

#crawl
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

# mail 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate

from timeout_decorator import timeout, TimeoutError

MAIL_CONFIG		= '../conf/mail.conf' 
ELICA_CONFIG	= '../conf/elica.conf' 
ENV = 'DEV'
SEAVICE_NAME = 'ELICA SYSTEM'
LS_TO_ADDRESS=['kazuyo.rikudo@gmail.com']#TODO : move it 


logging.basicConfig(level=logging.INFO)#TODO : move it


class UTIL:

	def __init__(self,version,service_name):
		self.version = version
		self.service_name =service_name 
		self.dt_init = dt.now()

	def set_logger(self):
		self.logger = logging.getLogger(self.service_name)



	def read_config(self,path_conf):
		config = configparser.ConfigParser()
		config.read(path_conf,encoding='utf-8')
		target_config = config[self.version]
		if target_config is None:
			return False
		else: 		
			self.config = target_config
			return True

	def set_time(self):
		self.now = datetime.datetime.now()

	@staticmethod
	def run_cmd(cmd):
		try:
			subprocess.call(cmd.split())
		except Exception as e:
			self.util.logger.warning('Cannot execute cmd: %s', e)
			return False
		return True 	



class MAILER:
	def __init__(self):
		self.util = UTIL(version=ENV,service_name=SEAVICE_NAME)
		self.util.set_logger()
		
		# read config and set
		self.util.read_config(MAIL_CONFIG)
		self.from_addr = self.util.config['FROM_ADDRESS']
		self.ls_to_addr = LS_TO_ADDRESS
		self.url_smtp =  self.util.config['URL_SMTP']
		self.port_smtp = self.util.config['PORT_SMTP']
		self.addr_login = self.util.config['LOGIN_ADDRESS']
		self.pw_login = self.util.config['LOGIN_PW']
		self.service_name = self.util.service_name
		# self.obj_msg = {}


	def set_smtp_obj(self):
		try:
			self.obj_smtp = smtplib.SMTP(self.url_smtp, self.port_smtp)
			self.obj_smtp.ehlo()
			self.obj_smtp.starttls()
			self.obj_smtp.ehlo()
			self.obj_smtp.login(self.addr_login, self.pw_login)
			self.util.logger.info('Get smtp object')
		except Exception as e:
			self.util.logger.warning('Cannot get smtp object:',e)
			return False
		return True


	def exec_send(self):

		if not self.obj_smtp is None:
			try:
				self.util.logger.info('Mail is sending for %s',str(self.ls_to_addr))
				self.obj_smtp.sendmail(self.from_addr, self.ls_to_addr, self.obj_msg.as_string())
				self.util.logger.info('Mail is sent')
				self.obj_smtp.close()
				return True
			except Exception as e:
				self.util.logger.warning('Cannot send mail: %s',e)		
				return False
		else:
			self.util.logger.warning('No smtp obj')	
			return False


	def make_content(self,subject, body):
		try:
			self.obj_msg = MIMEMultipart('alternative')
			part = MIMEText(self.finalize_html(body),'html')
			self.obj_msg['Subject'] = subject
			self.obj_msg['From']= self.from_addr
			self.obj_msg['To']	= ", ".join(self.ls_to_addr)
			self.obj_msg['Date']= formatdate()
			self.obj_msg.attach(part)
			self.util.logger.info('Get mail contents object')
		except Exception as e:
			self.util.logger.warning('Cannot make mail: %s',e)	
			return False

		return True

	def finalize_html(self,body):
		# add credit
		body += "<br>"
		body += "SENT BY "+self.service_name
		body += "<br>"
		return body	


class ACCESS:
	def __init__(self):

		#True/False
		self.headless = False

		#set log
		self.util = UTIL(version=ENV,service_name=SEAVICE_NAME)
		self.util.set_logger()

		# sec
		self.default_timeout_sec = 200

		# history
		self.ls_url_sucess = []
		self.ls_url_failed = []

		#driver
		self.set_driver()


	def set_driver(self):
		options = webdriver.ChromeOptions()
		if self.headless:
			options.add_argument('--headless')
		# driver = webdriver.Chrome(options=options,executable_path="/home/kotetsu219specialpartner/bin/chromedriver") 
		self.driver = webdriver.Chrome(options=options) 
		# driver = webdriver.Chrome()
		return True

	def del_driver(self):
		try:
			self.driver.quit()
			self.util.logger.info('Driver was killed')
		except Exception as e:
			self.util.logger.warning('Driver wasn\'t killed')
			return False

		try:
			self.util.run_cmd('pkill -9 chromedriver')
			self.util.logger.info('chromedriver pricess was killed')
		except Exception as e:
			self.util.logger.warning('chromedriver pricess wasn\'t killed:')
			return False

		return True


	def to_page(self,url,**kwargs):

		if 'waittime' in kwargs.keys():
			waittime = kwargs['waittime']
		else:
			waittime = 0			
		if 'timeout_sec' in kwargs.keys():
			timeout_sec = kwargs['timeout_sec']
		else:
			timeout_sec = 120

		@timeout(timeout_sec)
		def access_page(url):
			self.driver.get(url)



		try:
			access_page(url)
			self.util.logger.info('Driver get web page: %s',url)
			self.ls_url_sucess.append(url)
		except TimeoutError :
			self.util.logger.warning('Driver cannot get web page: %s',url)
			self.ls_url_failed.append(url)
			return False
		except Exception as e:
			self.util.logger.warning('Driver occur error in access page: %s',e)	
			self.ls_url_failed.append(url)
			return False

		if waittime>0:
			self.util.logger.info('Driver enter wait time : %d',waittime)
			time.sleep(waittime)
			self.util.logger.info('Driver restart from wait time')

		return True



	def get_login_page(self,url,allow_revisit=True,**kwargs):
		self.util.logger.info('Driver get to login status')
		#remove logout address #TODO

		access_kwargs = {}
		if 'waittime' in kwargs.keys():
			access_kwargs['waittime'] = kwargs['waittime']
		if 'timeout_sec' in kwargs.keys():
			access_kwargs['timeout_sec'] = kwargs['timeout_sec']

		try:
			if (url not in self.ls_url_sucess)or(allow_revisit):
				status = self.to_page(url,**access_kwargs)
			else:
				self.util.logger.info('Driver don\'t need to pass login process')
		except Exception as e:
			self.util.logger.warning('Driver occur error in login master: %s',e)	
			return False
		return True



	def get_logout_page(self,url,allow_revisit=True,**kwargs):
		self.util.logger.info('Driver get to logout status')
		#remove login address #TODO

		access_kwargs = {}
		if 'waittime' in kwargs.keys():
			access_kwargs['waittime'] = kwargs['waittime']
		if 'timeout_sec' in kwargs.keys():
			access_kwargs['timeout_sec'] = kwargs['timeout_sec']

		try:
			if (url not in self.ls_url_sucess)or(allow_revisit):
				status = self.to_page(url,**access_kwargs)
			else:
				self.util.logger.info('Driver don\'t need to pass logout process')
		except Exception as e:
			self.util.logger.warning('Driver occur error in logout master: %s',e)	
			return False
		return True





class NIKKEI:
	def __init__(self):
		self.agent = ACCESS()
		self.util = UTIL(version=ENV,service_name=SEAVICE_NAME)
		self.util.read_config(ELICA_CONFIG)
		self.util.set_logger()
		self.url_login = 'https://www.nikkei.com/login'
		self.url_logout= 'https://regist.nikkei.com/ds/etc/accounts/logout'


	def get_edition_paper(self,obj_dt=None,type='en'):
		# set dt
		if obj_dt is None:
			obj_dt = self.util.dt_init

		# set edition
		str_edition_paper=  "morning" if obj_dt.hour < 15 else "evening"

		# translate
		if type=='ja':
			dct_en_ja = {'morning':'朝','evening':'夕'}
			str_edition_paper = dct_en_ja[str_edition_paper]

		return str_edition_paper

	def get_paper_url(self,obj_dt=None):

		# set dt
		if obj_dt is None:
			obj_dt = self.util.dt_init

		# construct url
		url_paper = 'https://www.nikkei.com/paper/'+self.get_edition_paper(obj_dt)+'/?b='+"{0:%Y%m%d}".format(obj_dt)+'&d=0' 

		return url_paper

	def get_contents_in_paper(self):

		# get session
		self.logout()
		self.login()

		# get paper obj 
		self.util.logger.info('Accessing Web page..')
		is_obj = self.agent.to_page(self.get_paper_url(),**{'waittime':30})

		if not is_obj:
			self.util.logger.warning('Access is failed : May be not available today?')
			return False

		self.util.logger.info('Scraping Web page..')
		obj_content = self.scrape_paper()

		# make subject
		str_edition = self.get_edition_paper(obj_dt=None,type='ja')
		str_subject = "{0:%Y%m%d}".format(self.util.dt_init)+'日経紙面('+str_edition+'刊)一覧'

		# discard session
		self.logout()
		self.util.logger.info('Get content from web pagesucessfly')
		self.agent.del_driver()

		return  str_subject, obj_content

	def login(self):
		self.agent.get_login_page(self.url_login, allow_revisit=True, **{'waittime':30,'timeout_sec':120}	)
		self.agent.driver.find_element_by_id('LA7010Form01:LA7010Email').send_keys(self.util.config['ID'])
		self.agent.driver.find_element_by_id('LA7010Form01:LA7010Password').send_keys(self.util.config['PW'])
		self.agent.driver.find_element_by_class_name("btnM1").click();
		return 

	def logout(self):
		self.agent.get_logout_page(self.url_logout, allow_revisit=True, **{'waittime':10} )
		return 	

	def scrape_paper(self):
		ls_body = []
		try:
			ls_el_section = self.agent.driver.find_elements_by_css_selector('.cmn-section')

			for el_section in ls_el_section:
				# title
				try:
					section_title = el_section.find_element_by_css_selector('.cmnc-title').text
					if (section_title != '')&(section_title!='短信'): 
						# print("<"+section_title+">") 
						# body += ('<br>'+"＝＝"+section_title+"＝＝"+'<br>')
						dct_section = {}
						dct_section['section_name'] = section_title
						self.util.logger.info('[OK] %s',section_title)
						dct_section['ls_top_news'] = []

						#top news
						try:
							ls_el_article = el_section.find_elements_by_css_selector('.cmn-top_news')
							for el_article in  ls_el_article:
								try:
									ls_el_topic = el_article.find_elements_by_css_selector('.cmn-article_title')
									for el_topic in  ls_el_topic :
										topic_text =  el_topic.text.replace('<br>','')
										topic_text=  topic_text.strip()#空白削除

										dct_section['ls_top_news'].append(topic_text)
										self.util.logger.info('[OK] %s > (L)%s',section_title,topic_text)								
								except Exception as e:
									self.util.logger.warning('[NG] %s > (L)???',section_title,e)
									continue
						except Exception as e:
							self.util.logger.warning('[NG] %s : (L)No top news: %s ',section_title,e)

						#article
						dct_section['ls_article'] = []
						try:
							ls_el_article = el_section.find_elements_by_css_selector('.cmn-article_list')
							for el_article in  ls_el_article:
								try:
									ls_el_topic = el_article.find_elements_by_css_selector('.cmn-article_title')
									ls_small_topic = []
									for el_topic in ls_el_topic:

										#テキスト取得	
										topic_text = el_topic.text.replace('<br>','')
										topic_text=  topic_text.strip()#空白削除

										#すでにTOPnewsにある
										if topic_text in dct_section['ls_top_news']:
											self.util.logger.info('[・] %s > %s is already added',section_title,topic_text)										
											continue

										#すでに articleにある(small list外して)
										if topic_text in dct_section['ls_article']:
											self.util.logger.info('[・] %s > %s is already added',section_title,topic_text)										
											continue											

										#配置先チェック
										try:
											#小規模リスト
											if el_topic.tag_name == 'h5':

												#すでにls_small_topicある
												if topic_text in ls_small_topic:
													self.util.logger.info('[・] %s > > %s is already added',section_title,topic_text)										
												else:
													ls_small_topic.append(topic_text)
													self.util.logger.info('[OK] %s >  > %s',section_title,topic_text)	
											else:
												#直前までを挿入
												if len(ls_small_topic) > 0:
													dct_section['ls_article'].append(ls_small_topic)
												ls_small_topic = []

												#当該記事入れる
												dct_section['ls_article'].append(topic_text)
												self.util.logger.info('[OK] %s > %s',section_title,topic_text)
										except Exception as e:
											self.util.logger.warning('[NG] %s > %s (cannot insert): %s',section_title,topic_text,e)
											continue										

									#残存を挿入
									if len(ls_small_topic) > 0:
										dct_section['ls_article'].append(ls_small_topic)														
										
								except Exception as e:
									self.util.logger.warning('[NG] %s > ???(topic): %s',section_title,e)
									continue
						except Exception as e:
							self.util.logger.warning('[NG] %s > ???(topic list): %s',section_title,e)

						finally:
							ls_body.append(dct_section)

					else:
						self.util.logger.warning('[NG] ???(section title is null or excluded)')

				except Exception as e:
					self.util.logger.warning('[NG] ???(No section title): %s',e)
					continue
		except Exception as e:
			self.util.logger.warning('[NG] ???(Cannot find sections): %s',e)

		return ls_body		


	@staticmethod
	def make_html(obj_content):
		body =''
		for obj_section in obj_content:
			if isinstance(obj_section['section_name'],str):
				body += '=== {0} ===<br>'.format(obj_section['section_name']) 

			for obj_top_news in obj_section['ls_top_news']:
				if isinstance(obj_top_news,str):
					body += '　★ {0}<br>'.format(obj_top_news)
			for obj_article in obj_section['ls_article']:
				if isinstance(obj_article,str):
					body += '　・{0}<br>'.format(obj_article)
				else:
					for obj_small_article in obj_article:
						body += '　　・{0}<br>'.format(obj_small_article)
			body += '<br>'

		return body



class NEWSPICKS:
	def __init__():
		pass



	def newspicks_access():
		driver = setup()
		body = "<br>"
		
		# access
		driver.get('https://newspicks.com/theme-news/technology/')
		time.sleep(10)
		body = body + '<br>★テクノロジー★<br>'+newspicks_search(driver)

		# driver.get('https://newspicks.com/theme-news/innovation/')
		# time.sleep(10)
		# body = body + '<br>★イノベーション★<br>'+newspicks_search(driver)

		driver.quit()
		print("ACCESS SEND!")
		return  body

	def newspicks_search(driver):

		body = ""

		sections = driver.find_elements_by_css_selector('.news-card')
		# print("<"+sections.text+">") 
		for section in sections:
			# titl
			attr =section.find_element_by_tag_name('a')
			href = attr.get_attribute('href')
			attr = attr.find_elements_by_tag_name('div')[1]
			# print("<"+attr.text+">") 
			text = attr.text
			title = attr.get_attribute('title')
			if len(title) > len(text):
				# print("<"+title+">") 
				body += ('・<a href='+href+'>'+title+'</a><br>')
			else:
				body += ('・<a href='+href+'>'+text+'</a><br>')			
			# except:

		return body


def get_nikkei_and_mail():
	obj_nikkei = NIKKEI()

	str_subject,obj_content = obj_nikkei.get_contents_in_paper()
	save_pickle(obj_content,'content.pickle')

	# obj_content = read_pickle('content.pickle')
	body_html = obj_nikkei.make_html(obj_content)
	# save_pickle(body_html,'body.pickle')


	obj_mailer = MAILER()
	obj_mailer.set_smtp_obj()
	obj_mailer.make_content(str_subject,body_html)
	obj_mailer.exec_send()
	return 

def make_newspicks_mail():
	body = add_system_credit(newspicks_access())
	time_p_str =  "朝" if now.time().hour < 15 else "夕"
	subject = "{0:%Y%m%d}".format(now)+'Newspicks('+time_p_str+')一覧'
	return (body,subject)

def save_pickle(obj,name):
	# name = folder + name
	with open(name,'wb') as f:
		pickle.dump(obj,f)

def read_pickle(name):
	# name = folder + name
	with open(name,'rb') as f:
		obj = pickle.load(f)
	return obj



if __name__ == '__main__':
	get_nikkei_and_mail()
	# (body,subject) = make_nikkei_mail()
	# send_action(subject,body)

	# (body,subject) = make_newspicks_mail()
	# send_action(subject,body)


