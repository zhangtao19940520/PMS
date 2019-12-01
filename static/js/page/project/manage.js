$(function () {
    let to_sub = $('#to_sub').val();
    let li_msg = 'li[lay-id="' + to_sub + '"]';
    if (to_sub !== '') {
        $(li_msg).click();
        if (to_sub == 'has_create') {
            searchMyCreateProject();
        }
    }

    // 创建项目的项目详情富文本
    let edit_content = layedit.build('pj_content', {
        height: 200,
        uploadImage: {
            url: '/upload/',
            type: 'POST',
        },
    }); //建立编辑器
    // 查询我创建的项目
    $('#btn_search_my_create_project').click(function () {
        searchMyCreateProject();
    });
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
                if (!res.error) {
                    setTimeout(function () {
                        location.href = '/project/p_manage?for=has_create';
                    }, 1500)
                }
            },
            error: function () {
                layer.closeAll();
                $('.fly-imagecode').click();
                layer.msg('创建项目失败，请稍后再试！', {icon: 2});
            }
        });
    });

    // tab标签切换操作
    element.on('tab(project_manage)', function (data) {
        //已创建的项目
        if (data.index === 1) {
            //查询已创建项目
            searchMyCreateProject();
        }
    });
});

/**
 * 查询我创建的项目
 * */
function searchMyCreateProject() {
    let formData = $('#form_search_project').serializeObject();
    $.ajax({
        url: '/project/search_my_create_project',
        type: 'POST',
        data: formData,
        beforeSend: function () {
            layer.load(3);
        },
        success: function (res) {
            layer.closeAll();
            if (!res.error) {
                //第一个实例
                let menu_content_table = table.render({
                    id: 'pj_id',
                    elem: '#my_create_project_table'
                    , height: 500
                    , url: '' //数据接口
                    , page: true //开启分页
                    , limit: 10
                    , cols: [[ //表头
                        {field: 'pj_title', title: '项目标题', width: 270, sort: true, align: 'center'},
                        {field: 'pj_status', title: '项目状态', width: 120, sort: true, align: 'center'},
                        {field: 'pj_except_fee', title: '项目预算费用（￥）', width: 180, sort: true, align: 'center'},
                        {field: 'pj_except_day', title: '项目预算时间（天）', width: 180, sort: true, align: 'center'},
                        {field: 'create_time', title: '创建时间', width: 180, sort: true, align: 'center'},
                        {fixed: 'right', title: '操作', width: 165, align: 'center', toolbar: '#barDemo'}
                    ]],
                    data: res.data
                });

                //监听行工具事件
                table.on('tool(my_create_project)', function (obj) { //注：tool 是工具条事件名，test 是 table 原始容器的属性 lay-filter="对应的值"
                    var data = obj.data //获得当前行数据
                        , layEvent = obj.event; //获得 lay-event 对应的值
                    //编辑查看
                    if (layEvent === 'detail_edit') {
                        layer.msg('编辑');
                    }
                    if (layEvent === 'detail_del') {
                        layer.msg('删除');
                    }

                });
            } else {
                layer.msg("未查询到相关数据", {icon: 0});
            }
        },
        error: function () {
            layer.closeAll();
            layer.msg("查询异常，请稍后再试。", {icon: 2});

        }
    });
}