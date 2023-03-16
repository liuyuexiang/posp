
from log import PlatformLog
import select
from socket import *
# from rabbitmq_send import RabbitmqSend
from yml_config import SysConfig
import hex


# platFormLog = log.PlatformLog

class SocketServer(SysConfig):
    def __init__(self):
        # self.rabbitmqsend = RabbitmqSend()
        super(SocketServer, self).__init__()
        host = self.config['server']['host']
        port = self.config['server']['port']
        maxconn = self.config['server']['maxconn']
        self.s = socket()
        self.s.bind((host, port))
        self.s.listen(maxconn)
        self.s.setblocking(False)


class NonBlockingSocketServer(SocketServer):
    def __init__(self):
        super(NonBlockingSocketServer, self).__init__()
        r_list = []
        w_list = []
        while True:
            try:
                conn, addr = self.s.accept()
                r_list.append(conn)

            except BlockingIOError:
                # time.sleep(0.05)
                # print('可以去干其他的活了')
                # print('rlist: ', len(r_list))

                # 收消息
                del_rlist = []
                for conn in r_list:
                    try:
                        data = conn.recv(1024)
                        if not data:
                            conn.close()
                            del_rlist.append(conn)
                            continue

                        self.rabbitmqsend.send(data)
                        w_list.append((conn, self.rabbitmqsend))
                    except BlockingIOError:
                        continue
                    except ConnectionResetError:
                        conn.close()
                        # r_list.remove(conn)
                        del_rlist.append(conn)

                # 发消息
                del_wlist = []
                for item in w_list:
                    try:
                        conn = item[0]
                        _rabbitmqsend = item[1]
                        _rabbitmqsend.rcv()
                        PlatformLog.debug(_rabbitmqsend.response)
                        conn.send(_rabbitmqsend.response)
                        del_wlist.append(item)
                    except BlockingIOError:
                        continue
                    except ConnectionResetError:
                        conn.close()
                        del_wlist.append(item)

                # 回收无用连接
                for conn in del_rlist:
                    r_list.remove(conn)

                for item in del_wlist:
                    w_list.remove(item)


class SelectIOSocketServer(SocketServer):
    def __init__(self):
        super(SelectIOSocketServer, self).__init__()
        r_list = [self.s, ]

        w_list = []

        w_data = {}

        while True:

            PlatformLog.debug('被检测r_list：%d ', len(r_list))

            PlatformLog.debug('被检测w_list： %d', len(w_list))

            rl, wl, xl = select.select(r_list, w_list, [], )  # r_list=[server,conn] rl等存放等到数据的对象

            # print('rl: ',len(rl)) #rl=[conn,]

            # print('wl: ',len(wl))

            # 收消息

            for r in rl:  # r=conn

                if r == self.s:  # r l为已经有等到信息的对象，可能为s，亦可为conn；当为s时，执行accept，当为conn时，执行recv

                    conn, addr = r.accept()

                    PlatformLog.info('连接 %s ',conn)
                    PlatformLog.info('地址 %s',addr)

                    r_list.append(conn)  # 建立好连接后，将连接丢入r_list中监测

                else:

                    try:

                        data = r.recv(1024)

                        if not data:  # select模块不帮忙捕捉ConnectionResetError，此操作针对linux系统

                            r.close()

                            r_list.remove(r)

                            continue

                        # r.send(data.upper())
                        str = hex.Hex.bytes_to_hex(data)
                        PlatformLog.info('接收到数据 %s ', str)

                        w_list.append(r)

                        w_data[r] = data.upper()

                    except ConnectionResetError:  # select模块不帮忙捕捉ConnectionResetError，此操作针对windows系统

                        r.close()

                        r_list.remove(r)

                        continue

            # 发消息

            for w in wl:

                w.send(w_data[w])

                w_list.remove(w)

                w_data.pop(w)


# NonBlockingSocketServer()
SelectIOSocketServer()
