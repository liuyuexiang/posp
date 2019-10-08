import logging

import pika

from rabbitmq_template import RabbitmqTemplate


class RabbitmqRcv(RabbitmqTemplate):

    def __init__(self):
        super(RabbitmqRcv, self).__init__()

    # 消息处理函数，执行完成才说明接收完成，此时才可以接收下一条，串行
    def dongcallbackfun(self, bodyx):
        # print("得到的数据为:", bodyx)
        pass

    def rcv(self):
        # 接收准备
        self.channelx.basic_consume(self.queuename,  # 队列名
                                    self.on_request,  # 收到消息的回调函数
                                    False)  # 是否发送消息确认
        print("-------- 开始接收数据 -----------")

        # 开始接收消息
        self.channelx.start_consuming()

    # 收到消息就调用
    # ch 管道内存对象地址
    # method 消息发给哪个queue
    # props 返回给消费的返回参数
    # body数据对象
    def on_request(self, ch, method, props, body):
        # print("得到的数据为:[%s],消息队列为[%s]", body, props.reply_to)
        logging.debug("得到的数据为:%s,消息队列为%s" % (body, props.reply_to))
        ch.basic_publish(exchange='',
                         # 生产端随机生成的queue
                         routing_key=props.reply_to,
                         # 获取UUID唯一 字符串数值
                         properties=pika.BasicProperties(correlation_id= \
                                                             props.correlation_id),
                         # 消息返回给生产端
                         body=self.dongcallbackfun(body))
        # 确保任务完成
        ch.basic_ack(delivery_tag=method.delivery_tag)

# RabbitmqRcv().rcv()
