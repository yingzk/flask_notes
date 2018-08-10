$(function () {
   $(".highlight-btn").click(function (event) {
       event.preventDefault();
       var self = $(this);
       var tr = self.parent().parent();
       var post_id = tr.attr("data-id");
       var highlight = parseInt(tr.attr("data-highlight"));
       var url = "";
       if (highlight) {
           url = '/cms/d_highlight/';
       } else {
           url = '/cms/highlight/';
       }

       yajax.post({
           'url' : url,
           'data' : {
               'post_id': post_id
           },
           'success': function (data) {
               if (data['code'] == 200) {
                   xtalert.alertSuccessToast('操作成功！');
                   setTimeout(function () {
                       window.location.reload();
                   }, 500);
               } else {
                   xtalert.alertInfo(data['message']);
               }
           }
       });
   });
});