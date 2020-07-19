if msg.type == 'text':
    if msg.content == '基础架构':
        reply = TextReply(content='基础架构回复内容', message=msg)
    else:
        reply = create_reply('其他文本消息回复内容', message=msg)
elif msg.type == 'image':
    reply = ImageReply(message=msg)
    reply.media_id = '图片素材media_id'
elif msg.type == 'voice':
    reply = VoiceReply(message=msg)
    reply.media_id = '音频素材media_id'
else:
    reply = TextReply(content='其他消息类型的回复内容', message=msg)
response = HttpResponse(reply.render(), content_type="application/xml")
return response