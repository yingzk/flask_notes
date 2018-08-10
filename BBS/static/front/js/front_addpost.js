$(function () {
    var ue = UE.getEditor("editor", {
        "serverUrl": '/ueditor/upload/'
    });

    $("#submit-btn").click(function (event) {
        event.preventDefault();
        var titleInput = $("input[name='title']");
        var boardSelect = $("select[name='board_id']");

        var title = titleInput.val();
        var board_id = boardSelect.val();
        var content = ue.getContent();

        yajax.post({
            'url': '/add_post/',
            'data': {
                'title': title,
                'board_id': board_id,
                'content': content
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    xtalert.alertConfirm({
                        "msg": "帖子发表成功！",
                        "cancelText": "回到首页",
                        "confirmText": "再发一篇",
                        "cancelCallback": function () {
                            window.location = '/';
                        },
                        "confirmCallback": function () {
                            titleInput.val("");
                            ue.setContent("");
                        }
                    });
                } else {
                    xtalert.alertInfo(data['message']);
                }
            }
        });
    });
});