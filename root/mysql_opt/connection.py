from mysql import connector


class Connection(object):
    __mydb = connector.connect(
        host="192.168.1.20",
        user="root",
        passwd="123456",
        database="dg"
    )

    __cursor = None

    @classmethod
    def mycursor(cls):
        if cls.__cursor is None:
            cls.__cursor = cls.__mydb.cursor()
        return cls.__cursor


# mycursor = Connection.mycursor()
# mycursor.execute("select id, username, buy_name, buy_mobile from t_dg_buy_user limit 10 ")
# for x in mycursor:
#     print(x)

# mycursor.execute("select * from t_dg_buy_user")
# fileds = mycursor.description
# for x in fileds:
#     print(x)
