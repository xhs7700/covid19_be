from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from . import models
import json
import urllib.request

def sina_api(request):
    data = json.load(open("data/sina.json",encoding='utf-8'))
    return JsonResponse(data,json_dumps_params={'ensure_ascii':False})

def province(request):
    data = json.load(open("data/sina.json",encoding='utf-8'))
    pro = eval(request.GET['province'])
    pro_num = 0
    for i in range(len(data['data']['list'])):
        if data['data']['list'][i]['name']==pro or data['data']['list'][i]['ename']==pro:
            pro_num = i
    dic = data['data']['list'][pro_num]
    dic.pop('hejian')
    for item in dic['city']:
        item.pop('citycode')
        item.pop('hejian')
    dic['jwsr_econNum'] = 0
    for item in dic['city']:
        if item['name']=='境外输入':
            dic['jwsr_econNum'] = item['econNum'] 
    return JsonResponse(dic,json_dumps_params={'ensure_ascii':False})  

'''    
def country(request):
    data = json.load(open("data/sina.json",encoding='utf-8'))
    country = eval(request.GET['country'])
    country_num = 0
    for i in range(len(data['data']['worldlist'])):
        if data['data']['worldlist'][i]['name']==country:
            country_num = i
    dic = data['data']['worldlist'][country_num]
    dic.pop('is_show_entrance')
    dic.pop('is_show_map')
    citycode = dic['citycode']
    data_country = json.load(open("data/country/"+citycode+".json"))
    city = data_country['data']['city']
    for i in range(len(city)):
        city[i].pop('is_show_entrance')
        city[i].pop('is_show_map')
    dic['city'] = city
    return JsonResponse(dic,json_dumps_params={'ensure_ascii':False}) 
'''

def country(request):
    citycode = eval(request.GET['code'])    
    dic = json.load(open("data/country/"+citycode+".json",encoding='utf-8'))
    return JsonResponse(dic,json_dumps_params={'ensure_ascii':False}) 
    
def overall_China(request):
    data = json.load(open("data/sina.json",encoding='utf-8'))
    dic = {}
    dic['gntotal'] = int(data['data']['gntotal'])
    dic['deathtotal'] = int(data['data']['deathtotal'])
    dic['sustotal'] = int(data['data']['sustotal'])
    dic['curetotal'] = int(data['data']['curetotal'])
    dic['econNum'] = int(data['data']['econNum'])
    dic['heconNum'] = int(data['data']['heconNum'])
    dic['jwsrNum'] = int(data['data']['jwsrNum'])
    dic['addcon'] = int(data['data']['add_daily']['addcon'])
    dic['addcure'] = int(data['data']['add_daily']['addcure'])
    dic['adddeath'] = int(data['data']['add_daily']['adddeath'])
    dic['addecon_new'] = int(data['data']['add_daily']['addecon_new'])
    dic['addsus'] = int(data['data']['add_daily']['addsus'])
    dic['addhecon_new'] = int(data['data']['add_daily']['addhecon_new'])
    dic = json.dumps(dic,ensure_ascii=False)
    response = HttpResponse(dic)
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'POST,GET,OPTIONS'
    response['Access-Control-Max-Age'] = '2000'
    response['Access-Control-Allow-Headers'] = '*'
    return response
    
def overall_world(request):
    data = json.load(open("data/sina.json",encoding='utf-8'))
    dic = data['data']['othertotal']
    return JsonResponse(dic,json_dumps_params={'ensure_ascii':False}) 
    
def province_list(request):
    data = json.load(open("data/sina.json",encoding='utf-8'))
    dic = data['data']['list']
    for i in range(len(dic)):
        dic[i].pop('city')
        dic[i].pop('hejian')
    return JsonResponse(dic,json_dumps_params={'ensure_ascii':False},safe=False) 

def country_list(request):
    data = json.load(open("data/sina.json",encoding='utf-8'))
    dic = data['data']['otherlist']
    for i in range(len(dic)):
        dic[i].pop('is_show_entrance')
        dic[i].pop('is_show_map')
    return JsonResponse(dic,json_dumps_params={'ensure_ascii':False},safe=False)     
 
