 #coding=utf-8
import numpy as np
from log import PlatformLog
import pymongo
import config
# import time
from datetime import datetime
from dictionary import warn_dict

msg_type_dict = {
    "TERMINAL_REG_REQ":"0100",
    "TERMINAL_REG_RSP":"0810",
}

msg_type_dict_fun = {
    "0100":"func_0100",
    
}

print_dict_fun = {
    "0100":"print_0100",#终端注册
    "0102":"print_0102",#终端登陆鉴权
    "0002":"print_0002",#终端心跳
    "0900":"print_0900",#终端数据上行透传
    "0200":"print_0200",#终端位置信息汇报
}

deal_dict_fun = {
    "0100":"deal_0100", 
    "0102":"deal_0102",
    "0002":"deal_0002",
    "0900":"deal_0900",
    "0200":"deal_0200",#终端位置信息汇报
}

reg_res_dic = {
    "success":"00",
    "fail":"01",
    "no_car":"02",
    "registered":"03",
    "no_terminal":"04"
}

message_sub_type_dic = {
    "obd": "01",  #obd数据流上报
    "fault": "02",  #故障码数据上报
    "warn": "03",  #告警数据及驾驶行为数据上报
    "drive": "04",  #行程报告数据上报
}

drive_attr_dic = {
    "start": "01",
    "stop": "02"
}

base_key = '123456'

