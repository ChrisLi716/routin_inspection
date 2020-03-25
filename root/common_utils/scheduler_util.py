from root.common_utils.log_util import Logger

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import traceback


class SchedulerUtil:
    logger = Logger.get_instance()

    scheduler = BackgroundScheduler()

    @staticmethod
    def cron_job(func, crontab_exp, scheduler_name):
        try:
            SchedulerUtil.scheduler.add_job(func, CronTrigger.from_crontab(crontab_exp), id=scheduler_name)
            SchedulerUtil.scheduler.start()
            SchedulerUtil.logger.info(
                "add scheduler for func [" + scheduler_name + "] success. start at : " + crontab_exp)
        except Exception:
            SchedulerUtil.logger.error(traceback.format_exc())
