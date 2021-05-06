# -*- coding: utf-8 -*-


import json


def getParam(rule, obj):
    getRet = json.loads(rule)
    for key in getRet:
        getRet[key] = str(eval(getRet[key]))


    return getRet
    print(getRet[key])