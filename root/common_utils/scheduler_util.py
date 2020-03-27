from root.common_utils.log_util import Logger

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import traceback
from datetime import datetime


class SchedulerUtil:
    logger = Logger.get_instance()

    scheduler = BackgroundScheduler()

    @staticmethod
    def cron_job(func, crontab_exp, scheduler_name, **args):
        try:
            SchedulerUtil.scheduler.add_job(func, CronTrigger.from_crontab(crontab_exp), args,
                                            id=scheduler_name + str(datetime.now()))
            SchedulerUtil.logger.info(
                "add scheduler for func [" + scheduler_name + "] success. start at : " + crontab_exp)
        except Exception:
            SchedulerUtil.logger.error(traceback.format_exc())

    @staticmethod
    def test_job():
        print("1111")


if __name__ == '__main__':
    SchedulerUtil.cron_job(func=SchedulerUtil.test_job, crontab_exp="* * * * *", scheduler_name="test_job")
