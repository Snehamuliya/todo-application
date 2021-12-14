import time

from django.shortcuts import render, redirect
from django.http import HttpResponse
import pyodbc
from plyer import notification
import datetime


def index(request):
    if request.method == "GET":
        data = {}
        data['s_user'] = request.session.get('user')
        print(request.session.get('user'))
        return render(request, 'index.html', data)
    else:
        return render(request, 'index.html')


def signup(request):
    conn = pyodbc.connect('driver={sql server};'
                          'server=LAPTOP-3NNS80C3\SQLEXPRESS;'
                          'database=pysql;'
                          'Trusted_Connection=yes')
    if request.method == "GET":
        data = {}
        data['s_user'] = request.session.get('user')
        return render(request, 'signup.html', data)
    else:
        name = request.POST.get('fname')
        address = request.POST.get('add')
        email = request.POST.get('mail')
        mobile = request.POST.get('num')
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        error_msg = None

        if len(username) < 3:
            error_msg = 'username name should be more then 3 character'
        elif not password:
            error_msg = 'password is required !'
        elif len(password) < 4:
            error_msg = 'first name should be more then 4 character'

        if not error_msg:
            cursor = conn.cursor()
            cursor.execute("insert into signup values ('" + name + "','" + address + "','" + email + "','" + mobile + "','" + username + "','" + password + "')")
            cursor.commit()
            return render(request, 'signup.html')
        else:
            return render(request, 'signup.html', {'error': error_msg})


def login(request):
    conn = pyodbc.connect('driver={sql server};'
                          'server=LAPTOP-3NNS80C3\SQLEXPRESS;'
                          'database=pysql;'
                          'Trusted_Connection=yes')
    #if request.method == "POST" : this method also get used
    print(request.session.get('user'))
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        if 'log' in request.POST:
            name = request.POST.get('uname')
            passw = request.POST.get('pass')
            cursor = conn.cursor()
            cursor.execute("select * from signup where username='" + name + "' and password ='" + passw + "'")
            #rows_affected = cursor.rowcount
            tempvar = cursor.fetchall()
            rowcount = len(tempvar)
            print(rowcount)

            if rowcount > 0:
                request.session['user'] = name
                data = {}
                data['s_user'] = request.session.get('user')
                return render(request, 'header.html', data)

            else:
                msg = 'invalid username or password'
                return render(request, 'login.html', {'emsg': msg})
        else:
            return render(request, 'login.html')


def logout(request):
    #request.session.clear()
    del request.session['user']
    return redirect('log')


def account(request):
    conn = pyodbc.connect('driver={sql server};'
                          'server=LAPTOP-3NNS80C3\SQLEXPRESS;'
                          'database=pysql;'
                          'Trusted_Connection=yes')
    ab = request.session.get('user')
    cursor = conn.cursor()
    cursor.execute("select * from signup where username='" + ab + "'")
    #result = cursor.fetchall()
    data = {}
    data['s_user'] = request.session.get('user')
    data['result'] = cursor.fetchall()
    return render(request, 'account.html', data)


def up_acc(request):
    conn1 = pyodbc.connect('driver={sql server};'
                          'server=LAPTOP-3NNS80C3\SQLEXPRESS;'
                          'database=pysql;'
                          'Trusted_Connection=yes')
    data = {}
    data['s_user'] = request.session.get('user')
    if request.method == "GET":
        ab = request.session.get('user')
        cursor1 = conn1.cursor()
        cursor1.execute("select * from signup where username='" + ab + "'")
        # result = cursor.fetchall()
        data['result'] = cursor1.fetchall()
        return render(request, 'uaccount.html', data)
    else:
        if 'up_account' in request.POST:
            ab = request.session.get('user')
            name = request.POST.get('uname')
            add = request.POST.get('add')
            email = request.POST.get('mail')
            mno = request.POST.get('no')
            upass = request.POST.get('pass')
            cursor = conn1.cursor()
            cursor.execute("UPDATE signup SET name ='" + name + "',address ='" + add + "',email ='" + email + "',mobile ='" + mno + "',password ='" + upass + "' where username='" + ab + "'")
            cursor.commit()
            return redirect('update')


def todo_list(request):
    conn = pyodbc.connect('driver={sql server};'
                          'server=LAPTOP-3NNS80C3\SQLEXPRESS;'
                          'database=pysql;'
                          'Trusted_Connection=yes')
    data = {}
    data['s_user'] = request.session.get('user')
    if request.method == "GET":
        return render(request, 'task.html', data)
    else:
        tasks = request.POST.get('tas')
        info = request.POST.get('det')
        sdate = request.POST.get('start')
        edate = request.POST.get('end')
        prio = request.POST.get('pri')
        user = request.session.get('user')
        #return HttpResponse(tasks + info + sdate + edate + prio + user)
        cursor = conn.cursor()
        cursor.execute("insert into activity values ('" + tasks + "','" + info + "','" + sdate + "','" + edate + "','" + prio + "','" + user + "')")
        cursor.commit()
        return render(request, 'task.html',data)

        #next to me


