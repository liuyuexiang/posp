 #coding=utf-8
import numpy as np
from log import PlatformLog

msg_type_dict = {
    "TERMINAL_REG_REQ":"0100",
    "TERMINAL_REG_RSP":"0810",
}

msg_type_dict_fun = {
    "0100":"func_0100",
    
}

print_dict_fun = {
    "0100":"print_0100",
    
}

deal_dict_fun = {
    "0100":"deal_0100",
    
}



def chk(hex_str):
    x_b = b''
    for x in bytes().fromhex(hex_str):
      if x_b == b'':
        x_b = x
        continue
      x_b = np.bitwise_xor(x_b,x)
    return format(x_b,'02x')

class Msg:
    @staticmethod
    def start(self,str):
        PlatformLog.info('开始处理消息[%s]',str)
        msg_head = self.print_head(str[2:len(str)])
        msg = str[2:len(str)-2]
        msg_type = msg[0:4]
        chk_str = msg[len(msg)-2:len(msg)]
        local_chk_str = chk(msg[0:len(msg)-2])
        be_called_function = getattr(self, print_dict_fun[msg_type])
        msg_body = be_called_function(self,msg)
        # print (msg_body)
        if(local_chk_str != chk_str):
           PlatformLog.error('消息校验不通过,校验码[%s],本地校验码为[%s]',chk_str,local_chk_str)
        else:
            print('pass')
            be_called_function = getattr(self, deal_dict_fun[msg_type])
            be_called_function(self,msg_body)
        # if msg_type == msg_type_dict["TERMINAL_REG_REQ"]:
        #     be_called_function = getattr(self, msg_type_dict_fun[msg_type])
        #     be_called_function(self,str)

    @staticmethod
    def print_head(str):
        msg_head = {}
        msg_head['msg_type'] = str[0:4]
        msg_head['msg_attr'] = str[4:8]
        msg_head['msg_terminal_sn'] = str[8:20]
        msg_head['msg_seq'] = str[20:24]
        PlatformLog.info('消息类型[%s]',msg_head['msg_type'])
        PlatformLog.info('消息体属性[%s]',msg_head['msg_attr'])
        PlatformLog.info('终端SN[%s]',msg_head['msg_terminal_sn'])
        PlatformLog.info('消息流水号[%s]',msg_head['msg_seq'] )
        return msg_head
        

    @staticmethod
    def func_0100(self,str):
        print(str[4:8])
        print(bytes().fromhex(str[4:8]))

    @staticmethod
    def print_0100(self,str):
        # PlatformLog.info('消息类型[%s]',str[0:4])
        # PlatformLog.info('消息体属性[%s]',str[4:8])
        # PlatformLog.info('终端SN[%s]',str[8:20])
        # PlatformLog.info('消息流水号[%s]',str[20:24])
        msg_body={}
        msg_body['equ_build'] = str[24:28]
        msg_body['auth_level'] = str[28:32]
        msg_body['equ_type'] = bytes().fromhex(str[32:42]).decode('utf-8')
        msg_body['iccid'] =  bytes().fromhex(str[42:82]).decode()
        msg_body['equ_seq'] = bytes().fromhex(str[82:96]).decode()
        msg_body['plate_color'] = str[96:98]
        msg_body['car_recognize'] = str[98:len(str)-2]

        PlatformLog.info('设备制造商[%s]',msg_body['equ_build'] )
        PlatformLog.info('鉴权等级[%s]',msg_body['auth_level'])
        PlatformLog.info('设备类型[%s]',msg_body['equ_type'])
        PlatformLog.info('ICCID[%s]',msg_body['iccid'] )
        PlatformLog.info('设备序列号[%s]',msg_body['equ_seq'] )
        PlatformLog.info('车牌颜色[%s]',msg_body['plate_color'] )
        PlatformLog.info('车辆标识[%s]',msg_body['car_recognize'])
        return msg_body
        # print(bytes().fromhex(str[4:8]))

    @staticmethod
    def deal_0100(self,msg_obj):
        PlatformLog.info('start deal terminal register [%s]',msg_obj)
        # print(msg_obj)
    



if __name__ == '__main__':
    obj = Msg()
    obj.start(obj,'7e010000369778990031720078595a00013937373839383938363034413731343231373030333334323739303033313732000000000000000000000000000000000000037e')
    # chk_value = chk('7e010000369778990031720078595a00013937373839383938363034413731343231373030333334323739303033313732000000000000000000000000000000000000037e')
    # print(chk_value)