from django.shortcuts import render, redirect
import os
import json
from django.conf import settings
import csv
from django.http import HttpResponse
from .models import User
from .forms.login import StaffForm, ReportForm
from django.contrib.auth import authenticate, logout
from django.http import JsonResponse
from captcha.models import CaptchaStore
# from django.contrib.auth.decorators import login_required
import time
import datetime
import random
from .models import Child, Trip, Bus, Driver, School
from django.db.models import Count, Q
from django.core import serializers
from itertools import chain
# Create your views here.


def index(request):
    return render(request, 'cornerstone/index.html')


def officer(request):
    if request.session.get('isstaff', None):
        if request.session.get('isstaff') == 1:
            return render(request, 'cornerstone/upload.html')
    else:
        return render(request, 'cornerstone/404.html')


# def forbidden(request):
#     pass


def login(request):
    if request.session.get('islogin', None):
        return redirect('/index/')
    if request.method == 'POST':
        login_form = StaffForm(request.POST)
        message = 'Please check your input!'
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            passwd = login_form.cleaned_data['password']
            user = authenticate(username=username, password=passwd)
            if user is None:
                message = 'Incorrect username or password!'
                return render(request, 'cornerstone/login.html', {'message': message, 'login_form': login_form})
            else:
                userinfo = User.objects.get(username=username)
                token = str(time.time() + random.randrange(1, 10000))
                request.session['islogin'] = True
                request.session['id'] = userinfo.id
                request.session['name'] = userinfo.username
                request.session['token'] = token
                request.session['isstaff'] = userinfo.is_staff
                request.session['issuperuser'] = userinfo.is_superuser
                # firstname要和driver Model中的 driver_firstname保持一致
                request.session['firstname'] = userinfo.first_name
                request.session['lastname'] = userinfo.last_name
                # request.session.set_expiry(0)
                # 设置session的expirytime,如果为0，表示关闭浏览器，session就失效。
                # print('33333333')
                return redirect('/index/')
        else:
            return render(request, 'cornerstone/login.html', {'message': message, 'login_form': login_form})
    else:
        login_form = StaffForm()
        return render(request, 'cornerstone/login.html', {'login_form': login_form})


def quit(request):
    logout(request)
    return redirect('/index/')


def csvfile(request):
    if request.method == 'POST':
        if request.FILES.getlist('csvfile'):
            # 判断上传文件的后缀名必须是csv
            if request.FILES['csvfile'].name.split('.')[-1] == 'csv':
                # print(request.FILES['csvfile'].name.split('.')[-1])
                # print(request.FILES['csvfile'].name.split('.')[0])
                f = request.FILES['csvfile']
                # 防止文件名重复，文件名+当前时间重命名
                time1 = time.localtime(time.time())
                time2 = time.strftime('%Y-%m-%d-%H-%M-%S', time1)
                name = request.FILES['csvfile'].name.split(
                    '.')[0] + '_' + str(time2) + '.csv'
                # print(name)
                csvPath = os.path.join(settings.MEDIA_ROOT, name)
                # print(csvPath)
                # 文件保存
                with open(csvPath, 'wb') as f1:
                    for info in f.chunks():
                        # 文件流的形式上传，按段接受，每接收一段，存入到服务器端。
                        f1.write(info)
                # 读取文件数据并存入数据库
                infoList = []
                with open(csvPath, 'r') as f2:
                    info = csv.reader(f2)
                    for row in info:
                        infoList.append(row)
                # print(type(infoList))
                date = infoList[1][0].split()[-1]
                for x in range(3, len(infoList)):
                    child_firstname = infoList[x][0].split(' ')[0]
                    child_lastname = infoList[x][0].split(' ')[1]
                    # print(child_firstname)
                    # print(child_lastname)
                    list = infoList[x][1].split()
                    if len(list[-1].split(':')) > 1 or len(list[-1].split('.')) > 1:
                        p = list[-1]
                        pickup_time = date + ' ' + list[-1].replace('.', ':')
                        child_school = infoList[x][1].split(p)[0].strip()
                        School.objects.update_or_create(school_name=child_school, defaults={
                                                        'pickup_time': pickup_time})
                        Child.objects.update_or_create(child_firstname=child_firstname, child_lastname=child_lastname, child_school=School.objects.get(
                            school_name=child_school), defaults={'is_active': True, 'is_delete': False, 'on_trip': False, 'is_check': False})
                    else:
                        child_school = infoList[x][1].strip()
                        # pickup_time = ''
                        School.objects.update_or_create(
                            school_name=child_school, defaults={'pickup_time': date})
                        Child.objects.update_or_create(child_firstname=child_firstname, child_lastname=child_lastname, child_school=School.objects.get(
                            school_name=child_school), defaults={'is_active': True, 'is_delete': False, 'on_trip': False, 'is_check': False})
                if csvPath:
                    os.remove(csvPath)
                # if uploading and saving successful, then remove the file which in the server.
                return render(request, 'cornerstone/success.html')
            else:
                return HttpResponse('The file type must be .csv')
        else:
            return HttpResponse('Please select one file')
    else:
        return HttpResponse('upload failed')


