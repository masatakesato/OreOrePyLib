# -*- coding: utf-8 -*-
import time
import socket

g_ServerAddress = ('127.0.0.1', 6789)
g_ClientAddress =  ('127.0.0.1', 6790)



def server( address ):
    s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    s.bind( address )
    
    #s.listen(1)
    #conn, addr = s.accept()  # クライアントの接続を待つ
    
    data, cli_addr = s.recvfrom(1024) #conn.recv(1024)  # クライアントからのデータを受信する
    string = data.decode()
    print( "server: receive {}".format(string), ", client address: ", cli_addr )
    
    #conn.send(data.upper())  # クライアントにデータを送信する
    s.sendto( string.upper().encode(), cli_addr )

    #conn.close()
    s.close()



def client( server_address ):

    s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    #s.connect( server_address )# いらない

    s.bind( g_ClientAddress )

    s.sendto( b"hello", server_address )#s.send( b"hello")  # サーバにデータを送信する
    data, srv_addr = s.recvfrom(1024)  # サーバからのデータを受信する
    print( 'client: receive {}'.format(data.decode()), "server address: ", srv_addr )
    s.close()




import threading
class Server(threading.Thread):
    def run(self):
        server( g_ServerAddress )




print("//======= server start =========//\n")
s = Server()
s.start()


print("//======= client start =========//\n")
client( g_ServerAddress )