import json
import requests
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