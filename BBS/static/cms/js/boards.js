$(function () {
    $("#add-board-btn").click(function (event) {
        event.preventDefault();
        xtalert.alertOneInput({
            'text': '请输入板块名称',
            'placeholder': '板块名称',
            'confirmCallback': function (inputValue) {
                yajax.post({
                    'url': '/cms/add_board/',
                    'data': {
                        'name': inputValue
                    },
                    'success': function (data) {
                        if (data['code'] == 200) {
                            window.location.reload();
                        } else {
                            xtalert.alertInfo(data['message']);
                        }
                    }
                });
            }
        });
    });
});

$(function () {
    $(".edit-board-btn").click(function () {
        var self = $(this);
        var tr = self.parent().parent();
        var name = tr.attr("data-name");
        var board_id = tr.attr("data-id");

        xtalert.alertOneInput({
            'text': '请输入板块名称',
            'placeholder': name,
            'confirmCallback': function (inputValue) {
                yajax.post({
                    'url': '/cms/edit_board/',
                    'data': {
                        'board_id': board_id,
                        'name': inputValue
                    },
                    'success': function (data) {
                        if (data['code'] == 200) {
                            window.location.reload();
                        } else {
                            xtalert.alertInfo(data['message']);
                        }
                    }
                });
            }
        });
    });
});

$(function () {
    $(".delete-board-btn").click(function () {
        var self = $(this);
        var tr = self.parent().parent();
        var board_id = tr.attr("data-id");

        xtalert.alertConfirm({
            "msg": "是否要删除这个板块",
            "confirmCallback": function () {
                yajax.post({
                    'url': '/cms/delete_board/',
                    'data': {
                        'board_id':board_id
                    },
                    'success' : function (data) {
                        if (data['code'] == 200) {
                            window.location.reload();
                        } else {
                            xtalert.alertInfo(data['message']);
                        }
                    }
                });
            }
        });
    });
});