from socket import *
import auction_pb2
import time
import threading

# 试一下socket
server_ip = gethostname()
server_port = 12345
address = (server_ip, server_port)

# client属性
sock = socket(AF_INET, SOCK_DGRAM)  # 新建一个客户套接字
name = "Alice"
id = -1  # 初始值
key = ''

# 启动多个线程
def start():
    t_recv = threading.Thread(target=recv)
    t_recv.setDaemon(True)
    t_recv.start()

# 接受数据
def recv():
    # 接受服务端消息
    while True:
        data = sock.recv(1024)
        message_r = auction_pb2.Message()
        message_r.ParseFromString(data)  # 解析消息

        if message_r.type == 1:  # 分配id
            # 取得id
            recv_id_handler(message_r)
        elif message_r.type == 3:  # 当前拍卖状态通知
            # 展示拍卖状态
            recv_status_handler(message_r)
        elif message_r.type == 5:  # 竞价成功
            recv_bid_succeed_handler(message_r)
        elif message_r.type == 6:  # 竞价失败
            recv_bid_failed_handler(message_r)
        elif message_r.type == 8:  # 允许离开
            # sock.close()
            print("允许离开")
            break  # 离开后要跳出循环
        elif message_r.type == 9:  # 拒绝离开
            # 显示不允许离开的消息
            print("you are not allowed to leave!")
        elif message_r.type == 10:  # 拍卖开始
            print(message_r.type, message_r.data)
        elif message_r.type == 11:  # 拍卖结束
            print(message_r.type, message_r.data)
            # 展示拍卖结果
        elif message_r.type == 13:  # 成功登录
            print("login!")
        elif message_r.type == 14:  # 登陆失败
            print("no login")

        # time.sleep(5)
    # exit(0)  # 正常结束进程

# 登录
def login():
    pass

# 注册
def signin():
    name = input("input your name>>\n")
    key = input("input your key\n")
    message_s = auction_pb2.Message()
    message_s.type = 0  # 分配id请求
    message_s.client.name = name
    message_s.client.id = id
    message_s.client.key = key
    login_req_m_bytes = message_s.SerializeToString()  # 序列化准备发送的消息
    sock.sendto(login_req_m_bytes, address)  # 发送消息

# 收到type == 1 的message：接受分配的id
def recv_id_handler( message_r):
    id = message_r.client.id  # 接受server分配的id
    print("name:{},id{},current number of people:{}".format
          (message_r.client.name, message_r.client.id,
           message_r.status.current_competitor,
           ))

# 收到竞价成功消息
def recv_bid_succeed_handler( message_r):
    print("yes! msg type:{},current lowest price:{}".format(
        message_r.type,
        message_r.status.lowest_price))

# 收到竞价失败消息
def recv_bid_failed_handler( message_r):
    print("no! msg type{},current lowest price:{}".format(
        message_r.type,
        message_r.status.lowest_price))

# 收到拍卖状态消息
def recv_status_handler( message_r):
    print("current number of people:{}\n data:{}".format
          (message_r.status.current_competitor,
           message_r.data))

# 刷新
def refresh():
    message_s = auction_pb2.Message()
    message_s.client.id = id
    message_s.type = 2
    login_req_m_bytes = message_s.SerializeToString()  # 序列化准备发送的消息
    sock.sendto(login_req_m_bytes, address)  # 发送消息

# 竞价
def bid(price):
    message_s = auction_pb2.Message()
    message_s.client.id = id
    message_s.type = 4
    message_s.client.price = price  # 竞价价格
    message_s.client.price_time = time.time()  # 竞价时间
    login_req_m_bytes = message_s.SerializeToString()  # 序列化准备发送的消息
    sock.sendto(login_req_m_bytes, address)  # 发送消息

# 离开
def leave():
    message_s = auction_pb2.Message()
    message_s.type = 7  # 请求离开消息
    message_s.client.id = id
    msg_bytes = message_s.SerializeToString()  # 序列化
    sock.sendto(msg_bytes, address)  # 发送消息

def run():
    input("ready to fresh?\n")
    refresh()
    x = input("bid price ?\n")
    bid(int(x))
    input("input q to leave\n")
    leave()


if __name__ == '__main__':
    signin()
    start()
    input("ready to fresh?\n")
    refresh()
    x = input("bid price ?\n")
    bid(int(x))
    input("input q to leave\n")
    leave()
    time.sleep(2)










