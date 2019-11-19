$(function () {
    $('#register_btn').click(function (e) {
        e.preventDefault();
        // 表单数据格式化
        var formData = $('#reg_form').serializeObject();
        formData['r'] = Math.random();
        if (formData.pass != formData.repass) {
            layer.msg('两次输入密码不一致', {icon: 0});
            return false;
        }
        if (formData.agreement != 'on') {
            layer.msg('请先同意用户服务条款。', {icon: 0});
            return false;
        }
        if (formData.email != '' &&
            formData.mobile != '' &&
            formData.imagecode != '' &&
            formData.pass != '' &&
            formData.realname != '' &&
            formData.repass != '' &&
            formData.vercode != '') {
            $.ajax({
                url: '/user/register',
                type: 'POST',
                data: formData,
                dataType: 'JSON',
                beforeSend: function () {
                    layer.load(3);
                },
                success: function (res) {
                    layer.closeAll();
                    layer.msg(res.message, {icon: res.code});
                    if (!res.error) {
                        setTimeout(function () {
                            location.href = '/user/login';
                        }, 1500)
                    }
                },
                error: function () {
                    layer.msg('注册失败！', {icon: 2});
                }
            });
        }
    });
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
                layer.msg('获取验证码失败！', {icon: 2});
            }
        });
    });
});