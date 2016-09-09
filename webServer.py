# coding=utf-8

'''
要求（不做硬性规定）：1.完成基本网页访问，图片浏览等任务
                    2.实现并发请求，多线程、多进程、select随意
                    3.代码规范 +
                    4.类的设计思想完成服务器任务 +
                    5.实现的功能较多get,post请求等 +
'''

import select
from socket import *
import re
import os

# 创建套接字


def createSocket(addr):
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    return s

# 解析数据
'''
GET /html/ddd.jpg HTTP/1.1
Host: 192.168.13.47:8080
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Encoding: gzip, deflate, sdch
Accept-Language: zh-CN,zh;q=0.8
'''


def parse(msg):
    patern = re.compile(r'\s')
    result = re.split(patern, msg)
    if result[1] == '/html/' or result[1] == '/html':
        print('-------%s--------' % result[1])
        return './html/index.html'
    else:
        return '.' + result[1]


# 拼接返回给客户端的字符串
def myJoin(msg):
    return 'HTTP/1.1 200 OK\r\n' + 'Content-Type: text/html' + '\r\n\r\n' + msg


def main():
    addr = ('', 8080)
    # 创建主套接字
    s = createSocket(addr)
    inputs = [s]
    print('---等待客户端连接---')
    while True:
        readAble, writeable, exceptable = select.select(inputs, [], [])
        for socket in readAble:
            if socket == s:
                newSocket, clientAddr = socket.accept()
                print('%s已连接' % str(clientAddr))
                msg = newSocket.recv(1024)
                print('收到请求数据%s' % msg)
                if msg:
                    # 解析请求的内容
                    url = parse(msg)
                    # 判断请求的内容是否合法
                    if os.path.isfile(url):
                        # 打开文件，读取所有的内容
                        with open(url, 'r') as f:
                            finalMsg = f.read()
                        # 拼接字符串
                        finalMsg = myJoin(finalMsg)
                        newSocket.send(finalMsg)
                else:
                    newSocket.close()
# 运行主程序
if __name__ == '__main__':
    main()
