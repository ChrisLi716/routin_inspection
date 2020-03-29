import logging
import logging.config  # config 配置
import traceback


class Logger(object):
    # 定义三种日志输出格式开始
    # 其中name为getlogger指定的名字
    __standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
                        '[%(levelname)s][%(message)s]'
    __simple_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
    __id_simple_format = '[%(levelname)s][%(asctime)s] %(message)s'

    # log文件名
    # __logfile_path_staff = r'C:\Users\Administrator\Desktop\log\routin_inspection.log'
    __logfile_path_staff = r'D:\Python\python_workspace\routin_insepection.log'

    # log配置字典
    # LOGGING_DIC第一层的所有的键不能改变
    __log_dic = {
        'version': 1,  # 版本号
        'disable_existing_loggers': False,  # 固定写法
        'formatters': {
            'standard': {
                'format': __standard_format
            },
            'simple': {
                'format': __simple_format
            },
        },
        'filters': {},
        'handlers': {
            # 打印到终端的日志
            'sh': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',  # 打印到屏幕
                'formatter': 'simple'
            },
            # 打印到文件的日志,收集info及以上的日志
            'fh': {
                'level': 'DEBUG',
                # 'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
                'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',  # 解决logging模块多个进程往同一个文件写日志的问题
                'formatter': 'standard',
                'filename': __logfile_path_staff,  # 日志文件
                'maxBytes': 3000000,  # 日志大小 3M
                'backupCount': 5,  # 轮转文件的个数
                'encoding': 'utf-8',  # 日志文件的编码
            },
        },
        'loggers': {
            # logging.getLogger(__name__)拿到的logger配置
            '': {
                'handlers': ['sh', 'fh'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
                'level': 'DEBUG',
                'propagate': True,  # 向上（更高level的logger）传递
            }
        },
    }

    def __init__(self):
        # 导入上面定义的logging配置 通过字典方式去配置这个日志
        logging.config.dictConfig(self.__log_dic)

        # 生成一个log实例这里可以有参数传给task_id
        Logger.__instance = logging.getLogger()

    @classmethod
    def get_instance(cls):
        if not hasattr(Logger, "_instance"):
            Logger()
        return Logger.__instance


dic = {
    'username': '小黑'
}


def login():
    for i in range(0, 10000):
        Logger.get_instance().debug(f"{dic['username']}登陆成功")


if __name__ == '__main__':
    try:
        login()
    except Exception:
        Logger.get_instance().error(traceback.format_exc(Exception))
