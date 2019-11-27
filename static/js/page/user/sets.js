$(function () {
    // 修改用户信息
    $('#user_info_edit').click(function () {
        layer.confirm('确定修改信息？', {icon: 3, title: '修改个人资料'}, function () {
            var formData = $('#user_info_form').serializeObject();
            formData['technology_stack'] = formData['technology_stack'].join(',');
            formData['r'] = Math.random();
            $.ajax({
                url: '/user/edit_user',
                type: 'POST',
                data: formData,
                beforeSend: function () {
                    layer.load(3);
                },
                success: function (res) {
                    layer.closeAll();
                    layer.msg(res.message, {icon: res.code});
                    if (!res.error) {
                        setTimeout(function () {
                            location.href = '/user/sets';
                        }, 1500)
                    }
                },
                error: function () {
                    layer.msg('修改信息失败，请稍后再试！', {icon: 2});
                }
            });
        });
    });
    // 上传头像
    var uploadInst = upload.render({
        elem: '.upload-img' //绑定元素
        , url: '/upload/' //上传接口
        , size: 50
        , done: function (res) {
            //上传完毕回调
            // console.log(res);
            if (res.code == 0) {
                $.ajax({
                    url: '/user/edit_user_header',
                    type: 'POST',
                    data: {
                        'header_avatar': res.data.src,
                        'r': Math.random()
                    },
                    beforeSend: function () {
                        layer.load(3);
                    },
                    success: function (response) {
                        layer.closeAll();
                        layer.msg(response.message, {icon: response.code});
                        if (!response.error) {
                            $('.user_header_img').attr("src", res.data.src,);
                        }
                    },
                    error: function () {
                        layer.msg('修改头像失败，请稍后再试！', {icon: 2});
                    }
                });

            } else {
                layer.msg(res.message, {icon: 2});
            }
        }
        , error: function () {
            //请求异常回调
        }
    });
    // 修改密码
    $('#edit_pass').click(function () {
        var now_pass = $('#L_nowpass').val(),
            pass = $('#L_pass').val(),
            re_pass = $('#L_repass').val();
        if (pass.length < 6) {
            layer.msg('新密码长度最低6位。', {icon: 0});
            return false;
        }
        if (pass != re_pass) {
            layer.msg('新密码与确认密码不一致。', {icon: 0});
            return false;
        }
        $.ajax({
            url: '/user/edit_pass',
            type: 'POST',
            data: {
                now_pass: now_pass,
                new_pass: pass,
                re_pass: re_pass
            },
            beforeSend: function () {
                layer.load(3);
            },
            success: function (res) {
                layer.closeAll();
                layer.msg(res.message, {icon: res.code});
                if (!res.error) {
                    setTimeout(function () {
                        location.href = '/user/logout';
                    }, 1500)
                }
            },
            error: function () {
                layer.msg('密码修改失败，请稍后再试。', {icon: 2});
            }
        });

    });
});