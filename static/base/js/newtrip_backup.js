$(document).ready(function() {
    // 时间选择初始化
    $("#datetimepicker1").datetimepicker({
        format: 'yyyy-mm-dd H:ii P',
        todayBtn: true,
        autoclose: true,
        showMeridian: true,
        startView: 1,
        minView: 0,
    });
    // 默认只允许学校select向下拉。
    $('#school').selectpicker({
        dropupAuto: false,
    });
    // 为时间选择绑定事件，监听选择框。
    // 同时将按时间筛选的可用bus的结果返回到bus选择框
    $('#timeinput').on('change', function() {
        // var time = $('#timeinput').val()
        // console.log($.type(time))
        // 修改trip时间，school下拉菜单和学生显示均会被重置。
        $('#school').attr('lang', '0');
        $('#schoolbar').empty();
        var getData = {};
        getData['picktime'] = $('#timeinput').val()
            // console.log(typeof(getData));
        $.ajax({
            url: '/checktime/',
            type: 'GET',
            data: getData,
            success: function(arg) {
                // console.log(arg.schooldata);
                if (arg.status) {
                    // console.log(arg);
                    // console.log($.type(arg.data));
                    $('#bus').empty();
                    $('#driver').empty();
                    $('#school').empty();
                    // 每次添加之前先删除子元素
                    for (var key in arg.busdata) {
                        $('#bus').append("<option>" + key + "--" + arg.busdata[key] + "</option>");
                        // console.log(key)
                        // console.log(arg.busdata[key])
                    };
                    // bootstrap的selectpicker要手动刷新，不然不会显示新添加的内容
                    $('#bus').selectpicker('refresh');
                    $('#bus').selectpicker('render');
                    for (var i in arg.driverdata) {
                        $('#driver').append("<option>" + arg.driverdata[i] + "</option>")
                    };
                    $('#driver').selectpicker('refresh');
                    $('#driver').selectpicker('render');
                    // window.location.reload();
                    for (var x in arg.schooldata) {
                        $('#school').append("<option>" + arg.schooldata[x][0] + "--" + arg.schooldata[x][1] + "</option>")
                    }
                    $('#school').selectpicker('refresh');
                    $('#school').selectpicker('render');
                };
            },
        });
    });
    schoolBarReset();

    // when change the bus selector then reset the school selector.
    function schoolBarReset() {
        $('#bus').on('change', function() {
            $('#school').selectpicker('val', ['noneSelectedText']);
            $("#school").selectpicker('refresh');
            $('#schoolbar').empty();
        });
    };
    check();

    function check() {
        $('#school').on('change', function() {
            var a = $('#school').val();
            // 定义ajax请求数据变量，请求查询关键字段是school名称；
            var school = {};
            var schoolarr = new Array();
            // 循环读取school name；
            for (x in a) {
                // num += Number(a[x].split('--')[1]);
                schoolarr.push(a[x].split('--')[0]);
                // console.log(num);
            };
            // 将arry对象json化，便于后端读取数据；
            // console.log(JSON.stringify(schoolarr));
            school['school'] = schoolarr;
            // console.log(school);
            // console.log(typeof(school));
            $.ajax({
                url: '/tripschool/',
                type: 'GET',
                data: school,
                traditional: true,
                success: function(arg) {
                    if (arg.status) {
                        // console.log('OK');
                        // console.log(arg.data);
                        $('#schoolbar').empty();
                        for (var key in arg.data) {
                            $('#schoolbar').append('<label id="' + key + '" class="text-primary">' + key + '</label><br>')
                            for (var x in arg.data[key]) {
                                // console.log(arg.data[key][x])
                                var name = '';
                                for (y in arg.data[key][x]) {
                                    name += (arg.data[key][x][y] + ' ')
                                };
                                // 格式化字符串去掉前后的空格
                                var name1 = $.trim(name);
                                $('#schoolbar').append('<span><input name="' + key + '" type="checkbox" value="' + name1 + '" />' + name1 + '</span><br>')
                                    // console.log(name)
                                    // name,name1变量每次使用完后删除。
                                delete name;
                                delete name1;
                            }
                            $('#schoolbar').append('<hr>')
                        };
                    };
                },
            });
            // var num = $("input[type='checkbox']:checked").length;
            // console.log(num);
            // if (num > seats) {
            //     $('#schoolbar').empty();
            //     $('#span3').remove();
            //     $('#span2').remove();
            //     $('#span1').append('<span id="span2" class="text-danger"> &nbsp;&nbsp; Invalid! Seats : ' + seats + ',  but Kids: ' + num + '</span>');
            // } else {
            //     $('#span2').remove();
            //     $('#span3').remove();
            //     $('#span1').append('<span id="span3" class="text-primary"> &nbsp;&nbsp; Seats : ' + seats + ', Kids: ' + num + '</span>');
            // }
        });
    };
    checkbox();

    function checkbox() {
        var busseats = 0;
        $('#bus').on('change', function() {
            busseats = $('#bus').val().split('--')[1];
            // console.log(busseats);
        });
        $('#schoolbar').on('change', function() {
            var num = $("input[type='checkbox']:checked").length;
            // console.log(num);
            var seats = Number(busseats);
            if (num >= seats) {
                $("input[type='checkbox']:not(:checked)").attr('disabled', true);
                // alert('Invalid! Seat overflow!');
                // $('#schoolbar').empty();
                // $('#span3').remove();
                // $('#span2').remove();
                // $('#span1').append('<span id="span2" class="text-danger"> &nbsp;&nbsp; Invalid! Seats : ' + seats + ',  but Kids: ' + num + '</span>');
            } else {
                $("input[type='checkbox']").attr('disabled', false);
                // $('#span2').remove();
                // $('#span3').remove();
                // $('#span1').append('<span id="span3" class="text-primary"> &nbsp;&nbsp; Seats : ' + seats + ', Kids: ' + num + '</span>');
            }
        });
    };
    confirm();
    var schoollist = {};
    var triptime = '';
    var busname = '';
    var busseats = '';
    var drivername = '';
    var tripname = '';
    var students = '';

    function confirm() {
        $('#create').on('click', function() {
            var time = $('#timeinput').val();
            var bus = $('#bus').val();
            var driver = $('#driver').val();
            var school = $('#school').val();
            var checkedbox = $("input[type='checkbox']:checked").length;
            // console.log(time);
            // console.log(bus);
            // console.log(driver);
            // console.log(school);
            // console.log(checkedbox);
            // 为modal框添加选中的信息。
            delete triptime;
            delete busname;
            delete busseats;
            delete drivername;
            delete tripname;
            delete students;
            triptime = $('#timeinput').val();
            busname = $('#bus').val().split('--')[0];
            busseats = $('#bus').val().split('--')[1];
            drivername = $('#driver').val();
            tripname = triptime + '-' + busname;
            students = checkedbox;
            // console.log(triptime);
            // console.log(busname);
            // console.log(drivername);
            $('#tripnamespan').remove();
            $('#busnamespan').remove();
            $('#busseatsspan').remove();
            $('#drivernamespan').remove();
            $('#studentsspan').remove();
            $('#tripname').after('<span id="tripnamespan">' + '&nbsp;&nbsp;' + tripname + '</span>');
            $('#busname').after('<span id="busnamespan">' + '&nbsp;&nbsp;' + busname + '</span>');
            $('#busseats').after('<span id="busseatsspan">' + '&nbsp;&nbsp;' + busseats + '</span>');
            $('#drivername').after('<span id="drivernamespan">' + '&nbsp;&nbsp;' + drivername + '</span>');
            $('#students').after('<span id="studentsspan">' + '&nbsp;&nbsp;' + students + '</span>');
            // 判断所有的下拉菜单都必须有选择值，若没有，弹出警告。
            if (time == false || bus == false || driver == false || school == false) {
                swal({
                    title: 'All selections require at least one selected value.',
                    type: 'warning',
                    width: '40%'
                });
            } else {
                var seats = parseInt(bus.split('--')[1]);
                if (checkedbox >= 1 && checkedbox < seats) {
                    swal({
                        title: 'Make sure the selected bus has enough kids.',
                        type: 'warning',
                        width: '40%'
                    });
                    $('#confirmModal').modal('toggle');
                } else if (checkedbox < 1) {
                    swal({
                        title: 'You have not chosen any student!',
                        type: 'warning',
                        width: '40%'
                    });
                } else {
                    $('#confirmModal').modal('toggle');
                }
            };
            // 定义学校列表，学生列表，嵌套each循环取出被选中的学校及学生名。
            // schoollist是一个字典，key是学校名称，value是一个array包含了该学校的所有被选中的学生。
            // schoollist是一个全局变量，因为在ajax请求时也要使用，所有在给schoollist赋值前，先清空它的值;
            delete schoollist;
            $('#schoolbar').find('label').each(function() {
                // 区分两次each嵌套中的this。
                var labelthis = $(this).text();
                schoollist[labelthis] = new Array();
                // 选中name=labelthis且checked的所有checkbox，使用each将其添加到一个array中。
                $('input:checkbox[name="' + labelthis + '"]:checked').each(function() {
                    var inputthis = $(this).val();
                    // console.log(inputthis);
                    schoollist[labelthis].push(inputthis);
                });
            });

        });
    };
    create();

    function create() {
        $('#submit').on('click', function() {
            // console.log(schoollist);
            schoollist['tripname'] = tripname;
            schoollist['tripbus'] = busname;
            schoollist['tripdriver'] = drivername;
            schoollist['triptime'] = triptime;
            // console.log(schoollist);
            $.ajax({
                url: '/tripsave/',
                type: 'POST',
                data: schoollist,
                traditional: true,
                async: false,
                success: function(arg) {
                    if (arg.status) {
                        // console.log('ok');
                        // alert('Saved successful, go to "Manage Trip" and view the newtrip');
                        // window.location.reload();
                        // 请求成功，跳转到manage trip页面；
                        top.location.href = "/trip-info/";
                    } else {
                        swal({
                            title: 'Request failure!',
                            type: 'warning',
                            width: '40%'
                        });
                        window.location.reload();
                    }
                },
            });
        });
    };
})