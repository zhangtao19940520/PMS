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
                            location.href = '/';
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
        , done: function (res) {
            console.log(res);
            //上传完毕回调
            // console.log(res);
            if (res.error == 0) {
                $('#user_header_img').attr("src", res.url);
            } else {
                layer.msg(res.message, {icon: 2});
            }
        }
        , error: function () {
            //请求异常回调
        }
    });
});