def t_view(request):
    conn = pyodbc.connect('driver={sql server};'
                          'server=LAPTOP-3NNS80C3\SQLEXPRESS;'
                          'database=pysql;'
                          'Trusted_Connection=yes')
    ab = request.session.get('user')
    data = {}
    data['s_user'] = request.session.get('user')
    if request.method == "GET":
        cursor = conn.cursor()
        cursor.execute("select * from activity where [user]='" + ab + "'")
        data['result1'] = cursor.fetchall()
        return render(request, 'tasksview.html', data)
    else:
        if 'upd' in request.POST:
            cursor = conn.cursor()
            uid = request.POST.get('ta_upd')
            cursor.execute("select * from activity where id='" + uid + "'")
            data['result1'] = cursor.fetchall()
            return render(request, 'utask.html', data)
        if 'up_task' in request.POST:
            user = request.session.get('user')
            tid = request.POST.get('t_id')
            task = request.POST.get('task')
            tinfo = request.POST.get('info')
            start_date = request.POST.get('start')
            end_date = request.POST.get('end')
            pri = request.POST.get('prio')
            print(user , task , tinfo , start_date , end_date , pri)
            cursor = conn.cursor()
            cursor.execute("UPDATE activity SET task ='" + task + "',information ='" + tinfo + "',sdate ='" + start_date + "',edate ='" + end_date + "',priority ='" + pri + "' where id='" + tid + "'")
            cursor.commit()
            return redirect('ta_view')
        if 'del' in request.POST:
            did = request.POST.get('ta_del')
            cursor = conn.cursor()
            cursor.execute("delete from activity where id ='" + did + "'")
            cursor.commit()
            """ here cursor.commit() is very important because it commit is used to tell the database
            to save all the changes in the current transaction."""
            return redirect('ta_view')


def account(request):
    conn = pyodbc.connect('driver={sql server};'
                          'server=LAPTOP-3NNS80C3\SQLEXPRESS;'
                          'database=pysql;'
                          'Trusted_Connection=yes')
    ab = request.session.get('user')
    cursor = conn.cursor()
    cursor.execute("select * from signup where username='" + ab + "'")
    #result = cursor.fetchall()
    data = {}
    data['s_user'] = request.session.get('user')
    data['result'] = cursor.fetchall()
    return render(request, 'account.html', data)


def remind(request):
    conn = pyodbc.connect('driver={sql server};'
                          'server=LAPTOP-3NNS80C3\SQLEXPRESS;'
                          'database=pysql;'
                          'Trusted_Connection=yes')
    data = {}
    data['s_user'] = request.session.get('user')
    if request.method == "GET":
        return render(request, 'reminder.html', data)
    else:
        tasks = request.POST.get('tas')
        info = request.POST.get('det')
        sdate = request.POST.get('start')
        hour = request.POST.get('htime')
        min = request.POST.get('mtime')
        ampm = request.POST.get('am')
        user = request.session.get('user')
        # return HttpResponse(tasks + info + sdate + hour + min + ampm + user)
        cursor = conn.cursor()
        cursor.execute("insert into reminder values ('" + tasks + "','" + info + "','" + sdate + "','" + hour + "','" + min + "','" + ampm + "','" + user + "')")
        cursor.commit()

        return render(request, 'reminder.html',data)

        #next to me


def r_view(request):
    conn = pyodbc.connect('driver={sql server};'
                          'server=LAPTOP-3NNS80C3\SQLEXPRESS;'
                          'database=pysql;'
                          'Trusted_Connection=yes')
    ab = request.session.get('user')
    data = {}
    data['s_user'] = request.session.get('user')
    if request.method == "GET":
        cursor = conn.cursor()
        cursor.execute("select * from reminder where username='" + ab + "'")
        data['result1'] = cursor.fetchall()
        return render(request, 'reminderview.html', data)
    else:
        if 'upd' in request.POST:
            cursor = conn.cursor()
            uid = request.POST.get('ta_upd')
            cursor.execute("select * from reminder where id='" + uid + "'")
            data['result1'] = cursor.fetchall()
            return render(request, 'up_reminder.html', data)
        if 'up_task' in request.POST:
            user = request.session.get('user')
            rid = request.POST.get('r_id')
            task = request.POST.get('task')
            tinfo = request.POST.get('info')
            rdate = request.POST.get('start')
            rhour = request.POST.get('hour')
            rmin = request.POST.get('minu')
            rzone = request.POST.get('zon')
            print(user , task , tinfo , rhour , rmin , rzone)
            cursor = conn.cursor()
            cursor.execute("UPDATE reminder SET task ='" + task + "',information ='" + tinfo + "',remdate ='" + rdate + "',hour ='" + rhour + "',minute ='" + rmin + "',zone ='" + rzone + "' where id='" + rid + "'")
            cursor.commit()
            return redirect('re_view')
        if 'del' in request.POST:
            did = request.POST.get('re_del')
            cursor = conn.cursor()
            cursor.execute("delete from reminder where id ='" + did + "'")
            cursor.commit()
            """ here cursor.commit() is very important because it commit is used to tell the database
            to save all the changes in the current transaction."""
            return redirect('re_view')


