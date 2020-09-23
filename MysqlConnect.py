from mysql.connector import connect, errorcode, Error


def ConnectMySql():
    try:
        mydb = connect(
            host="localhost", user="pizzadb", password="1234", database="pizza_order",
        )
        return mydb
    except Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return False
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return False
        else:
            print(err)
            return False

def update_table(pizzadb):
    try:
        mycursor = pizzadb.cursor()
        sql = "update list_of_orders set status_of_order='preaparing' where now()+1>=preparation_time"
        mycursor.execute(sql)
        pizzadb.commit()
        sql = "update list_of_orders set status_of_order='delivered' where now()+1>=delivery_time"
        mycursor.execute(sql)
        pizzadb.commit()
        return True
    except Error as err:
        print(err)
        return False

