$(document).ready(function() {
    dateCheck();
    delmodal();
    delConfirm();
    setFooter();
});
// 检查当前trip的创建日期，并确认其在同一天。
function dateCheck() {
    var a = new Array;
    $("#tb tr td[na='tripname']").each(function() {
        t = $(this).text().split('-')[0] + $(this).text().split('-')[1] + $(this).text().split('-')[2]
            // console.log(t);
        a.push(t);
    });
    // console.log($.unique(a));
    if ($.unique(a).length > 1) {
        $.alert({
            title: 'Warning!',
            content: 'Trips are not on same day. Please check your trip name and time!',
            icon: 'glyphicon glyphicon-exclamation-sign',
            type: 'red',
            theme: 'supervan',
        });
    }
};

function delmodal() {
    $('#tb').on('click', '.del-row', function() {
        var did = $(this).parent().parent().attr('id');
        // console.log(did);
        $('#delnid').val(did);
        $('#delmodal').modal('toggle');
    });
};

function delConfirm() {
    $('#delconfirm').click(function() {
        var tid = $('#delnid').val();
        // console.log(id);
        $.ajax({
            url: '/deltrip/',
            type: 'POST',
            data: { 'tid': tid },
            async: false,
            success: function(arg) {
                if (arg.status) {
                    $('#delModal').modal('toggle');
                    window.location.reload();
                }
            },
        });
    });
};



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
    console.log(bottomD);
    $('.content').css('padding-bottom', bottomD);
};