def register(request):
    pass
    return render(request, 'cornerstone/login.html')


def ajax_val(request):
    if request.is_ajax():
        cs = CaptchaStore.objects.filter(
            response=request.GET['response'], hashkey=request.GET['hashkey'])
        if cs:
            json_data = {'status': 1}
        else:
            json_data = {'status': 0}
        return JsonResponse(json_data)
    else:
        # raise Http404
        json_data = {'status': 0}
        return JsonResponse(json_data)


def childinfo(request):
    if request.session.get('isstaff', None):
        if request.session.get('isstaff') == 1:
            childList = Child.objects.filter(
                is_delete=False).order_by('child_school')
            return render(request, 'cornerstone/children.html', {'child_list': childList})
        else:
            return render(request, 'cornerstone/404.html')
    else:
        return render(request, 'cornerstone/404.html')


def schoolinfo(request):
    if request.session.get('isstaff', None):
        schoolList = School.objects.values(
            'id', 'school_name', 'pickup_time').annotate(num=Count('child'))
        # schoolList = School.objects.values('id', 'school_name', 'pickup_time').filter(
        #     child__is_delete=False).annotate(num=Count('child'))
        return render(request, 'cornerstone/school.html', {'schoollist': schoolList})
    else:
        return render(request, 'cornerstone/404.html')


def studentinschool(request):
    response = {'status': True, 'message': None, 'data': None}
    try:
        sid = int(request.GET.get('sid'))
        # print(sid)
        studentList = Child.objects.filter(child_school__id=sid)
        # print(studentList)
        students = serializers.serialize('json', studentList)
        response['message'] = 'successful'
        response['data'] = students
    except Exception as e:
        response['status'] = False
        response['message'] = 'error'
    return JsonResponse(response)


def addchild(request):
    response = {'status': True, 'message': None, 'data': None}
    try:
        fn = request.POST.get('firstname')
        ln = request.POST.get('lastname')
        sc = request.POST.get('school')
        print(fn, ln, sc)
        # print(request.POST.get('isactive'))
        if Child.objects.filter(child_firstname=fn, child_lastname=ln, child_school__school_name=sc):
            response['message'] = "Child's info already exist"
            response['status'] = False
            # print('exist')
        else:
            School.objects.update_or_create(school_name=sc)
            new = Child(child_firstname=fn, child_lastname=ln, child_school=School.objects.get(
                school_name=sc), is_active=True, on_trip=False, is_check=False)
            new.save()
            response['message'] = 'ok'
            # print('save successful')
    except Exception as e:
        response['status'] = False
        response['message'] = 'input error'
    return JsonResponse(response)