def admin_log(request):
    conn = pyodbc.connect('driver={sql server};'
                          'server=LAPTOP-3NNS80C3\SQLEXPRESS;'
                          'database=pysql;'
                          'Trusted_Connection=yes')
    # if request.method == "POST" : this method also get used
    if request.method == "GET":
        return render(request, 'admin.html')
    else:
        if 'log' in request.POST:
            aname = request.POST.get('uname')
            passw = request.POST.get('pass')
            if aname == 'admin' and passw == '12345':
                request.session['a_user'] = aname
                cursor = conn.cursor()
                cursor.execute("select * from signup")
                adata = {}
                adata['ad_user'] = request.session.get('a_user')
                adata['cdata'] = cursor.fetchall()
                return render(request, 'apanel.html', adata)
            else:
                msg = 'invalid admin username or admin password'
                return render(request, 'admin.html', {'emsg': msg})
        if 'del' in request.POST:
            did = request.POST.get('da_del')
            cursor = conn.cursor()
            cursor.execute("delete from signup where id ='" + did + "'")
            cursor.commit()
            """ here cursor.commit() is very important because it commit is used to tell the database
             to save all the changes in the current transaction."""
            # return HttpResponse(did)
            adata = {}
            adata['ad_user'] = request.session.get('a_user')

            return render(request, 'apanel.html', adata)


def alogout(request):
    request.session.clear()
    return redirect('alog')


def a_act(request):
    conn = pyodbc.connect('driver={sql server};'
                          'server=LAPTOP-3NNS80C3\SQLEXPRESS;'
                          'database=pysql;'
                          'Trusted_Connection=yes')
    adata = {}
    adata['ad_user'] = request.session.get('a_user')
    if request.method == "GET":
        cursor = conn.cursor()
        cursor.execute("select * from activity")
        adata['result1'] = cursor.fetchall()
        print(request.session.get('a_user'))
        return render(request, 'admin_activityview.html', adata)
    else:
        if 'upd' in request.POST:
            cursor = conn.cursor()
            uid = request.POST.get('ta_upd')
            cursor.execute("select * from activity where id='" + uid + "'")
            adata['result1'] = cursor.fetchall()
            return render(request, 'ad_uptask.html', adata)
        if 'up_task' in request.POST:
            user = request.session.get('a_user')
            tid = request.POST.get('t_id')
            task = request.POST.get('task')
            tinfo = request.POST.get('info')
            start_date = request.POST.get('start')
            end_date = request.POST.get('end')
            pri = request.POST.get('prio')
            print(user , task , tinfo , start_date , end_date , pri)
            cursor = conn.cursor()
            cursor.execute("UPDATE activity SET task ='" + task + "',information ='" + tinfo + "',sdate ='" + start_date + "',edate ='" + end_date + "',priority ='" + pri + "' where id='" + tid + "'")
            cursor.commit()
            return redirect('ad_task')
        if 'del' in request.POST:
            did = request.POST.get('ta_del')
            cursor = conn.cursor()
            cursor.execute("delete from activity where id ='" + did + "'")
            cursor.commit()
            """ here cursor.commit() is very important because it commit is used to tell the database
            to save all the changes in the current transaction."""
            return redirect('ad_task')




def a_remi(request):
    conn = pyodbc.connect('driver={sql server};'
                          'server=LAPTOP-3NNS80C3\SQLEXPRESS;'
                          'database=pysql;'
                          'Trusted_Connection=yes')
    adata = {}
    adata['ad_user'] = request.session.get('a_user')
    if request.method == "GET":
        cursor = conn.cursor()
        cursor.execute("select * from reminder")
        print(request.session.get('a_user'))
        adata['result1'] = cursor.fetchall()
        return render(request, 'admin_reminderview.html', adata)
    else:
        if 'upd' in request.POST:
            cursor = conn.cursor()
            uid = request.POST.get('re_upd')
            cursor.execute("select * from reminder where id='" + uid + "'")
            adata['result1'] = cursor.fetchall()
            return render(request, 'ad_upreminder.html', adata)
        if 'up_task' in request.POST:
            user = request.session.get('user')
            rid = request.POST.get('r_id')
            task = request.POST.get('task')
            tinfo = request.POST.get('info')
            rdate = request.POST.get('start')
            rhour = request.POST.get('hour')
            rmin = request.POST.get('minu')
            rzone = request.POST.get('zon')
            print(user, task, tinfo, rhour, rmin, rzone)
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE reminder SET task ='" + task + "',information ='" + tinfo + "',remdate ='" + rdate + "',hour ='" + rhour + "',minute ='" + rmin + "',zone ='" + rzone + "' where id='" + rid + "'")
            cursor.commit()
            return redirect('ad_rem')
        if 'del' in request.POST:
            rid = request.POST.get('re_del')
            cursor = conn.cursor()
            cursor.execute("delete from reminder where id ='" + rid + "'")
            cursor.commit()
            """ here cursor.commit() is very important because it commit is used to tell the database
            to save all the changes in the current transaction."""
            return redirect('ad_rem')



