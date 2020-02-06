import json
import time
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#
def gooddata_website_login(driver, project_id, username, password):
    driver.get('https://analytics.totvs.com.br/#s=/gdc/projects/'+ project_id +'|objectPage|none|metric')
    username_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='ember894']")))
    username_box.send_keys(username)
    password_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='ember901']")))
    password_box.send_keys(password)
    driver.find_element_by_xpath("//button[@id='ember949']").click()
#
def create_basic_metrics(driver, project_id, fact_name, fact_id):
    code_list = ['SELECT SUM ([{}])']
    for i in range(0,len(code_list)):
        #group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
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