import json
import time
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
#
def gooddata_website_login(driver, project_id, username, password):
    driver.get('https://analytics.totvs.com.br/#s=/gdc/projects/'+ project_id +'|objectPage|none|metric')
    time.sleep(10)
    driver.find_element_by_xpath("//input[@id='ember894']").send_keys(username)
    driver.find_element_by_xpath("//input[@id='ember901']").send_keys(password)
    driver.find_element_by_xpath("//button[@id='ember949']").click()
    time.sleep(10)
#
def gooddata_api_login(username, password):
    login_request = requests.post('https://analytics.totvs.com.br/gdc/account/login'
                                  , headers={'Accept':'application/json', 'Content-type':'application/json'} 
                                  ,json = {'postUserLogin':{"login": username, "password": password, "remember": 1}})
    auth_cookie = {login_request.headers['Set-Cookie'].split("; ")[0].split("=")[0] : login_request.headers['Set-Cookie'].split("; ")[0].split("=")[1]}
    return(auth_cookie)
#
def get_fact_list(auth_cookie, project_id):
    fact_api_response = requests.get('https://analytics.totvs.com.br/gdc/md/' + project_id + '/query/facts'
                                  , headers={'Accept':'application/json', 'Content-type':'application/json'} 
                                  , cookies = auth_cookie)
    fact_json = json.loads(fact_api_response.text)
    fact_dict = {}
    for element in range(0, len(fact_json['query']['entries'])):
        fact_dict[fact_json['query']['entries'][element]['title']] = fact_json['query']['entries'][element]['link']
    return(fact_dict)
#
def get_attribute_list(auth_cookie, project_id):
    attribute_api_response = requests.get('https://analytics.totvs.com.br/gdc/md/' + project_id + '/query/attributes'
                                  , headers={'Accept':'application/json', 'Content-type':'application/json'} 
                                  , cookies = auth_cookie)
    attribute_json = json.loads(attribute_api_response.text)
    attribute_dict = {}
    for element in range(0, len(attribute_json['query']['entries'])):
        attribute_dict[attribute_json['query']['entries'][element]['title']] = attribute_json['query']['entries'][element]['link']
    return(attribute_dict)
#
def get_metric_list(auth_cookie, project_id):
    metric_api_response = requests.get('https://analytics.totvs.com.br/gdc/md/' + project_id + '/query/metrics'
                                  , headers={'Accept':'application/json', 'Content-type':'application/json'} 
                                  , cookies = auth_cookie)
    metric_json = json.loads(metric_api_response.text)
    metric_dict = {}
    for element in range(0, len(metric_json['query']['entries'])):
        metric_dict[metric_json['query']['entries'][element]['title']] = metric_json['query']['entries'][element]['link']
    return(metric_dict)
#
def create_basic_metrics(driver, project_id, fact_name, fact_id):
    code_list = ['SELECT SUM ([{}])']
    for i in range(0,len(code_list)):
        time.sleep(5)
        frame_metriceditor = driver.find_element_by_xpath("//iframe[@class='metricEditorFrame']")
        driver.switch_to.frame(frame_metriceditor)
        time.sleep(5)
        tag_custommetric = driver.find_element_by_xpath("//div[@class='customMetric']")
        tag_custommetric.click()
        actions = ActionChains(driver)
        actions = actions.send_keys('KPI - {} '.format(fact_name))
        actions.perform()
        actions = actions.send_keys(Keys.TAB)
        actions.perform()
        actions = actions.send_keys(code_list[0].format(fact_id))
        actions.perform()
        tag_addmetric = driver.find_element_by_xpath("//button[@class='button editor add']")
        tag_addmetric.click()
        time.sleep(5)
        driver.get('https://analytics.totvs.com.br/#s=/gdc/projects/'+ project_id +'|objectPage|none|metric')
        time.sleep(10)
    return(0)
#
def create_month_related_metrics(driver, project_id, metric_name, metric_id, date_attribute):
    name_list = ['{} do mês anterior',
                 '{} do mês do ano anterior']
    code_list = ['SELECT [{}] FOR PREVIOUS ([{}], 1)',
                 'SELECT [{}] FOR PREVIOUS ([{}], 12)']
    for i in range(0,len(code_list)):
        time.sleep(5)
        frame_metriceditor = driver.find_element_by_xpath("//iframe[@class='metricEditorFrame']")
        driver.switch_to.frame(frame_metriceditor)
        time.sleep(10)
        tag_custommetric = driver.find_element_by_xpath("//div[@class='customMetric']")
        tag_custommetric.click()
        actions = ActionChains(driver)
        actions = actions.send_keys(name_list[i].format(metric_name))
        actions.perform()
        actions = actions.send_keys(Keys.TAB)
        actions.perform()
        actions = actions.send_keys(code_list[i].format(metric_id, date_attribute))
        actions.perform()
        tag_addmetric = driver.find_element_by_xpath("//button[@class='button editor add']")
        tag_addmetric.click()
        time.sleep(5)
        driver.get('https://analytics.totvs.com.br/#s=/gdc/projects/'+ project_id +'|objectPage|none|metric')
        time.sleep(10)
    return(0)
#
def create_percentage_metric(driver, project_id, dividend_metric, divider_metric, metric_name):
    name_list = ['KPI - % Var {}']
    code_list = ['SELECT [{}] / [{}] - 1']
    time.sleep(5)
    for i in range(0, len(code_list)):
        time.sleep(5)
        frame_metriceditor = driver.find_element_by_xpath("//iframe[@class='metricEditorFrame']")
        driver.switch_to.frame(frame_metriceditor)
        time.sleep(10)
        tag_custommetric = driver.find_element_by_xpath("//div[@class='customMetric']")
        tag_custommetric.click()
        actions = ActionChains(driver)
        actions = actions.send_keys(name_list[i].format(metric_name))
        actions.perform()
        actions = actions.send_keys(Keys.TAB)
        actions.perform()
        actions = actions.send_keys(code_list[i].format(dividend_metric, divider_metric))
        actions.perform()
        tag_addmetric = driver.find_element_by_xpath("//button[@class='button editor add']")
        tag_addmetric.click()
        time.sleep(5)
        driver.get('https://analytics.totvs.com.br/#s=/gdc/projects/' + project_id + '|objectPage|none|metric')
        time.sleep(10)
    return(0)