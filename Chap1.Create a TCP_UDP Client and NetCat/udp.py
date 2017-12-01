

# Python Implementation of a simple UDP Client
# 实现UDP的客户端连接
#%%
import socket

target_host = "127.0.0.1"
target_port = 80

# 建立一个socket对象
client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# 无须建立连接

# 注意python3需要encode
client.sendto("GOOD".encode(),(target_host,target_port))

# 接受数据
data,addr = client.recvfrom(4096)

print(data)


