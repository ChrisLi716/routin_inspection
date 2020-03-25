class SqlBean:
    def __init__(self, file_name, biz_email_to, biz_email_cc,
                 tech_email_to, tech_email_cc, sql, comment):
        self.file_name = file_name
        self.biz_email_to = biz_email_to
        self.biz_email_cc = biz_email_cc
        self.tech_email_to = tech_email_to
        self.tech_email_cc = tech_email_cc
        self.sql = sql
        self.comment = comment

    def __str__(self):
        lst = [self.file_name, self.biz_email_to, self.biz_email_cc, self.tech_email_to,
               self.tech_email_cc, self.sql, self.comment]
        return ",".join(lst)
