from common.DataHandle import DataHandle
from common.httpHandle import httpRequest
from common.assertRes import assertRes
from common.getParam import getParam
from common.logger import logger
import json
from urllib.parse import unquote
from common.getRootPath import rootPath
import threading
import os
import time
from configparser import ConfigParser

# 解决ConfigParser大小写问题
class MyConfigParser(ConfigParser):

    def __init__(self, defaults=None):
        ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr


def readConfig():
    filePath = fr'{rootPath}\config\param.ini'
    conf = MyConfigParser()
    conf.read(filePath, encoding='utf-8')
    tempDict = {}
    for i in conf['default']:
        tempDict[i] = conf['default'][i]
    return tempDict



def runTest(dataHand):
    log = logger(dataHand.testResultDataDir)
    testData = dataHand.getTestData()
    leng = len(testData)
    paramDict = readConfig()
    for index,i in enumerate(testData):
        res = httpRequest(i, paramDict)

        ret = assertRes(i['断言/表达式'], res)

        getRet = {}
        if i['参数提取/表达式']:
            getRet = getParam(i['参数提取/表达式'], res)
            paramDict.update(getRet)


        log.info('\n{}\n{}\n{}\n\n{}\n{}\n\n'.format(
            f'╭─ 用例{i["用例编号"]}{"─"*14}request begin{"─"*13}{index+1}/{leng} ─╮',
            f'{res.request.method}  {unquote(res.url)}',
            '\n'.join('{}: {}'.format(k, v) for k, v in res.request.headers.items()),
            type(res.request.body),
            f'╰─ {res.status_code}{"─"*16}request end{"─"*14}{ret[1]} ─╯'
        ))

        row = i['用例编号']+2

        list = [
            [row, dataHand.data[0].index('实际(返回)结果')+1, res.text],
            [row, dataHand.data[0].index('接口耗时(s)')+1, int(res.elapsed.total_seconds()*1000)/1000],
            [row, dataHand.data[1].index('参考结果')+1, ret[0]],
            [row, dataHand.data[0].index('测试结果')+1, ret[1]],
            [row, dataHand.data[1].index('提取结果')+1, json.dumps(getRet) if getRet else None]
        ]
        dataHand.writeData(list)


# 获取数据地址
testDataDir = fr'{rootPath}\testData'
# 存放数据地址
testResultDir = fr'{rootPath}\testResult'

testDataFileName = []
for root, dirs, files in os.walk(testDataDir):
    testDataFileName = files

testResultDataDir = []
for i in testDataFileName:
    yearMonth = time.strftime('%Y%m', time.localtime())
    day = time.strftime('%d', time.localtime())
    hms = time.strftime('%H%M%S', time.localtime())
    dir = fr'{testResultDir}\{i.split(".")[0]}\{yearMonth}\{day}\{hms}'
    testResultDataDir.append(dir)
    os.makedirs(dir)


threads = []
for i in range(len(testDataFileName)):
    testDataFilePath = fr'{testDataDir}\{testDataFileName[i]}'
    t = threading.Thread(target=runTest, args=(DataHandle(testDataFilePath,testResultDataDir[i]),))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
os.system('pause')