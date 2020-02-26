# -*- coding: utf-8 -*-
from django.shortcuts import render,HttpResponse
# from django.views.decorators.csrf import csrf_exempt

import hashlib

# @csrf_exempt
# def weixin(request):
#     if request.method == "GET" and request.GET:
#         signature = request.GET.get('signature')
#         timestamp = request.GET.get('timestamp')
#         nonce = request.GET.get('nonce')
#         echostr = request.GET.get('echostr')
#         token = "fanshengliang2020"
#         tmpArr = [token,timestamp,nonce]
#         tmpArr.sort()
#         string = ''.join(tmpArr).encode('utf-8')
#         string = hashlib.sha1(string).hexdigest()
#         if string == signature:
#             return HttpResponse(echostr)
#         else:
#             return HttpResponse("false")
#     return render(request,'wx.html')

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.views.generic.base import View
from lxml import etree
from django.utils.encoding import smart_str
import hashlib
import time
from django.template.loader import render_to_string
from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.


#csrf_exempt装饰器是取消Django的csrf标记的，毕竟微信不会有这种标记。这次认证通过之后，这个方法你注销了都行，除非你再次认证，不然不会再使用这个方法了。
@csrf_exempt
#如果request提供，它必须是一个HttpRequest。然后，引擎必须将其以及模板中可用的CSRF令牌。
@ensure_csrf_cookie

def weixin(request):

    if request.method == 'GET' and request.GET:
        #下面这四个参数是在接入时，微信的服务器发送过来的参数
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)

        #这里的token需要自己设定，主要是和微信的服务器完成验证使用
        token = 'fanshengliang2020'

        #把token，timestamp, nonce放在一个序列中，并且按字符排序
        hashlist = [token, timestamp, nonce]
        hashlist.sort()

        #将上面的序列合成一个字符串
        hashstr = ''.join([s for s in hashlist])

        #通过python标准库中的sha1加密算法，处理上面的字符串，形成新的字符串。
        hashstr = hashlib.sha1(hashstr.encode(encoding='utf-8')).hexdigest()

        #把我们生成的字符串和微信服务器发送过来的字符串比较，
        #如果相同，就把服务器发过来的echostr字符串返回去
        if hashstr == signature:
          return HttpResponse(echostr)

    if request.method == 'POST' and request.POST:
        #将程序中字符输出到非 Unicode 环境（比如 HTTP 协议数据）时可以使用 smart_str 方法
        data = smart_str(request.body)
        print(data)
        #将接收到数据字符串转成xml
        xml = etree.fromstring(data)

        #从xml中读取我们需要的数据。注意这里使用了from接收的to，使用to接收了from，
        #这是因为一会我们还要用这些数据来返回消息，这样一会使用看起来更符合逻辑关系
        fromUser = xml.find('ToUserName').text
        toUser = xml.find('FromUserName').text
        msgType = xml.find('MsgType').text

        #这里获取当前时间的秒数，time.time()取得的数字是浮点数，所以有了下面的操作
        nowtime = str(int(time.time()))

        #加载text.xml模板,参见render()调用render_to_string()并将结果馈送到 HttpResponse适合从视图返回的快捷方式 。
        if msgType =='text':
            content = xml.find('Content').text
            rendered = render_to_string('wechat/text.xml',{'toUser': toUser,'fromUser': fromUser,'nowtime': nowtime,'content': '文本消息，功能正在开发中'})
            return HttpResponse(rendered)
        if msgType =='image':
            rendered = render_to_string('wechat/text.xml',{'toUser': toUser,'fromUser': fromUser,'nowtime': nowtime,'content': '图片消息，功能正在开发中'})
            return HttpResponse(rendered)
        if msgType =='voice':
            rendered = render_to_string('wechat/text.xml',{'toUser': toUser,'fromUser': fromUser,'nowtime': nowtime,'content': '语音消息，功能正在开发中'})
            return HttpResponse(rendered)
        if msgType =='video':
            rendered = render_to_string('wechat/text.xml',{'toUser': toUser,'fromUser': fromUser,'nowtime': nowtime,'content': '视频消息，功能正在开发中'})
            return HttpResponse(rendered)
        if msgType =='shortvideo':
            rendered = render_to_string('wechat/text.xml',{'toUser': toUser,'fromUser': fromUser,'nowtime': nowtime,'content': '小视频消息，功能正在开发中'})
            return HttpResponse(rendered)
        if msgType =='location':
            rendered = render_to_string('wechat/text.xml',{'toUser': toUser,'fromUser': fromUser,'nowtime': nowtime,'content': '地理位置消息，功能正在开发中'})
            return HttpResponse(rendered)
        if msgType =='link':
            rendered = render_to_string('wechat/text.xml',{'toUser': toUser,'fromUser': fromUser,'nowtime': nowtime,'content': '链接消息，功能正在开发中'})
            return HttpResponse(rendered)

    return render(request, 'wx.html')