import datetime

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

now = datetime.datetime.now()
options = webdriver.ChromeOptions()
options.add_argument('-headless')
options.add_argument('-no-sandbox')
options.add_argument('-disable-dev-shm-usage')

# fromStn = 'Stony Brook'
# toStn = 'Penn Station'
# time = '08:00 AM'

def getTrains(fromStn, toStn, time):
 
	time_split = time.split()
 
	browser = webdriver.Chrome('chromedriver',options=options)
	browser.get('http://lirr42.mta.info/index.php')
	#print(wd.page_source) # results

	from_location = browser.find_element_by_name("FromStation")
	to_location = browser.find_element_by_name("ToStation")
	web_date   = browser.find_element_by_name("RequestDate")
	web_time   = browser.find_element_by_id("RequestTime")
	ampm   = browser.find_element_by_id("RequestAMPM")

	from_location.send_keys(toStn)
	to_location.send_keys(fromStn)
	date.send_keys(str(now)[:10])
	web_time.send_keys(time_split[0])
	ampm.send_keys(time_split[1])

	submit = browser.find_element_by_name("schedules")

	submit.click()

	depart1 = browser.find_element_by_css_selector('#contentbox > div.roundCorners.push-1.span-92.pad-10 > div.span-70 > table:nth-child(6) > tbody > tr:nth-child(2) > td:nth-child(2)').text
	arrive1 = browser.find_element_by_css_selector('#contentbox > div.roundCorners.push-1.span-92.pad-10 > div.span-70 > table:nth-child(6) > tbody > tr:nth-child(2) > td:nth-child(4)').text
	transfer1 = browser.find_element_by_css_selector('#contentbox > div.roundCorners.push-1.span-92.pad-10 > div.span-70 > table:nth-child(6) > tbody > tr:nth-child(2) > td:nth-child(6)').text

	depart2 = browser.find_element_by_css_selector('#contentbox > div.roundCorners.push-1.span-92.pad-10 > div.span-70 > table:nth-child(6) > tbody > tr.bestRoute.strong > td:nth-child(2)').text
	arrive2 = browser.find_element_by_css_selector('#contentbox > div.roundCorners.push-1.span-92.pad-10 > div.span-70 > table:nth-child(6) > tbody > tr.bestRoute.strong > td:nth-child(4)').text
	transfer2 = browser.find_element_by_css_selector('#contentbox > div.roundCorners.push-1.span-92.pad-10 > div.span-70 > table:nth-child(6) > tbody > tr:nth-child(2) > td:nth-child(6)').text

	return("The following are the trains you are looking for: \n Depart at " + depart1 + ", arrive at " + arrive1 + ", transfer to " + transfer1 + "\n Depart at " + depart2 + ", arrive at " + arrive2 + ", transfer to " + transfer2)
	 
# print(getTrains(fromStn, toStn, time))