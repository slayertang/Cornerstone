$(document).ready(function() {
    // attend列事件；点击会重置absent列，并实现attend列显示信息的切换。
    $("#tb").on('click', '.attend', function() {
        var t = $(this).text();
        if (t == 'Confirm?') {
            // console.log($(this).parent().next().find('select').selectpicker('val'));
            // 若点击attend下的按钮，absent下拉菜单自动重置为空。
            $(this).parent().next().find('select').selectpicker('val', '');
            $(this).text('Boarded');
            $(this).removeClass('btn-info');
            $(this).addClass('btn-success');
            $(this).toggleClass('active');
            // $(this).addClass('active');
            $(this).button('toggle');
        } else {
            $(this).text('Confirm?');
            $(this).removeClass('btn-success');
            $(this).addClass('btn-info');
            $(this).toggleClass('active');
            // $(this).removeClass('active');
            $(this).button('toggle');
        }
    });
    // absent列事件；点击后会重置attend列。
    $("#tb").on('click', '.absent', function() {
        var v = $(this).find('.absent').selectpicker('val');
        var t = $(this).parent().prev().find('button').text();
        // console.log(t);
        // console.log(v)
        if (v) {
            // console.log('true');
        } else {
            if (t == 'Confirm?') {} else {
                $(this).parent().prev().find('button').text('Confirm?');
                $(this).parent().prev().find('button').removeClass('btn-success');
                $(this).parent().prev().find('button').addClass('btn-info');
                $(this).parent().prev().find('button').addClass('active');
                $(this).parent().prev().find('button').button('toggle');
            }
        }
    });
    var schoolDict = {};
    schoolCheck();

    function schoolCheck() {
        $('#students').find('.school').each(function() {
            var s = $(this).attr('value').split(':');
            schoolDict[s[0]] = s[1];
        });
        // console.log('schoolDict:', schoolDict);
    };
    color();

    function color() {
        var colorlist = new Array()
        colorlist[0] = '#239B56';
        colorlist[1] = '#B7950B';
        colorlist[2] = '#76448A';
        colorlist[3] = '#2874A6';
        colorlist[4] = '#148F77';
        var sn = 0;
        $.each(schoolDict, function(k) {
            if (sn > 4) {
                sn = 0;
                $('#tb td[na="' + k + '"]').each(function() {
                    $(this).attr('bgcolor', colorlist[sn]);
                });
                sn++;
            } else {
                $('#tb td[na="' + k + '"]').each(function() {
                    $(this).attr('bgcolor', colorlist[sn]);
                });
                sn++;
            }
        });
    };
    saveButton();
    // savebutton事件，检查每一列absent和attend。
    function saveButton() {
        $('#savebutton').on('click', function() {
            var data = {};
            var abs = new Array();
            var att = new Array();
            var flag = false;
            $.each(schoolDict, function(k, v) {
                // console.log(k, v);
                var n = 0;
                $('#tb td[na="' + k + '"]').each(function() {
                    var id = $(this).parent().attr('id');
                    var attend = $(this).parent().find('.attend').text();
                    var absent = $(this).parent().find('select').selectpicker('val');
                    var l = new Array();
                    if (attend == 'Boarded') {
                        att.push(id);
                        n++;
                    } else if (absent) {
                        l.push(id);
                        l.push(absent);
                        abs.push(l);
                        n++;
                    }
                });
                // console.log(n);
                if (n === Number(v)) {
                    flag = true;
                    return true;
                } else if (n > Number(v)) {
                    $.alert({
                        title: k,
                        content: 'Need:' + v + '  Marked:' + n,
                        icon: 'glyphicon glyphicon-exclamation-sign',
                        type: 'red',
                    });
                    flag = false;
                    return false;
                } else {
                    $.alert({
                        title: 'School: ' + k,
                        content: 'Need:' + v + '  Marked:' + n,
                        icon: 'glyphicon glyphicon-exclamation-sign',
                        type: 'red',
                    });
                    flag = false;
                    return false;
                }
            });
            // console.log('abs:', abs);
            // console.log('att:', att);
            // console.log('flag:', flag);
            if (flag) {
                var tid = $('#tripname').attr('nid');
                data['attend'] = att;
                data['absent'] = abs;
                data['tripid'] = tid;
                // console.log(data);
                $.ajax({
                    url: '/marktrip/',
                    type: 'POST',
                    data: data,
                    traditional: true,
                    async: false,
                    success: function(arg) {
                        if (arg.status) {
                            top.location.href = "/trip-driver/";
                        } else {
                            $.alert({
                                title: 'Request failure.',
                                content: 'Please try again.',
                            });
                            window.location.reload();
                        }
                    },
                });
            }
        });
    };
})