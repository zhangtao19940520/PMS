/**
 * 倒计时
 * @target 需要针对的dom对象
 * time 倒计时时长（单位：s）
 * */
function djs(target, time) {
    $(target).addClass('layui-btn-disabled');
    $(target).prop('disabled', true);
    var timer = setInterval(function () {
        if (time > 0) {
            $(target).text(time + 's后重新获取');
        } else {
            $(target).removeClass('layui-btn-disabled');
            $(target).prop('disabled', false);
            $(target).text('获取验证码');
            clearInterval(timer);
        }
        time--;
    }, 1000)
}

/**
 * JQuery扩展方法，将数据格式化为json对象
 * */
$.fn.serializeObject = function () {
    var o = {};
    var a = this.serializeArray();
    $.each(a, function () {
        if (o[this.name]) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};