import lib
from selenium import webdriver
fact_file = open('facts.txt','r').read().splitlines()
#
    #to do:
	#excel integration
    #wait until element is clickable, not wait x seconds
    #exception treatment and user basic interface/text
#
project_id = 'yr2dq0d2i93sc04hx6t6uo91ww809qch'
username = 'suporte.gd@totvs.com.br'
password = 'fastanalytics'
date_attribute_name = 'Month/Year (Data)'

auth_cookie = lib.gooddata_api_login(username,password)

if False:
    driver = webdriver.Chrome(executable_path='./chromedriver/chromedriver.exe')
    lib.gooddata_website_login(driver, project_id, username, password)
    

    facts = lib.get_fact_list(auth_cookie, project_id)
    attributes = lib.get_attribute_list(auth_cookie, project_id)
    date_attribute = attributes[date_attribute_name]
    
    for element in fact_file:
        for fact_name, fact_id in facts.items():
            if (element == fact_name):
                lib.create_basic_metrics(driver, project_id, fact_name, fact_id)
    
    metrics = lib.get_metric_list(auth_cookie, project_id)
    
    for metric_name, metric_id in metrics.items():
        if metric_name[0:3] == 'KPI':
           lib.create_month_related_metrics(driver, project_id, metric_name, metric_id, date_attribute)

metrics = lib.get_metric_list(auth_cookie, project_id)

for element in fact_file:
    for metric_name, metric_id in metrics.items():
        if metric_name == 'KPI - {}'.format(element):
            sum_metric_id = metric_id
            print(metric_name, sum_metric_id)
        if metric_name == 'KPI - {} do mês anterior'.format(element):
            month_metric_id = metric_id
            print(metric_name, month_metric_id)

for element in fact_file:
    for metric_name, metric_id in metrics.items():
        if metric_name == 'KPI - {}'.format(element):
            sum_metric_id = metric_id
            print(metric_name, sum_metric_id)
        if metric_name == 'KPI - {} do mês do ano anterior'.format(element):
            month_metric_id = metric_id
            print(metric_name, month_metric_id)
        #lib.create_percentage_metric()


#driver.quit()