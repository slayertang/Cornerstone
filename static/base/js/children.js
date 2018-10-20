$(document).ready(function() {
    $('#addstandby').click(function() {
        $('#addpicktime').show();
    });
    $('#addcancel').click(function() {
        $('#addpicktime').hide();
    });
    $('#chstandby').click(function() {
        $('#chpicktime').show();
    });
    $('#chcancel').click(function() {
        $('#chpicktime').hide();
    });
    bindSave();
    bindDel();
    bindDelConfirm();
    bindEdit();
    bindClick();
    bindViewTrip();
    setFooter();

})

function bindSave() {

    $('#addform').submit(function() {
        var postData = {};
        postData['firstname'] = $('#addfirstname').val();
        postData['lastname'] = $('#addlastname').val();
        postData['school'] = $('#addschool').val();
        // postData['isactive'] = $('input[name="addisactive"]:checked').val();
        // postData['picktime'] = $('input[name="addpicktime"]').val();
        $.ajax({
            url: '/addchild/',
            type: 'POST',
            data: postData,
            async: false,
            success: function(arg) {
                if (arg.status) {
                    window.location.reload();
                    // createRow(postData, arg.data);
                    // $('#addmodal').modal('hide');
                    // window.location.reload();
                } else {
                    // console.log(arg)
                    $('#errormsg').text(arg.message);
                    $('#errormsg').show();
                }
            }
        });
    });
};


function bindEdit() {

    $('#chform').submit(function() {
        var postData = {};
        // postData['firstname'] = $('#addfirstname').val();
        // postData['lastname'] = $('#addlastname').val();
        // postData['school'] = $('#addschool').val();
        postData['id'] = $('#chid').attr('placeholder');
        postData['isactive'] = $('input[name="chisactive"]:checked').val();
        postData['picktime'] = $('input[name="chpicktime"]').val();
        $.ajax({
            url: '/chchild/',
            type: 'POST',
            data: postData,
            async: false,
            success: function(arg) {
                if (arg.status) {
                    window.location.reload();
                    // createRow(postData, arg.data);
                    // $('#addmodal').modal('hide');
                    // window.location.reload();
                } else {
                    // console.log(arg)
                    $('#errormsg').text(arg.message);
                    $('#errormsg').show();
                }
            }
        })
    });
};

function bindClick() {
    $('#tb').on('click', '.edit-row', function() {
        $(this).parent().prevAll().each(function() {
            var t = $(this).text();
            // console.log(t);
            var n = $(this).attr('na');
            // console.log(n)
            if (n == 'school') {
                $('#chschool').attr('placeholder', t)
            }
            if (n == 'lastname') {
                $('#chlastname').attr('placeholder', t)
            }
            if (n == 'firstname') {
                $('#chfirstname').attr('placeholder', t)
            }
            if (n == 'nid') {
                $('#chid').attr('placeholder', t)
            }
        })
    });
};

function bindDelConfirm() {
    $('#delconfirm').click(function() {
        var id = $('#delnid').val();
        // console.log(id);
        $.ajax({
            url: '/delchild/',
            type: 'POST',
            data: { 'id': id },
            async: false,
            success: function(arg) {
                if (arg.status) {
                    $('#delModal').modal('hide');
                    window.location.reload();
                }
            }
        });
    });
};

function bindDel() {
    $('#tb').on('click', '.del-row', function() {
        var did = $(this).parent().parent().attr('id');
        $('#delnid').val(did);
    });
};

function bindViewTrip() {
    $('#tb').on('click', '.linktrip', function() {
        var sid = $(this).parent().parent().attr('id');
        // console.log(sid);
        $.ajax({
            url: '/studentlinktrip/',
            type: 'GET',
            data: { 'sid': sid },
            success: function(arg) {
                if (arg.status) {
                    if (arg.message) {
                        $.alert({
                            title: arg.message,
                            icon: 'glyphicon glyphicon-exclamation-sign',
                            type: 'red',
                        });
                    } else {
                        top.location.href = '/confirmtrip/' + arg.url + '/';
                    }
                }
            }
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