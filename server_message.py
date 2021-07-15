from socket import *
import auction_pb2
import threading
import time
import pandas as pd


server_ip = gethostname()
server_port = 12345

class Server():
    def __init__(self):
        # server属性
        self.sock = socket(AF_INET,SOCK_DGRAM)  # 套接字
        self.sock.bind((server_ip, server_port))
        self.client_pool = {}  # 客户池 {id:[address,name,key]}
        self.id_now = 0  # 当前可分配的id号
        self.is_auction_begin = 0  # 拍卖是否开始
        self.licence_num = 10  # 车牌总数
        self.licence_range = (0,9)  # 车牌范围
        self.floor_price = 1000  # 车牌起拍价
        self.price_range = [1000, 1060]  # 合理出价区间
        self.current_lowest_bid = (1000, 0, 0)  # 当前最低竞拍价格，出价时间，出价人id
        self.bidder_pool = []  # 当前能够中标的人元组(id,[address,name,key])
        self.mean_bid_price = 0  # 平均中标价格
        self.run()  # 调度recv函数开始listen消息


    # 运行多个线程
    def run(self):
        t_recv = threading.Thread(target = self.recv)
        # t_recv.setDaemon(True)
        t_recv.start()

    # 服务器端接收消息
    def recv(self):
        while True:
            data, address = self.sock.recvfrom(1024)
            message_r = auction_pb2.Message()
            message_r.ParseFromString(data)  # 解析消息
            # 调度函数处理请求
            if message_r.type == 0:  # signin request
                self.bidderID_distributor(message_r, address)
            elif message_r.type == 2:  # refresh request
                self.msg(bidderID=message_r.client.id)
            elif message_r.type == 12:  # login request
                self.login_handler(message_r, address)
            elif message_r.type == 7:  # ask for leave
                self.leave_handler(message_r)
            elif self.is_auction_begin == 0:  # 拍卖还没开始
                continue
            else:  # 拍卖已经开始了
                if message_r.type == 4:  # bid request
                    self.new_bid_handler(message_r)


    # 生成一个AuctionStatus的消息类，用当前的状态重写该类，并返回该类
    def wrap_status(self):
        status = auction_pb2.AuctionStatus()
        status.is_begin = self.is_auction_begin  # 拍卖是否开始
        status.current_competitor = len(self.client_pool)  # 当前登录人数
        status.licence.num = self.licence_num  # 拍卖车牌总数
        status.licence.lower_bound = self.licence_range[0]  # 拍卖车牌号码最低号
        status.licence.upper_bound = self.licence_range[1]  # 拍卖车牌号码最高号
        status.floor_price = self.floor_price
        status.lowest_price = self.current_lowest_bid[0]
        status.lowest_time = self.current_lowest_bid[1]
        # status.current_time = time.asctime(time.localtime(time.time()))
        status.current_time = time.time()  # 当前时间
        return status


    def bidderID_distributor(self,message_r,address):
        """
        分配id给新登录用户
        :param address: (str,str)UDP套接字二元组
        """
        message = message_r
        message.client.id = self.id_now
        message.type = 1  # 消息类型为分配id响应

        self.df = pd.read_excel('client_pool.xlsx')  # 读取储存客户信息的表单
        data = pd.DataFrame(self.df)
        data.loc[self.id_now] = [self.id_now,str(address),  # 新增一行用户信息
                                 str(message.client.name),
                                 str(message.client.key)]
        data.to_excel('client_pool.xlsx',index = False)  # 写入电子表格
        self.id_now += 1  # 可分配id后移一位
        login_rsp_m_bytes = message.SerializeToString()  # 序列化准备发送的消息
        self.sock.sendto(login_rsp_m_bytes, address)  # 发送消息给客户端

    # 登录处理
    def login_handler(self, message_r, address):
        self.df = pd.read_excel('client_pool.xlsx')
        data = pd.DataFrame(self.df)
        client_info = data.values[message_r.client.id]
        input_key = message_r.client.key  # 取得用户输入的密码
        message_s = auction_pb2.Message()
        print("用户client_info[{}]登录了".format(message_r.client.id))
        if str(client_info[3]) == input_key:  # 密码正确
            message_s.type = 13  # 成功登录
        else:
            message_s.type = 14 # 登陆失败密码错误
        msg_bytes = message_s.SerializeToString()
        self.sock.sendto(msg_bytes,address)  # 发送消息
        if message_s.type == 13:  # 登录成功的时候
            # 往id池中加入该client信息（cookie）
            self.client_pool[message_r.client.id] = [address,
                                             str(client_info[2]),
                                             message_r.client.key,
                                             ]
            self.msg(bidderID=message_r.client.id)  # 把当前状态通知给客户

    # 群发和向指定用户发送消息，用以某些提示。
    def msg(self, data='', bidderID = -1):
        message = auction_pb2.Message()
        message.type = 3
        message.status.CopyFrom(self.wrap_status())
        message.data = data
        msg_bytes = message.SerializeToString()  # 序列化
        if(bidderID != -1):  # 单独发消息
            address = self.client_pool[bidderID][0]
            self.sock.sendto(msg_bytes, address)
        else:  # 群发
            for id,value in self.client_pool.items():
                address = value[0]  # 套接字二元组
                self.sock.sendto(msg_bytes,address)


    # 新的投标到来，对整个投标进行排序
    def new_bid_handler(self,message_r):
        message_r.client.price_time = time.time()  # 服务器端接收到bid的时间
        client_bid = (message_r.client.price,
                 message_r.client.price_time,
                 message_r.client.id)
        message = message_r

        if client_bid[0]<self.price_range[0] or client_bid[0]>self.price_range[1]:
            # 投标价格不合理
            message.type = 6  # 错误的竞价
            msg_bytes = message.SerializeToString()  # 返回失败消息
            self.sock.sendto(msg_bytes,self.client_pool[message_r.client.id][0])

        else:  # 接受并处理该投标
            if len(self.bidder_pool)<self.licence_num:  # 当前竞价人还少于车牌数目
                self.bidder_pool.append(client_bid)  # 加入竞价池中 竞价池大小至多为车牌总数
            # 当前竞价人多于车牌数目
            elif message_r.client.price > self.current_lowest_bid[0]:
                del self.bidder_pool[self.licence_num-1]  # 删除出价最低的那个
                self.bidder_pool.append(client_bid)
            # 竞标价格从高到低排序,修改当前最低可中标信息（就是中标人群中价格最低的那位的信息）
            self.bidder_pool.sort(key=lambda clientbid:clientbid[0], reverse=True)
            self.current_lowest_bid = self.bidder_pool[-1]  # 取竞价池中价位最低的
            # 修改合理价格区间
            self.price_range[0] = max(self.current_lowest_bid[0]-30, self.floor_price)
            self.price_range[1] = self.current_lowest_bid[0]+30
            # 返回成功消息
            message.type = 5
            message.status.CopyFrom(self.wrap_status())
            msg_bytes = message.SerializeToString()
            self.sock.sendto(msg_bytes, self.client_pool[message_r.client.id][0])  # 发送消息给客户

    # 处理客户端离开请求
    def leave_handler(self, message_r):
        # 客户在中标人群内
        id = message_r.client.id
        address = self.client_pool[id][0]
        message_s = auction_pb2.Message()
        for i in self.bidder_pool:
            # 如果当前这个人属于中标人群内
            if i[2] == id:
                message_s.type = 9  # deny leave request
                message_s.data = "你不能离开！\n"
                break
        else:
            message_s.type = 8  # allow to leave
            message_s.data = "你可以离开,欢迎下次再来\n"
            data_to_all = "用户id为：{}的客户离开拍卖\n".format(id)
            del self.client_pool[id]  # 从客户池中删除该人
            self.msg(data_to_all, -1)  # 广播离开消息

        msg_bytes = message_s.SerializeToString()  # 发送离开应答消息给原客户
        self.sock.sendto(msg_bytes, address)

    # # 列出当前参加竞拍者的情况
    # def list(self):
    #     # for id,value in self.client_pool.items():
    #     print(self.client_pool)

    # 将某竞拍参与者踢出竞拍室，以防止一些捣乱的竞拍者，如胡乱出价者。并且向参加
    # 该拍卖中的其他人发送踢出的消息。
    def kick_out(self, bidderID):
        message = auction_pb2.Message()
        message.type = 8  # allow to leave or ask to leave
        message.data = "管理员已将您移出拍卖会\n"
        data_to_all = "用户id为：{}的客户被移出拍卖会\n".format(bidderID)
        self.msg(data_to_all, -1)  # 广播离开消息
        msg_bytes = message.SerializeToString()  # 发送离开应答消息给原客户
        self.sock.sendto(msg_bytes, self.client_pool[bidderID][0])
        del self.client_pool[bidderID]  # 从客户池中删除该人

    #  开始车牌拍卖，并将本次拍卖的有关情况如本次拍卖车牌数，拍卖持续时间通知已登录的用户
    def open_new_auction(self):
        message = auction_pb2.Message()
        self.is_auction_begin = 1
        self.msg(data="拍卖开始了各位！\n",bidderID=-1)  # 广播拍卖开始消息

    #  关闭本次车牌拍卖，并将本次最低中标价，最高中标价，平均中标价每位参拍者是否
    #  中标，车牌价钱通知每一位参加竞拍者。
    def close_auction(self):
        self.msg(data="拍卖结束了各位！\n", bidderID=-1)  # 广播拍卖结束消息
        message_s = auction_pb2.Message()
        message_s.type = 11  # server 结束拍卖信息
        if(self.bidder_pool):
            message_s.result.highest_bid_price = self.bidder_pool[0][0]  # 最高中标价
            message_s.result.lowest_bid_price = self.bidder_pool[-1][0]  # 最低中标价
        mean_price = 0
        if(self.bidder_pool):  # 投标人数不为0
            for bidder in self.bidder_pool:
                mean_price+=bidder[0]
            mean_price /= len(self.bidder_pool)  # 平均中标价格
            message_s.result.mean_bid_price = mean_price
            self.mean_bid_price = mean_price
        message_s.data = "恭喜您拍到车牌了\n"
        # 先对中标的人发消息
        for bidder in self.bidder_pool:
            address = self.client_pool[bidder[2]][0]
            message_s.result.is_win = 1  # 表示中标了
            message_s.result.plate_price = bidder[0]  # 等于投标价格
            msg_bytes = message_s.SerializeToString()
            self.sock.sendto(msg_bytes,address)  # 发送中标消息
            del self.client_pool[bidder[2]]  # 从客户池中删除该人

        # 然后对没有中标的人发消息
        message_s.result.is_win = 0
        message_s.result.plate_price = 0
        message_s.data = "很遗憾您没有拍到车牌\n"
        for id,value in self.client_pool.items():
            address = value[0]
            msg_bytes = message_s.SerializeToString()
            self.sock.sendto(msg_bytes, address)  # 发送没有中标消息


if __name__ == '__main__':
    server = Server()
    server.open_new_auction()