def delchild(request):
    response = {'status': True, 'message': None, 'data': None}
    try:
        id = int(request.POST.get('id'))
        # print(id)
        # print(type(id))
        Child.objects.filter(pk=id).update(is_delete=True)
        response['message'] = 'successful'
    except Exception as e:
        response['status'] = False
        response['message'] = 'input error'
    return JsonResponse(response)


def tripstaff(request):
    if request.session.get('isstaff', None):
        tripList = Trip.objects.filter(
            is_active=True).order_by('trip_driver')
        for trip in tripList:
            trip.trip_school = json.loads(trip.trip_school)
            # print(type(trip.trip_school))
        return render(request, 'cornerstone/trip_staff.html', {'triplist': tripList})
    else:
        return render(request, 'cornerstone/404.html')


def tripdriver(request):
    if request.session.get('islogin', None) and not request.session.get('isstaff', None):
        name = request.session['name']
        id = request.session.get('id')
        did = Driver.objects.get(driver_user=int(id))
        tripList = Trip.objects.filter(
            trip_driver=did, is_active=True, is_check=False).order_by('trip_name')
        for trip in tripList:
            trip.trip_school = json.loads(trip.trip_school)
        return render(request, 'cornerstone/trip_driver.html', {'triplist': tripList, 'drivername': name})
    else:
        return render(request, 'cornerstone/404.html')


def newtrip(request):
    if request.session.get('isstaff', None):
        busList = Bus.objects.all()
        for bus in busList:
            if Bus.objects.get(bus_number=bus).trip_set.filter(is_active=True):
                bus.bus_number = bus.bus_number + '*' + \
                    str(len(Bus.objects.get(
                        bus_number=bus).trip_set.filter(is_active=True)))
        driverList = Driver.objects.all()
        for d in driverList:
            if Driver.objects.get(driver_firstname=d).trip_set.filter(is_active=True):
                d.driver_lastname = d.driver_lastname + '--' + \
                    str(len(Driver.objects.get(
                        driver_firstname=d).trip_set.filter(is_active=True))) + 'trip'
        schoolList = School.objects.values('id', 'school_name', 'pickup_time').filter(
            child__is_active=True, child__is_check=False, child__on_trip=False, child__is_delete=False).annotate(num=Count('child'))
        dateSchool = School.objects.values(
            'pickup_time').filter(child__is_delete=False)[0]
        date = dateSchool['pickup_time'].split()[0]
        return render(request, 'cornerstone/newtrip.html', {'buslist': busList, 'driverlist': driverList, 'schoollist': schoolList, 'date': date})
    else:
        return render(request, 'cornerstone/404.html')


def tripsave(request):
    if request.session.get('isstaff', None):
        if request.method == 'POST':
            response = {'status': True, 'message': None, 'data': None}
            try:
                bid = request.POST.get('bus')
                did = request.POST.get('driver')
                tname = request.POST.get('tname')
                # print(bid, did)
                # 拿出key列表并删除除去school名称意外的key
                keys = list(request.POST.keys())
                # print(keys)
                keys.remove('bus')
                keys.remove('driver')
                keys.remove('tname')
                schoolDict = {}
                for sid in keys:
                    snum = int(request.POST.get(sid))
                    sname = School.objects.get(pk=int(sid)).school_name
                    schoolDict[sname] = request.POST.get(sid)
                    childList = School.objects.get(
                        pk=int(sid)).child_set.filter(on_trip=False, is_active=True, is_check=False, is_delete=False)[:snum]
                    for child in childList:
                        child.on_trip = True
                        child.save()
                schoolDict = json.dumps(schoolDict)
                Trip.objects.create(trip_name=tname, trip_driver=Driver.objects.get(pk=int(
                    did)), trip_bus=Bus.objects.get(pk=int(bid)), trip_school=schoolDict, is_check=False, is_active=True)
                response['data'] = 'OK'
            except Exception as e:
                response['status'] = False
                response['message'] = 'error'
            return JsonResponse(response)
    else:
        return render(request, 'cornerstone/404.html')


