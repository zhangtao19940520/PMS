$(function () {
    // 创建项目的项目详情富文本
    let edit_content = layedit.build('pj_content', {
        height: 200,
        uploadImage: {
            url: '/upload/',
            type: 'POST',
        },
    }); //建立编辑器
    // 创建项目
    $('#btn_create_my_project').click(function () {
        let formData = $('#create_project_form').serializeObject();
        formData['pj_content'] = layedit.getContent(edit_content);
        let pj_stack = formData['pj_stack'] || '';
        if (pj_stack !== '' && typeof pj_stack == "object") {
            pj_stack = formData['pj_stack'].join(',');
        }
        formData['pj_stack'] = pj_stack;
        if (formData.pj_title.trim() === '') {
            layer.msg('请输入项目的标题', {icon: 0});
            $('#pj_title').focus();
            return false;
        }
        if (formData.pj_content.trim() === '') {
            layer.msg('请输入项目的详细描述', {icon: 0});
            $('#pj_content').focus();
            return false;
        }
        if (formData.pj_except_fee <= 0) {
            layer.msg('请输入您的项目预算金额', {icon: 0});
            $('#pj_except_fee').focus();
            return false;
        }
        if (formData.pj_except_day <= 0) {
            layer.msg('请输入您的项目预算时间', {icon: 0});
            $('#pj_except_day').focus();
            return false;
        }
        if (formData.imagecode.trim() === '') {
            layer.msg('请输入图形码', {icon: 0});
            $('#image_mode').focus();
            return false;
        }
        $.ajax({
            url: '/project/create_project',
            type: 'POST',
            data: formData,
            beforeSend: function () {
                layer.load(3);
            },
            success: function (res) {
                layer.closeAll();
                $('.fly-imagecode').click();
                layer.msg(res.message, {icon: res.code});
                // if (!res.error) {
                //     setTimeout(function () {
                //         location.href = '/project/p_manage';
                //     }, 1500)
                // }
            },
            error: function () {
                layer.closeAll();
                $('.fly-imagecode').click();
                layer.msg('创建项目失败，请稍后再试！', {icon: 2});
            }
        });
    });
});