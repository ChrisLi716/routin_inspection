from mysql import connector
from root.common_utils.settings_util import SettingsUtil


class MyConnection(object):
    __settings = SettingsUtil.get_instance()

    def __init__(self):
        self.conn = connector.connect(
            host=self.__settings.mysql_host,
            user=self.__settings.mysql_user,
            passwd=self.__settings.mysql_pwd,
            database=self.__settings.mysql_db
        )
        self.cursor = self.conn.cursor()

    def close_conn(self):
        if self.conn:
            self.conn.close()

# mycursor = Connection.mycursor()
# mycursor.execute(
#     "  SELECT t.id, t.username, t.buy_name, t.buy_mobile FROM t_dg_buy_user t, t_dg_invitation_code c WHERE im_token IS NOT NULL AND t.create_date >= DATE_FORMAT('2020-01-23 00:00:00', '%Y-%m-%d %H:%k:%s') AND t.create_date <= DATE_FORMAT('2020-02-29 23:59:00', '%Y-%m-%d %H:%k:%s') AND t.buy_mobile = c.mobile ORDER BY t.create_date DESC")
# result_set = mycursor.fetchall()
# print("totla:" + str(len(result_set)))
#
# mycursor.execute("select id, username, buy_name, buy_mobile from t_dg_buy_user")
# result_set = mycursor.fetchall()
# print("totla:" + str(len(result_set)))

# mycursor.execute("select * from t_dg_buy_user")
# fileds = mycursor.description
# for x in fileds:
#     print(x)
