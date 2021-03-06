from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('upload/', views.officer, name='officer'),
    path('csvfile/', views.csvfile, name='csvfile'),
    path('ajax_val/', views.ajax_val, name='ajax_val'),
    path('quit/', views.quit, name='quit'),
    path('children/', views.childinfo, name='childinfo'),
    path('schoolinfo/', views.schoolinfo, name='schoolinfo'),
    path('studentinschool/', views.studentinschool, name='studentinschool'),
    path('trip-staff/', views.tripstaff, name='tripstaff'),
    path('trip-driver/', views.tripdriver, name='tripdriver'),
    path('addchild/', views.addchild, name='addchild'),
    # path('chchild/', views.chchild, name='chchild'),
    path('delchild/', views.delchild, name='delchild'),
    path('newtrip/', views.newtrip, name='newtrip'),
    # path('tripschool/', views.tripschool, name='tripschool'),
    path('tripsave/', views.tripsave, name='tripsave'),
    # path('gettrip/', views.gettrip, name='gettrip'),
    path('confirmtrip/<str:tripid>/', views.confirmtrip, name='confirmtrip'),
    path('confirmtripsave/', views.confirmtripsave, name='confirmtripsave'),
    path('checktripsave/<str:tripid>/', views.checktripsave, name='checktripsave'),
    path('deltrip/', views.deltrip, name='deltrip'),
    # path('deltripstudent/', views.deltripstudent, name='deltripstudent'),
    # path('addtripstudent/', views.addtripstudent, name='addtripstudent'),
    path('starttrip/<str:tripid>/', views.starttrip, name='starttrip'),
    path('marktrip/', views.marktrip, name='marktrip'),
    path('archivedtrip/', views.archivedtrip, name='archivedtrip'),
    path('editarchivedtrip/<str:tripid>/', views.archivedtripview, name='archivedtripview'),
    path('archivedtripedit/', views.archivedtripedit, name='archivedtripedit'),
    path('studentlinktrip/', views.studentlinktrip, name='studentlinktrip'),
    path('reportview/', views.reportview, name='reportview'),
    path('reportsearch/', views.reportsearch, name='reportsearch'),
    path('download/', views.download, name='download'),
    path('downloadeach/<str:tripid>/', views.downloadeach, name='downloadeach'),
]
app_name = 'cornerstone'
