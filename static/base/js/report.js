$(document).ready(function() {
    setFooter();

    function setFooter() {
        var browserH = $(window).height();
        var h = $('.content').height();
        var topH = $('.content').offset().top;
        var scroll = $(document).scrollTop();
        var footer = $('.footer').height();
        // console.log(browserH);
        // console.log(h);
        // console.log(topH);
        // console.log(scroll);
        // console.log(footer);
        var bottomD = browserH - (h + topH - scroll) - footer - 60;
        // console.log(bottomD);
        $('.content').css('padding-bottom', bottomD);
    };
    // 限制时间选择，结束日期不能小于开始日期。
    $("#datetimepicker1").datetimepicker({
        format: "yyyy-mm-dd",
        minView: "month",
        // todayBtn: 1,
        autoclose: true,
        clearBtn: true,
    }).on('changeDate', function() {
        var starttime = $("#start").val();
        $('#end').val('');
        $("#datetimepicker2").datetimepicker('setStartDate', starttime);
        $("#datetimepicker1").datetimepicker('hide');
    });
    $("#datetimepicker2").datetimepicker({
        format: "yyyy-mm-dd",
        minView: "month",
        // todayBtn: 1,
        autoclose: true,
        clearBtn: true,
    });
    // .on('changeDate', function() {
    //     var endtime = $("#end").val();
    //     $("#datetimepicker1").datetimepicker('setEndDate', endtime);
    //     $("#datetimepicker2").datetimepicker('hide');
    // });
    searchBtn();

    function searchBtn() {
        $('#search').on('click', function() {
            var startTime = $('#start').val();
            var endTime = $('#end').val();
            var data = {};
            if (startTime && endTime) {
                $('#starttip').hide();
                $('#endtip').hide();
                // console.log(startTime, endTime);
                data['start'] = startTime;
                data['end'] = endTime;
                // console.log(data);
                $.ajax({
                    url: '/reportsearch/',
                    type: 'GET',
                    data: data,
                    success: function(arg) {
                        if (arg.status) {
                            // console.log(arg.data);
                            trips = JSON.parse(arg.data);
                            $('#tb').empty();
                            $('#note').empty();
                            // console.log(trips);
                            // json化之后的trips是一个Array数组，遍历数组，fields属性中包含所有查询内容，pk为每条结果的主键字段。
                            var total = 0;
                            for (var i = 1; i <= trips.length; i++) {
                                var t = trips[i - 1].fields.date_changed.split('.')[0].replace('T', ' ');
                                var s = JSON.parse(trips[i - 1].fields.trip_school);
                                var school = '';
                                for (k in s) {
                                    school += k + "(" + s[k] + "), ";
                                }
                                $('#tb').append(
                                    "<tr id=" + trips[i - 1].pk + " class='active'>" +
                                    "<td bgcolor='#80DEEA'>" + i + "</td>" +
                                    "<td na='nid' name='tripid'>" + trips[i - 1].pk + "</td>" +
                                    "<td na='tripname'>" + trips[i - 1].fields.trip_name + "</td>" +
                                    "<td na='school'>" + school + "</td>" +
                                    "<td na='lastchanged'>" + t + "</td>" +
                                    "<td na='tripstatus'><span class='text-danger'><b>Archived</b></span></td></tr>"
                                );
                                total = i;
                            }
                            $('#note').append("<span class='text-primary'>Found <span class='text-danger'>" + total + "</span> items.</span>");
                            $('#downloaddiv').show();
                        } else {
                            $.alert({
                                title: 'Request failure!',
                                icon: 'glyphicon glyphicon-exclamation-sign',
                                type: 'red',
                            });
                        }
                    },
                });
            } else if (!startTime) {
                $('#starttip').show();
            } else if (!endTime) {
                $('#endtip').show();
            }
        });
    };
    download();

    function download() {
        $('#download').on('click', function() {
            starttime = $('#start').val();
            endtime = $('#end').val();
            if (starttime && endtime) {
                url = "/download/" + "?start=" + starttime + "&end=" + endtime;
                console.log(url);
                window.location.href = url;
            }
        });
    };
})