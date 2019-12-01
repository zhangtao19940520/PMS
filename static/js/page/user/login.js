$(function () {
    $('#login_btn').click(function () {
        var formData = $('#login_form').serializeObject();
        // console.log(formData);
        if (formData.loginName.trim().length == 0) {
            layer.msg('请输入手机/邮箱', {icon: 0});
            return false;
        }
        if (formData.pass.trim().length == 0) {
            layer.msg('请输入登录密码', {icon: 0});
            return false;
        }
        if (formData.imagecode.trim().length == 0) {
            layer.msg('请输入图形码', {icon: 0});
            return false;
        }
        formData['r'] = Math.random();
        $.ajax({
            url: '/user/login',
            type: 'POST',
            data: formData,
            dataType: 'JSON',
            beforeSend: function () {
                layer.load(3);
            },
            success: function (res) {
                layer.closeAll();
                layer.msg(res.message, {icon: res.code});
                $('.fly-imagecode').click();
                if (!res.error) {
                    setTimeout(function () {
                        location.href = '/';
                    }, 1500)
                }
            },
            error: function () {
                layer.closeAll();
                $('.fly-imagecode').click();
                layer.msg('登录失败！请稍后再试', {icon: 2});
            }
        });
    });
});

$(document).keyup(function (event) {
    console.log(event.keyCode);
    if (event.keyCode == 13) {
        //这里填写你要做的事件
        $('#login_btn').click();
    }
});