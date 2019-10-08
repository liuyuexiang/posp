import logging
import time
import uuid

import pika

from rabbitmq_template import RabbitmqTemplate


class RabbitmqSend(RabbitmqTemplate):

    def __init__(self):
        super().__init__()
        # 　随机一次唯一的字符串
        self.corr_id = str(uuid.uuid4())
        # 生成随机queue
        self.response = None
        result = self.channelx.queue_declare('', exclusive=True)
        # 随机取queue名字，发给消费端
        self.callback_queue = result.method.queue
        self.rcv()

    def __int__(self):
        super(RabbitmqTemplate, self).__init__()

    def send(self, msg=""):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        # 发送数据，发送一条，如果要发送多条则复制此段
        self.channelx.basic_publish(exchange="",
                                    routing_key=self.queuename,  # 队列名
                                    body=msg,  # 发送的数据
                                    properties=pika.BasicProperties(
                                        delivery_mode=2,  # 实现消息永久保存
                                        # 执行命令之后结果返回给self.callaback_queue这个队列中
                                        reply_to=self.callback_queue,
                                        # 生成UUID 发送给消费端
                                        correlation_id=self.corr_id,
                                    )
                                    )
        logging.debug("--------发送数据完成-----------")
        logging.debug("发送数据为:%s" % msg)
        logging.debug("回调队列为:%s" % self.callback_queue)

        while self.response is None:
            # 非阻塞版的start_consuming()
            # 没有消息不阻塞
            self.conn.process_data_events()
            logging.debug("no msg...")
            time.sleep(0.5)
        return self.response
        # 关闭连接
        # self.conn.close()

    def rcv(self):

        # self.on_response 回调函数:只要收到消息就调用这个函数。
        # 声明收到消息后就 收queue=self.callback_queue内的消息
        self.channelx.basic_consume(self.callback_queue,  # 队列名
                                    self.on_response,  # 收到消息的回调函数
                                    False)  # 是否发送消息确认

    # 收到消息就调用
    # ch 管道内存对象地址
    # method 消息发给哪个queue
    # body数据对象
    def on_response(self, ch, method, props, body):
        # 判断本机生成的ID 与 生产端发过来的ID是否相等
        if self.corr_id == props.correlation_id:
            # 将body值 赋值给self.response
            self.response = body

    def response_deal(self):
        pass

# RabbitmqSend().send("hello")
# RabbitmqSend().rcv()
