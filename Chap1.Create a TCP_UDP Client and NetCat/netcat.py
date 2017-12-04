# Create a netcat alternative using python
# 使用Python创建一个netcat的替代品

#%%
import sys
import socket
import getopt
import threading
import subprocess

# 定义一些全局变量
listen = False
command = False
upload = False
execute = ""
target = ""
upload_dest = ""
port = 0

def usage():
    print("BHP Net Tool\r\n")
    print("")
    print("Usage : netcat.py -t target_host -p port")
    print(" -l --listen                 - listen on [host]:[port] for conns")
    print(" -e --execute=file_to_run    - Execute the given file upon receiving a connection")
    print(" -c --command                - init a command shell")
    print(" -u --upload=destionation    - when receive conn upload a file and write to [dest]\n\n")
    print("Examples:")
    print("netcat.py -t 127.0.0.1 -p 5555 -l -c")
    print("netcat.py -t 127.0.0.1 -p 5555 -l -u=c\\target.exe")
    print("netcat.py -t 127.0.0.1 -p 5555 -l -e=\"cat ./ect/passwd\"")
    print("echo 'ABC' | ./netcat.py -t 127.0.0.1 -p 135")
    sys.exit(0)

def main():
    global listen,port,execute,command,upload_dest,target

    # 如果没有参数执行，显示帮助
    if not len(sys.argv[1:]):
        usage()
    
    try:
        opts,args = getopt.getopt(sys.argv[1:],"hle:t:p:cu:",["help","listen","execute","target","port","command","upload"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o,a in opts:
        if o in ("-h","--help"):
            usage()
        elif o in ("-l","--listen"):
            listen = True
        elif o in ("-e","--execute"):
            execute=a
        elif o in ("-c","--command"):
            command =True
        elif o in ("-u","--upload"):
            upload_dest = a
        elif o in ("-t","--target"):
            target = a
        elif o in ("-p","--port"):
            port = int(a)
        else:
            assert False,"Unhandled Option"
    
    # 我们是进行监听还是仅从标准输入发送数据
    if not listen and len(target) and port > 0:

        # 从命令行读取内存数据
        # 进行阻塞，不在发送数据时发送CTRL-D
        buffer = sys.stdin.read()

        # 发送数据
        client_sender(buffer)
    
    # 开始监听，上传文件
    # 放置反弹shell
    if listen:
        server_loop()

def client_sender(buffer):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try:
        # 连接到目标主机
        client.connect((target,port))

        if len(buffer):
            client.send(buffer)
        
        while True:
            # 现在等待数据回传
            recv_len =1 
            response = ""

            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data

                if recv_len <4096:
                    break
            print(response)

            # 等待更多输入
            buffer=raw_input("")
            buffer += "\n"

            client.send(buffer)
    except:
        print("[*] Exception found. Quiting")
        client.close()

def server_loop():
    global target

    # 如果没有定义目标，那么我们监听所有端口
    if not len(target):
        target = "0.0.0.0"  
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((target,port))
    server.listen(5)
    while True:
        client_socket, addr = server.accept()
        # 分拆一个thread处理客户
        client_thread=threading.Thread(target=client_handler,args=(client_socket,))
        client_thread.start()

def run_command(command=""):
    # 执行命令

    command= command.rstrip()
    # 运行命令，输出结果
    try:
        output = subprocess.check_output(command,stderr = subprocess.STDOUT,shell=True)
    except:
        output = "Failed to execute command. \r\n"
    
    return output

def client_handler(client_socket):
    global upload
    global execute
    global command

    if len(upload_dest):
        # 读取字符，写给目标
        file_buffer =""

        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            else:
                file_buffer+=data
                

    

main()
