import time

from ty_api_test.page.login_api import login
from ty_api_test.common.readconfig import *
from ty_api_test.common.readapi import *
import requests


from datetime import datetime,timedelta

# 获取当前时间
now = datetime.now()

# 将当前时间格式化为字符串
formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
date1 = now + timedelta(weeks=1)

time1 = datetime

print("当前时间是:", formatted_now)
print(date1.strftime("%Y-%m-%d"))

#列表元素之和




