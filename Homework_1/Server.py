from socket import *
import threading
import sys
import datetime as t

class Server():

    def listenClient(self,client,addr,client_name):
        while True:
                message = client.recv(1024).decode()
                if message=="exit":
                    print (addr , " is disconnected")
                    self.client_names.pop(client_name)
                    client.close()
                    exit(0)
                else:
                    print (addr , " says: ", message)
                    stamp = t.datetime.now().strftime('%H:%M:%S %p')
                    message = client_name + " @ " + stamp + " >> " + message 
                    for (name,sckt) in self.client_names.items():
                        if name is not client_name:
                             sckt.send(message.encode())



    def __init__(self,serverPort):
        self.client_names = {}

        try:
            serverSocket = socket(AF_INET,SOCK_STREAM)
        except:
            print ("Socket creation is failed!")
            exit(1)
            
        print ("Socket is successfully created.")

        try:
            serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        except:
    
            print ("Socket cannot be used!")
            exit(1)

        print ("Socket is being used.")

        try:
            serverSocket.bind(('',serverPort))
        except:
        
            print ("Binding is failed!")
            exit(1)

        print ("Binding is done.")

        try:
            serverSocket.listen(50)
        except:
    
            print ("Server is failed to listen!")
            exit(1)

        print ("The server is ready to receive users.")


        while True:

            connectionSocket,addr = serverSocket.accept()
            print('%s is connected to the server' %str(addr))
            client_name = connectionSocket.recv(1024).decode()
            if client_name not in self.client_names:
                print('%s is claimed %s username' %(str(addr) , str(client_name)))
                self.client_names[client_name] = connectionSocket
                connectionSocket.send("Welcome to the server. Here is users in the chat room:\n".encode())
                clientlist = ""
                for i in self.client_names.keys():
                    if(i is not client_name):
                        clientlist += i + "\n"
                
                if clientlist is "":
                    clientlist = "*No user found*\n"
                connectionSocket.send(clientlist.encode())
                threading.Thread(target = self.listenClient,args = (connectionSocket,addr,client_name)).start()
            else:
                connectionSocket.send("There is already user with that name. You will be disconnected.\n".encode())
                connectionSocket.close()


if __name__=="__main__":
    serverPort = 12000
    Server(serverPort)