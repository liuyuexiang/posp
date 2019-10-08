import logging

from rabbitmq_rcv import RabbitmqRcv
from yml_config import SysConfig


class MsgDeal(RabbitmqRcv):
    # def __int__(self):
    #     super(MsgDeal, self).__init__()

    def dongcallbackfun(self, bodyx):
        logging.debug("得到的数据为:%s" % bodyx)
        msgdispatch = MsgDispatch()
        msg = msgdispatch.dealmsg(bodyx)
        return msg


class MsgDispatch(SysConfig):
    def __int__(self):
        super(MsgDispatch, self).__init__()

    def dealmsg(self, msg):
        logging.debug("得到的数据为:%s" % msg)
        if len(msg) < 4:
            return "消息长度小于4"
        return "应答成功"


MsgDeal().rcv()
