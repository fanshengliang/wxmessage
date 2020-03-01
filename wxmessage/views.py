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
from wechatpy import parse_message, create_reply
from wechatpy.replies import ArticlesReply
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.pay import logger
from wechatpy.replies import TextReply
from wechatpy.utils import check_signature
from wechatpy import WeChatClient

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
            msg = parse_message(request.body)
            if msg.type == 'text':
                if msg.content == '基础架构':
                    reply = TextReply(content='根据您的输入，为您推荐：<br>\
                    <a href="https://mp.weixin.qq.com/s/JlsGLhwvwzhqOiGFUIib2g">漫谈传统IT基础设施01-综述</a><br>\
                    <a href="https://mp.weixin.qq.com/s/mjYAk1as2f-acc8PYynsxg">漫谈传统IT基础设施02-服务器（上）</a><br>', message=msg)
                    # 转换成 XML
                    xml = reply.render()
                elif msg.content == '服务器':
                    reply = ArticlesReply(message=msg, articles=[
                        {
                            'title': u'漫谈传统IT基础设施02-服务器（上）',
                            'description': u'用通俗的语言，从不同的角度，介绍不同种类服务器的区别。',
                            'url': u'https://mp.weixin.qq.com/s/mjYAk1as2f-acc8PYynsxg',
                            'image': 'https://mmbiz.qpic.cn/mmbiz_jpg/e4G78KtkFo9yEzLdiaD97rxevWTAAlsJqttX3q13qibVQ3ia9aEthTib0ia9nhicINIqT6gGLDrqQ71xt47yrBsVCBoA/0?wx_fmt=jpeg',
                        },
                    ])
                    # 转换成 XML
                    xml = reply.render()
                else:
                    reply = create_reply('此功能正在开发中', msg)
            elif msg.type == 'image':
                reply = ArticlesReply(message=msg, articles=[
                    {
                        'title': u'漫谈传统IT基础设施01-综述',
                        'description': u'讲人话，用最通俗的语言，介绍支撑传统互联网与移动互联网业务系统的IT基础设施。',
                        'url': u'https://mp.weixin.qq.com/s/JlsGLhwvwzhqOiGFUIib2g',
                        'image': 'https://mmbiz.qpic.cn/mmbiz_jpg/e4G78KtkFo8GMkb5R9PWzyLgyMe2xALtsK2aoCHndCWdLUgP6sqH6zlpsJB5a324UibNbIxGYibM4fsgzHP0c42A/0?wx_fmt=jpeg',
                    },
                    {
                        'title': u'漫谈传统IT基础设施02-服务器（上）',
                        'description': u'用通俗的语言，从不同的角度，介绍不同种类服务器的区别。',
                        'url': u'https://mp.weixin.qq.com/s/mjYAk1as2f-acc8PYynsxg',
                        'image': 'https://mmbiz.qpic.cn/mmbiz_jpg/e4G78KtkFo9yEzLdiaD97rxevWTAAlsJqttX3q13qibVQ3ia9aEthTib0ia9nhicINIqT6gGLDrqQ71xt47yrBsVCBoA/0?wx_fmt=jpeg',
                    },
                ])
                reply.add_article({
                    'title': u'标题3',
                    'description': u'描述3',
                    'url': u'http://www.qq.com',
                })
            elif msg.type == 'voice':
                reply = ArticlesReply(message=msg, articles=[
                    {
                        'title': u'漫谈传统IT基础设施01-综述',
                        'description': u'讲人话，用最通俗的语言，介绍支撑传统互联网与移动互联网业务系统的IT基础设施。',
                        'url': u'https://mp.weixin.qq.com/s/JlsGLhwvwzhqOiGFUIib2g',
                        'image': 'https://mmbiz.qpic.cn/mmbiz_jpg/e4G78KtkFo8GMkb5R9PWzyLgyMe2xALtsK2aoCHndCWdLUgP6sqH6zlpsJB5a324UibNbIxGYibM4fsgzHP0c42A/0?wx_fmt=jpeg',
                    },
                    {
                        'title': u'漫谈传统IT基础设施02-服务器（上）',
                        'description': u'用通俗的语言，从不同的角度，介绍不同种类服务器的区别。',
                        'url': u'https://mp.weixin.qq.com/s/mjYAk1as2f-acc8PYynsxg',
                        'image': 'https://mmbiz.qpic.cn/mmbiz_jpg/e4G78KtkFo9yEzLdiaD97rxevWTAAlsJqttX3q13qibVQ3ia9aEthTib0ia9nhicINIqT6gGLDrqQ71xt47yrBsVCBoA/0?wx_fmt=jpeg',
                    },
                ])
                reply.add_article({
                    'title': u'标题3',
                    'description': u'描述3',
                    'url': u'http://www.qq.com',
                })
                # 转换成 XML
                xml = reply.render()
            else:
                reply = ArticlesReply(message=msg, articles=[
                    {
                        'title': u'漫谈传统IT基础设施01-综述',
                        'description': u'讲人话，用最通俗的语言，介绍支撑传统互联网与移动互联网业务系统的IT基础设施。',
                        'url': u'https://mp.weixin.qq.com/s/JlsGLhwvwzhqOiGFUIib2g',
                        'image': 'https://mmbiz.qpic.cn/mmbiz_jpg/e4G78KtkFo8GMkb5R9PWzyLgyMe2xALtsK2aoCHndCWdLUgP6sqH6zlpsJB5a324UibNbIxGYibM4fsgzHP0c42A/0?wx_fmt=jpeg',
                    },
                    {
                        'title': u'漫谈传统IT基础设施02-服务器（上）',
                        'description': u'用通俗的语言，从不同的角度，介绍不同种类服务器的区别。',
                        'url': u'https://mp.weixin.qq.com/s/mjYAk1as2f-acc8PYynsxg',
                        'image': 'https://mmbiz.qpic.cn/mmbiz_jpg/e4G78KtkFo9yEzLdiaD97rxevWTAAlsJqttX3q13qibVQ3ia9aEthTib0ia9nhicINIqT6gGLDrqQ71xt47yrBsVCBoA/0?wx_fmt=jpeg',
                    },
                ])
                reply.add_article({
                    'title': u'标题3',
                    'description': u'描述3',
                    'url': u'http://www.qq.com',
                })
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