def history(request):
    data = json.load(open("data/sina.json",encoding='utf-8'))
    data = data['data']['historylist']
    dic = {}
    dic['date'] = []
    dic['conadd'] = []
    dic['econNum'] = []
    dic['conNum'] = []
    dic['cureNum'] = []
    dic['deathNum'] = []
    dic['cureRate'] = []
    dic['deathRate'] = []
    n = len(data)
    for i in range(n-1,-1,-1):
        dic['date'].append(data[i]['date'])
        dic['conadd'].append(data[i]['cn_conadd'])
        dic['econNum'].append(data[i]['cn_econNum'])
        dic['conNum'].append(data[i]['cn_conNum'])
        dic['cureNum'].append(data[i]['cn_cureNum'])
        dic['deathNum'].append(data[i]['cn_deathNum'])
        dic['cureRate'].append(data[i]['cn_cureRate'])
        dic['deathRate'].append(data[i]['cn_deathRate'])
        
    data = json.load(open("data/sina.json",encoding='utf-8'))
    data = data['data']['otherhistorylist']
    dic['conaddw'] = ["0" for i in range(n)]
    dic['conNumw'] = ["0" for i in range(n)]
    dic['cureNumw'] = ["0" for i in range(n)]
    dic['deathNumw'] = ["0" for i in range(n)]
    m = len(data)
    for i in range(m):
        dic['conaddw'][n-1-i] = data[i]['certain_inc']
        dic['conNumw'][n-1-i]= data[i]['certain']
        dic['cureNumw'][n-1-i] = data[i]['recure']
        dic['deathNumw'][n-1-i] = data[i]['die']   
    dic = json.dumps(dic,ensure_ascii=False)
    response = HttpResponse(dic)
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'POST,GET,OPTIONS'
    response['Access-Control-Max-Age'] = '2000'
    response['Access-Control-Allow-Headers'] = '*'
    return response
    
def rate(request):
    data = json.load(open("data/sina.json",encoding='utf-8'))
    data = data['data']['list']
    lis = []
    for i in range(len(data)):
        dic = {}
        dic['name'] = data[i]['name']
        dic['ename'] = data[i]['ename']
        x = 100.0*float(data[i]['cureNum'])/float(data[i]['value'])
        dic['cureRate'] = format(x,'.2f')
        x = 100.0*float(data[i]['deathNum'])/float(data[i]['value'])
        dic['deathRate'] = format(x,'.2f')
        lis.append(dic)
    return JsonResponse(lis,json_dumps_params={'ensure_ascii':False},safe=False) 

def continent(request):
    data = json.load(open("data/continent_list.json",encoding='utf-8'))
    return JsonResponse(data,json_dumps_params={'ensure_ascii':False},safe=False) 
    
def scatter_diagram(request):
    data = json.load(open("data/scatter_diagram.json",encoding='utf-8'))
    dic = json.dumps(data,ensure_ascii=False)
    response = HttpResponse(dic)
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'POST,GET,OPTIONS'
    response['Access-Control-Max-Age'] = '2000'
    response['Access-Control-Allow-Headers'] = '*'
    return response
 
def news(request):
    data = json.load(open("data/news.json",encoding='utf-8'))
    dic = json.dumps(data,ensure_ascii=False)
    response = HttpResponse(dic)
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'POST,GET,OPTIONS'
    response['Access-Control-Max-Age'] = '2000'
    response['Access-Control-Allow-Headers'] = '*'
    return response
    
def rumor0(request):
    data = json.load(open("data/rumor0.json",encoding='utf-8'))
    dic = json.dumps(data,ensure_ascii=False)
    response = HttpResponse(dic)
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'POST,GET,OPTIONS'
    response['Access-Control-Max-Age'] = '2000'
    response['Access-Control-Allow-Headers'] = '*'
    return response

def rumor2(request):
    data = json.load(open("data/rumor2.json",encoding='utf-8'))
    dic = json.dumps(data,ensure_ascii=False)
    response = HttpResponse(dic)
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'POST,GET,OPTIONS'
    response['Access-Control-Max-Age'] = '2000'
    response['Access-Control-Allow-Headers'] = '*'
    return response
    
'''
with open('history_China.json','w') as f:
    json.dump(dic,f,ensure_ascii=False)
'''    
    