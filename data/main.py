import lib
from selenium import webdriver
fact_file = open('Facts.txt','r')
#
    #to do:
	#excel integration
    #wait until element is clickable, not wait x seconds
    #exception treatment and user basic interface/text
#
project_id = ''
username = ''
password = ''
date_attribute_name = ''

driver = webdriver.Chrome(executable_path='./chromedriver/chromedriver.exe')
lib.gooddata_website_login(driver, project_id, username, password)

auth_cookie = lib.gooddata_api_login(username,password)
facts = lib.get_fact_list(auth_cookie, project_id)
attributes = lib.get_attribute_list(auth_cookie, project_id)
date_attribute = attributes[date_attribute_name]

for element in fact_file.read().splitlines():
    for fact_name, fact_id in facts.items():
        if (element == fact_name):
            lib.create_basic_metrics(driver, project_id, fact_name, fact_id)

metrics = lib.get_metric_list(auth_cookie, project_id)

for metric_name, metric_id in metrics.items():
    if metric_name[0:3] == 'KPI':
       lib.create_month_related_metrics(driver, project_id, metric_name, metric_id, date_attribute)

metrics = lib.get_metric_list(auth_cookie, project_id)

for metric_name, metric_id in metrics.items():
    if metric_name[0:3] == 'KPI':
       lib.create_percentage_metric()

driver.quit()