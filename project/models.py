from django.db import models
import django.utils.timezone as timezone
from user.models import UserInfo
from utils.enums import ProjectStatus, ProjectFuncStatus


class ProjectInfo(models.Model):
    """
    项目信息
    """
    pj_id = models.AutoField(primary_key=True, verbose_name='项目ID')
    pj_title = models.CharField(default='', max_length=100, unique=True, verbose_name='项目标题')
    pj_sub = models.CharField(default='', max_length=300, verbose_name='项目简介')
    pj_content = models.TextField(default='', verbose_name='项目描述')
    pj_stack = models.CharField(default='', max_length=120, verbose_name='项目所用技术栈')
    pj_is_del = models.BooleanField(default=False, verbose_name='是否删除')
    pj_except_fee = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name='项目预算费用')
    pj_except_day = models.IntegerField(default=0, verbose_name='项目期望开发周期（天）')
    pj_actual_fee = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name='项目实际费用')
    pj_actual_day = models.IntegerField(default=0, verbose_name='项目实际开发周期（天）')
    pj_status = models.SmallIntegerField(default=1, choices=ProjectStatus, verbose_name='项目状态')
    pj_start_time = models.DateField(default=timezone.now().today, verbose_name='项目开始开发时间')
    pj_end_time = models.DateField(default=timezone.now().today, verbose_name='项目完结时间')
    last_update_time = models.DateTimeField(auto_now=True, verbose_name='上一次修改时间')
    create_user = models.ForeignKey(to=UserInfo, to_field='user_id', on_delete=models.CASCADE, blank=True, null=True,
                                    default=None, verbose_name='创建用户')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.pj_title

    class Meta:
        verbose_name_plural = verbose_name = "项目信息"
