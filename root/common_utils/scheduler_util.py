from root.common_utils.log_util import Logger

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import traceback
from datetime import datetime
import time


class SchedulerUtil:
    logger = Logger.get_instance()

    scheduler = BackgroundScheduler()

    @staticmethod
    def cron_job(func, crontab_exp, scheduler_name, args=None):
        try:
            SchedulerUtil.scheduler.add_job(func, max_instances=10, trigger=CronTrigger.from_crontab(crontab_exp),
                                            args=args,
                                            id=scheduler_name + str(datetime.now().strftime("%y%m%d%H%M%S%f")))
            SchedulerUtil.logger.info(
                "add scheduler for func [" + scheduler_name + "] success. start at : " + crontab_exp)
        except Exception:
            SchedulerUtil.logger.error(traceback.format_exc())

    @staticmethod
    def test_job():
        print("for testing purpose")


if __name__ == '__main__':
    SchedulerUtil.cron_job(func=SchedulerUtil.test_job, crontab_exp="* * * * *", scheduler_name="test_job")
    SchedulerUtil.scheduler.start()
    time.sleep(30 * 60)
