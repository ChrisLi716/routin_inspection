from configparser import ConfigParser
from root.common_utils.log_util import Logger
from root.common_utils.const import Const


class SettingsUtil:
    logger = Logger().get_instance()
    __instance = None

    __const = Const()
    __const.MYSQL_SECTION = "mysql"
    __const.EMAIL_SECTION = "email"

    @classmethod
    def init_settings(cls):
        config = ConfigParser()
        config.read("../sources/settings.ini")
        cls.mysql_host = config.get(cls.__const.MYSQL_SECTION, "host")
        cls.mysql_user = config.get(cls.__const.MYSQL_SECTION, "user")
        cls.mysql_pwd = config.get(cls.__const.MYSQL_SECTION, "passwd")
        cls.mysql_db = config.get(cls.__const.MYSQL_SECTION, "database")

        cls.email_host = config.get(cls.__const.EMAIL_SECTION, "host")
        cls.email_sender = config.get(cls.__const.EMAIL_SECTION, "sender")
        cls.email_pwd = config.get(cls.__const.EMAIL_SECTION, "pwd")
        cls.email_non_ssl_port = config.get(cls.__const.EMAIL_SECTION, "non_ssl_port")
        cls.email_ssl_port = config.get(cls.__const.EMAIL_SECTION, "ssl_port")

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = SettingsUtil()
        return cls.__instance


if __name__ == '__main__':
    SettingsUtil.init_settings()
    print(SettingsUtil.mysql_host)
    print(SettingsUtil.email_host)
