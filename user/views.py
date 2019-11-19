from django.shortcuts import render
from utils.common import *
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from io import BytesIO
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from user import models


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
        ret_val.error = True
        request_data = request.POST
        mobile = request_data.get('mobile', None)
        password = request_data.get('pass', None)
        re_password = request_data.get('repass', None)
        real_name = request_data.get('realname', None)
        email = request_data.get('email', None)
        imagecode = request_data.get('imagecode', None)
        vercode = request_data.get('vercode', None)
        # 参数验证
        if not mobile or not password or not re_password or not real_name or not email or not imagecode or not vercode:
            ret_val.error = True
            ret_val.message = '所有参数均为必填，请如实填写'
            ret_val.code = 2
            return JsonResponse(ret_val.dict())
        if password != re_password:
            ret_val.error = True
            ret_val.message = '两次输入密码不一致，请确认！'
            ret_val.code = 2
            return JsonResponse(ret_val.dict())
        if imagecode != request.session['ImageCode']:
            ret_val.error = True
            ret_val.message = '请输入正确的图片验证码！'
            ret_val.code = 2
            return JsonResponse(ret_val.dict())
        if not cache.has_key(email):
            ret_val.error = True
            ret_val.message = '请先获取验证码！'
            ret_val.code = 2
            return JsonResponse(ret_val.dict())
        if cache.get(email) != vercode:
            ret_val.error = True
            ret_val.message = '验证码错误，请确认！'
            ret_val.code = 2
            return JsonResponse(ret_val.dict())
        # 构建用户参数
        user_info = {
            'user_name': email,
            'password': Common.sha1_encryption(password),
            'real_name': real_name,
            'mobile': mobile,
            'email': email,
        }
        if models.UserInfo.objects.filter(user_name=email):
            ret_val.error = True
            ret_val.code = 2
            ret_val.message = '该邮箱账号已注册过，请直接登录！'
            return JsonResponse(ret_val.dict())
        if models.UserInfo.objects.create(**user_info):
            ret_val.error = False
            ret_val.code = 1
            ret_val.message = '注册成功！'
        else:
            ret_val.error = True
            ret_val.code = 2
            ret_val.message = '注册失败，请稍后再试！'
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


@require_http_methods(['POST'])
def getvercode(request):
    """
    获取验证码
    :param request:
    :return:
    """
    # 返回结果
    ret_val = ReturnValue()
    email = request.POST.get('email', None)
    img_code = request.POST.get('img_code', None)
    # 参数验证
    if not email:
        ret_val.error = True
        ret_val.code = 2
        ret_val.message = '请输入正确的邮箱！'
        return JsonResponse(ret_val.dict())
    if not img_code:
        ret_val.error = True
        ret_val.code = 2
        ret_val.message = '请输入正确的图片验证码！'
        return JsonResponse(ret_val.dict())
    if img_code != request.session['ImageCode']:
        ret_val.error = True
        ret_val.code = 2
        ret_val.message = '图片验证码错误！'
        return JsonResponse(ret_val.dict())
    # 生成随机验证码
    code = Common().get_num_code(6)
    # 邮件接收方
    mailto_list = [email]
    mail = SendEmail()
    sub = '你好：{0}'.format(code)
    email_msg = "<h1>{0}</h1><p>您正在登录【如期-项目跟踪系统】，唯一标识码是{0}，10分钟内有效。如非本人操作，可不予理会。</p>".format(code)
    if mail.sendTxtMail(mailto_list, sub, email_msg, is_html=True):
        ret_val.message = '验证码已发送至邮箱，10分钟内有效。'
        cache.set(email, code, 10 * 60)
    else:
        ret_val.error = True
        ret_val.message = '邮件发送失败'
    return JsonResponse(ret_val.dict())
