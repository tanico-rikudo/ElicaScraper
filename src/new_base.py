import datetime,time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate

import ConfigParser



print("{0:%Y%m%d}".format(now))


MAIL_CONFIG		= 'elica_mail.conf' 
NIKKEI_CONFIG	= 'elica_nikkei.conf' 

# login page
ID = "kotetsu219specialpartner@gmail.com"
PASS = "25802580"

print config.get(section1, 'port') # 10001

class UTIL:

	def __init__():


	def read_config(path_conf):
		config = ConfigParser.ConfigParser()
		config.read(path_conf)
	 	FROM_ADDRESS = config.get(section1, 'FROM_ADDRESS') # localhost

	 def set_time():
	 	self.now = datetime.datetime.now()

	 def run_cmd(cmd):
	 	try:
	 		subprocess.call(cmd.split())
	 	except Exception as e:
			logger.warning('Cannot execute cmd:',e)
			return False
		return True 	



class MAILER:
	def __init__():
		self.from_addr = 
		self.ls_to_addr = 
		self.obj_smtp = None
		self.url_smtp = 'smtp.gmail.com'
		self.port_smtp = 587
		self.addr_login = 
		self.service_name =  
		# self.obj_msg = {}

	def set_smtp_obj():
		try:
			self.obj_smtp = smtplib.SMTP(self.url_smtp, self.port_smtp)
			self.obj_smtp.ehlo()
			self.obj_smtp.starttls()
			self.obj_smtp.ehlo()
			self.obj_smtp.login(self.addr_login, self.pw_login)
			logger.info('Get smtp object')
		except Exception as e:
			del self.obj_smtp
			logger.warning('Cannot get smtp object:',e)
			return False
		return True


	def exec_send(self):
		if not self.obj_smtp is None:
			try:
				self.obj_smtp.sendmail(self.from_addr, self.ls_to_addr, self.obj_msg.as_string())
				self.obj_smtp.close()
				return True
			except Exception as e:
				logger.warning('Cannot send mail: ',e)		
				return False
		else:
			logger.warning('No smtp obj')	
			return False


	def make_content(self,subject, body):
		self.obj_msg = MIMEMultipart('alternative')
		part = MIMEText(self.finalize_html(body),'html')
		self.obj_msg['Subject'] = subject
		self.obj_msg['From']= self.from_addr
		self.obj_msg['To']	= self.to_addr
		self.obj_msg['Date']= formatdate()
		self.obj_msg.attach(part)
		return

	def finalize_html(self,body):
		# add credit
		body += "<br>"
		body += "SENT BY "+self.service_name
		body += "<br>"
		return body	





class ACCESS:
	def __init__():
		self.headless = 
		self.default_timeout = 
		self.url_logout	= 
		self.url_login	= 
		self.ls_url_sucess = []
		self.ls_url_failed = []
		self.driver = self.set_driver()
		return self

	def set_driver(self):
		options = webdriver.ChromeOptions()
		if self.headless
			options.add_argument('--headless')
		# driver = webdriver.Chrome(options=options,executable_path="/home/kotetsu219specialpartner/bin/chromedriver") 
		self.driver = webdriver.Chrome(options=options) 
		# driver = webdriver.Chrome()
		return True

	def del_driver(self,):
		try:
			self.driver.quit()
			logger.info('Driver was killed')
		except Exception as e:
			logger.warning('Driver wasn\'t killed')
			return False

		try:
			self.util.run_cmd('pkill -9 chromedriver')
			logger.info('chromedriver pricess was killed')
		except Exception as e:
			logger.warning('chromedriver pricess wasn\'t killed:')
			return False

		return True


	def to_page(self,url,waittime=0,timeout=120):

		@timeout(timeout)
		def access_page(url):
			self.driver.get(url)

		try:
			access_page(url)
			logger.info('Driver get web page:',url)
			self.ls_url_sucess.append(url)
		except Timeout:
			logger.warning('Driver cannot get web page:',url)
			self.ls_url_failed.append(url)
			return False
		except Exception as e:
			logger.warning('Driver occur error in access page :',e)	
			self.ls_url_failed.append(url)
			return False

		if waittime>0:
			logger.info('Driver enter wait time')
			time.sleep(waittime)
			logger.info('Driver restart from wait time')

		return True



	def get_login_page(self,url,allow_revisit):
		logger.info('Driver get to login status')
		#remove logout address #TODO
		try:
			if (url not in self.ls_url_sucess)or(allow_revisit):
				status = self.to_url(url)
			else:
				logger.info('Driver don\'t need to pass login process')
		except Exception as e:
			logger.warning('Driver occur error in login master:',e)	
			return False
		return True



	def get_logout_page(self,url,allow_revisit):
		logger.info('Driver get to logout status')
		#remove login address #TODO
		try:
			if (url not in self.ls_url_sucess)or(allow_revisit):
				status = self.to_url(url)
			else:
				logger.info('Driver don\'t need to pass logout process')
		except Exception as e:
			logger.warning('Driver occur error in logout master:',e)	
			return False
		return True





