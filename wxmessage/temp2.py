# -*- coding: utf-8 -*-
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
import receive
import reply

# Create your views here.


#csrf_exempt装饰器是取消Django的csrf标记的，毕竟微信不会有这种标记。这次认证通过之后，这个方法你注销了都行，除非你再次认证，不然不会再使用这个方法了。
@csrf_exempt
#如果request提供，它必须是一个HttpRequest。然后，引擎必须将其以及模板中可用的CSRF令牌。

def weixin(request):
    try:
        if request.method == 'GET' and request.GET:
        #下面这四个参数是在接入时，微信的服务器发送过来的参数
            signature = request.GET.get('signature', None)
            timestamp = request.GET.get('timestamp', None)
            nonce = request.GET.get('nonce', None)
            echostr = request.GET.get('echostr', None)

            #这里的token需要自己设定，主要是和微信的服务器完成验证使用
            token = 'fanshengliang2020'

            #把token，timestamp, nonce放在一个序列中，并且按字符排序
            list = [token, timestamp, nonce]
            list.sort()
            hashstr = ''.join([s for s in list])

        # 通过python标准库中的sha1加密算法，处理上面的字符串，形成新的字符串。
            hashstr = hashlib.sha1(hashstr.encode(encoding='utf-8')).hexdigest()

            if hashstr == signature:
                return HttpResponse(echostr)
            else:
                return ""

        if request.method == 'POST':
        # 后台打日志
            webData= request.body
            print "Handle Post webdata is ", webData
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                content = "test"
                print toUser,fromUser,content
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            else:
                print "暂且不处理"
                return "success"

    except Exception, Argument:
        return Argument

    return render(request, 'wx.html')