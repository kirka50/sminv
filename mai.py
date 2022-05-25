import pickle
import numpy as np
import pandas as pd
import pymysql
#import mysql
import mysqlx
from tensorflow import keras


host = "localhost"
user = "root"
password = "2131"
db_name = "smartinv"

#получаем с ардуино
Current_Cab = 0
Rf_Id = '00:00:00:01'


compare = 0
status = 0


def addNewPosition():
    try:
        with connection.cursor() as cursor:
            insert_query = "INSERT INTO `Inv_Table`(Position_name,Excel_Inv_Number,Rf_Id,Current_Cab,Parrent_Cab,Status) " \
                           "VALUES ('Тактический веник', 'M0001', '00:00:00:10', 315, 315,0);"
            cursor.execute(insert_query)
            connection.commit()
        print("Значения добавленны")
    except Exception as ex:
        print('Не добавлено')
        print(ex)


def visual():
    global status, Rf_Id, compare,Current_Cab
    try:
        with connection.cursor() as cursor:
            select_users = "SELECT * FROM Inv_Table"
            cursor.execute(select_users)
            result = cursor.fetchall()

            for user in result:
                if user['Rf_Id'] == Rf_Id:
                    if Current_Cab == user['Parrent_Cab']:
                        compare = 1
                    else:
                        compare = 0
                    status = user['Status']
                    print(user)
        print('Саксекс')
    except Exception as ex:
        print("Хуйня, переделывай")
        print(ex)


def update(id,cab,stat):
    try:
        with connection.cursor() as cursor:
            print(id,cab,stat)
            if stat == 1:
              cab == -1
            update = """Update Inv_Table set Current_Cab = {0}, Status ={1} where Rf_Id = "{2}" """.format(cab,stat,id)

            cursor.execute(update)
            connection.commit()
        print("Значения изменены")
    except Exception as ex:
        print("Хуйня, переделывай")
        print(ex)



try:
    connection = pymysql.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    print("Соединение установлено")

except Exception as ex:
    print("Jopa")
    print(ex)

#addNewPosition()



try:
    filename = 'model.h5'
    model = keras.models.load_model(filename)
except Exception as ex:
    print("Пиздец")

status = np.argmax(model.predict([[compare,status]]))
visual()
update(Rf_Id, Current_Cab, status)
#update('00:00:00:01', 315,0)
visual()

print(np.argmax(model.predict([[compare,status]])))


connection.close()
