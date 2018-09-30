$(document).ready(function() {
    displayOptions();
    tips();
    submit();
    $("#datetimepicker1").datetimepicker({
        format: "yyyy-mm-dd",
        minView: "month",
        todayBtn: 1,
        autoclose: true,
    });
});

function displayOptions() {
    // 选取na='count'的所有td标签，并获取其值；
    $("#tb tr td[na='count']").each(function() {
        var num = $(this).text();
        // console.log(num);
        // 利用for循环将数值逐一加入到select下拉菜单中；
        for (var i = 0; i <= num; i++) {
            $(this).parent().find('select').append("<option>" + i + "</option>");
        }
        // 添加完成后，刷新select；
        $(this).parent().find('select').selectpicker('refresh');
    });
};

function tips() {
    // 添加对于所有select改变的监测事件；
    $("#tb tr td select").each(function() {
        $(this).on('change', function() {
            var num = $(this).val();
            var sname = $(this).parent().parent().prev().prev().prev().text();
            var sid = $(this).parent().parent().parent().attr('id');
            // 获取改变值，并将其添加到tips中；
            // console.log(sid, sname, num);
            // 添加前先判断是否有class值为该学校id的p标签，若有，先删除再添加;
            $('#tips p').remove('.' + sid);
            if (Number(num) > 0) {
                $('#tips').append("<p class='text-danger " + sid + "'" + "sid=" + sid + ">" + sname + ": " + num + "</p>");
            };
        });
    });
    // $('#driver').on('change', function() {
    //     var dname = $(this).val();
    //     var did = $(this).find('option:selected').attr('did');
    //     console.log(did, dname);
    // });
    // $('#bus').on('change', function() {
    //     var bname = $(this).val().split('--')[0];
    //     var bid = $(this).find('option:selected').attr('bid');
    //     console.log(bid, bname);
    // });
};

function submit() {
    $("#create").on('click', function() {
        var tripDic = {};
        var sum = 0;
        $('#tips p.text-danger').each(function() {
            sid = $(this).attr('sid');
            num = $.trim($(this).text().split(':')[1]);
            tripDic[sid] = num;
            sum += Number(num);
        });
        var bus = $('#bus').val();
        var driver = $('#driver').val();
        var time = $('#date').text().split('/')[2] + '-' + $('#date').text().split('/')[1] + '-' + $('#date').text().split('/')[0];
        // var time = $('#timeinput').val();
        if (!sum) {
            $.alert({
                title: 'Error!',
                content: 'Please make sure you selected the School.',
                icon: 'glyphicon glyphicon-exclamation-sign',
                type: 'red',
            });
            return false;
        } else if (!bus) {
            $('#bustip').show();
            return false;
        } else if (!driver) {
            $('#drivertip').show();
            return false;
        } else {
            var bseats = Number(bus.split('--')[1]);
            if (sum <= bseats) {
                tripDic['bus'] = $("#bus").find('option:selected').attr('bid');
                tripDic['driver'] = $('#driver').find('option:selected').attr('did');
                // 获取当前时间的 h，m，s，拼接为trip的name
                var myDate = new Date();
                var h = myDate.getHours();
                var m = myDate.getMinutes();
                var s = myDate.getSeconds();
                var tname = time + '-' + h + m + s;
                // console.log(tname);
                tripDic['tname'] = tname;
                // console.log(tripDic);
                $.ajax({
                    url: '/tripsave/',
                    type: 'POST',
                    data: tripDic,
                    traditional: true,
                    async: false,
                    success: function(arg) {
                        if (arg.status) {
                            top.location.href = "/trip-staff/";
                        } else {
                            $.alert({
                                title: 'Request failure!',
                                icon: 'glyphicon glyphicon-exclamation-sign',
                                type: 'red',
                            });
                        }
                    },
                });
            } else {
                $.alert({
                    title: 'Error!',
                    content: 'Make sure the selected bus has enough seats.',
                    icon: 'glyphicon glyphicon-exclamation-sign',
                    type: 'red',
                });
            }
        }
    });
};