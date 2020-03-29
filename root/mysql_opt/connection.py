from mysql import connector
from threading import Lock
from root.common_utils.settings_util import SettingsUtil


class Connection(object):
    __settings = SettingsUtil.get_instance()
    __thread_lock = Lock()
    __mydb = connector.connect(
        host=__settings.mysql_host,
        user=__settings.mysql_user,
        passwd=__settings.mysql_pwd,
        database=__settings.mysql_db
    )

    __cursor = None

    @classmethod
    def mycursor(cls):
        cls.__thread_lock.acquire()
        if cls.__cursor is None:
            cls.__cursor = cls.__mydb.cursor()
        cls.__thread_lock.release()
        return cls.__cursor

# mycursor = Connection.mycursor()
# mycursor.execute("select id, username, buy_name, buy_mobile from t_dg_buy_user limit 10 ")
# for x in mycursor:
#     print(x)

# mycursor.execute("select * from t_dg_buy_user")
# fileds = mycursor.description
# for x in fileds:
#     print(x)
