# -*- coding: utf-8 -*-

# 正则把配置文件的URL遍历出来
import re

def paramReplace(content, paramDict):
    if content:
        ret = re.findall('\$\{.*?\}', content)
        if ret:
            for i in ret:
                value = paramDict[i]
                content = content.replace(i, value)

    return content


def getDate():
    pass

def getNumber():
    pass