import os
from root.common_utils.log_util import Logger
from root.common_utils.parse_xml import ParseXml
from root.mysql_opt.connection import MyConnection
from root.common_utils.excel_util import ExcelGenerator
from root.common_utils.email_utils import EmailUtils
from root.common_utils.scheduler_util import SchedulerUtil
from datetime import datetime
from threading import Lock
import re


class Dispatcher:
    logger = Logger.get_instance()

    __base_path = "../sources"
    __xml_file_path = __base_path + os.sep + "/sql.xml"
    __excel_extension = ".xlsx"
    __thread_lock = Lock()

    @classmethod
    def __tackle_routin_inspection_for_each_config(cls, sqlbean):
        try:
            if sqlbean:
                file_name = sqlbean.file_name
                biz_email_to = sqlbean.biz_email_to
                biz_email_cc = sqlbean.biz_email_cc
                tech_email_to = sqlbean.tech_email_to
                tech_email_cc = sqlbean.tech_email_cc
                sql = sqlbean.sql
                header = Dispatcher.build_header(sqlbean.sql)

                comment = sqlbean.comment
                email_body = sqlbean.email_body

                excel_file_dir = cls.__base_path + os.sep + "excel"

                now = datetime.now()
                time2file = now.strftime("%Y%m%d%H%M%S%f")
                time2email = now.strftime("%Y-%m-%d %H:%M:%S.%f")

                excel_file_name = file_name + "_" + time2file + cls.__excel_extension
                file_path = excel_file_dir + os.sep + excel_file_name
                cls.logger.info("going to generate excel file:" + file_path)
                my_conn = MyConnection()
                cursor = my_conn.cursor
                cls.logger.info("begin to query sql : " + sql)
                cursor.execute(sql)
                result_set = cursor.fetchall()
                cls.logger.info("result_set_size:" + str(len(result_set)))
                if result_set:
                    generate_excel_succeed = ExcelGenerator.generate_excel_file(header, result_set, file_path)
                    file_tuple = (file_path,)
                    if generate_excel_succeed:
                        if biz_email_to:
                            EmailUtils.sent_email(biz_email_to, biz_email_cc, comment,
                                                  email_body.format(time=time2email, count=len(result_set)),
                                                  file_tuple)
                        if tech_email_to:
                            EmailUtils.sent_email(tech_email_to, tech_email_cc, comment,
                                                  email_body.format(time=time2email, count=len(result_set)), file_tuple)
                else:
                    if tech_email_to:
                        EmailUtils.sent_email(tech_email_to, tech_email_cc, comment,
                                              email_body.format(time=time2email, count=len(result_set)))
        finally:
            my_conn.close_conn()

    @classmethod
    def build_header(cls, sql_tmp):
        # get the header for excel file
        if sql_tmp:
            sql_tmp = str(sql_tmp).lower()
            begin_index = sql_tmp.index("select") + 7
            end_index = sql_tmp.index("from") - 1
            header_list = sql_tmp[begin_index:end_index].strip().split(", ")

            excel_file_header = []
            for tmp in header_list:
                if "as" in tmp:
                    as_index = tmp.index("as")
                    column_index = as_index + 2
                    header = tmp[column_index:len(tmp)]
                elif "." in tmp:
                    dot_index = tmp.index(".") + 1
                    header = tmp[dot_index:len(tmp)]
                else:
                    header = tmp

                excel_file_header.append(re.sub("'", "", header.strip()))

            cls.logger.info("header:" + str(excel_file_header))
        return excel_file_header

    @classmethod
    def assign_to_scheduler(cls):
        sql_beans = ParseXml.parsexml2bean(Dispatcher.__xml_file_path)
        if sql_beans:
            for sqlbean in sql_beans:
                if sqlbean:
                    scheduler_time = sqlbean.scheduler
                    func_name = sqlbean.file_name
                    running = sqlbean.running
                    if running.capitalize() == str(True):
                        # rename func for scheduler job
                        # since the add_job method of apscheduler can't be same for multiple job
                        setattr(cls, func_name, cls.__tackle_routin_inspection_for_each_config)
                        func = getattr(cls, func_name)
                        SchedulerUtil.cron_job(func, scheduler_time, func_name, (sqlbean,))

            SchedulerUtil.scheduler.start()
            cls.logger.info("scheduler start at :" + str(datetime.now()))
