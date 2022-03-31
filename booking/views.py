from django.http import HttpRequest, request, HttpResponse
from django.shortcuts import render, redirect
from django.db import connection

import dashboard.views
import login.views as login_views
from datetime import datetime


# Create your views here.


def load(request):
    cursor = connection.cursor()
    sql = "SELECT * FROM Customer"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    print("jkabsdjkabsdkljabkjd")
    print(result)
    flag = 0
    if request.session.is_empty():
        flag = 0
    else:
        flag = request.session['logged']

    contex = {
        'flag': flag,
        'route': route()
    }
    route()
    if request.method == "POST" and 'auto_selection' in request.POST:
        print(request.POST)
        request.session['tempReq'] = request.POST
        print("=========================")
        return redirect(booking_details)

    if request.method == "POST" and 'search' in request.POST:
        start1 = request.POST['From_p']
        destination = request.POST['To_p']
        start1 = str(start1)
        destination = str(destination)
        date = request.POST['date']
        what_class = request.POST['class']
        no_of_passengers = request.POST['passengers']
        class_pass = []
        if what_class == 1:
            class_pass.append('AC')
        else:
            class_pass.append('Non-Ac')

        class_pass.append(no_of_passengers)
        class_pass_dic = {
            "class": class_pass[0],
            "no_of_passengers": class_pass[1]
        }
        contex['class_pass'] = class_pass_dic
        # print(start)
        # print(destination)

        cursor = connection.cursor()
        cursor.execute("SELECT Route_id FROM Route WHERE From_r = %s and To_r=%s", [start1, destination])
        result = cursor.fetchall()
        cursor.close()
        if len(result) == 0:  # if there is no direct train betW those two points
            print("Jawa jabena bradar")
        else:  # is there are trains available for these points
            print("9090909")
            print(request.POST)
            route_id = result[0][0]
            route_id = str(route_id)
            # print(route_id)
            cursor = connection.cursor()
            cursor.execute(
                "SELECT  Train_name,Departure_time,AC_fare,Non_AC_fare,Journey_id FROM Journey WHERE Route_id=%s",
                [route_id])
            result_journey = cursor.fetchall()
            cursor.close()
            train_info = []
            for data in result_journey:
                row = {
                    "train_name": data[0],
                    "time": data[1],
                    'ac_fare': data[2],
                    'non_ac_fare': data[3],
                    'journey_id': data[4],
                    'selected_date': request.POST['date']
                }
                train_info.append(row)
            contex['train_information'] = train_info
            return render(request, 'home.html', contex)

    return render(request, "home.html", contex)


def route():
    cursor = connection.cursor()
    sql = "SELECT From_r,To_r FROM Route"
    cursor.execute(sql)
    result = cursor.fetchall()
    # print("Route gula : ")
    # print(result)
    cursor.close()
    route_table = []
    for data in result:
        row = {"From": data[0], "To": data[1]}
        route_table.append(row)
    return route_table


def search(request):
    flag = 0
    if request.session.is_empty():
        flag = 0
    else:
        flag = request.session['logged']
    print("Session:")
    print(flag)
    contex = {
        'flag': flag,
        'route': route()
    }
    route()
    if request.method == "POST" and request.POST['button'] == 'search':
        start1 = request.POST['From_p']
        destination = request.POST['To_p']
        start1 = str(start1)
        destination = str(destination)
        date = request.POST['date']
        what_class = request.POST['class']
        no_of_passengers = request.POST['passengers']
        class_pass = []
        if what_class == 1:
            class_pass.append('AC')
        else:
            class_pass.append('Non-Ac')

        class_pass.append(no_of_passengers)
        class_pass_dic = {
            "class": class_pass[0],
            "no_of_passengers": class_pass[1]
        }
        contex['class_pass'] = class_pass_dic
        # print(start)
        # print(destination)

        cursor = connection.cursor()
        cursor.execute("SELECT Route_id FROM Route WHERE From_r = %s and To_r=%s", [start1, destination])
        result = cursor.fetchall()
        cursor.close()

        if len(result) == 0:  # if there is no direct train betW those two points
            print("Jawa jabena bradar")
        else:  # is there are trains available for these points
            route_id = result[0][0]
            route_id = str(route_id)
            # print(route_id)
            cursor = connection.cursor()
            cursor.execute("SELECT  Train_name,Departure_time,AC_fare,Non_AC_fare FROM Journey WHERE Route_id=%s",
                           [route_id])
            result_journey = cursor.fetchall()
            cursor.close()
            train_info = []
            for data in result_journey:
                row = {
                    "train_name": data[0],
                    "time": data[1],
                    'ac_fare': data[2],
                    'non_ac_fare': data[3]
                }
                train_info.append(row)
            contex['train_information'] = train_info

            return render(request, 'search.html', contex)