# def gettrip(request):
#     if request.session.get('isstaff', None):
#         if request.method == 'GET':
#             response = {'status': True, 'message': None, 'data': None}
#             try:
#                 tripId = int(request.GET.get('id'))
#                 sList = list(
#                     set(list(Trip.objects.get(pk=tripId).trip_kids.values_list('child_school'))))
#                 schoolDict = {}
#                 for x in sList:
#                     schoolDict[x[0]] = list(Trip.objects.get(pk=tripId).trip_kids.filter(
#                         child_school=x[0]).values_list('child_firstname', 'child_lastname'))
#                 response['data'] = schoolDict
#                 response['message'] = 'OK'
#             except Exception as e:
#                 response['status'] = False
#                 response['message'] = 'error'
#             return JsonResponse(response)
#     else:
#         return render(request, 'cornerstone/404.html')


def deltrip(request):
    if request.session.get('isstaff', None):
        if request.method == 'POST':
            response = {'status': True, 'message': None, 'data': None}
            try:
                tid = int(request.POST.get('tid'))
                # print(tid)
                try:
                    schoolDict = Trip.objects.get(pk=tid).trip_school
                    schoolJson = json.loads(schoolDict)
                    for k in schoolJson:
                        num = int(schoolJson[k])
                        childList = School.objects.get(
                            school_name=k).child_set.filter(on_trip=True, is_check=False, is_active=True, is_delete=False)[:num]
                        for child in childList:
                            child.on_trip = False
                            child.save()
                    Trip.objects.get(pk=tid).delete()
                    response['data'] = 'OK'
                    response['message'] = 'OK'
                except Exception as e:
                    response['status'] = False
                    response['message'] = 'error'
            except Exception as e:
                response['status'] = False
                response['message'] = 'error'
            return JsonResponse(response)
    else:
        return render(request, 'cornerstone/404.html')


# def deltripstudent(request):
#     if request.session.get('isstaff', None):
#         if request.method == 'POST':
#             response = {'status': True, 'message': None, 'data': None}
#             try:
#                 studentId = int(request.POST.get('studentid'))
#                 tripId = int(request.POST.get('tripid'))
#                 # print(studentId)
#                 # print(tripId)
#                 Trip.objects.get(pk=tripId).trip_kids.remove(studentId)
#                 Child.objects.filter(pk=studentId).update(on_trip=False)
#                 response['data'] = 'deleted'
#                 response['message'] = 'OK'
#             except Exception as e:
#                 response['status'] = False
#                 response['message'] = 'error'
#             return JsonResponse(response)
#     else:
#         return render(request, 'cornerstone/404.html')


# def addtripstudent(request):
#     if request.session.get('isstaff', None):
#         if request.method == 'POST':
#             response = {'status': True, 'message': None, 'data': None}
#             try:
#                 addList = request.POST.getlist('addid')
#                 # print(addList)
#                 tripid = int(request.POST.get('tripid'))
#                 trip = Trip.objects.get(pk=tripid)
#                 for id in addList:
#                     trip.trip_kids.add(int(id))
#                     Child.objects.filter(pk=int(id)).update(on_trip=True)
#                 response['data'] = 'Add successfully'
#                 response['message'] = 'OK'
#             except Exception as e:
#                 response['status'] = False
#                 response['message'] = 'error'
#             return JsonResponse(response)
#     else:
#         return render(request, 'cornerstone/404.html')


def starttrip(request, tripid):
    if request.session.get('islogin', None):
        trip = Trip.objects.get(pk=int(tripid))
        trip.trip_school = json.loads(trip.trip_school)
        # 定义一个空的Queryset集合
        newQuery = School.objects.filter(pk=0)
        # 循环遍历字典，合并成一个集合
        for key in trip.trip_school:
            s = School.objects.filter(school_name=key)
            newQuery = chain(newQuery, s)
        return render(request, 'cornerstone/start_trip.html', {'trip': trip, 'schoollist': newQuery})
    else:
        return render(request, 'cornerstone/404.html')


