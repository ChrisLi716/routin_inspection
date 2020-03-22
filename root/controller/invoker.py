import os
from root.common_utils.log_util import Logger
from root.common_utils.parse_xml import ParseXml
from root.mysql_opt.connection import Connection
from root.common_utils.excel_util import ExcelGenerator
from root.common_utils.email_utils import EmailUtils

cursor = Connection.mycursor()

if __name__ == '__main__':
    logger = Logger.get_instance()
    sqlbean_list = ParseXml.parsexml2bean("")
    for sqlbean in sqlbean_list:
        if sqlbean:
            base_path = sqlbean.base_path
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
                header = sql[begin_index: end_index].strip().split(" ")

            comment = sqlbean.comment

            file_path = base_path + os.sep + file_name

            result_set = cursor.execute(sql)
            if result_set:
                generate_excel_succeed = ExcelGenerator.generate_excel_file(header, result_set, file_path)
                if generate_excel_succeed:
                    EmailUtils.sent_email(biz_email_to, comment, "body", tuple(file_path))
                    EmailUtils.sent_email(tech_email_to, comment, "body", tuple(file_path))
