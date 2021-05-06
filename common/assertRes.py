import re
import json
import requests
# 断言数据

def assertRes(expect, obj):
    flag = False
    assertRetList = []
    expectList = expect.split('\n')

    for i in expectList:
        expectDict = json.loads(i)
        tempDict = {}
        for key in expectDict:
            value = eval(key)
            tempDict[key] = value
            if not isinstance(expectDict[key], str):
                if value != expectDict[key]:
                    break
            else:
                ret = re.search(expectDict[key], str(value))[0]
                if not ret:
                    break
        else:
            flag = True
        assertRetList.append(json.dumps(tempDict))
        if flag:
            break
    return '\n'.join(assertRetList), 'Pass' if flag else 'Fail'


if __name__ == '__main__':
    method = 'get'
    url = 'http://api.nnzhp.cn/api/user/stu_info'
    params = {"stu_name":"小黑"}
    res = requests.request(method=method, url=url, params=params)

    expect = '''{"obj.json()['stu_info'][1]['phone']":"\\\\d*"}'''
    ret = assertRes(expect, res)
    print(ret)