class NIKKEI:
	def __init__():
		self.agent = ACCESS()
		self.util = UTIL()
		self.url_login = 'https://www.nikkei.com/login'
		self.url_logout= 'https://regist.nikkei.com/ds/etc/accounts/logout'


	def get_edition_paper(self,obj_dt=None,type='en'):
		# set dt
		if obj_dt is None:
			obj_dt = self.util.now

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
			obj_dt = self.util.now

		# construct url
		url_paper = 'https://www.nikkei.com/paper/'+self.get_edition_paper(obj_dt)+'/?b='+"{0:%Y%m%d}".format(obj_dt)+'&d=0' 

		return url_paper

	def get_contents_in_paper(self):

		# get session
		self.logout()
		self.login()

		# get paper obj 
		is_obj = self.to_page(self.get_paper_url)

		if not is_obj:
			message = 'Access is failed. May be not available today?'
			return False

		contents = self.scrape_paper()

		# make subject
		str_edition = get_edition_paper(self,obj_dt=None,type='en')
		subject = "{0:%Y%m%d}".format(now)+'日経紙面('+str_edition+'刊)一覧'

		# discard session
		self.logout()
		logger.info('Get content from web pagesucessfly')

		return  subject,contents

	def make_html(body):
		html =body
		return html


	def scrape_paper(self):
		ls_body = []
		try:
			sections = self.agent.driver.find_elements_by_css_selector('.cmn-section')

			for section in sections:
				# title
				try:
					section_title = section.find_element_by_css_selector('.cmnc-title').text
					if not section_title == '': 
						# print("<"+section_title+">") 
						# body += ('<br>'+"＝＝"+section_title+"＝＝"+'<br>')
						dc = {}
						dct_section['section_name'] = section_title
						dct_section['ls_top_news'] = []

						#top news
						try:
							articles = section.find_elements_by_css_selector('.cmn-top_news')
							for article in  articles:
								try:
									article_titles = article.find_elements_by_css_selector('.cmn-article_title')
									for article_title in  article_titles:
										article_title_text =  article_title.text.replace('<br>','')
										# print("　★"+article_title_text)
										# body += ("　★"+article_title_text+'<br>')
										dct_section['ls_top_news'].append(article_title_text)										
								except:
									pass
						except:
							pass

						#article
						dct_section['ls_article'] = []
						try:
							articles = section.find_elements_by_css_selector('.cmn-article_list')
							for article in  articles:
								try:
									# 1
									article_title = article.find_element_by_css_selector('.cmn-article_title')
									article_title_text2 = article_title.text.replace('<br>','')
									if article_title_text2 != article_title_text:
										# print("　・"+article_title_text2)
										# body += ("　・"+article_title_text2+'<br>')
										dct_section['ls_article'].append(article_title_text2)

										ls_small_article = []
										small_articles = article.find_elements_by_css_selector('.cmn-article_list')
										for small_article in small_articles:
											try:
												small_article_titles = small_article.find_elements_by_css_selector('.cmn-article_title')
												for small_article_title in small_article_titles:
													small_article_title_text = small_article_title.text.replace('<br>','')
													# print("　　・"+small_article_title_text)
													# body += ("　　・"+small_article_title_text+'<br>')
													ls_small_article.append(small_article_title_text)
											except:
												pass

										dct_section['ls_article'].append(ls_small_article)

								except:
									pass
						except:
							pass


						ls_body.append(dct_section)


					else:
						pass

				except:
					continue
		except:
			pass
		return ls_body		


	def login(self):
		self.agent.get_login_page(self.url_login,waittime=10)
		self.agent.driver.find_element_by_id('LA7010Form01:LA7010Email').send_keys(ID)
		self.agent.driver.find_element_by_id('LA7010Form01:LA7010Password').send_keys(PASS)
		self.agent.driver.find_element_by_class_name("btnM1").click();
		return 

	def logout(self):
		self.agent.get_login_page(self.url_login,waittime=10)
		return 		



class NEWSPICKS:
	def __init__():




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




def mail(subject,body,to_addr):
	msg = create_message(FROM_ADDRESS, to_addr,  subject, body)
	send(FROM_ADDRESS, to_addr, msg)



def get_nikkei_and_mail():
	obj_nikkei = NIKKEI()
	subject,content = obj.get_contents_in_paper()
	body_html = obj_nikkei.make_html(content)
	obj_mailer = MAILER()
	obj_mailer.set_smtp_obj()
	obj_mailer.make_content()
	obj_mailer.exec_send()
	return 

def make_newspicks_mail():
	body = add_system_credit(newspicks_access())
	time_p_str =  "朝" if now.time().hour < 15 else "夕"
	subject = "{0:%Y%m%d}".format(now)+'Newspicks('+time_p_str+')一覧'
	return (body,subject)



if __name__ == '__main__':
	get_nikkei_and_mail()
	# (body,subject) = make_nikkei_mail()
	# send_action(subject,body)

	# (body,subject) = make_newspicks_mail()
	# send_action(subject,body)


