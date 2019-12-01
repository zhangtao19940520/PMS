$(function () {
    //获取验证码
    $('#getvercode').click(function () {
        var email = $('#email').val().trim();
        if (email == '' || email.indexOf('@') < 0) {
            layer.msg('请输入正确的邮箱账号', {icon: 0});
            return false;
        }
        var imgCode = $('#imagecode').val().trim();
        if (imgCode == '') {
            layer.msg('请输入正确的图片验证码', {icon: 0});
            return false;
        }
        $.ajax({
            url: '/user/getvercode',
            type: 'POST',
            data: {
                r: Math.random(),
                email: email,
                img_code: imgCode
            },
            beforeSend: function () {
                layer.load(3);
            },
            success: function (res) {
                layer.closeAll();
                if (!res.error) {
                    djs($('#getvercode'), 60);
                    $('.fly-imagecode').click();
                }
                layer.msg(res.message, {icon: res.code});
            },
            error: function () {
                layer.closeAll();
                $('.fly-imagecode').click();
                layer.msg('获取验证码失败！', {icon: 2});
            }
        });
    });

    //重置密码提交
    $('#forget_btn').click(function (e) {
        e.preventDefault();
        // 表单数据格式化
        var formData = $('#form_forget').serializeObject();
        formData['r'] = Math.random();
        console.log(formData);
        if (formData.email.length == 0 || formData.email.indexOf('@') < 0) {
            layer.msg('请输入正确的邮箱账号！', {icon: 0});
            return false;
        }
        if (formData.imagecode.length == 0) {
            layer.msg('请输入图形码！', {icon: 0});
            return false;
        }
        if (formData.vercode.length == 0) {
            layer.msg('请输入验证码！', {icon: 0});
            return false;
        }

        $.ajax({
            url: '/user/forget',
            type: 'POST',
            data: formData,
            dataType: 'JSON',
            beforeSend: function () {
                layer.load(3);
            },
            success: function (res) {
                layer.closeAll();
                layer.msg(res.message, {icon: res.code, time: 5000});
                if (!res.error) {
                    setTimeout(function () {
                        location.href = '/user/login';
                    }, 5000)
                }
            },
            error: function () {
                layer.closeAll();
                $('.fly-imagecode').click();
                layer.msg('重置密码失败！', {icon: 2});
            }
        });

    });
});