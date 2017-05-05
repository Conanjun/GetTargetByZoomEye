# coding: utf-8
# author: Conan
# datetime: 2017/5/5

import os
import requests
import json
from getpass import getpass
from urllib import urlencode

access_token = ''
ip_list = []
max_page = 20
query = ''


def login():
    user = raw_input('[-] input : username :')
    passwd = getpass('[-] input : password :')
    data = {
        'username': user,
        'password': passwd
    }
    data_encoded = json.dumps(data)
    try:
        r = requests.post(url='https://api.zoomeye.org/user/login', data=data_encoded)
        r_decoded = json.loads(r.text)
        global access_token
        access_token = r_decoded['access_token']
    except Exception, e:
        print '[-] info : username or password is wrong, please try again '
        exit()


def saveStrToFile(file, str):
    with open(file, 'w') as output:
        output.write(str)


def saveListToFile(file, list):
    s = '\n'.join(list)
    with open(file, 'w') as output:
        output.write(s)


def setQuery():
    global query
    query = raw_input('[-] query: ')


def apiTest():
    page = 1
    total = None
    global access_token
    with open('access_token.txt', 'r') as input:
        access_token = input.read()
    # 将 token 格式化并添加到 HTTP Header 中
    headers = {
        'Authorization': 'JWT ' + access_token,
    }
    # print headers
    while (True):
        try:
            temp_data = {
                'query': query,
                'facet': 'app,os',
                'page': str(page)
            }
            r = requests.get(url='http://api.zoomeye.org/host/search?' + urlencode(temp_data), headers=headers)
            r_decoded = json.loads(r.text)
            # print r_decoded['matches']
            for x in r_decoded['matches']:
                print x['ip']+':'+str(x['portinfo']['port'])
                ip_list.append(x['ip']+':'+str(x['portinfo']['port']))
                # print '[-] info : count ' + str(page * 10)

        except Exception, e:
            # 若搜索请求超过 API 允许的最大条目限制 或者 全部搜索结束，则终止请求
            if str(e.message) == 'matches':
                print '[-] info : account was break, excceeding the max limitations'
                break
            else:
                print  '[-] info : ' + str(e.message)
        if page == max_page:
            break
        page += 1


def main():
    # 访问口令文件不存在则进行登录操作
    if not os.path.isfile('access_token.txt'):
        print '[-] info : access_token file is not exist, please login'
        login()
        saveStrToFile('access_token.txt', access_token)

    setQuery()
    apiTest()
    saveListToFile('ip_list.txt', ip_list)


if __name__ == '__main__':
    main()
