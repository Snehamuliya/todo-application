from django.contrib import admin
from django.urls import path
from list.views import index, signup, login, logout, account, up_acc, admin_log
from list.views import t_view, todo_list,alogout,remind,a_act,a_remi,r_view

urlpatterns = [
    path('', index),
    path('signup', signup),
    path('login', login, name='log'),
    path('logout', logout),
    path('acc', account),
    path('up_account', up_acc, name='update'),
    path('alogin', admin_log, name='alog'),
    path('tasks', todo_list),
    path('tview', t_view, name='ta_view'),
    path('alogout', alogout),
    path('reminder', remind),
    path('ad_activity', a_act, name='ad_task'),
    path('ad_reminder', a_remi, name='ad_rem'),
    path('rview', r_view, name='re_view')
]
