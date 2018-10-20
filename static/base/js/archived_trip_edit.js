$(document).ready(function() {
    bindClick();
    bindSubmit();
    setFooter()
});

function bindClick() {
    $('#tb').on('click', '.edit-row1', function() {
        var id = $(this).parent().parent().children().eq(0).text();
        var school = $(this).parent().parent().children().eq(1).text();
        var sname = $(this).parent().parent().children().eq(2).text();
        $('#nid').attr('placeholder', id);
        $('#school').attr('placeholder', school);
        $('#sname').attr('placeholder', sname);
        $('#editmodal').modal('toggle');
    });
    $('#tb').on('click', '.edit-row2', function() {
        var id = $(this).parent().parent().children().eq(0).text();
        var school = $(this).parent().parent().children().eq(1).text();
        var sname = $(this).parent().parent().children().eq(2).text();
        $('#nid').attr('placeholder', id);
        $('#school').attr('placeholder', school);
        $('#sname').attr('placeholder', sname);
        $('#editmodal').modal('toggle');
    });
};

function bindSubmit() {
    $('#submit').on('click', function() {
        // 点击submit按钮，获取当前选中的单选框的值和id值；
        var tid = $('#editmodal').attr('nid');
        var status = $("input[type='radio']:checked").val();
        var sid = $('#nid').attr('placeholder');
        if (status && sid && tid) {
            $.ajax({
                url: '/archivedtripedit/',
                type: 'POST',
                data: { 'tid': tid, 'sid': sid, 'status': status },
                async: false,
                success: function(arg) {
                    if (arg.status) {
                        window.location.reload();
                        // createRow(postData, arg.data);
                        // $('#addmodal').modal('hide');
                        // window.location.reload();
                    } else {
                        $.alert({
                            title: 'Error!',
                            content: 'Please try again.',
                        });
                    }
                },
            });
        }
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
    // console.log(bottomD);
    $('.content').css('padding-bottom', bottomD);
};