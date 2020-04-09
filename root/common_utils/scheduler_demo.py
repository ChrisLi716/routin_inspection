import time
from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.schedulers.background import BackgroundScheduler
import datetime
from apscheduler.triggers.cron import CronTrigger
import logging


class SchedulerUtil:
    logging.basicConfig()
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    scheduler = BlockingScheduler()  # 后台运行

    @staticmethod
    def interval_job():
        # 创建调度器：BlockingScheduler
        scheduler = BlockingScheduler()

        # 添加任务,时间间隔2S
        scheduler.add_job(SchedulerUtil.func(), 'interval', seconds=2, id='test_job1')

        # 添加任务,时间间隔5S
        scheduler.add_job(SchedulerUtil.func2(), 'interval', seconds=3, id='test_job2')
        scheduler.start()

    @staticmethod
    def cron_job():
        crontab_exp = "*/2 * * * *"
        # 使用标准crontab表达式 minute, hour, day of month, month, day of week
        SchedulerUtil.scheduler.add_job(SchedulerUtil.func, CronTrigger.from_crontab(crontab_exp))
        SchedulerUtil.scheduler.start()

    @staticmethod
    def my_listener(event):
        if event.exception:
            print('The job crashed :(')
        else:
            print('The job worked :)')

    @staticmethod
    def func():
        now = datetime.datetime.now()
        ts = now.strftime('%Y-%m-%d %H:%M:%S')
        print('do func time :', ts)

    @staticmethod
    def func2():
        # 耗时2S
        now = datetime.datetime.now()
        ts = now.strftime('%Y-%m-%d %H:%M:%S')
        print('do func2 time：', ts)
        time.sleep(2)

    # @staticmethod
    # @scheduler.scheduled_job('cron', day_of_week='*', hour=22, minute=3, second=50)
    # def func3():
    #     print("111")


if __name__ == '__main__':
    SchedulerUtil.cron_job()
    # SchedulerUtil.scheduler.start()
