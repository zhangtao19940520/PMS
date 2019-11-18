$(function () {
    $('#register_btn').click(function (e) {
        e.preventDefault();

        layer.msg('register');
        $.ajax({
            url: '/user/register',
            type: 'POST',
            data: {

                r: Math.random()
            },
            dataType: 'JSON',
            beforeSend: function () {
                layer.load(3);
            },
            success: function (res) {
                layer.closeAll();
                console.log(res);
            },
            error: function () {
                layer.msg('登录失败，请联系管理员');
            }
        });
    });
});