 /* AJAX */

 $(function () {
     $("#captcha-btn").click(function (even) {
         even.preventDefault();
         var email = $("input[name=email]").val();
         if (!email){
             xtalert.alertInfoToast('请输入邮箱');
             return;
         }
         yajax.get({
             'url':'/cms/email_captcha/',
             'data':{
                 'email':email
             },
             'success': function (data) {
                 if (data['code'] == 200) {
                     xtalert.alertSuccessToast('验证码发送成功！');
                 } else {
                     xtalert.alertInfo(data['message']);
                 }
             },
             'fail': function (data) {
                 xtalert.alertNetworkError();
             }
         });
     });
 });
 
 $(function () {
     $("#submit").click(function (event) {
         event.preventDefault();
         var emailE = $("input[name=email]");
         var captchaE = $("input[name=captcha]");

         var email = emailE.val();
         var captcha = captchaE.val();
         yajax.post({
             'url':'/cms/resetemail/',
             'data': {
                 'email' : email,
                 'captcha' : captcha
             },
             'success':function (data) {
                 if (data['code'] == 200) {
                     xtalert.alertSuccessToast('修改邮箱成功！');
                     captchaE.val("");
                 } else {
                     xtalert.alertInfo(data['message']);
                 }
             },
             'fail':function (data) {
                 xtalert.alertNetworkError();
             }
         });
     });
 });