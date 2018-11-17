#coding:utf-8
#   1、只要html中有对应资源的地址浏览器都会使用这个地址发送一次请求
#如html中有图片地址就使用图片地址发送一次请求，得到返回的数据后。
#就在对应的位置把这个文件解析出来。所以有多少个地址就好默认发送多少次请求
#   2、由于每次返回的数据是头+文件体后面再也不能接受头了否则会认为这个头为一般的文字
#解决方法是：每次返回一个请求后关闭流，下次再开启流。使用Content-Length:不起作用，一次只能一个头
#   3、把所有的文件多次发送到同一个浏览器页面后，浏览器会根据html来组织文件。
import socket
import sys
from  multiprocessing import Process
import copy
import RenderTool
import time
count=0
server_address = ('localhost', 8080)
class WebServer():
    count=0
    def run(self):
        print(sys.stderr, 'starting up on %s port 127.0.0.1:%s' % server_address)
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #这里是指重启后端口可以重用，否则由于先前程序使用一次默认是占用的
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        sock.bind(server_address)
        sock.listen(128)
        #count是计数，看有多少次请求，根据不同次数加载不同的数据
        #图标一次（最后一次）是默认的，是浏览器自己要求的。

        while True:
            connection, client_address = sock.accept()
            self.count+=1
            p=Process(target=self.yun,args=(self.count,newc(connection).re(),))
            p.start()


    def yun(self,count,connection):


        print (sys.stderr, 'waiting for a connection')
        try:
            data = connection.recv(1024)
            biao=data.decode("utf-8").replace("GET /","").split("HTTP/1.1")[0].replace(" ","")
            print(biao,"***%%%%%%%%%%%%%%%%%%%%%")
            print (data,"*****")
            if data and biao=="":
                #注意：响应html一定要使用http头，每个关键的使用\r\n换行同时报头最后结尾要两个\r\n
                #      报头要在同一行不能在三个冒号来标记时的使用回车键
                with open("index.html","r") as fl:
                    op=fl.read()
                    fl.close()
                    index=RenderTool.RenderTemplate()
                    result=index.getHtmlResult(op)
                    html=bytes('''HTTP/1.1 200 OK\r\n Content-Type: text/html;charset=utf-8\r\n\r\n  ''',"utf-8")+bytes(result,"utf-8")
                    connection.sendall(html)
                    #由于没有在头中标记响应的长度所有使用关闭来结束响应
                    connection.close()

            elif data and ".mp4" in biao:
                ty=0
                print ("3---", count)
                #由于返回的是流对象，每次返回只有播放的数据量，不能拖动到没有数据量上的进度条
                # 所以要指定Accept-Ranges:bytes\r\nContent-Length:视频大小（不是占的空间大小）\r\nContent-Range:bytes 0-视频大小（不是占的空间大小-1/视频大小（不是占的空间大小）
                html=bytes("HTTP/1.1 200 OK\r\nAccept-Ranges:bytes\r\nContent-Length:23639964\r\nContent-Range:bytes 0-23639963/23639964\r\nContent-Type:video/mp4\r\n\r\n","utf-8")
                connection.sendall(html)
                n=""
                with open("3.mp4","rb") as file :
                    for i in  file:
                       
                            #由于浏览器只认流所以每次返回一点数据。
                            #所以要在页面中点击下载要等所有数据加载完成后点击。
                        connection.sendall(i)

                    file.close()
                
            elif data and ".jpg" in biao:
                html = bytes("HTTP/1.1 200 OK\r\nAccept-Ranges:bytes\r\nContent-Type:image/jpg\r\n\r\n","utf-8")
                connection.sendall(html)
                with open(biao,"rb") as file:
                    for i in file:
                        connection.sendall(i)
                connection.close()
            elif data and ".js" in biao:
                html=bytes("HTTP/1.1 200 OK\r\nAccept-Ranges:bytes\r\nContent-Type:application/javascript\r\n\r\n","utf-8")
                connection,sendall(html)
                with open(biao,"rb") as file:
                    for i in file:
                        connection.sendall(i)
                connection.close()
            elif data and ".css" in biao:
                print(biao)
                html=bytes("HTTP/1.1 200 OK\r\nContent-Type:text/css\r\n\r\n","utf-8")
                connection.sendall(html)
                with open(biao,"rb") as file:
                    connection.sendall(file.read())
                    file.close()
                connection.close()
                
            else:#都最后一次请求后置零
                    print ("else")

        finally:
            pass

class newc():
    def __init__(self,connect):
        self.connect=connect
        
    def re(self):
        return self.connect



if __name__ == '__main__':
    server=WebServer()
    server.run()
