from mysql import connector


class Connection(object):
    __mydb = connector.connect(
        host="192.168.1.20",
        user="root",
        passwd="123456",
        database="dg"
    )

    @classmethod
    def mycursor(cls):
        return cls.__mydb.cursor()


# mycursor = Connection.mycursor()
# mycursor.execute("SHOW TABLES")
# for x in mycursor:
#     print(x)

# mycursor.execute("select * from t_dg_buy_user")
# fileds = mycursor.description
# for x in fileds:
#     print(x)
