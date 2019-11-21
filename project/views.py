from django.shortcuts import render
from utils.authorize import check_login


# Create your views here.

@check_login
def market(request):
    """
    项目市场
    :param request:
    :return:
    """
    return render(request, 'project/market.html')
