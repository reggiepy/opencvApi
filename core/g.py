# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2023/7/16 9:51
from py3utils.notify_utils.dingding import DingDingNotification
from core import settings

dingding = DingDingNotification(settings.DINGDING_ACCESS_TOKEN, settings.DINGDING_SECRET)
if __name__ == '__main__':
    dingding.send_text("test")
