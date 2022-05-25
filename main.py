import pymysql
import mysql
import mysqlx
from Config import *

def dropTable():
    try:
        with connection.cursor() as cursor:
            drop_table_query = "DROP TABLE `Inv_Table`;"
            cursor.execute(drop_table_query)
        print('Table was deleted')
    except Exception as ex:
        print("Something goes wrong")
        print(ex)

def createTable():
    try:
        with connection.cursor() as cursor:
            create_table_query = "CREATE TABLE `Inv_Table`(Position_Number int AUTO_INCREMENT," \
                                 "Position_Name varchar(32)," \
                                 "Excel_Inv_Number varchar(32)," \
                                 "Rf_Id varchar(32)," \
                                 "Current_Cab int," \
                                 "Parrent_Cab int," \
                                 "Status int, PRIMARY KEY (Position_Number));"
            cursor.execute(create_table_query)
        print('Table was created')
    except Exception as ex:
        print("Something goes wrong")
        print(ex)


def addNewPosition():
    try:
        with connection.cursor() as cursor:
            insert_query = "INSERT INTO `Inv_Table`(Position_name,Excel_Inv_Number,Rf_Id,Current_Cab,Parrent_Cab,Status) " \
                           "VALUES ('Стул', 'M0001', '00:00:00:01', 304, 315,2);"
            cursor.execute(insert_query)
            connection.commit()
        print("Значения добавленны")
    except Exception as ex:
        print('Не добавлено')
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
createTable()
addNewPosition()
connection.close()