def marktrip(request):
    if request.session.get('islogin', None):
        if request.method == 'POST':
            response = {'status': True, 'message': None, 'data': None}
            try:
                tripId = int(request.POST.get('tripid'))
                absentList = request.POST.getlist('absent')
                attendList = request.POST.getlist('attend')
                # print(tripId)
                # print(type(absentList))
                # print(type(attendList))
                # 将absent数据以id为key的方式存入字典
                absentKids = {}
                for a in absentList:
                    sid = a.split(',')[0]
                    status = a.split(',')[1]
                    tl = []
                    firstname = Child.objects.get(pk=int(sid)).child_firstname
                    lastname = Child.objects.get(pk=int(sid)).child_lastname
                    schoolname = Child.objects.get(
                        pk=int(sid)).child_school.school_name
                    tl.append(firstname)
                    tl.append(lastname)
                    tl.append(schoolname)
                    tl.append(status)
                    absentKids[sid] = tl
                    Child.objects.filter(pk=int(sid)).update(is_check=True)
                # print(absentKids)
                # print(type(absentKids))
                # 存储前将数据json dunpms化
                j = json.dumps(absentKids)
                t = Trip.objects.get(pk=tripId)
                t.absent_kids = j
                t.is_check = True
                for cid in attendList:
                    c = Child.objects.get(id=int(cid))
                    t.trip_kids.add(c)
                    c.is_check = True
                    c.save()
                t.save()
                response['data'] = 'successfully'
                response['message'] = 'OK'
            except Exception as e:
                response['status'] = False
                response['message'] = 'error'
            return JsonResponse(response)
    else:
        return render(request, 'cornerstone/404.html')


def confirmtrip(request, tripid):
    if request.session.get('isstaff', None):
        # print(type(tripid))
        try:
            trip = Trip.objects.get(pk=int(tripid))
            j = json.loads(trip.absent_kids)
            trip.absent_kids = j
            return render(request, 'cornerstone/confirm_trip.html', {'trip': trip})
        except Exception as e:
            return HttpResponse('error')
    else:
        return render(request, 'cornerstone/404.html')


def confirmtripsave(request):
    if request.session.get('isstaff', None):
        if request.method == 'POST':
            response = {'status': True, 'message': None, 'data': None}
            try:
                tid = request.POST.get('tid')
                sid = request.POST.get('sid')
                status = request.POST.get('status')
                t = Trip.objects.get(pk=int(tid))
                # print(tid, sid, status)
                if status == 'Attended':
                    # 判断trip_kids中是否存在，再拿出json数据，删除以sid为key的键值对;再将sid的数据添加到trip_kids;
                    if not t.trip_kids.filter(pk=int(sid)):
                        d = json.loads(t.absent_kids)
                        d.pop(sid, 'NotFound')
                        t.absent_kids = json.dumps(d)
                        t.trip_kids.add(int(sid))
                        t.save()
                else:
                    if t.trip_kids.filter(pk=int(sid)):
                        d = json.loads(t.absent_kids)
                        l1 = []
                        l1.append(Child.objects.get(
                            pk=int(sid)).child_firstname)
                        l1.append(Child.objects.get(
                            pk=int(sid)).child_lastname)
                        l1.append(Child.objects.get(
                            pk=int(sid)).child_school.school_name)
                        l1.append(status)
                        d[sid] = l1
                        t.absent_kids = json.dumps(d)
                        t.trip_kids.remove(int(sid))
                        t.save()
                    else:
                        d = json.loads(t.absent_kids)
                        l2 = d[sid]
                        l2[-1] = status
                        d[sid] = l2
                        t.absent_kids = json.dumps(d)
                        t.save()
                        # Trip.objects.filter(pk=int(tid)).update(absent_kids=d1)
                response['data'] = 'Successfully'
                response['message'] = 'OK'
            except Exception as e:
                response['status'] = False
                response['message'] = 'error'
            return JsonResponse(response)
    else:
        return render(request, 'cornerstone/404.html')


