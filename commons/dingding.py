from datetime import datetime

from dingtalkchatbot.chatbot import DingtalkChatbot

# 可以改为自己的钉钉机器人
webhook = 'https://oapi.dingtalk.com/robot/send?access_token=xxx'
secret = 'xxx'


def send_dingding_msg(text):
    """
    发送指定dingding消息
    :param text:
    :return:
    """
    try:
        ding = DingtalkChatbot(webhook=webhook, secret=secret)
        msg = text + "\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ding.send_text(msg=f"{msg}\n\n", is_at_all=True)
        print('发送钉钉成功')
    except BaseException as e:
        print('钉钉发送信息出错了, ', str(e))
