# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def weixin(request):
    if request.method == 'POST':
        webData = request.body
        print webData
    return render(request,'wx.html')