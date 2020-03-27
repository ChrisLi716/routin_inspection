from root.mysql_opt.connection import Connection

mycursor = Connection.mycursor()
mycursor.execute("select id, username, buy_name, buy_mobile from t_dg_buy_user limit 10 ")
for x in mycursor:
    print(x)
