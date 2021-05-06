import json
from common.paramReplace import paramReplace
from requests import request
import  requests
# 请求头的设置

def httpRequest(requestData, paramDict):
    method = requestData['请求方式']
    url = paramReplace(requestData['URL地址'], paramDict)
    headers = jsonLoads(paramReplace(requestData['请求头部'], paramDict))
    cookies = jsonLoads(paramReplace(requestData['请求cookies'], paramDict))
    files = eval(requestData['请求参数/files']) if requestData['请求参数/files'] else None

    params = paramReplace(requestData['请求参数/params'], paramDict)
    data = eval(paramReplace(requestData['请求参数/data'], paramDict))if requestData['请求参数/data'] else None
    # auth = requestData['']
    # hooks = requestData['']
    jsonData = jsonLoads(paramReplace(requestData['请求参数/json'], paramDict))

    print(type(data))
    res = requests.request(method=method, url=url, headers=headers,
                   cookies=cookies, params=params, data=data,
                   json=jsonData, files=files)
    return res


def jsonLoads(data):
    '''
    对传入的数据进行判断，不为空则转为字典，为空不做操作
    :return:
    '''
    return json.loads(data) if data else None


def delNone(text):
    text = text.replace(' ', '').replace('\n', '')
    return text

