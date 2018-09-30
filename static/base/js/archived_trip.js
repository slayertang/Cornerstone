$(document).ready(function() {
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
})