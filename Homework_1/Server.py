from socket import *
import threading
import sys
import datetime as t

class Server():

    def listenClient(self,client,addr,client_name):
        while True:
                message = client.recv(1024).decode()
                if message=="exit" : # If user decide to exit
                    print (addr , " is disconnected")
                    stamp = t.datetime.now().strftime('%H:%M:%S %p') # Get the current time
                    message = client_name + " is disconnected from the chat " + " @ "   + stamp
                    # Notify the users that this client is disconnected
                    for (name,sckt) in self.client_names.items():
                        if name is not client_name:
                             sckt.send(message.encode())
                    # Remove the client from the server user list
                    self.client_names.pop(client_name)
                    # Close the socket
                    client.close()
                    exit(0)
                elif message == "" : # If connection closed unexpectedly
                	print (addr , " is disconnected") 
                	self.client_names.pop(client_name)
                	client.close()
                	exit(1)
                else:
                    print (addr , " says: ", message) # Print to the console 
                    stamp = t.datetime.now().strftime('%H:%M:%S %p')
                    message = client_name + " @ " + stamp + " >> " + message 
                    # Send message to all clients but not to the sender
                    # Names are the usernames and sckt are the sockets of the users
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
        	# Accept the incoming requests
            connectionSocket,addr = serverSocket.accept()
            print('%s is connected to the server' %str(addr))
            # List all the usernames to the new user
            connectionSocket.send("Welcome to the server. Here is users in the chat room:\n".encode())
            clientlist = ""
            for i in self.client_names.keys():
            	clientlist += i + "\n"
            
            if clientlist is "":
                clientlist = "*No user found*\n"
            connectionSocket.send(clientlist.encode())
            # Notify the user because user should choose username
            connectionSocket.send("Please choose username:".encode())
            client_name = connectionSocket.recv(1024).decode()
            client_name = client_name.strip()
            if client_name not in self.client_names:
            	# If user selected appropriate username then it can start to chat with others
                print('%s is claimed %s as its username' %(str(addr) , str(client_name)))
                connectionSocket.send("You have selected your username. You can now chat with the others.".encode())
                self.client_names[client_name] = connectionSocket
                threading.Thread(target = self.listenClient,args = (connectionSocket,addr,client_name)).start()
            elif client_name is not "":
            	# User selected wrong username so 
                connectionSocket.send("There is already user with that name. You will be disconnected.\n".encode())
                connectionSocket.close()
                exit(1)
            else:
            	connectionSocket.send("You have selected invalid username. You will be disconnected.\n".encode())
            	connectionSocket.close()
            	exit(1)


if __name__=="__main__":
    serverPort = 12000
    Server(serverPort)