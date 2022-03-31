from django.http import HttpRequest, request
from django.shortcuts import render, redirect
from django.db import connection
import booking.views as booking_views
import login.views as login_views


def load(request):
    if request.session.is_empty():
        return redirect(login_views.load)
    else:
        nw = []
        name = request.session['name']
        flag = request.session['logged']
        phone_no = request.session['username']
        if request.session['official'] == '1':
            print("Here it is...")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Transaction_1 WHERE Valid = 0")
            transaction_table = cursor.fetchall()
            table = []
            for data in transaction_table:
                trx_id = data[6]
                trx_num = data[7]
                ac_seats = data[3]
                non_ac_seats = data[4]
                seats = 0
                amount = 0
                cls = 0
                if ac_seats != 0:
                    seats = ac_seats
                    amount = ac_seats * 680
                    cls = "AC"
                else:
                    seats = non_ac_seats
                    amount = non_ac_seats * 350
                    cls = "Non-AC"
                row = {
                    'trx_id': trx_id,
                    'trx_num': trx_num,
                    'seats': seats,
                    'class': cls,
                    'amount': amount
                }
                table.append(row)
            official_flag = 0
            if request.session['official'] == 1:
                official_flag = 1
            else:
                official_flag = 0
            print("---------------------------------------------------------")
            print(f"Official flag request session: {request.session['official']}")
            print(official_flag)
            print("---------------------------------------------------------")
            nw = []
            cursor.execute("SELECT Bkash_id,Transaction_phone_no FROM Transaction_1 where Valid=%s", [-1])
            temp_2 = cursor.fetchall()
            print("8888888888888888888888888888888888")
            print(temp_2)
            for item in temp_2:
                nw.append({'bkash': item[0], 'num': item[1]})

        else:
            cursor = connection.cursor()
            # cursor.execute("SELECT Seats_AC,Seats_non_AC,Time_1,Journey_id FROM Transaction_1 WHERE Customer_id = (SELECT Customer_id FROM Customer WHERE Phone_no =""""%s"""""),[request.session['username']])
            sql = "SELECT Seats_AC,Seats_non_AC,Time_1,Journey_id,Bkash_id FROM Transaction_1 WHERE Valid=1 and Customer_id = (SELECT Customer_id FROM Customer WHERE Phone_no =" + str(request.session['username']) + ")"
            cursor.execute(sql)
            result = cursor.fetchall()
            table = []

            for i in result :
                ac = i[0]
                non_ac = i[1]
                t = i[2]
                j_id = i[3]
                b_kash= i[4]
                cursor.execute("SELECT Train_name FROM Journey WHERE Journey_id=%s", [j_id])
                temp = cursor.fetchall()

                data = {'ac': ac, 'non_ac': non_ac, 't': t, 'j_id': j_id,'train_name':temp[0][0],'trx_id':b_kash}
                table.append(data)
            print("++++++++++++++++++++++++++++")
            print(result)
            print("++++++++++++++++++++++++++++++++")
            print(table)




        return render(request, 'Dashboard.html',
                      {'name': name, 'phone_no': phone_no, 'validation': table,
                       'refund':nw,
                       'official': request.session['official']})
