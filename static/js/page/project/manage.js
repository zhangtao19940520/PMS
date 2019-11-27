$(function () {
    let edit_content = layedit.build('pj_content', {
        height: 280,
        uploadImage: {
            url: '/upload/',
            type: 'POST',
        },
    }); //建立编辑器

    $('#btn_create_my_project').click(function () {
        layer.msg('我的项目');
    });
});