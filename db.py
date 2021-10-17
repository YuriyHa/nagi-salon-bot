# import sqlite3
# from sqlite3.dbapi2 import connect
# class SQLighter: 
#     def __init__(self , database) :
#         self.connection = sqlite3.connect(database)
#         self.cursor = self.connection.cursor()

#     # def getUsers(self, ru): 
#     #     with self.connection: 
#     #         return self.connection.execute("SELECT*FROM `table` WHERE `RU` = ?", (ru)).fetchall()

#     def user_in_base(self, user_id): 
#         with self.connection: 
#             result = self.connection.execute("SELECT*FROM `users` WHERE `user_id`=?", (user_id,)).fetchall()
#             return bool(len(result))

#     def add_user(self, username, userid, language): 
#         with self.connection: 
#             self.connection.execute("INSERT INTO `users` (`user_id`, `user_name`, `lan`) VALUEs(?, ?, ?)", (userid, username, language,))

#     def user_lan(self, user_id): 
#         with self.connection: 
#             lan = self.connection.raw_qury
from datetime import datetime
import sqlite3

def add_user(id, name, lan): 
    sqlite_connection = sqlite3.connect('db.db')
    cursor = sqlite_connection.cursor()
    print("Подключен к SQLite")

    sqlite_select_query = "INSERT into `aaa` ( `user_id`, `user_name`, `lan`) values(?, ?, ?)"
    sqlite_connection.execute(sqlite_select_query, (id,name, lan,))
    sqlite_connection.commit()
    cursor.close()
    print("Соединение с SQLite закрыто")

def user_in_base(id): 
    sqlite_connection = sqlite3.connect('db.db')
    cursor = sqlite_connection.cursor()
    print("Подключен к SQLite")

    sqlite_select_query = "SELECT * from `aaa` where `user_id` = ?"
    cursor.execute(sqlite_select_query, (id,))
    records = cursor.fetchall()
    # print("Всего строк:  ", len(records)) количетво length
    cursor.close()
    print("Соединение с SQLite закрыто")
    return bool(len(records))

    
def read_sqlite_table(id):
    sqlite_connection = sqlite3.connect('db.db')
    cursor = sqlite_connection.cursor()
    print("Подключен к SQLite")

    sqlite_select_query = "SELECT * from `aaa` where `user_id` = ?"
    cursor.execute(sqlite_select_query, (id,))
    records = cursor.fetchall()
    print("Всего строк:  ", len(records))
     
    for row in records:
        print("ID:", row[0])
        print("User id:", row[1])
        print("User name:" , row[2])
        print("lan:", row[3])
        print("keshback:", row[5])
        print("buyed cont:", row[4], "\n\n")
        name = row[2]
        lan = row[3]
        kesh = row[5]
        buyed_cont = row[4]
        user_id = row[1]

    cursor.close()

    sqlite_connection.close()
    print("Соединение с SQLite закрыто")
    return [lan, name, kesh, buyed_cont, user_id]

def update_data(id, this_element, to_element): 
    sqlite_connection = sqlite3.connect('db.db')
    cursor = sqlite_connection.cursor()
    print("Подключен к SQLite")

    sqlite_connection.execute("UPDATE `aaa` set " + this_element + " = ? where `user_id` = ?", (to_element, id,))
    sqlite_connection.commit()

    cursor.close()
    sqlite_connection.close()
    print("Соединение с SQLite закрыто")





#####################
#`occurred at` table#
def select_times(): 
    sqlite_connection = sqlite3.connect('db.db')
    cursor = sqlite_connection.cursor()
    print("Подключен к SQLite")

    cursor.execute("SELECT * from `occurred_at` limit 10")
    listt = cursor.fetchall()

    cursor.close()
    sqlite_connection.close()
    print("Соединение с SQLite закрыто")
    return listt

def add_time(userid, username, time, types):
    sqlite_connection = sqlite3.connect('db.db')
    cursor = sqlite_connection.cursor()
    print("Подключен к SQLite")

    sqlite_connection.execute("INSERT into `occurred_at` (`user_id`, `user_name`, `time`, `order_type`) values(? ,?, ?, ?)", (userid,  username, time, types))
    sqlite_connection.commit()
    print('added: ', time)

    cursor.close()
    sqlite_connection.close()
    print("Соединение с SQLite закрыто")









########################
#orders_types table#####
def delete_order_types(id): 
    sqlite_connection = sqlite3.connect('db.db')
    cursor = sqlite_connection.cursor()
    print("Подключен к SQLite")

    sqlite_connection.execute("DELETE from `order_types` where `id` = ?", (id,))
    sqlite_connection.commit()

    cursor.close()
    sqlite_connection.close()
    print("Соединение с SQLite закрыто")


def add_order_types(order_type): 
    sqlite_connection = sqlite3.connect('db.db')
    cursor = sqlite_connection.cursor()
    print("Подключен к SQLite")

    sqlite_connection.execute("INSERT into `order_types` (`order_type`) values (?)", (order_type,))
    sqlite_connection.commit()

    cursor.close()
    sqlite_connection.close()
    print("Соединение с SQLite закрыто")
def select_all_types(): 
    sqlite_connection = sqlite3.connect('db.db')
    cursor = sqlite_connection.cursor()
    print("Подключен к SQLite")

    cursor.execute("SELECT * FROM `order_types`")
    types_list = cursor.fetchall()
    ord_types = []
    ids = []
    for row in types_list: 
        print ('id = ', row[0])
        print ('order_types = ', row[1])
        ord_types.append(row[1]) 
        ids.append(row[0]) 

    cursor.close()
    sqlite_connection.close()
    print("Соединение с SQLite закрыто")
    return [ord_types, ids]


def returnData(exexu, param): 
    sqlite_connection = sqlite3.connect('db.db')
    cursor = sqlite_connection.cursor()
    print("Подключен к SQLite")

    cursor.execute(exexu, param)
    types_list = cursor.fetchall()
    print(types_list)

    cursor.close()
    sqlite_connection.close()
    print("Соединение с SQLite закрыто")
    return types_list

returnData("SELECT `user_name`, COUNT(*) FROM `occurred_at` GROUP BY `user_name`", ())
def return_byTime(timing, time_now, object_): 
    ahaha = returnData("SELECT  "  +object_  + ", date(max(`time`)), COUNT(*) FROM (SELECT  " + object_+",`time` FROM `occurred_at` where datetime(`time`, " + timing + ") = datetime(?, " + timing + ") order by `time` desc) GROUP BY 1 order by COUNT(*) desc LIMIT 10", (time_now,))
    # thistime = datetime.now()
    # reallist=[]
    # for a in ahaha: 
    #     sqlstrtime = a[1]
    #     sqltime = datetime.strptime(sqlstrtime, '%Y-%m-%d')
        
    #     if sqltime.year == thistime.year: 
    #         if sqltime.month == sqltime.month: 
    #             reallist.append(a)
    return ahaha