myclient = pymongo.MongoClient(config.db_url)

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
        str = str.replace('7d02','7e')
        str = str.replace('7d01','7d')
        PlatformLog.info('转义后字符串[%s]',str)
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
            be_called_function = getattr(self, deal_dict_fun[msg_type])
            ret_msg = be_called_function(self,msg_head,msg_body,reg_res_dic['fail'])
            return ret_msg
        else:
            print('pass')
            be_called_function = getattr(self, deal_dict_fun[msg_type])
            ret_msg = be_called_function(self,msg_head,msg_body,reg_res_dic['success'])
            return ret_msg
        # if msg_type == msg_type_dict["TERMINAL_REG_REQ"]:
        #     be_called_function = getattr(self, msg_type_dict_fun[msg_type])
        #     be_called_function(self,str)

    @staticmethod
    def print_head(str):
        msg_head = {}
        msg_head['msg_type'] = str[0:4]
        msg_head['msg_attr'] = str[4:8] #+ bytes.fromhex(str[6:8]).decode('utf-8').rjust(2,'0')
        # print(msg_head['msg_attr'])
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
    def deal_0100(self,msg_head,msg_body,res):
        PlatformLog.info('开始处理终端注册 [%s][%s]',msg_head,msg_body)
        # print(msg_obj)
        # msg_head['msg_attr'] = bytes.fromhex(msg_head['msg_attr']).decode('utf-8').rjust(5,'0')
        # print(msg_head['msg_attr'])
        msg_attr = msg_head['msg_attr'][0:2]
        # print(msg_attr)
        msg_attr += bytes.fromhex(msg_head['msg_attr'][2:]).decode('utf-8').rjust(2,'0')
        # print(msg_attr)
        str = '8100'
        str += msg_attr
        str += msg_head['msg_terminal_sn']
        str += msg_head['msg_seq']
        str += msg_head['msg_seq']
        str += res
        str += base_key
        # print(str)
        str += chk(str)
        str = '7e' + str + '7e'
        # print(str)
        return str
        # print(chk(str))

    @staticmethod
    def print_0102(self,str):
        msg_body={}
        msg_body['base_key'] = str[24:]
        return msg_body
    
    @staticmethod
    def deal_0102(self,msg_head,msg_body,res):
        PlatformLog.info('开始处理终端登陆鉴权 [%s][%s]',msg_head,msg_body)
        # print(msg_obj)
        # str = '8001'
        # str += msg_head['msg_attr']
        # str += msg_head['msg_terminal_sn']
        # str += msg_head['msg_seq']
        str = ''
        str += msg_head['msg_seq']
        str += msg_head['msg_type']
        str += res
        str = Msg.func_8001(self,msg_head,str)
        print(str)
        return str
    
    @staticmethod
    def print_0002(self,str):
        msg_body={}
        return msg_body
    
    @staticmethod
    def deal_0002(self,msg_head,msg_body,res):
        PlatformLog.info('开始处理终端心跳 [%s][%s]',msg_head,msg_body)
        # print(msg_obj)
        # str = '8001'
        # str += msg_head['msg_attr']
        # str += msg_head['msg_terminal_sn']
        # str += msg_head['msg_seq']
        str = ''
        str += msg_head['msg_seq']
        str += msg_head['msg_type']
        str += res
        str = Msg.func_8001(self,msg_head,str)
        print(str)
        return str
    
    @staticmethod
    def print_0900(self,str):
        msg_body={}
        msg_body['content']=str[24:len(str)-2]
        return msg_body
    
    @staticmethod
    def deal_0900(self,msg_head,msg_body,res):
        PlatformLog.info('开始处理终端数据上行透传 [%s][%s]',msg_head,msg_body)
        message_type = msg_body['content'][0:2]
        PlatformLog.info('透传消息类型[%s]',message_type)
        event_time = '20'+msg_body['content'][2:14]
        PlatformLog.info('事件产生时间[%s]',event_time)
        data_type = msg_body['content'][14:16]
        PlatformLog.info('数据类型[%s]',data_type)
        car_type = msg_body['content'][16:18]
        PlatformLog.info('车辆类型[%s]',car_type)
        message_sub_type = msg_body['content'][18:20]
        PlatformLog.info('消息子类[%s]',message_sub_type )

        mydb = myclient[config.db]
        terminal_event = mydb["terminal_event"]
        event ={
            'terminal_sn':msg_head['msg_terminal_sn'],
            'message_type':message_type,
            'event_time':event_time,
            'data_type':data_type,
            'car_type':car_type,
            'local_time':datetime.now().strftime(config.str_date_format0)
        
        }
        terminal_event.insert_one(event)
        
        if(message_sub_type == message_sub_type_dic['obd']):
            PlatformLog.info('OBD数据流解析: %s',msg_body['content'][20:])
            content = msg_body['content'][20:]
            data_num = int(content[0:2],16)
            start = 2
            obds=[]
            while data_num:
                obd ={}
                data_id = content[start:start+4]
                data_len = int(content[start+4:start + 4 + 2])
                data = content[start + 4 + 2:start + 4 + 2 + data_len*2]
                start = start + 4 +2 + data_len*2
                PlatformLog.info('数据ID[%s]数据长度[%s]数据内容[%s]',data_id,data_len,data)
                obd['terminal_sn'] = msg_head['msg_terminal_sn']
                obd['local_time'] = datetime.now().strftime(config.str_date_format0)
                obd['data_id'] = data_id
                obd['data_len'] = data_len
                obd['data'] = data
                obd['event_time'] = event_time
                obds.append(obd)
                data_num = data_num - 1
            print(obds)
            terminal_obd = mydb["terminal_obd"]
            if(len(obds)>0):
                terminal_obd.insert_many(obds)
        if(message_sub_type == message_sub_type_dic['fault']):
            PlatformLog.info('故障码数据解析: %s',msg_body['content'][20:])
            content = msg_body['content'][20:]
            data_num = int(content[0:4],16)
            start = 4
            faults= []
            while data_num:
                fault={}
                fault['sys_id'] = content[start:start+8]
                fault['fault_num'] = int(content[start+8:start+12],16)
                fault['fault_codes'] = content[start+12: start + 12 + 32 *fault['fault_num']]
                start = start + 12 + 32 *fault['fault_num']
                faults.append(fault)
                data_num = data_num - 1
            terminal_fault = mydb["terminal_fault"]
            terminal_fault.insert_many(faults)
            terminal_event.update_one({'terminal_sn':msg_head['msg_terminal_sn'],'event_time':event_time},
                                      {'$set':{'warn_status':content[start:start + 8],'lat':content[start + 8:start + 16],'lng':content[start + 16:start + 24]}})
        if(message_sub_type == message_sub_type_dic['warn']):
            PlatformLog.info('告警数据及驾驶行为数据解析: %s',msg_body['content'][20:])
            content = msg_body['content'][20:]
            data_num = int(content[0:2],16)
            start = 2
            warns= []
            while data_num:
                warn = {}
                warn['warn_data_id']=content[start:start+2]
                warn['warn_dict_content']=warn_dict[warn['warn_data_id'].upper()]
                warn['warn_data_len']=int(content[start+2:start+4],16)
                warn['warn_data_desc']=content[start+4:warn['warn_data_len']*2 + 4 + start]
                # warn['warn_status']=content[warn['warn_data_len']*2 + 4 + start : warn['warn_data_len']*2 + 12 + start]
                # warn['lat']=content[warn['warn_data_len']*2 + 12 + start : warn['warn_data_len']*2 + 20 + start]
                # warn['lng']=content[warn['warn_data_len']*2 + 20 + start : warn['warn_data_len']*2 + 28 + start]
                start = start + warn['warn_data_len']*2 + 4

                warn['terminal_sn'] = msg_head['msg_terminal_sn']
                warn['local_time'] = datetime.now().strftime(config.str_date_format0)
                warn['event_time'] = event_time

                warns.append(warn)
                data_num = data_num - 1
            terminal_warn = mydb["terminal_warn"]
            terminal_warn.insert_many(warns)
            terminal_event.update_one({'terminal_sn':msg_head['msg_terminal_sn'],'event_time':event_time},
                                      {'$set':{'warn_status':content[start:start + 8],'lat':content[start + 8:start + 16],'lng':content[start + 16:start + 24]}})
        if(message_sub_type == message_sub_type_dic['drive']):
            PlatformLog.info('行程报告数据解析: %s',msg_body['content'][20:])
            content = msg_body['content'][20:]
            drive_attr = content[0:2]
            terminal_drive = mydb["terminal_drive"]
            if(drive_attr == drive_attr_dic['start']):
                start = {}
                start['terminal_sn'] = msg_head['msg_terminal_sn']
                start['start_event_time'] = event_time
                start['start_local_time'] = datetime.now().strftime(config.str_date_format0)
                start['drive_seq'] = content[2:10]
                start['start_time'] = '20' + content[10:22]
                terminal_drive.insert_one(start)
            if(drive_attr == drive_attr_dic['stop']):
                stop = {}
                stop['terminal_sn'] = msg_head['msg_terminal_sn']
                stop['stop_event_time'] = event_time
                stop['stop_local_time'] = datetime.now().strftime(config.str_date_format0)
                stop['drive_seq'] = content[2:10]
                stop['start_time'] = '20' + content[10:22]
                stop['stop_time'] = '20' + content[22:34]
                stop['start_lat'] = int(content[34:42],16)
                stop['start_lng'] = int(content[42:50],16)
                stop['stop_lat'] = int(content[50:58],16)
                stop['stop_lng'] = int(content[58:66],16)
                stop['lat_lng_type'] = content[66:68]
                stop['zero_speed_count'] = int(content[68:72],16)
                stop['zero_speed_time'] = int(content[72:76],16)
                stop['drive_mile'] = int(content[76:80],16)
                stop['drive_oil'] = int(content[80:84],16)
                terminal_drive.update_one({'terminal_sn':stop['terminal_sn'],'drive_seq':stop['drive_seq'],'start_time':stop['start_time']},{'$set':stop})

        str = ''
        str += msg_head['msg_seq']
        str += msg_head['msg_type']
        str += res
        str = Msg.func_8001(self,msg_head,str)
        print(str)
        return str
    
    @staticmethod
    def print_0200(self,str):
        msg_body={}
        msg_body['content']=str[24:]
        return msg_body
    
    @staticmethod
    def deal_0200(self,msg_head,msg_body,res):
        PlatformLog.info('开始处理终端位置信息汇报 [%s][%s]',msg_head,msg_body)
        # print(msg_obj)
        # str = '8001'
        # str += msg_head['msg_attr']
        # str += msg_head['msg_terminal_sn']
        # str += msg_head['msg_seq']
        warn_flag = msg_body['content'][0:8]
        print('报警标志',warn_flag)
        position_status = msg_body['content'][8:16]
        print('状态',position_status)
        lat = int(msg_body['content'][16:24],16)
        print('纬度',msg_body['content'][16:24],'十进制',lat)
        lng = int(msg_body['content'][24:32],16)
        print('经度',msg_body['content'][24:32],'十进制',lng)
        elevation = int(msg_body['content'][32:36],16)
        print('高程',msg_body['content'][32:36],'十进制',elevation)
        speed = int(msg_body['content'][36:40],16)*10
        print('速度',speed)
        direction = msg_body['content'][40:44]
        print('方向',direction)
        position_time = '20' + msg_body['content'][44:56]
        print('时间',position_time)

        mydb = myclient[config.db]
        terminal_position = mydb["terminal_position"]
        event ={
            'terminal_sn':msg_head['msg_terminal_sn'],
            'warn_flag':warn_flag,
            'position_status':position_status,
            'lat':lat,
            'lng':lng,
            'elevation':elevation,
            'speed':speed,
            'direction':direction,
            'position_time':position_time,
            'local_time':datetime.now().strftime(config.str_date_format0)
        
        }
        terminal_position.insert_one(event)

        str = ''
        str += msg_head['msg_seq']
        str += msg_head['msg_type']
        str += res
        str = Msg.func_8001(self,msg_head,str)
        return str
    
    @staticmethod
    def func_8001(self,msg_head,str):
        str1 = '8001'
        str1 += msg_head['msg_attr']
        str1 += msg_head['msg_terminal_sn']
        str1 += msg_head['msg_seq']
        str1 += str
        str1 += chk(str1)
        str1 = '7e' + str1 + '7e'
        return str1
    



if __name__ == '__main__':
    obj = Msg()
    # obj.start(obj,'7e010000369778990031720078595a00013937373839383938363034413731343231373030333334323739303033313732000000000000000000000000000000000000037e')
    # obj.start(obj,'7e010200039778990031720084123456c17e')
    # obj.start(obj,'7e0900001e977899003172000ef02303281538330001010305300235fc0546040000000005450400000000347e')
    obj.start(obj,'7e0900001997789900317200c7f0230330165047000103011c000000000d0000000000000000117e')
    # obj.start(obj,'7e0200001c977899003172000b0000000000000002015eac3206c1c6f8000e00000000230324164302477e')
    # warn_data_id='00'
    # print(warn_dict[warn_data_id])
    # obj.start(obj,'7e00020000977899003172000c3b7e')
    # chk_value = chk('7e010000369778990031720078595a00013937373839383938363034413731343231373030333334323739303033313732000000000000000000000000000000000000037e')
    # print(chk_value)
