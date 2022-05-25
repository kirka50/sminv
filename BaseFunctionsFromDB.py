import pymysql
from Config import *
import keras as ker
import numpy as np
import json


def createSmartInvTable():
    try:
        connection = createConnection()
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
        closeConnection(connection)
    except Exception as ex:
        print("Something goes wrong")
        print(ex)


def visual(Rf_Id,Current_Cab):
    try:
        dict = findByRdID(Rf_Id)
        print(Current_Cab,dict['Parrent_Cab'])
        if Current_Cab == int(dict['Parrent_Cab']):
            compare = 1
        else:
            compare = 0
        status = dict['Status']
        print(status,compare)
        status = changeNet(status,compare)
        if status == 1:
            Current_Cab = 0
        updateStatusAndCurrentCabByRFID(Current_Cab,status,dict['Rf_Id'])
        print('Саксекс')
    except Exception as ex:
        print("Хуйня, переделывай")
        print(ex)


def findBadMebel():
    try:
        connection = createConnection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT Position_Name,Excel_Inv_Number,Current_Cab FROM `Inv_Table` WHERE (Status = 2 OR Status = 1) AND Position_Type = 'Мебель'")
            badMabel = cursor.fetchall()
            closeConnection(connection)
            return badMabel
    except Exception as ex:
        print('Не выполненно')
        print(ex)
        return ex


def findBadObur():
    try:
        connection = createConnection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT Position_Name,Excel_Inv_Number,Current_Cab FROM `Inv_Table` WHERE (Status = 2 OR Status = 1) AND Position_Type = 'Оборудование'")
            badObur = cursor.fetchall()
            closeConnection(connection)
            return badObur
    except Exception as ex:
        print('Не выполненно')
        print(ex)
        return ex


def findBadElec():
    try:
        connection = createConnection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT Position_Name,Excel_Inv_Number,Current_Cab FROM `Inv_Table` WHERE (Status = 2 OR Status = 1) AND Position_Type = 'Электроника'")
            badElec = cursor.fetchall()
            closeConnection(connection)
            return badElec
    except Exception as ex:
        print('Не выполненно')
        print(ex)
        return ex


def changeNet(status,compare):
    try:
        filename = 'model.h5'
        model = ker.models.load_model(filename)
        value = np.argmax(model.predict([[status,compare]]))
        return value
    except Exception as ex:
        print("Что-то не так")

def findByOldExcelNumber(ExcelNumber):
    try:
        connection = createConnection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM `Inv_Table` WHERE Excel_Inv_Number = %s",(ExcelNumber))
            InvItem = cursor.fetchone()
            closeConnection(connection)
            return InvItem
    except Exception as ex:
        print(ex)


def insertValues(Position_Number,Position_name,Excel_Inv_Number,Rf_Id,Current_Cab,Parrent_Cab,Status,Position_Type):
    try:
        connection = createConnection()
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO `Inv_Table` VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(Position_Number,Position_name,Excel_Inv_Number,Rf_Id,
                           Current_Cab,Parrent_Cab,Status,Position_Type))
            connection.commit()
        print("Значения добавленны")
        closeConnection(connection)
    except Exception as ex:
        print('Не добавлено')
        print(ex)


def updateStatusAndCurrentCabByRFID(Current_Cab,Status,Rf_Id):
    try:
        connection = createConnection()
        with connection.cursor() as cursor:
            cursor.execute("Update Inv_Table set Current_Cab = %s, Status = %s where Rf_Id = %s;",(Current_Cab,Status,Rf_Id))
            connection.commit()
        print("Значения изменены")
        closeConnection(connection)
    except Exception as ex:
        print('Значения не изменены')
        print(ex)


def findByRdID(Rf_Id):
    try:
        connection = createConnection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM `Inv_Table` WHERE Rf_Id = %s",Rf_Id)
            dataFromRfID = cursor.fetchone()
        closeConnection(connection)
    except Exception as ex:
        print("Не найдено")
        print(ex)
        return ("Не найдено")
    return dataFromRfID


def dropTable(tableName):
    try:
        connection = createConnection()
        with connection.cursor() as cursor:
            cursor.execute("DROP TABLE `%s`", tableName)
        print('Table was deleted')
        closeConnection(connection)
    except Exception as ex:
        print("Something goes wrong")
        print(ex)



def createConnection():
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
        return connection

    except Exception as ex:
        print("Jopa")
        print(ex)


def closeConnection(connection):
    connection.close()
    print("Соединение закрыто")


def commitConnection(connection):
    connection.commit()
    print("Прошёл коммит")

def converToJson(Data):
    return json.dumps(Data)

def unzipFetch(List):
    data = ['Position_Name','Excel_Inv_Number','Current_Cab']
    result = {'Position_Name':[],'Excel_Inv_Number':[],'Current_Cab':[]}
    for i in List:
        result[data[0]].append(i[data[0]])
        result[data[1]].append(i[data[1]])
        result[data[2]].append(i[data[2]])
    print(result)
    return result


print(findByOldExcelNumber('M0001'))

