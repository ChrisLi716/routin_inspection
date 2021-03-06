import re
import traceback
from lxml import etree
from root.beans.sqlbean import SqlBean
from root.common_utils.log_util import Logger


class ParseXml:
    logger = Logger.get_instance()

    @staticmethod
    def parse2sqlbean_by_attr_name(file_path, attr_name):
        try:
            sqlbean_list = []
            ParseXml.logger.info("file_path:" + file_path + ", attr_name:" + attr_name)
            parse = etree.parse(file_path, etree.XMLParser())
            ele_config_list = parse.xpath("//config[@name=\"" + attr_name + "\"]")
            biz_email_to = ""
            biz_email_cc = ""
            tech_email_to = ""
            tech_email_cc = ""

            if ele_config_list:
                ele_config = ele_config_list[0]
                config_name = ele_config.xpath("./@name")
                if config_name:
                    config_name = config_name[0]

                config_running = ele_config.xpath("./@running")
                if config_running:
                    config_running = config_running[0]
                biz_email = ele_config.xpath("./biz_email")
                if biz_email:
                    biz_email_to = biz_email[0].find("./to").text
                    biz_email_cc = biz_email[0].find("./cc").text

                tech_email = ele_config.xpath("./tech_email")
                if tech_email:
                    tech_email_to = tech_email[0].find("./to").text
                    tech_email_cc = tech_email[0].find("./cc").text

                sql = ele_config.find("./sql").text
                if sql:
                    sql = re.sub("[\\s]+", " ", sql)

                comment = ele_config.find("./comment").text
                scheduler = ele_config.find("./scheduler").text

                sqlbean = SqlBean(config_name, config_running, biz_email_to, biz_email_cc, tech_email_to, tech_email_cc,
                                  sql, comment, scheduler)

                ParseXml.logger.info("sqlbean: " + sqlbean.__str__())
            ParseXml.logger.info("sqlbean_list size:" + str(len(sqlbean_list)))

            return sqlbean

        except Exception:
            ParseXml.logger.error(traceback.format_exc())

    @staticmethod
    def parsexml2bean(file_path):
        try:
            sqlbean_list = []
            # parse = etree.parse("./sql.xml", etree.XMLParser())
            ParseXml.logger.info("file_path:" + file_path)
            parse = etree.parse(file_path, etree.XMLParser())
            ele_config_list = parse.xpath("//config")
            ParseXml.logger.info("config size : " + str(len(ele_config_list)))
            biz_email_to = ""
            biz_email_cc = ""
            tech_email_to = ""
            tech_email_cc = ""
            for ele_config in ele_config_list:
                config_name = ele_config.xpath("./@name")
                if config_name:
                    config_name = config_name[0]

                config_running = ele_config.xpath("./@running")
                if config_running:
                    config_running = config_running[0]

                biz_email = ele_config.xpath("./biz_email")
                if biz_email:
                    biz_email_to = biz_email[0].find("./to").text
                    biz_email_cc = biz_email[0].find("./cc").text

                tech_email = ele_config.xpath("./tech_email")
                if tech_email:
                    tech_email_to = tech_email[0].find("./to").text
                    tech_email_cc = tech_email[0].find("./cc").text

                comment = ele_config.find("./comment").text
                email_body = ele_config.find("./email_body").text

                ParseXml.logger.info("email_body:" + email_body)

                sql = ele_config.find("./sql").text
                if sql:
                    sql = re.sub("[\\s]+", " ", sql)

                scheduler = ele_config.find("./scheduler").text
                sqlbean = SqlBean(config_name, config_running, biz_email_to, biz_email_cc, tech_email_to, tech_email_cc,
                                  sql, comment, email_body, scheduler)
                ParseXml.logger.info("sqlbean: " + sqlbean.__str__())
                sqlbean_list.append(sqlbean)
                ParseXml.logger.info("sqlbean_list size:" + str(len(sqlbean_list)))

            return sqlbean_list

        except Exception:
            ParseXml.logger.error(traceback.format_exc())


if __name__ == '__main__':
    ParseXml.parsexml2bean("../sources/sql.xml")
    # ParseXml.parse2sqlbean_by_attr_name("../sources/sql.xml", "get_all_user")
