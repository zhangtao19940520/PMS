from django.shortcuts import render, redirect
from utils.common import *
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from io import BytesIO
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from user import models
from django.db.models import Q
from utils.authorize import check_login
from utils import enums


# Create your views here.

@check_login
def index(request):
    """
    首页
    :param request:
    :return:
    """
    # 从session中获取登录邮箱
    user_info_email = request.session.get('user_info')
    user_info = models.UserInfo.objects.filter(email=user_info_email).first()
    return render(request, 'user/index.html', {
        'user_info': user_info,
        'TechnologyStack': [{'id': i[0], 'name': i[1]} for i in enums.TechnologyStack],
        'user_technology_stack': [int(i) for i in user_info.technology_stack.split(',')]
    })


@check_login
@require_http_methods(['POST'])
def edit_user(request):
    """
    修改个人资料
    :return:
    """
    user_info_email = request.session.get('user_info')
    ret_val = ReturnValue()
    post_data = request.POST
    user_info_edit = {
        'mobile': post_data.get('mobile', ''),
        'real_name': post_data.get('real_name', ''),
        'user_sex': post_data.get('user_sex', 1),
        'alipay_account': post_data.get('alipay_account', ''),
        'technology_stack': post_data.get('technology_stack', ''),
    }
    if models.UserInfo.objects.filter(email=user_info_email).update(**user_info_edit):
        ret_val.message = '用户信息修改成功！'
    else:
        ret_val.error = True
        ret_val.code = 2
        ret_val.message = '用户信息修改失败，请稍后再试。'
    return JsonResponse(ret_val.dict())


@check_login
@require_http_methods(['POST'])
def edit_user_header(request):
    """
    修改头像
    :return:
    """
    user_info_email = request.session.get('user_info')
    ret_val = ReturnValue()
    post_data = request.POST
    new_header = post_data.get('header_avatar', '/static/images/header_avatar.jpg')
    if models.UserInfo.objects.filter(email=user_info_email).update(header_avatar=new_header):
        # 修改session中的头像
        user_info = request.session['user_info']
        user_info.header_avatar = new_header
        request.session['user_info'] = user_info
        ret_val.message = '头像修改成功！'
    else:
        ret_val.error = True
        ret_val.code = 2
        ret_val.message = '头像修改失败，请稍后再试。'
    return JsonResponse(ret_val.dict())


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
        if models.UserInfo.objects.filter(email=email):
            ret_val.error = True
            ret_val.code = 2
            ret_val.message = '该邮箱账号已注册过，请直接登录！'
            return JsonResponse(ret_val.dict())
        # if models.UserInfo.objects.filter(mobile=mobile):
        #     ret_val.error = True
        #     ret_val.code = 2
        #     ret_val.message = '该手机号已注册过，请直接登录！'
        #     return JsonResponse(ret_val.dict())
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
    if request.method == 'GET':
        return render(request, 'user/login.html', {'loginName': request.COOKIES.get('loginName', '')})
    else:
        ret_val = ReturnValue()
        post_data = request.POST
        # 获取参数
        email_or_mobile = post_data.get('loginName', None)
        passwd = post_data.get('pass', None)
        img_code = post_data.get('imagecode', None)
        remember = post_data.get('remember', None)
        # 参数验证
        if not email_or_mobile or not passwd or not img_code:
            ret_val.error = True
            ret_val.message = '所有参数均为必填，请如实填写'
            ret_val.code = 2
            return JsonResponse(ret_val.dict())
        if img_code != request.session['ImageCode']:
            ret_val.error = True
            ret_val.message = '请输入正确的图片验证码！'
            ret_val.code = 2
            return JsonResponse(ret_val.dict())
        # 获取用户信息
        # user_info = models.UserInfo.objects.filter(Q(email=email_or_mobile) | Q(mobile=email_or_mobile)).first()
        user_info = models.UserInfo.objects.filter(email=email_or_mobile).first()
        if not user_info:
            ret_val.error = True
            ret_val.code = 2
            ret_val.message = '该邮箱不存在，请确认！'
            return JsonResponse(ret_val.dict())
        if user_info.password != Common.sha1_encryption(passwd):
            ret_val.error = True
            ret_val.code = 2
            ret_val.message = '登录密码错误，请确认！'
            return JsonResponse(ret_val.dict())

        ret_val.error = False
        ret_val.code = 1
        ret_val.message = '登录成功！'
        res = JsonResponse(ret_val.dict())
        # 保存用户名到cookie
        if remember == 'on':
            res.set_cookie("loginName", email_or_mobile)
        else:
            res.set_cookie("loginName", '')
        # 保存用户信息到session
        request.session['user_info'] = user_info
        return res


def logout(request):
    """
    注销
    :param request:
    :return:
    """
    request.session.clear()

    return redirect('/user/login')


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
    email_msg = "<h1>{0}</h1><p>您正在操作【如期-项目跟踪系统】，唯一标识码是{0}，10分钟内有效。如非本人操作，可不予理会。</p>".format(code)
    if mail.sendTxtMail(mailto_list, sub, email_msg, is_html=True):
        ret_val.message = '验证码已发送至邮箱，10分钟内有效。'
        cache.set(email, code, 10 * 60)
    else:
        ret_val.error = True
        ret_val.message = '邮件发送失败'
    return JsonResponse(ret_val.dict())


def terms(request):
    """
    用户条款
    :param request:
    :return:
    """
    return render(request, 'user/terms.html')


def forget(request):
    """
    忘记密码
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'user/forget.html')
    else:
        ret_val = ReturnValue()
        # 初始默认返回错误
        ret_val.error = True
        ret_val.code = 2
        # 请求数据
        request_data = request.POST
        email = request_data.get('email', None)
        imagecode = request_data.get('imagecode', None)
        vercode = request_data.get('vercode', None)
        # 参数验证
        if not email or not imagecode or not vercode:
            ret_val.message = '所有参数均为必填，请如实填写'
            return JsonResponse(ret_val.dict())
        if imagecode != request.session['ImageCode']:
            ret_val.message = '请输入正确的图片验证码！'
            return JsonResponse(ret_val.dict())
        if not cache.has_key(email):
            ret_val.message = '请先获取验证码！'
            return JsonResponse(ret_val.dict())
        if cache.get(email) != vercode:
            ret_val.message = '验证码错误，请确认！'
            return JsonResponse(ret_val.dict())
        user_info = models.UserInfo.objects.filter(email=email).first()
        if not user_info:
            ret_val.message = '该邮箱不存在，请先注册！'
            return JsonResponse(ret_val.dict())
        else:
            # new_pas = Common().get_num_code(6)
            new_pas = ValidateCode().getCode(8)
            if models.UserInfo.objects.filter(email=email).update(password=Common.sha1_encryption(new_pas)):
                mailto_list = [email]
                mail = SendEmail()
                sub = '您好：{0}'.format(new_pas)
                email_msg = '<h1>{0}</h1>您的【如期-项目跟踪系统】的登录密码已经重置为：{0}。请尽快登录用户中心更改密码！'.format(new_pas)
                if mail.sendTxtMail(mailto_list, sub, email_msg, is_html=True):
                    ret_val.error = False
                    ret_val.code = 1
                    ret_val.message = '密码重置成功，临时密码【{0}】已发送至邮箱！请尽快登录用户中心进行修改！'.format(new_pas)
                else:
                    ret_val.message = '系统异常，请稍后重试。'
            else:
                ret_val.message = '密码重置失败，请稍后再试。'
        return JsonResponse(ret_val.dict())
