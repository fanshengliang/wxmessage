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
from wechatpy.replies import ImageReply
from wechatpy.replies import VoiceReply
from wechatpy import events

from wechatpy import parse_message
from wechatpy.crypto import WeChatCrypto
from wechatpy.exceptions import InvalidSignatureException, InvalidAppIdException



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
                    reply = TextReply(content='根据您的输入，为您推荐：\n'
                                              '<a href="https://mp.weixin.qq.com/s/hM8wRsFAL4qDCFlKhQsIGQ">1、漫谈传统IT基础设施01-综述</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/KCV2EbjG2xXd1hdUr6RVPw">2、漫谈传统IT基础设施02-服务器（上）</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/PL0F6rEmkw3QSFJfDx39Lw">3、漫谈传统IT基础设施03-服务器（中）</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/5KqvggkdmG5vhSW_-K-iiA">4、漫谈传统传统IT基础设施04-服务器（下）</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/_ye4rfENEVeGFyWWERhuzg">5、漫谈传统IT基础设施05-网络（上）</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/FY0FBS0mC7idKV2CSbPCRQ">6、漫谈传统IT基础设施06-网络（下）</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/jJfrXpEHBQR25gjdlR4Iog">7、漫谈传统IT基础设施07-存储（01）</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/Nwk_E-gzXvoz4b4LULfmgw">8、漫谈传统IT基础设施08-存储（02）</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/b8AxVdV5yaZXWKPcYxh_4A">9、漫谈传统IT基础设施09-存储（03）</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/dz17sM32G1SkKRBid4rw8A">10、漫谈传统IT基础设施10-存储（04）</a>',
                                              message = msg)
                    # 转换成 XML
                    xml = reply.render()
                elif msg.content == '服务器':
                    reply = TextReply(content='根据您的输入，为您推荐：\n'
                                              '<a href="https://mp.weixin.qq.com/s/KCV2EbjG2xXd1hdUr6RVPw">1、漫谈传统IT基础设施02-服务器（上）</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/PL0F6rEmkw3QSFJfDx39Lw">2、漫谈传统IT基础设施03-服务器（中）</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/5KqvggkdmG5vhSW_-K-iiA">3、漫谈传统传统IT基础设施04-服务器（下）</a>', message=msg)
                    # 转换成 XML
                    xml = reply.render()
                elif msg.content == '综述':
                    reply = ArticlesReply(message=msg, articles=[
                        {
                            'title': u'漫谈传统IT基础设施01-综述',
                            'description': u'讲人话，用最通俗的语言，介绍支撑传统互联网与移动互联网业务系统的IT基础设施。',
                            'url': u'https://mp.weixin.qq.com/s/hM8wRsFAL4qDCFlKhQsIGQ',
                            'image': 'https://mmbiz.qpic.cn/mmbiz_jpg/e4G78KtkFo8GMkb5R9PWzyLgyMe2xALtsK2aoCHndCWdLUgP6sqH6zlpsJB5a324UibNbIxGYibM4fsgzHP0c42A/0?wx_fmt=jpeg',
                        },
                    ])
                elif msg.content == '网络':
                    reply = TextReply(content='根据您的输入，为您推荐：\n'
                                              '<a href="https://mp.weixin.qq.com/s/_ye4rfENEVeGFyWWERhuzg">1、漫谈传统IT基础设施05-网络（上）</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/FY0FBS0mC7idKV2CSbPCRQ">2、漫谈传统IT基础设施06-网络（下）</a>',
                                      message=msg)
                    # 转换成 XML
                    xml = reply.render()
                elif msg.content == '存储':
                    reply = TextReply(content='根据您的输入，为您推荐：\n'
                                              '<a href="https://mp.weixin.qq.com/s/jJfrXpEHBQR25gjdlR4Iog">1、漫谈传统IT基础设施07-存储（01）</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/Nwk_E-gzXvoz4b4LULfmgw">2、漫谈传统IT基础设施08-存储（02）</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/b8AxVdV5yaZXWKPcYxh_4A">3、漫谈传统IT基础设施09-存储（03）</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/dz17sM32G1SkKRBid4rw8A">4、漫谈传统IT基础设施10-存储（04）</a>',
                                      message=msg)
                    # 转换成 XML
                    xml = reply.render()
                elif msg.content == '云计算':
                    reply = TextReply(content='根据您的输入，为您推荐：\n'
                                              '<a href="https://mp.weixin.qq.com/s/WTM1b2HiGgWtcXDt1QpQCw">1、漫谈云计算IT基础设施01-综述</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/Sfy6HEQt-V-KT9JxEEaDqA">2、漫谈云计算IT基础设施02-计算虚拟化</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/vTybXVmdlloddzGtFhsc6g">3、漫谈云计算IT基础设施03-网络虚拟化</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/xnQDw11Jc7OIUB28kOKFBw">4、漫谈云计算IT基础设施03-存储虚拟化</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/Mr5CQePXaIBhZexTxKQLlg">5、漫谈云计算IT基础设施03-超融合技术</a>\n',

                                      message=msg)
                    # 转换成 XML
                    xml = reply.render()
                elif msg.content == '动手折腾':
                    reply = TextReply(content='根据您的输入，为您推荐：\n'
                                              '<a href="https://mp.weixin.qq.com/s/EdrZRuWbotU9zDJ03b1qdA">1、心意大于价值的女神节礼物</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/mPGiSepN0SvI122YPlukVQ">2、比闪电侠还快~3分钟完成个人博客搭建</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/eg0Mm2pbzwNyG5PwY6br4A">3、人云亦云~我的博客也上云</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/zWphnZmNO63clnTaG2flRw">4、VMware Workstation安装</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/DMXD2GjZ-QfreVYI1Z2M_g">5、愚公移山~纯手工Lamp搭建Wordpress个人博客</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/JWA0rMCWehfUeB0Ri0y9OQ">6、公有云PaaS服务搭建WordPress个人博客</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/SaCT_zPvZocNsG4gglEq9Q">7、公有云Docker服务搭建WordPress个人博客</a>\n',
                                      message=msg)
                    # 转换成 XML
                    xml = reply.render()
                elif msg.content == 'Linux':
                    reply = TextReply(content='根据您的输入，为您推荐：\n'
                                              '<a href="https://mp.weixin.qq.com/s/Bywqau7Nnkedm7ilJGJ9UQ">1、Linux操作系统01-CentOS6安装</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/0TGW93elSEqs3YgdIMsdYA">2、Linux操作系统02-CentOS7安装</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/HQDriEnHc2dScCshZssnCA">3、Linux操作系统03-Linux常用命令</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/-oxwNP3uFLToOrENfWq65Q">4、Linux操作系统04-配置yum源</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/phHzApogEMD_UffHCh41MQ">5、Linux操作系统05-Mysql5.7安装</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/CTvIP0gprLATTiy7ZqoqoA">6、Linux操作系统06-用tomcat搭建仿京东风格电商网站</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/4p-V6Z0MRa8pbVTcdeopgw">7、Linux操作系统07-zabbix3.4监控系统安装</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/F_A0HJbsQMOhy5eqiM6f0g">8、Linux操作系统08-zabbix3.4监控系统使用</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/vpD2ZWsM1fhRXz5edZJjDg">9、Linux操作系统09-快速搭建SMTP邮箱</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/QY-elLrNycwWZqa6oVBcyw">10、Linux操作系统10-搭建SMB/FTP/NFS文件共享服务</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/TW_FEe4S9iD82KP8s6QVIA">11、Linux操作系统11-安装VNC图形化界面远程管理</a>\n',
                                      message=msg)
                elif msg.content == '高可用' or msg.content == '容灾':
                    reply = TextReply(content='根据您的输入，为您推荐：\n'
                                              '<a href="https://mp.weixin.qq.com/s/DBzEyuQWwkRqNze-OF9NKw">1、业务系统容灾高可用系列01-高可用及负载均衡综述</a>\n',
                                      message=msg)
                elif msg.content == 'DevOps':
                    reply = TextReply(content='根据您的输入，为您推荐：\n'
                                              '<a href="https://mp.weixin.qq.com/s/flUaCWtZ0FFHtxOufEku2A">1、一起DevOps系列01-Python与Django安装</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/x80_IXSW6ThhgNRKwZEYMA">2、一起DevOps系列02-Django完整开发环境部署</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/mzchDcrh8SAWAsAUODsnxA">3、一起DevOps系列03-Django初始配置与第一个网页</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/PKk04gDOV31zINP4NAeHsw">4、一起DevOps系列04-HTML静态页面开发</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/KsI-_bO6thO0rjCmn8j8Mg">5、一起DevOps系列05-CSS开发Django导航Base页</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/opIvB3eKyf98wM8EyQiu5A">6、一起DevOps系列06-非BASE导航页的开发</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/ZAlI5VUKzyYkMoVmJPNL3g">7、一起DevOps系列07-前后端的数据交互</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/HQDriEnHc2dScCshZssnCA">8、一起DevOps系列08-微信公众号对接</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/82kXzi2oMN7MWB4yGcZnsQ">9、一起DevOps系列09-数据库的基本原理与介绍</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/DSby6TARwpPPNGro5MDDuw">10、一起DevOps系列10-数据库设计与开发的范式</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/E9txUnaFcxzqll3RlbtZCw">11、一起DevOps系列11-数据库基本SQL命令</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/lSxdbLsFSeqSwsWQv_sF8w">12、一起DevOps系列12-django数据库创建与使用</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/VIcLLuVWBg_LhTC5qx0GFQ">13、一起DevOps系列13-django后台管理及用户组与权限管理</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/mVlAMUTTx_aMKh5fJQRPSA">14、一起DevOps系列14-JavaScritp/JQuery前后端交互</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/9J2cfaLVDJALv7WhNf73lA">15、一起DevOps系列15-django前端展示后台数据</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/vm5RKiZybzWv4sWWyCexMQ">16、一起DevOps系列16-课程选课与退选业务逻辑添加</a>\n'
                                              '<a href="https://mp.weixin.qq.com/s/TUMGPai4ndo3IxvTh9IJDg">17、一起DevOps系列17-成绩查询与成绩录入</a>\n'
                                      ,
                                      message=msg)
                elif msg.content == '女神节礼物':
                    reply = TextReply(content='提取码：63cy',message=msg)
                    # 转换成 XML
                    xml = reply.render()
                else:
                    reply = create_reply('已收到您的留言，我会尽快回复，谢谢。\n'
                                         '输入“基础架构”、“服务器”、“网络”、“存储”、“云计算”、“动手折腾”、“Linux”、“DevOps”、“容灾”、“高可用”关键字，系统会为您自动推荐文章。', msg)
            elif msg.type == 'image':
                reply = ImageReply(message=msg)
                reply.media_id = 'rv1KVRYx5FzG8zdZIj31Bxw4LbLjpoNYwlybyiDSvdBjDYnmHqHRMqWORcsKJIiF'
                # 转换成 XML
                xml = reply.render()
            elif msg.type == 'voice':
                #仅支持AXX格式
                reply = VoiceReply(message=msg)
                reply.media_id = 'b7jKLKqmmZmSAi9FteOFjwi3Xfh-V3SmQSxU7Tj633TelviHPieQ6yyF6-qB_lPV'
                # 转换成 XML
                xml = reply.render()
            else:
                reply = TextReply(content='已收到您的留言，我会尽快回复，谢谢。\n'
                                          '输入“基础架构”、“服务器”、“网络”、“存储”、“云计算”、“动手折腾”、“Linux”、“DevOps”、“容灾”、“高可用”关键字，系统会为您自动推荐文章。',
                                  message=msg)
                # 转换成 XML
                xml = reply.render()
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