def checktripsave(request, tripid):
    if request.session.get('isstaff', None):
        try:
            Trip.objects.filter(pk=int(tripid)).update(is_active=False)
            t = Trip.objects.get(pk=int(tripid))
            t.trip_kids.all().update(is_active=False)
            absDict = json.loads(t.absent_kids)
            # print(absDict)
            # print(type(absDict))
            for k in absDict:
                Child.objects.filter(pk=int(k)).update(is_active=False)
            return redirect('/trip-staff/')
        except Exception as e:
            return HttpResponse('error')
    else:
        return render(request, 'cornerstone/404.html')


def archivedtrip(request):
    if request.session.get('isstaff', None):
        searchValue = ReportForm(request.GET)
        key = {}
        if searchValue.is_valid():
            try:
                start = request.GET.get('starttime')
                end = request.GET.get('endtime')
                student = request.GET.get('studentname')
                key['Start_time'] = start
                key['End_time'] = end
                startTime = datetime.date(
                    int(start.split('-')[0]), int(start.split('-')[1]), int(start.split('-')[2]))
                endTime = datetime.date(int(end.split(
                    '-')[0]), int(end.split('-')[1]), int(end.split('-')[2])) + datetime.timedelta(days=1)
                if student:
                    key['Student_name'] = student
                    if len(student.split()) > 1:
                        tripList1 = Trip.objects.filter(Q(trip_kids__child_firstname__icontains=student.split()[0]), Q(
                            trip_kids__child_lastname__icontains=student.split()[1]), date_changed__range=(startTime, endTime), is_active=False)
                        tripList2 = Trip.objects.filter(Q(absent_kids__icontains=student.split()[0]), Q(
                            absent_kids__icontains=student.split()[1]), date_changed__range=(startTime, endTime), is_active=False)
                        tripList = chain(tripList1, tripList2)
                        leng = len(tripList1) + len(tripList2)
                        # print(tripList1)
                        # print(tripList2)
                    else:
                        tripList1 = Trip.objects.filter(Q(trip_kids__child_firstname__icontains=student) | Q(
                            trip_kids__child_lastname__icontains=student), date_changed__range=(startTime, endTime), is_active=False)
                        tripList2 = Trip.objects.filter(absent_kids__icontains=student, date_changed__range=(
                            startTime, endTime), is_active=False)
                        tripList = chain(tripList1, tripList2)
                        leng = len(tripList1) + len(tripList2)
                        # print(tripList)
                else:
                    tripList = Trip.objects.filter(
                        date_changed__range=(startTime, endTime), is_active=False)
                    leng = len(tripList)
                return render(request, 'cornerstone/archived_trip.html', {'triplist': tripList, 'key': key, 'leng': leng})
            except Exception as e:
                return HttpResponse('error')
        else:
            try:
                now = datetime.datetime.now()
                tripList = Trip.objects.filter(
                    is_active=False, date_changed__month=now.month)
                return render(request, 'cornerstone/archived_trip.html', {'triplist': tripList})
            except Exception as e:
                return HttpResponse('error')
    else:
        return render(request, 'cornerstone/404.html')


def archivedtripview(request, tripid):
    if request.session.get('isstaff', None):
        try:
            trip = Trip.objects.get(pk=int(tripid))
            data1 = trip.absent_kids
            absdict = json.loads(data1)
            return render(request, 'cornerstone/archived_trip_edit.html', {'trip': trip, 'absdict': absdict})
        except Exception as e:
            return HttpResponse('error')
    else:
        return render(request, 'cornerstone/404.html')


