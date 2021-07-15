from socket import *
import auction_pb2
import time
import threading
# 试一下socket
server_ip = gethostname()
server_port = 12345
address = (server_ip,server_port)

class Client():
    def __init__(self):
        # client属性
        self.sock = socket(AF_INET,SOCK_DGRAM)  # 新建一个客户套接字
        self.name = "Alice"
        self.id = -1  # 初始值
        self.key = ''

    # 启动多个线程
    def start(self):
        t_recv = threading.Thread(target=self.keep_recv)
        t_recv.setDaemon(True)
        t_recv.start()

    # 接受数据
    def recv(self):
        # 接受服务端消息
        data = self.sock.recv(1024)
        message_r = auction_pb2.Message()
        message_r.ParseFromString(data)  # 解析消息

        if message_r.type == 1:  # 分配id
            return self.recv_id_handler(message_r)
        elif message_r.type == 3:  # 当前拍卖状态通知
            # 展示拍卖状态
            return self.recv_status_handler(message_r)
        elif message_r.type == 5:  # 竞价成功
            return self.recv_bid_succeed_handler(message_r)
        elif message_r.type == 6:  # 竞价失败
            return self.recv_bid_failed_handler(message_r)
        elif message_r.type == 8:  # 允许离开
            s = "您可以离开，再见~\n"
            return s
        elif message_r.type == 9:  # 拒绝离开
            s = "您不能离开\n"
            return s
        # elif message_r.type == 10:  # 拍卖开始
        #     print(message_r.type,message_r.data)
        elif message_r.type == 11:  # 拍卖结束
            # 展示拍卖结果
            return self.recv_end_handler(message_r)
        elif message_r.type == 13:  # 成功登录
            return 0
        elif message_r.type == 14:  # 登陆失败
            return -1
            
            # time.sleep(5)

    def keep_recv(self):
        while True:
            self.recv()
    # 登录
    def login(self,id,key):
        self.id = int(id)
        self.key = key
        message_s = auction_pb2.Message()
        message_s.type = 12
        message_s.client.id = self.id
        message_s.client.key = self.key
        msg_bytes = message_s.SerializeToString()
        self.sock.sendto(msg_bytes,address)


    # 注册
    def signin(self,name,key):
        self.name = name
        self.key = key
        message_s = auction_pb2.Message()
        message_s.type = 0  # 分配id请求
        message_s.client.name = self.name
        message_s.client.id = self.id
        message_s.client.key = self.key
        login_req_m_bytes = message_s.SerializeToString()  # 序列化准备发送的消息
        self.sock.sendto(login_req_m_bytes, address)  # 发送消息

    # 收到type == 1 的message：接受分配的id
    def recv_id_handler(self,message_r):
        self.id = message_r.client.id  # 接受server分配的id
        s = "您的用户名:{}\n您的id:{}".format(message_r.client.name, message_r.client.id)
        return s  # 返回字符串

    def recv_bid_succeed_handler(self,message_r):
        s = "您:id = {},竞价成功\n投标价格为:{}\n投标时间为:{}\n".format(
            message_r.client.id,message_r.client.price,
            time.asctime(time.localtime(message_r.client.price_time)))
        return s

    def recv_bid_failed_handler(self,message_r):
        s = "竞价失败\n"
        return s

    def recv_status_handler(self,message_r):
        s = ''
        data = message_r.data
        if message_r.status.is_begin:
            s += "拍卖已经开始\n"
            s += "今日拍卖车牌数目:{}\n".format(message_r.status.licence.num)
            s += "车牌范围：[{},{}]\n".format(message_r.status.licence.lower_bound,
                                       message_r.status.licence.upper_bound)
            s += "起拍价:{}\n".format(message_r.status.floor_price)
            s += "当前最低可中标价格:{}\n".format(message_r.status.lowest_price)
            s += "当前最低可中标价格投标时间:{}\n".format(
                time.asctime(time.localtime(message_r.status.lowest_time)))
            s += "当前时间:{}\n".format(
                 time.asctime(time.localtime(message_r.status.current_time)))
        else:
            s += "拍卖还未开始\n"
        s += "当前在线人数:{}\n".format(message_r.status.current_competitor)

        if data != '':
            s += "服务器通知消息:{}\n".format(data)
        return s

    # 收到拍卖结束的消息
    def recv_end_handler(self,message_r):
        s = '拍卖结束了...\n'
        s += message_r.data  # 是否中标
        if(message_r.result.is_win):
            s += '您的中标价格为:{}\n'.format(message_r.result.plate_price)
        s += '本次拍卖结果:\n'
        s += '最高中标价格:{}\n'.format(message_r.result.highest_bid_price)
        s += '最低中标价格:{}\n'.format(message_r.result.lowest_bid_price)
        s += '平均中标价格:{}\n'.format(message_r.result.mean_bid_price)
        s += "当前时间:{}\n".format(
            time.asctime(time.localtime(time.time())))
        return s

    #登录成功
    # def recv_login_succeed(self):
    #     s = '登陆成功\n'
    #     return s

    #登录失败
    # def recv_login_failed(self):
    #     s = '用户id或密码错误,请重试\n'

    # 刷新
    def refresh(self):
        message_s = auction_pb2.Message()
        message_s.client.id = self.id
        message_s.type = 2
        login_req_m_bytes = message_s.SerializeToString()  # 序列化准备发送的消息
        self.sock.sendto(login_req_m_bytes, address)  # 发送消息

    #竞价
    def bid(self, price):
        message_s = auction_pb2.Message()
        message_s.client.id = self.id
        message_s.type = 4
        message_s.client.price = price  # 竞价价格
        login_req_m_bytes = message_s.SerializeToString()  # 序列化准备发送的消息
        self.sock.sendto(login_req_m_bytes, address)  # 发送消息

    # 离开
    def leave(self):
        message_s = auction_pb2.Message()
        message_s.type = 7  # 请求离开消息
        message_s.client.id = self.id
        msg_bytes = message_s.SerializeToString()  # 序列化
        self.sock.sendto(msg_bytes, address)  # 发送消息


       
if __name__ == '__main__':
    c = Client()
    # c.signin()
    c.login()
    c.start()
    # input("ready to fresh?\n")
    # c.refresh()
    x = input("bid price ?\n")
    c.bid(int(x))
    input("input q to leave\n")
    c.leave()
    time.sleep(2)










