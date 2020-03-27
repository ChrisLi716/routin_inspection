import os
from root.common_utils.log_util import Logger
from root.common_utils.parse_xml import ParseXml
from root.mysql_opt.connection import Connection
from root.common_utils.excel_util import ExcelGenerator
from root.common_utils.email_utils import EmailUtils
from root.common_utils.scheduler_util import SchedulerUtil
from datetime import datetime


class Dispatcher:
    logger = Logger.get_instance()

    __base_path = "../sources"
    __xml_file_path = __base_path + os.sep + "/sql.xml"
    __excel_extension = ".xlsx"

    @classmethod
    def get_all_user(cls, sqlbean):
        cls.__tackle_routin_inspection(sqlbean)

    @classmethod
    def get_daily_new_user(cls, sqlbean):
        cls.__tackle_routin_inspection(sqlbean)

    @classmethod
    def __tackle_routin_inspection(cls, base_path, sqlbean):
        if sqlbean:
            file_name = sqlbean.file_name
            biz_email_to = sqlbean.biz_email_to
            biz_email_cc = sqlbean.biz_email_cc
            tech_email_to = sqlbean.tech_email_to
            tech_email_cc = sqlbean.tech_email_cc
            sql = sqlbean.sql
            header = Dispatcher.__build_header(sqlbean.sql)

            comment = sqlbean.comment
            file_path = base_path + os.sep + file_name + cls.__excel_extension
            cursor = Connection.mycursor()
            cursor.execute(sql)
            result_set = cursor.fetchall()
            cls.logger.info("sql:" + sql + ", size:" + str(len(result_set)))
            if result_set:
                generate_excel_succeed = ExcelGenerator.generate_excel_file(header, result_set, file_path)
                file_tuple = (file_path,)
                if generate_excel_succeed:
                    EmailUtils.sent_email(biz_email_to, biz_email_cc, comment, "", file_tuple)
                    EmailUtils.sent_email(tech_email_to, tech_email_cc, comment, "", file_tuple)

    @classmethod
    def __build_header(cls, sql_tmp):
        # get the header for excel file
        if sql_tmp:
            sql_tmp = str(sql_tmp).lower()
            begin_index = sql_tmp.index("select") + 7
            end_index = sql_tmp.index("from") - 1
            excel_file_header = sql_tmp[begin_index: end_index].strip().split(", ")
            Dispatcher.logger.info("header:" + str(excel_file_header))
        return excel_file_header

    @classmethod
    def assign_to_scheduler(cls):
        sql_beans = ParseXml.parsexml2bean(Dispatcher.__xml_file_path)
        if sql_beans:
            for sqlbean in sql_beans:
                if sqlbean:
                    scheduler_time = sqlbean.scheduler
                    func_name = sqlbean.file_name
                    SchedulerUtil.cron_job(cls.func_name, scheduler_time, (sqlbean,), func_name)
            SchedulerUtil.scheduler.start()
            Dispatcher.logger.info("scheduler start at :" + str(datetime.now()))