def booking_details(request):
    print("**********************")
    print(request.POST)
    if "tempReq" in request.session:
        request.POST = request.session['tempReq']
    if 'logged' not in request.session:
        return redirect(login_views.load)

    journey_id = request.POST['auto_selection'].split('_')[1]

    date = request.POST['auto_selection'].split('_')[2]
    use_class = request.POST['class_final']
    use_seats_no = request.POST['passengers_final']
    print(use_class)
    print(use_seats_no)
    print("**********************")
    cursor = connection.cursor()
    cursor.execute("SELECT AC,Non_ac FROM Seats WHERE J_Date=%s and  Journey_id=%s", [date, journey_id])
    result = cursor.fetchall()
    print(result)
    cursor.close()
    no_ac = 0
    no_nonac = 0
    # print(type(result[0][0]))
    for i in result:
        no_ac += i[0]
        no_nonac += i[1]

    print("Database:")
    print(no_ac, no_nonac)
    if use_class == "AC":
        print("inside use class AC")
        if 250 - no_ac >= int(use_seats_no):
            print("Ac seats ache")
            cursor = connection.cursor()
            # sql = "INSERT INTO Seats(J_Date,Journey_id,AC) VALUES(\"%s\",%s,%s)"
            # sql_1 = "INSERT INTO  Seats(J_Date,Journey_id,AC,Non_ac VALUES(\""+date+"\""+","+journey_id+","+use_seats_no+",0)"
            # sql_2 = "INSERT INTO Seats(J_Date,Journey_id,AC,Non_ac) VALUES(\""+ "%s\"" + ",%s,%s,%d)"
            sql_3 = "INSERT INTO Seats(J_Date,Journey_id,AC,Non_ac) VALUES(""""%s"""",%s,%s,%s)"
            # cursor.execute(sql, [date, journey_id, use_seats_no, 0])
            cursor.execute(sql_3, [date, journey_id, use_seats_no, 0])
            connection.commit()
            cursor.close()
        else:
            print("Ac seats nai")
    elif use_class == "Non-Ac":
        if 250 - no_nonac >= int(use_seats_no):
            print("Non-Ac seats ache")
            cursor = connection.cursor()
            sql_3 = "INSERT INTO Seats(J_Date,Journey_id,AC,Non_ac) VALUES(""""%s"""",%s,%s,%s)"
            # cursor.execute(sql, [date, journey_id, use_seats_no, 0])
            cursor.execute(sql_3, [date, journey_id, 0, use_seats_no])
            connection.commit()

        else:
            print("Non-Ac seats nai")
    print(request.POST)
    contex1 = {}
    contex1['Date'] = date
    contex1['class'] = use_class
    contex1['No of Seats'] = use_seats_no
    contex1['Journey_id'] = journey_id
    contex1['seats'] = use_seats_no
    contex1['seat_class'] = use_class
    cursor = connection.cursor()
    cursor.execute("SELECT Train_name,Departure_time FROM Journey WHERE Journey_id=%s", [journey_id])
    result1 = cursor.fetchall()
    print(result1)
    contex1['Train_Name'] = result1[0][0]
    contex1['Departure_time'] = result1[0][1]
    cursor.execute("SELECT Route_id from Journey WHERE Journey_id = %s", [journey_id])
    rid = cursor.fetchall()
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print(rid)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    cursor.execute(
        "SELECT From_r,To_r from Route where Route_id= %s",
        [rid[0][0]])
    result2 = cursor.fetchall()
    print(result2)
    print("---------------------------")
    contex1['From'] = result2[0][0]
    contex1['To'] = result2[0][1]
    super = -1
    # print("username :")
    # print(request.session['username'])
    phone_no = request.session['username']
    cursor.execute("SELECT Official FROM Customer WHERE Phone_no=%s", [phone_no])
    result3 = cursor.fetchall()
    official = result3[0][0]
    print("OFFICIAL", official)
    if int(official) == 1:
        super = 1
    print(super)
    cursor.close()
    print("==================contxt================")
    print(contex1)
    print("========================================")
    contex1['flag'] = 0
    if (super == -1):
        if use_class == "AC":
            contex1['Total_Amount'] = int(use_seats_no) * 680
        elif use_class == 'Non-Ac':
            contex1['Total_Amount'] = int(use_seats_no) * 350
    else:
        contex1['flag'] = 1
        print("Flag", contex1['flag'])
        if use_class == "AC":
            contex1['Total_Amount'] = int(use_seats_no) * 680
        elif use_class == 'Non-Ac':
            contex1['Total_Amount'] = int(use_seats_no) * 350
        contex1['discount'] = contex1['Total_Amount'] * 0.40
        contex1['Final_dicounted_amount'] = contex1['Total_Amount'] - contex1['Total_Amount'] * 0.40

    flag_1 = 0
    # if request.method == "POST" and 'proceed' in request.POST:
    #
    #
    # contex1['flag1']  = flag_1
    contex1['nextForm'] = 0
    return render(request, "trasaction_1.html", contex1)


