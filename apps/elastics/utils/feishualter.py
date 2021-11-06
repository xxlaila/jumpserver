# -*- coding: utf-8 -*-
"""
@File    : feishualter.py
@Time    : 2021/10/22 2:23 下午
@Author  : xxlaila
@Software: PyCharm
"""

import json, requests
import logging
import time
from django.conf import settings

try:
    JSONDecodeError = json.decoder.JSONDecodeError
except AttributeError:
    JSONDecodeError = ValueError

def is_not_null_and_blank_str(content):
    '''
    非空字符串
    :param content:  字符串
    :return: 非空 - True，空 - False
    '''
    if content and content.strip():
        return True
    else:
        return False

class FeishuAlter:

    def __init__(self, fail_notice=False):
        '''
        :param fail_notice: 消息发送失败提醒，默认为False不提醒，开发者可以根据返回的消息发送结果自行判断和处理
        '''
        super(FeishuAlter, self).__init__()
        self.webhook = settings.FEISHU['WEBHOOK']
        self.key_words = settings.FEISHU['KEY_WORDS']
        self.headers = {'Content-Type': 'application/json'}
        self.fail_notice = fail_notice

    def send_text(self, msg):
        '''
        消息类型为text类型
        :param msg: 消息内容
        :return: 返回消息发送结果
        '''
        data = {"msg_type": "text", "at": {}}
        if is_not_null_and_blank_str(msg):
            data["content"] = {"text": msg}
        else:
            logging.error("text类型，消息内容不能为空！")
            raise ValueError("text类型，消息内容不能为空！")

        logging.debug('text类型：%s' % data)
        return self.SendMessage(data)

    def SendMessage(self, data):
        '''
        富文本消息
        发送消息（内容UTF-8编码）
        :param data: 消息数据（字典）
        :return: 返回消息发送结果
        '''
        try:
            response = requests.request("POST", self.webhook, headers=self.headers, data=json.dumps(data))
        except requests.exceptions.HTTPError as exc:
            logging.error("消息发送失败，Http error: %d, reasion: %s" % (exc.response.status_code, exc.response.reason))
        except requests.exceptions.ConnectionError:
            logging.error("消息发送失败，HTTP connection error!")
            raise
        except requests.exceptions.Timeout:
            logging.error("消息发送失败，Timeout error!")
            raise
        except requests.exceptions.RequestException:
            logging.error("消息发送失败, Request Exception!")
            raise
        else:
            try:
                result = response.json()
            except JSONDecodeError:
                logging.error("服务器响应异常，状态码：%s，响应内容：%s" % (response.status_code, response.text))
                return {'errcode': 500, 'errmsg': '服务器响应异常'}
            else:
                logging.debug('发送结果：%s' % result)
                if self.fail_notice and result.get('errcode', True):
                    time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                    error_data = {
                        "msgtype": "text",
                        "text": {
                            "content": "[注意-自动通知]飞书机器人消息发送失败，时间：%s，原因：%s，请及时跟进，谢谢!" % (
                                time_now, result['errmsg'] if result.get('errmsg', False) else '未知异常')
                        },
                        "at": {
                            "isAtAll": False
                        }
                    }
                    logging.error("消息发送失败，自动通知：%s" % error_data)
                    requests.post(self.webhook, headers=self.headers, data=json.dumps(error_data))
            # print(result)
            return result