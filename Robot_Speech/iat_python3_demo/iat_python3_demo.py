# -*- coding: utf-8 -*-
# 语音听写 WebAPI 接口调用示例 接口文档（必看）：https://doc.xfyun.cn/rest_api/%E8%AF%AD%E9%9F%B3%E5%90%AC%E5%86%99.html
# webapi 听写服务参考帖子（必看）：http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=38947&extra=
# 语音听写WebAPI 服务，热词使用方式：登陆开放平台https://www.xfyun.cn/后，找到控制台--我的应用---语音听写---服务管理--上传热词
#（Very Important）创建完webapi应用添加听写服务之后一定要设置ip白名单，找到控制台--我的应用--设置ip白名单，如何设置参考：http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=41891
# 注意：热词只能在识别的时候会增加热词的识别权重，需要注意的是增加相应词条的识别率，但并不是绝对的，具体效果以您测试为准。
# 错误码链接：https://www.xfyun.cn/document/error-code （code返回错误码时必看）
# * @author iflytek

import requests
import time
import hashlib
import base64
import urllib

import pdb

# 听写的webapi接口地址
URL = "http://api.xfyun.cn/v1/service/v1/iat"
# 应用APPID（必须为webapi类型应用，并开通语音听写服务，参考帖子如何创建一个webapi应用：http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=36481）
APPID = "5cb43391"
# 接口密钥（webapi类型应用开通听写服务后，控制台--我的应用---语音听写---相应服务的apikey）
API_KEY = "9cc007416b70c7c1957df355eb10051d"

FILE_NAME = "iat_wav_16k.wav"

def getHeader(aue, engineType):
    curTime = str(int(time.time()))
    # curTime = '1526542623'
    param = "{\"aue\":\"" + aue + "\"" + ",\"engine_type\":\"" + engineType + "\"}"
    print("param:{}".format(param))
    paramBase64 = str(base64.b64encode(param.encode("utf-8")), "utf-8")
    print("x_param:{}".format(paramBase64))
    m2 = hashlib.md5()
    m2.update((API_KEY + curTime + paramBase64).encode("utf-8"))
    checkSum = m2.hexdigest()
    print("checkSum:{}".format(checkSum))
    # http请求头
    header = {
        "X-CurTime": curTime,
        'X-Param': paramBase64,
        'X-Appid': APPID,
        'X-CheckSum': checkSum,
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    print(header)
    return header


def getBody(filepath):
    binfile = open(filepath, 'rb')
    data = {'audio': base64.b64encode(binfile.read())}
    print(data)
    print('data:{}'.format(type(data['audio'])))
    # print("type(data['audio']):{}".format(type(data['audio'])))
    return data
#  音频编码
aue = "raw"
#  引擎类型
# （听写服务：engine_type为识别引擎类型，开通webapi听写服务后默认识别普通话与英文：示例音频请在听写接口文档底部下载
#  sms16k（16k采样率、16bit普通话音频、单声道、pcm或者wav）
#  sms8k（8k采样率、16bit普通话音频、单声道、pcm或者wav） 
#  sms-en16k（16k采样率，16bit英语音频，单声道，pcm或者wav）
#  sms-en8k（8k采样率，16bit英语音频，单声道，pcm或者wav）
#  请使用cool edit Pro软件查看音频格式是否满足相应的识别引擎类型，不满足则识别为空（即返回的data为空，code为0），或者识别为错误文本）
#  音频格式转换可参考（讯飞开放平台语音识别音频文件格式说明）：https://doc.xfyun.cn/rest_api/%E9%9F%B3%E9%A2%91%E6%A0%BC%E5%BC%8F%E8%AF%
engineType = "sms16k"
# 音频文件地址,示例音频请在听写接口文档底部下载
audioFilePath = FILE_NAME
r = requests.post(URL, headers=getHeader(aue, engineType), data=getBody(audioFilePath))
pdb.set_trace()
# print(r.content.decode('utf-8'))

print("Done.")
