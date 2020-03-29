import sys
from root.common_utils.const import Const

const = Const()
const.MYSQL_SECTION = "mysql"
const.EMAIL_SECTION = "email"

print(sys.modules[__name__])