def archivedtripedit(request):
    if request.session.get('isstaff', None):
        if request.method == 'POST':
            response = {'status': True, 'message': None, 'data': None}
            try:
                tid = request.POST.get('tid')
                sid = request.POST.get('sid')
                status = request.POST.get('status')
                t = Trip.objects.get(pk=int(tid))
                # print(tid, sid, status)
                if status == 'Attended':
                    # 判断trip_kids中是否存在，再拿出json数据，删除以sid为key的键值对;再将sid的数据添加到trip_kids;
                    if not t.trip_kids.filter(pk=int(sid)):
                        d = json.loads(t.absent_kids)
                        d.pop(sid, 'NotFound')
                        # 使用update更新数据，不会修改date_changed的时间，下同
                        Trip.objects.filter(pk=int(tid)).update(
                            absent_kids=json.dumps(d))
                        Trip.objects.get(
                            pk=int(tid)).trip_kids.add(int(sid))
                        # t.absent_kids = json.dumps(d)
                        # t.trip_kids.add(int(sid))
                        # t.save()
                else:
                    if t.trip_kids.filter(pk=int(sid)):
                        d = json.loads(t.absent_kids)
                        l1 = []
                        l1.append(Child.objects.get(
                            pk=int(sid)).child_firstname)
                        l1.append(Child.objects.get(
                            pk=int(sid)).child_lastname)
                        l1.append(Child.objects.get(
                            pk=int(sid)).child_school.school_name)
                        l1.append(status)
                        d[sid] = l1
                        Trip.objects.filter(pk=int(tid)).update(
                            absent_kids=json.dumps(d))
                        Trip.objects.get(
                            pk=int(tid)).trip_kids.remove(int(sid))
                        # t.absent_kids = json.dumps(d)
                        # t.trip_kids.remove(int(sid))
                        # t.save()
                    else:
                        d = json.loads(t.absent_kids)
                        l2 = d[sid]
                        l2[-1] = status
                        d[sid] = l2
                        Trip.objects.filter(pk=int(tid)).update(
                            absent_kids=json.dumps(d))
                        # t.absent_kids = json.dumps(d)
                        # t.save()
                response['data'] = 'Successfully'
                response['message'] = 'OK'
            except Exception as e:
                response['status'] = False
                response['message'] = 'error'
            return JsonResponse(response)
    else:
        return render(request, 'cornerstone/404.html')


def studentlinktrip(request):
    if request.session.get('isstaff', None):
        response = {'status': True, 'message': None, 'url': None}
        try:
            sid = request.GET.get('sid')
            if Trip.objects.filter(trip_kids__pk=int(sid), is_active=True):
                tid = Trip.objects.get(
                    trip_kids__pk=int(sid), is_active=True).id
            elif Trip.objects.filter(~Q(trip_kids__pk=int(sid)) | Q(absent_kids__contains=sid), is_active=True):
                tid = Trip.objects.get(~Q(trip_kids__pk=int(sid)) | Q(
                    absent_kids__contains=sid), is_active=True).id
            response['url'] = tid
            response['message'] = False
        except Exception as e:
            response['status'] = False
            response['message'] = 'error'
        return JsonResponse(response)
    else:
        return render(request, 'cornerstone/404.html')


def reportview(request):
    if request.session.get('isstaff', None):
        return render(request, 'cornerstone/report.html')
    else:
        return render(request, 'cornerstone/404.html')


def reportsearch(request):
    if request.session.get('isstaff', None):
        response = {'status': True, 'message': None, 'data': None}
        try:
            start = request.GET.get('start')
            end = request.GET.get('end')
            startTime = datetime.date(
                int(start.split('-')[0]), int(start.split('-')[1]), int(start.split('-')[2]))
            endTime = datetime.date(int(end.split(
                '-')[0]), int(end.split('-')[1]), int(end.split('-')[2])) + datetime.timedelta(days=1)
            tripData = Trip.objects.filter(
                date_changed__range=(startTime, endTime), is_active=False)
            trips = serializers.serialize('json', tripData)
            response['data'] = trips
            response['message'] = 'success'
        except Exception as e:
            response['status'] = False
            response['message'] = 'error'
        return JsonResponse(response)
    else:
        return render(request, 'cornerstone/404.html')


