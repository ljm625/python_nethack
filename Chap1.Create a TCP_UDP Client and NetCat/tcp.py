

# Python Implementation of a simple TCP Client
# 实现TCP的客户端连接
#%%
import socket

target_host = "www.google.com"
target_port = 80

# 建立一个socket对象
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# 建立连接
client.connect((target_host,target_port))
# 发送HTTP请求

# 注意python3需要encode
client.send("GET / HTTP/1.1\r\nHost: google.com\r\n\r\n".encode())

# 接受数据
response = client.recv(4096)

print(response)


# Python Implementation of a simple TCP Server
# 实现简单的TCP的服务器
#%%
import socket
import threading

bind_ip="0.0.0.0"
bind_port=3389

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定IP和端口

server.bind((bind_ip,bind_port))
# 开始监听
server.listen(5)
print("Listening on {}:{}".format(bind_ip,bind_port))

# 创建一个处理数据的线程
def handle_client(client_socket):
    # 打印出内容
    request = client_socket.recv(1024)
    print("[*] Received: {}".format(request))
    # 返回
    client_socket.send("ACK!".encode())
    client_socket.close()

while True:
    client,addr = server.accept()
    print("[*] Accepted connection from: {}:{}".format(addr[0],addr[1]))

    # 处理数据
    client_handler = threading.Thread(target=handle_client,args=(client,))
    client_handler.start()

