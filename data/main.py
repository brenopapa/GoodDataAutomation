import api_lib
import web_lib
from selenium import webdriver

fact_file = open('facts.txt', 'r').read().splitlines()
#
# to do:
# excel integration
# wait until element is clickable, not wait x seconds
# exception treatment and user basic interface/text
# remove 'KPI - ' of the metric's name
# formatação da metrica
#
project_id = 's2vfuj27fr38xqyn1kt1mkfynw89hg0h'
username = 'suporte.gd@totvs.com.br'
password = 'fastanalytics'
date_attribute_name = 'Month/Year (Data)' #ler campo do arquivo facts.txt

auth_cookie = api_lib.gooddata_api_login(username, password)

driver = webdriver.Chrome(executable_path='./chromedriver/chromedriver.exe')
web_lib.gooddata_website_login(driver, project_id, username, password)

facts = api_lib.get_fact_list(auth_cookie, project_id)
attributes = api_lib.get_attribute_list(auth_cookie, project_id)
date_attribute = attributes[date_attribute_name]

for element in fact_file:
    for fact_name, fact_id in facts.items():
        if element == fact_name:
            web_lib.create_basic_metrics(driver, project_id, fact_name, fact_id)

    metrics = api_lib.get_metric_list(auth_cookie, project_id)

for metric_name, metric_id in metrics.items():
    if metric_name[0:3] == 'KPI':
        web_lib.create_month_related_metrics(driver, project_id, metric_name, metric_id, date_attribute)

metrics = api_lib.get_metric_list(auth_cookie, project_id)

for element in fact_file:
    for metric_name, metric_id in metrics.items():
        if metric_name == 'KPI - {}'.format(element):
            sum_metric_id = metric_id
        if metric_name == 'KPI - {} do mês anterior'.format(element):
            month_metric_name = metric_name
            month_metric_id = metric_id
    if sum_metric_id != '' and month_metric_id != '':
        web_lib.create_percentage_metric(driver, project_id, sum_metric_id, month_metric_id, month_metric_name)

for element in fact_file:
    for metric_name, metric_id in metrics.items():
        if metric_name == 'KPI - {}'.format(element):
            sum_metric_id = metric_id
        if metric_name == 'KPI - {} do mês do ano anterior'.format(element):
            month_metric_name = metric_name
            month_metric_id = metric_id
    if sum_metric_id != '' and month_metric_id != '':
        web_lib.create_percentage_metric(driver, project_id, sum_metric_id, month_metric_id, month_metric_name)

driver.quit()


