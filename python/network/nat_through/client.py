#!  -*- coding: utf-8 -*-
import socket
import SocketServer
import time

"""Client """


class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        print u"收到远端链接请求:", self.client_address[0]
        print u"开始等待远端回传数据..."
        while True:
            _data = self.request.recv(1024).strip()
            if not _data:
                print u"等待重新连接....."
                time.sleep(1)
            print u"收到{}传回的数据:".format(self.client_address[0])
            print u">>>", _data
            self.request.sendall(_data.upper())


def start_get(_ip, _port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print u"Connect:开始链接远端服务器:", _ip, _port
    try:
        sock.connect((_ip, _port))
    except Exception, e:
        print u"链接远端服务器失败，3秒后重试: ", e
        time.sleep(3)
        return start_get(_ip, _port)
    else:
        _end_point = sock.getsockname()
        _data = 'MSG:Start request from Local Address: %s:%s' % _end_point
        print _data
        sock.sendall(_data)
        sock.shutdown(socket.SHUT_RD)
        return _end_point


def read_back(end_point):
    time.sleep(1)
    new_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print u"Listen:客户端开始切换为监听模式:", end_point
    server = SocketServer.TCPServer(end_point, MyTCPHandler)
    server.serve_forever()


ip = "127.0.0.1"
port = 8088

end_point = start_get(ip, port)
read_back(end_point)