def download(request):
    if request.session.get('isstaff', None):
        try:
            start = request.GET.get('start')
            end = request.GET.get('end')
            # print(start, end)
            startTime = datetime.date(
                int(start.split('-')[0]), int(start.split('-')[1]), int(start.split('-')[2]))
            endTime = datetime.date(
                int(end.split('-')[0]), int(end.split('-')[1]), int(end.split('-')[2]))
            filename = 'Attendance for ' + start + '_' + end + '.csv'
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = "attachment; filename=" + filename
            writer = csv.writer(response)
            writer.writerow(['Cornerstone Care - After School'])
            writer.writerow(['Attendance for ' + start + '_' + end])
            timeList = ['']
            weekList = ['Student Name']
            weekdayList = ['Monday', 'Tuesday', 'Wednesday',
                           'Thursday', 'Friday', 'Saturday', 'Sunday']
            for x in range((endTime - startTime).days + 1):
                day = startTime + datetime.timedelta(days=x)
                timeList.append(day)
                dayWeek = weekdayList[day.weekday()]
                weekList.append(dayWeek)
            writer.writerow(timeList)
            writer.writerow(weekList)
            studentList = Child.objects.all()
            for kid in studentList:
                kidList = []
                kidList.append(kid.child_firstname+' '+kid.child_lastname)
                for x in range((endTime - startTime).days + 1):
                    day = startTime + datetime.timedelta(days=x)
                    y = int(str(day).split('-')[0])
                    m = int(str(day).split('-')[1])
                    d = int(str(day).split('-')[2])
                    if Trip.objects.filter(date_changed__year=y, date_changed__month=m, date_changed__day=d, trip_kids__pk=kid.id, is_active=False):
                        kidList.append('Y')
                    else:
                        kidList.append('')
                    # elif Trip.objects.filter(Q(absent_kids__contains=str(kid.id)), Q(absent_kids__contains=kid.child_firstname), Q(absent_kids__contains=kid.child_lastname), Q(absent_kids__contains=kid.child_school.school_name),
                    # date_changed__contains=day, is_active=False):
                writer.writerow(kidList)
            return response
        except Exception as e:
            return HttpResponse('error')
    else:
        return render(request, 'cornerstone/404.html')


def downloadeach(request, tripid):
    if request.session.get('isstaff', None):
        tid = int(tripid)
        try:
            trip = Trip.objects.get(pk=tid)
            filename = 'Attendance for ' + trip.trip_name + '.csv'
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = "attachment; filename=" + filename
            writer = csv.writer(response)
            writer.writerow(['Cornerstone Care - After School'])
            writer.writerow(['Attendance for ' + trip.trip_name])
            timeStr = trip.trip_name.split('-')
            time = datetime.date(int(timeStr[0]), int(
                timeStr[1]), int(timeStr[2]))
            timeList = ['']
            weekList = ['Student Name']
            weekdayList = ['Monday', 'Tuesday', 'Wednesday',
                           'Thursday', 'Friday', 'Saturday', 'Sunday']
            timeList.append(time)
            weekList.append(weekdayList[time.weekday()])
            writer.writerow(timeList)
            writer.writerow(weekList)
            studentList = Child.objects.all()
            for kid in studentList:
                kidList = []
                kidList.append(kid.child_firstname+' '+kid.child_lastname)
                if Trip.objects.filter(trip_kids__pk=kid.id, is_active=False):
                    kidList.append('Y')
                else:
                    kidList.append('')
                writer.writerow(kidList)
            return response
        except Exception as e:
            return HttpResponse('error')
    else:
        return render(request, 'cornerstone/404.html')
