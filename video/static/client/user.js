$(function () {
    // 注册
    $('#register-submit').click(function () {
        var username = $('#username').val();
        var password = $('#password').val();
        var csrftoken = $("input[name='csrfmiddlewaretoken']").val();
        var url = $(this).attr('data-url');

        if (!username || !password) {
            alert('缺少必要字段');
            return;
        }

        $.ajax(url, {
            type: 'post',
            data: {
                username: username,
                password: password,
                csrfmiddlewaretoken: csrftoken,
            },

            success: function (data) {
                console.log(data);
                alert(data['msg']);
            },
            fail: function (e) {
                console.log('error:%s', e);
            }

        });
    });

    // 登录
    $('#login-submit').click(function () {
        var username = $('#username').val();
        var password = $('#password').val();
        var csrftoken = $("input[name='csrfmiddlewaretoken']").val();
        var url = $(this).attr('data-url');

        if (!username || !password) {
            alert('缺少必要字段');
            return;
        }

        $.ajax({
            url: url,
            type: 'post',
            data: {
                username: username,
                password: password,
                csrfmiddlewaretoken: csrftoken,
            },

            success: function (data) {
                console.log(data);
                if(data.code){
                    alert(data['msg']);
                }else{
                    alert('登陆成功')
                }
            },
            fail: function (e) {
                console.log('error:%s', e);
            }

        });
    });
});