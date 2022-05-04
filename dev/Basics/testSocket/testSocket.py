# -*- coding: utf-8 -*-

import socket

address = ('localhost', 6789)


def server( address ):
    s = socket.socket( socket.AF_INET,socket.SOCK_STREAM )
    s.bind( address )
    s.listen(1)
    conn, addr = s.accept()  # クライアントの接続を待つ
    data = conn.recv(1024)  # クライアントからのデータを受信する
    print( "server: receive {}".format(data) )
    conn.send(data.upper())  # クライアントにデータを送信する
    conn.close()
    s.close()


def client( address ):
    s = socket.socket()
    s.connect( address )
    s.send( b"hello")  # サーバにデータを送信する
    data = s.recv(1024)  # サーバからのデータを受信する
    print( 'client: receive {}'.format(data) )
    s.close()


# 実行してみる
import threading
class Server(threading.Thread):
    def run(self):
        server( address )


s = Server()
s.start()
client( address )