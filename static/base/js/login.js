$(function() {
    $('#id_captcha_1').blur(function() {
        // #id_captcha_1为输入框的id，当该输入框失去焦点时触发函数
        json_data = {
            'response': $('#id_captcha_1').val(), // 获取输入框和隐藏字段id_captcha_0的数值
            'hashkey': $('#id_captcha_0').val()
        }
        $.getJSON('/ajax_val/', json_data, function(data) {
            //ajax发送
            var ok = document.getElementById('ok')
            var remove = document.getElementById('remove')
            var br = document.getElementById('br')
            $('#captcha_status').remove()
            if (data['status']) { //status返回1为验证码正确， status返回0为验证码错误， 在输入框的后面写入提示信息
                ok.style.display = 'block'
                remove.style.display = 'none'
                br.style.display = 'none'
                document.getElementById('login').disabled = false
                    // 验证输入正确，提交按钮会被开启
            } else {
                ok.style.display = 'none'
                remove.style.display = 'block'
                br.style.display = 'none'
                document.getElementById('login').disabled = true
                    // 验证输入错误，提交按钮会被禁用
            }
        });
    });
    $('.captcha').click(function() {
        $.getJSON("/captcha/refresh/", function(result) {
            $('.captcha').attr('src', result['image_url']);
            $('#id_captcha_0').val(result['key'])
        });
    });
    var m = document.getElementById('message')
    $('.form-control').click(function() {
        if (message) {
            m.style.display = 'none'
        }
    });
})