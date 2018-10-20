$(document).ready(function() {
    bindDel();
    bindDelConfirm();
    bindAdd();
    bindAddSubmit();
    setFooter();
});

function bindDelConfirm() {
    $('#delconfirm').click(function() {
        var studentid = $('#delnid').val();
        var tripid = $('#delnid1').text();
        $.ajax({
            url: '/deltripstudent/',
            type: 'POST',
            data: {
                'studentid': studentid,
                'tripid': tripid
            },
            async: false,
            success: function(arg) {
                if (arg.status) {
                    $('#delmodal').modal('toggle');
                    window.location.reload();
                }
            },
        });
    });
};

function bindDel() {
    $('#tb').on('click', '.del-row', function() {
        var did = $(this).parent().parent().attr('id');
        $('#delnid').val(did);
        $('#delmodal').modal('toggle');
    });
};

function bindAdd() {
    $('#add').on('click', function() {
        var busseats = parseInt($('#seats').text());
        var students = parseInt($('#students').text());
        $("input[type='checkbox']").each(function() {
            $(this).prop('checked', false);
            $(this).prop('disabled', false);
        });
        // console.log(students);
        if (students >= busseats) {
            $.alert({
                title: 'Seems the bus is full!',
                icon: 'glyphicon glyphicon-exclamation-sign',
                type: 'red',
            });
            // alert('full!');
        } else {
            $('#addModal').modal('toggle');
            $('#studentslist').on('change', function() {
                var seatsleft = busseats - students;
                var num = $("input[type='checkbox']:checked").length;
                // console.log(num);
                // console.log(seatsleft);
                if (num >= seatsleft) {
                    $("input[type='checkbox']:not(:checked)").each(function() {
                        $(this).prop('disabled', true);
                    });
                } else {
                    $("input[type='checkbox']").each(function() {
                        $(this).prop('disabled', false);
                    });
                }
            });
        };
    });
};

function bindAddSubmit() {
    $('#submit').on('click', function() {
        var addId = new Array();
        var tripId = $('#studentslist').attr('nid');
        $("input[type='checkbox']:checked").each(function() {
            var id = $(this).val();
            addId.push(id);
        });
        // console.log(addId);
        $.ajax({
            url: '/addtripstudent/',
            type: 'POST',
            data: { 'addid': addId, 'tripid': tripId },
            traditional: true,
            async: false,
            success: function(arg) {
                if (arg.status) {
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
    // console.log(bottomD);
    $('.content').css('padding-bottom', bottomD);
};