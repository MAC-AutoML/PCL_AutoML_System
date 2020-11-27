import os
import sys

#这个文件拿来定义一些请求包的通用结构

def Parser(data:dict,errcode:str="1001",errmessage:str="error message"):
    MESSAGE={
        "success": "true",
        "data": data,
        "errorCode":errcode,
        "errorMessage": errmessage,
        }
    return MESSAGE
def errParser(errcode:int=1001,errmessage:str="error message"):
    MESSAGE={
    "success": "false",
    "data": {},
    "errorCode":str(errcode),
    "errorMessage": errmessage,
    }
    return MESSAGE
    
