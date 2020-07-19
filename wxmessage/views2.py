# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import hashlib
from wechatpy import parse_message, create_reply
from wechatpy.replies import ArticlesReply
from wechatpy.replies import TextReply
from wechatpy import WeChatClient
from wechatpy.replies import ImageReply
from wechatpy.replies import VoiceReply

# Create your views here.
#csrf_exempt装饰器是取消Django的csrf标记的，毕竟微信不会有这种标记。这次认证通过之后，这个方法你注销了都行，除非你再次认证，不然不会再使用这个方法了。
@csrf_exempt
#如果request提供，它必须是一个HttpRequest。然后，引擎必须将其以及模板中可用的CSRF令牌。
@csrf_exempt
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
            msg = parse_message(request.body)
            if msg.type == 'text':
                if msg.content == '基础架构':
                    reply = TextReply(content='基础架构回复内容',message = msg)
                else:
                    reply = create_reply('其他文本消息回复内容',message = msg)
            elif msg.type == 'image':
                reply = ImageReply(message=msg)
                reply.media_id = '图片素材media_id'
            elif msg.type == 'voice':
                reply = VoiceReply(message=msg)
                reply.media_id = '音频素材media_id'
            else:
                reply = TextReply(content='其他消息类型的回复内容',message=msg)
            response = HttpResponse(reply.render(), content_type="application/xml")
            return response

    except Exception, Argument:
        return Argument
    return render(request, 'wx.html')

def create_menu(request):
    client = WeChatClient("wxfd99820aaa79b8ae", "a82ca1787197371ef415a503dbe30f68")
    client.menu.create({
        "button": [
            {
                "type": "click",
                "name": "原创文章",
                "key": "V1001_TODAY_MUSIC"
            },
            {
                "type": "click",
                "name": "转载新闻",
                "key": "V1001_TODAY_SINGER"
            },
            {
                "name": "菜单",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "搜索",
                        "url": "http://www.soso.com/"
                    },
                    {
                        "type": "view",
                        "name": "联系我们",
                        "url": "http://v.qq.com/"
                    },
                ]
            }
        ]
    })
    return HttpResponse('ok')
    # return render(request, 'create_menu.html')


def test(request):
    user = "usertest"
    passwd="passwordtest"
    data = {
        'user':user,
        'passwd':passwd,
    }
    return render(request,'test.html',locals())

def test(request):
    if request.method == 'POST' and request.POST:
        user = request.POST['username']
        passwd = request.POST['password']
        print user,passwd
    return render(request,'test.html')