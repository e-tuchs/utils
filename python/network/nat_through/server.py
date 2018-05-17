#!  -*- coding: utf-8 -*-
import socket
import time

"""Server """


def start_get(_ip, _port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.connect((_ip, _port))
    except Exception, e:
        print u"反向链接局域网失败， 5秒后重试:", time.time(), e
        time.sleep(5)
        print u"重新连接中...", time.time()
        return start_get(_ip, _port)
    else:
        print u"RR:开始反向打洞到客户端: 链接成功", _ip, _port
        time.sleep(1)
    finally:
        end_point = sock.getsockname()
        while True:
            _data = 'Start request from remote Address: %s:%s' % end_point
            print _data
            sock.sendall(_data)
            time.sleep(1)
        sock.shutdown(socket.SHUT_RD)
        return end_point


def read_back(_end_point):
    new_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print u"Listen:服务器端开始监听:", _end_point
    new_sock.bind(_end_point)
    new_sock.listen(5)
    conn, addr = new_sock.accept()
    print u"Listen:获取到客户端请求:", addr
    while True:
        try:
            data = conn.recv(1024)
            print u"Listen:收到客户端数据:", data
            if not data:
                break
            conn.sendall('>>>   get:  %s\n' % data)
        except Exception, e:
            print "Error while get data:", e
            time.sleep(2)
        finally:
            new_sock.close()
    return addr


ip = "0.0.0.0"
port = 8088
end_point = read_back((ip, port))
start_get(*end_point)

