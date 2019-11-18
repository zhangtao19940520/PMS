from django.shortcuts import render
from utils.common import *
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from io import BytesIO


# Create your views here.


def index(request):
    """
    首页
    :param request:
    :return:
    """
    return render(request, 'user/index.html')


def register(request):
    """
    注册页面及操作
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'user/register.html')
    else:
        ret_val = ReturnValue()

        return JsonResponse(ret_val.dict())


def login(request):
    """
    注册页面及操作
    :param request:
    :return:
    """
    return render(request, 'user/login.html')


def getimagecode(request):
    """
    生成验证码图片
    :param request:
    :return:
    """
    stream = BytesIO()

    Vcode = ValidateCode()
    code = Vcode.getCode(4)
    img = Vcode.getCodeImage(code)
    img.save(stream, 'PNG')

    request.session['ImageCode'] = code
    return HttpResponse(stream.getvalue())