def booking_proceed(request):
    if 'trxButtonSubmit' in request.POST:
        print("booking button pressed...")
    request.POST = request.session['tempReq']
    print("inside booking_proceed")
    print(request.POST)
    journey_id = request.POST['auto_selection'].split('_')[1]
    date = request.POST['auto_selection'].split('_')[2]
    use_class = request.POST['class_final']
    use_seats_no = request.POST['passengers_final']
    contex1 = {}
    cursor = connection.cursor()
    cursor.execute("SELECT Train_name,Departure_time FROM Journey WHERE Journey_id=%s", [journey_id])
    result1 = cursor.fetchall()
    print(result1)
    contex1['Date'] = date
    contex1['Train_Name'] = result1[0][0]
    contex1['Departure_time'] = result1[0][1]
    contex1['seats'] = use_seats_no
    contex1['seat_class'] = use_class
    cursor.execute("SELECT Route_id from Journey WHERE Journey_id = %s", [journey_id])
    rid = cursor.fetchall()
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print(rid)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    cursor.execute(
        "SELECT From_r,To_r from Route where Route_id= %s",
        [rid[0][0]])
    result2 = cursor.fetchall()
    contex1['From'] = result2[0][0]
    contex1['To'] = result2[0][1]
    if use_class == "AC":
        contex1['Total_Amount'] = int(use_seats_no) * 680
    elif use_class == 'Non-Ac':
        contex1['Total_Amount'] = int(use_seats_no) * 350
    contex1['nextForm'] = 1
    contex1['Journey_id'] = journey_id
    return render(request, 'trasaction_1.html', contex1)


def ticketOrderPlaced(request):
    print(request.POST)
    print("inside ticket order placed......")
    cursor = connection.cursor()
    cursor.execute("SELECT Customer_id FROM Customer WHERE Phone_no=%s", [request.session['username']])
    cid = cursor.fetchall()
    cid = cid[0][0]
    if (request.POST['seats_class'] == 'Non-Ac'):
        cursor.execute(
            "INSERT INTO Transaction_1(Customer_id,Transaction_phone_no,Bkash_id,Seats_AC,Seats_non_AC,Journey_id) VALUES(%s,""""%s"""",""""%s"""",%s,%s,%s)",
            [cid, request.POST['trxnum'], request.POST['trxid'], 0, request.POST['seats'], request.POST['j_id']])
        nw_result = cursor.fetchall()
        print("==========")
        print(nw_result)
        print("==========")
    else:
        cursor.execute(
            "INSERT INTO Transaction_1(Customer_id,Transaction_phone_no,Bkash_id,Seats_AC,Seats_non_AC,Journey_id) VALUES(%s,""""%s"""",""""%s"""",%s,%s,%s)",
            [cid, request.POST['trxnum'], request.POST['trxid'], request.POST['seats'], 0, request.POST['j_id']])
        nw_result = cursor.fetchall()
        print("==========")
        print(nw_result)
        print("==========")
    return redirect(load)


def approve_order(request, trx_id):
    now = datetime.now()
    cursor = connection.cursor()
    cursor.execute("UPDATE Transaction_1 SET Valid=1,Time_1=%s WHERE Bkash_id=%s", [now, trx_id])
    connection.commit()
    cursor.close()
    current_time = now.strftime("%H:%M")

    return redirect(dashboard.views.load)



def refund(request, trx_id):
    request.session['t_id'] = trx_id
    cursor = connection.cursor()
    cursor.execute("UPDATE Transaction_1 SET Valid=-1 WHERE Bkash_id=%s",[trx_id])
    connection.commit()
    cursor.close()

    return redirect(dashboard.views.load)

def approve_refund_req(request,bkash):
    cursor = connection.cursor()
    cursor.execute("DELETE  FROM Transaction_1 where Bkash_id = %s",[bkash])
    connection.commit()
    cursor.close()
    return  redirect(dashboard.views.load)