import os
from root.common_utils.log_util import Logger
from root.common_utils.parse_xml import ParseXml
from root.mysql_opt.connection import Connection
from root.common_utils.excel_util import ExcelGenerator
from root.common_utils.email_utils import EmailUtils

cursor = Connection.mycursor()

if __name__ == '__main__':
    logger = Logger.get_instance()
    base_path = "../sources"
    file_path = base_path + os.sep + "/sql.xml"
    sqlbean_list = ParseXml.parsexml2bean(file_path)
    logger.info("sqlbean size : " + str(len(sqlbean_list)))
    for sqlbean in sqlbean_list:
        if sqlbean:
            file_name = sqlbean.file_name
            biz_email_to = sqlbean.biz_email_to
            biz_email_cc = sqlbean.biz_email_cc
            tech_email_to = sqlbean.tech_email_to
            tech_email_cc = sqlbean.tech_email_cc
            sql = sqlbean.sql

            # get the hader for excel file
            if sql:
                sql = str(sql).lower()
                begin_index = sql.index("select") + 7
                end_index = sql.index("from") - 1
                header = sql[begin_index: end_index].strip().split(", ")
                logger.info("header:" + str(header))

            comment = sqlbean.comment
            file_path = base_path + os.sep + file_name + ".xlsx"

            cursor.execute(sql)
            result_set = cursor.fetchall()
            logger.info("sql:" + sql)
            if result_set:
                generate_excel_succeed = ExcelGenerator.generate_excel_file(header, result_set, file_path)
                file_tuple = (file_path,)
                if generate_excel_succeed:
                    EmailUtils.sent_email(biz_email_to, biz_email_cc, comment, "body", file_tuple)
                    EmailUtils.sent_email(tech_email_to, tech_email_cc, comment, "body", file_tuple)
