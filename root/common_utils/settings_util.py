from configparser import ConfigParser
from root.common_utils.log_util import Logger
from root.common_utils.const import Const


class SettingsUtil:
    logger = Logger().get_instance()
    __instance = None

    __const = Const()
    __const.MYSQL_SECTION = "mysql"
    __const.EMAIL_SECTION = "email"

    def __init__(self):
        config = ConfigParser()
        config.read("../sources/settings.ini")
        self.mysql_host = config.get(self.__const.MYSQL_SECTION, "host")
        self.mysql_user = config.get(self.__const.MYSQL_SECTION, "user")
        self.mysql_pwd = config.get(self.__const.MYSQL_SECTION, "passwd")
        self.mysql_db = config.get(self.__const.MYSQL_SECTION, "database")

        self.email_host = config.get(self.__const.EMAIL_SECTION, "host")
        self.email_sender = config.get(self.__const.EMAIL_SECTION, "sender")
        # self.email_pwd = config.get(self.__const.EMAIL_SECTION, "pwd")
        self.email_non_ssl_port = config.get(self.__const.EMAIL_SECTION, "non_ssl_port")
        self.email_ssl_port = config.get(self.__const.EMAIL_SECTION, "ssl_port")

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = SettingsUtil()
        return cls.__instance


if __name__ == '__main__':
    settings = SettingsUtil()
    print(settings.mysql_host)
    print(settings.email_host)
