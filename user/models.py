from django.db import models
import django.utils.timezone as timezone


# Create your models here.


class UserInfo(models.Model):
    """
    用户信息
    """
    user_id = models.AutoField(primary_key=True, verbose_name='用户ID')
    user_name = models.CharField(default='', max_length=10, unique=True, verbose_name='用户名')
    password = models.CharField(default='', max_length=64, verbose_name='登录密码')
    real_name = models.CharField(default='', max_length=10, verbose_name='真实姓名')
    mobile = models.CharField(default='', max_length=11, verbose_name='手机号码')
    email = models.EmailField(default='', max_length=50, verbose_name='邮箱')
    alipay_account = models.CharField(default='', max_length=50, verbose_name='支付宝账号')
    is_enable = models.BooleanField(default=True, verbose_name='是否启用')
    id_card = models.CharField(default='', max_length=18, verbose_name='身份证号码')
    last_login_time = models.DateTimeField(default=timezone.now, verbose_name='上一次登录时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.user_name
