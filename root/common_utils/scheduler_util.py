import time
from apscheduler.schedulers.blocking import BlockingScheduler

from apscheduler.schedulers.background import BackgroundScheduler

import datetime

from apscheduler.triggers.cron import CronTrigger

import logging


class SchedulerUtil:
    logging.basicConfig()
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)

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
        scheduler = BackgroundScheduler()
        # 使用标准crontab表达式 minute, hour, day of month, month, day of week
        scheduler.add_job(SchedulerUtil.func(), CronTrigger.from_crontab('38 18 * * *'))
        scheduler.start()

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


SchedulerUtil.cron_job()
