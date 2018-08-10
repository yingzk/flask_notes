$(function () {
    $("#save-banner-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var dialog = $("#banner-dialog");
        var nameInput = dialog.find("input[name='name']");
        var imageInput = dialog.find("input[name='image_url']");
        var linkInput = dialog.find("input[name='link_url']");
        var priorityInput = dialog.find("input[name='priority']");

        var name = nameInput.val();
        var image_url = imageInput.val();
        var link_url = linkInput.val();
        var priority = priorityInput.val();
        var submitType = self.attr("data-type");
        var bannerId = self.attr("data-id");

        if (!name || !image_url || !link_url || !priority) {
            xtalert.alertInfoToast('请输入轮播图完整信息！');
            return;
        }

        var url = '';
        if (submitType == 'edit') {
            url = '/cms/edit_banner/';
        } else {
            url = '/cms/add_banner/';
        }

        yajax.post({
            'url': url,
            'data': {
                'name': name,
                'image_url': image_url,
                'link_url': link_url,
                'priority': priority,
                'banner_id' : bannerId
            },
            'success' : function (data) {
                dialog.modal("hide");
                if (data['code'] == 200) {
                    window.location.reload();
                } else {
                    xtalert.alertInfo(data['message']);
                }
            },
            'fail' : function () {
                xtalert.alertNetworkError();
            }
        });
    });
});

$(function () {
    $(".edit-banner-btn").click(function (event) {
        var self = $(this);
        var dialog = $("#banner-dialog");
        dialog.modal("show");

        //获取填充信息
        var tr = self.parent().parent();
        var name = tr.attr("data-name");
        var image_url = tr.attr("data-image");
        var link_url = tr.attr("data-link");
        var priority = tr.attr("data-priority");

        var nameInput = dialog.find("input[name='name']");
        var imageInput = dialog.find("input[name='image_url']");
        var linkInput = dialog.find("input[name='link_url']");
        var priorityInput = dialog.find("input[name='priority']");
        var saveBtn = dialog.find("#save-banner-btn");

        nameInput.val(name);
        imageInput.val(image_url);
        linkInput.val(link_url);
        priorityInput.val(priority);

        saveBtn.attr('data-type', 'edit');
        saveBtn.attr('data-id', tr.attr('data-id'));
    });
});


$(function () {
   $(".delete-banner-btn").click(function (event) {
       var self = $(this);
       var tr = self.parent().parent();
       var banner_id = tr.attr("data-id");
       xtalert.alertConfirm({
           "msg" : "是否要删除这个轮播图",
           "confirmCallback": function () {
               yajax.post({
                   'url' : '/cms/delete_banner/',
                   'data' : {
                       'banner_id': banner_id
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

$(function () {
    yqiniu.setUp({
        'domain': "http://xxxxxxxxxxxx.xxx.clouddn.com/",
        'browse_btn': 'upload-btn',
        'uptoken_url' : '/c/uptoken/',
        'success': function (up, file, info) {
            var imageInput = $("input[name='image_url']");
            imageInput.val(file.name);
        }
    });
});