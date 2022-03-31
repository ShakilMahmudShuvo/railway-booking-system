from django.http import HttpRequest, request
from django.shortcuts import render, redirect
from django.db import connection
import booking.views as booking_views
import login.views as login_views
import dashboard.views as dashboard_views
import hashlib
import os
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages


def create_session(request, username):
    request.session['username'] = username
    request.session['logged'] = 1
    cursor = connection.cursor()
    cursor.execute("SELECT Official FROM Customer WHERE Phone_no = %s ", [username])
    result = cursor.fetchall()
    request.session['official'] = result[0][0]


def del_session(request):
    request.session.flush()
    request.session.clear_expired()
    return redirect(load)


def load(request):
    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        password = hashlib.md5(password.encode('utf-8')).hexdigest()

        print(username)
        print(password)

        sql = "SELECT Phone_no,Password,Name FROM Customer WHERE Phone_no = '" + username + "';"

        result = []
        print(len(result))

        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
        print(len(result))
        username_fetched = ""
        password_fetched = ""
        name = ""
        print(cursor.rowcount)
        if len(result) > 0:
            print(111)
            username_fetched = [value[0] for value in result]
            username_fetched = str(username_fetched[0])

            password_fetched = [value[1] for value in result]
            password_fetched = str(password_fetched[0])

            name = [value[2] for value in result]
            name = str(name[0])

        cursor.close()
        print("eikhane")
        print(username_fetched)
        print(password_fetched)
        print(name)

        if username_fetched == username:
            if password_fetched == password:
                create_session(request, username)
                request.session['name'] = name
                print("Session Created...")
                return redirect(dashboard_views.load)
        messages.error(request, "Username or password not correct")
        return render(request, 'login.html')
    else:

        return render(request, 'login.html')


def logout(request):
    del_session(request)
    if request.session.is_empty():
        print("Session empty")
    return redirect(booking_views.load)
    return redirect(register)


def register(request):
    if request.method == 'POST':
        print("Dhukche")
        name = request.POST['name']
        mobile_no = request.POST['phone_no']
        confimed_mobile_no = request.POST['confirmed_phone_no']
        password = request.POST['password']
        confirmed_password = request.POST['confirmed_password']
        sql = "SELECT COUNT(*)  FROM Customer WHERE phone_no = %s "
        cursor = connection.cursor()
        cursor.execute(sql, [mobile_no])
        count = cursor.fetchall()
        count = count[0][0]

        print(type(count))
        print(count)
        cursor.close()
        if (count > 0):
            messages.info(request, "An account already exists with this Mobile Number")
            return redirect(register)

        if (mobile_no == confimed_mobile_no) and (password == confirmed_password):
            sql = "INSERT INTO Customer(Name,Phone_no,Password,Official) VALUES(%s,%s,%s,%s);"

            password = hashlib.md5(password.encode('utf-8')).hexdigest()
            cursor = connection.cursor()
            cursor.execute(sql, [name, mobile_no, password, str(0)])
            connection.commit()
            cursor.close()

            return redirect(load)
        else:
            return redirect(register)
    else:
        return render(request, 'register.html')
