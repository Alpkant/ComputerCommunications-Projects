from socket import *
import threading


class Client():
	def receiveMessage(self,socket):
		while self.is_running and self.is_server_up:
			try:
				message = socket.recv(1024).decode()
				if(message is ""): # If socket closed it will return EOF. Server cannot send EOF via stream
					self.is_server_up = False
					self.is_running = False
					exit(1)
				print(message)
			except:
				print("Server connection is failed. You will be disconnected.")
				self.is_running = False
				self.is_server_up = False
				exit(0)


	def sendMessage(self,socket):
		while self.is_running and self.is_server_up:
			message = input()
			if message is 'exit':
				self.is_running = False
				self.is_server_up = False
				socket.send(message.encode())
				socket.close()
				exit(0)
			
			socket.send(message.encode())

	def __init__(self,username,server_ip,server_port):
		# Set the properties
		self.is_running = False
		self.is_server_up = False
		self.username = username
		self.server_ip = server_ip
		self.server_port = server_port

		client_socket = socket(AF_INET,SOCK_STREAM)
		client_socket.connect((self.server_ip,self.server_port))
		self.is_server_up = True

		client_socket.send(self.username.encode())
		self.is_running = True
		threading.Thread(target = self.receiveMessage, args = (client_socket,)).start()
		threading.Thread(target = self.sendMessage, args=(client_socket,)).start()




if __name__ == "__main__":
	username = input("Enter your username: ")
	server_ip = "160.75.196.214"
	if server_ip is '':
		server_ip = input("There is no default server. Enter the server ip that you want to connect: ")
	server_port = 12000

	Client(username,server_ip,server_port)