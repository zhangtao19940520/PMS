from django.shortcuts import render
from utils.authorize import check_login
from utils import enums
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from utils.common import ReturnValue
from project import models
from utils import enums, common


# Create your views here.

@check_login
def market(request):
    """
    项目市场
    :param request:
    :return:
    """
    return render(request, 'project/market.html')


@check_login
def manage(request):
    """
    我的项目
    :param request:
    :return:
    """
    # 页面需要跳转的sub标签
    to_sub = request.GET.get('for', '')
    return render(request, 'project/manage.html', {
        'TechnologyStack': [{'id': i[0], 'name': i[1]} for i in enums.TechnologyStack],
        'to_sub': to_sub
    })


@check_login
def func(request):
    """
    功能开发
    :param request:
    :return:
    """
    return render(request, 'project/func.html')


@check_login
@require_http_methods(['POST'])
def create_project(request):
    """
    创建项目
    :param request:
    :return:
    """
    ret_val = ReturnValue()
    user_info = request.session.get('user_info')
    post_data = request.POST
    imagecode = post_data.get('imagecode', '')
    # 构建项目信息参数
    project_info = {
        'pj_title': post_data.get('pj_title', None),
        'pj_sub': post_data.get('pj_sub', None),
        'pj_content': post_data.get('pj_content', None),
        'pj_stack': post_data.get('pj_stack', None),
        'pj_except_fee': common.Common.str_to_int(post_data.get('pj_except_fee', None)),
        'pj_except_day': common.Common.str_to_int(post_data.get('pj_except_day', None)),
        'pj_status': common.Common.get_enum_val_by_str(enums.ProjectStatus, '已创建待审核'),
        'create_user': user_info
    }
    # 参数校验
    if not project_info['pj_title'] or not project_info['pj_content'] \
            or not project_info['pj_except_fee'] or not project_info['pj_except_day']:
        ret_val.error = True
        ret_val.message = '请输入合法的必填参数！'
        ret_val.code = 2
        return JsonResponse(ret_val.dict())
    if imagecode != request.session['ImageCode']:
        ret_val.error = True
        ret_val.message = '请输入正确的图片验证码！'
        ret_val.code = 2
        return JsonResponse(ret_val.dict())
    if models.ProjectInfo.objects.filter(pj_title=project_info['pj_title']):
        ret_val.error = True
        ret_val.message = '该项目标题已经存在！请重新换一个项目标题'
        ret_val.code = 2
        return JsonResponse(ret_val.dict())
    try:
        if models.ProjectInfo.objects.create(**project_info):
            ret_val.message = '项目创建成功，进入审核流程'
    except Exception as e:
        ret_val.error = True
        ret_val.message = '创建项目异常，请稍后再试。'
        ret_val.code = 2
        return JsonResponse(ret_val.dict())
    return JsonResponse(ret_val.dict())


@check_login
@require_http_methods(['POST'])
def update_project_delete(request):
    """
    逻辑删除创建的项目
    :param request:
    :return:
    """
    ret_val = ReturnValue()
    user_info = request.session.get('user_info')
    post_data = request.POST
    pj_id = post_data.get('pj_id', 0)
    pj_info = models.ProjectInfo.objects.filter(pj_id=pj_id, pj_is_del=False).first()
    if not pj_info:
        ret_val.error = True
        ret_val.message = '该项目不存在，请确认后再试！'
        ret_val.code = 2
        return JsonResponse(ret_val.dict())
    if pj_info.pj_status != common.Common.get_enum_val_by_str(enums.ProjectStatus, '已创建待审核'):
        ret_val.error = True
        ret_val.message = '审核通过的项目无法删除！'
        ret_val.code = 2
        return JsonResponse(ret_val.dict())
    if models.ProjectInfo.objects.filter(pj_id=pj_id).update(pj_is_del=True):
        ret_val.message = '已删除！'
    return JsonResponse(ret_val.dict())


@check_login
def search_my_create_project(request):
    """
    搜索我创建的项目
    :param request:
    :return:
    """
    ret_val = ReturnValue()
    user_info = request.session.get('user_info')
    post_data = request.POST
    my_create_projects = models.ProjectInfo.objects.filter(create_user=user_info.user_id,
                                                           pj_title__contains=post_data.get('pj_title_search', ''),
                                                           pj_is_del=False
                                                           ) \
        .order_by('-create_time').all().values("pj_id", "pj_title", "pj_sub", 'pj_content', "pj_actual_day",
                                               "pj_actual_fee", "pj_except_fee",
                                               "pj_except_day", "pj_start_time", "pj_end_time", 'create_time',
                                               "pj_status", "pj_is_del")
    ret_val.data = [{
        'pj_id': i.get('pj_id'),
        'pj_title': i.get('pj_title'),
        'pj_sub': i.get('pj_sub'),
        'pj_content': i.get('pj_content'),
        'pj_actual_day': i.get('pj_actual_day'),
        'pj_actual_fee': i.get('pj_actual_fee'),
        'pj_except_fee': i.get('pj_except_fee'),
        'pj_except_day': i.get('pj_except_day'),
        'pj_is_del': i.get('pj_is_del', False),
        'pj_start_time': i.get('pj_start_time').strftime('%Y-%m-%d'),
        'pj_end_time': i.get('pj_end_time').strftime('%Y-%m-%d'),
        'create_time': i.get('create_time').strftime('%Y-%m-%d %H:%M:%S'),
        'pj_status': common.Common.get_enum_str_by_val(enums.ProjectStatus, i.get('pj_status')),
    } for i in my_create_projects]

    return JsonResponse(ret_val.dict())
