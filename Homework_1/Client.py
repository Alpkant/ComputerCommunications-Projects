from socket import *
import threading,os,sys


class Client():
	def receiveMessage(self,socket):
		while True:
			try:
				message = socket.recv(1024).decode()
				if(message is ""): # If socket closed it will return EOF. Server cannot send EOF via stream
					print("Server connection is failed. You will be disconnected...")
					os._exit(1)
				print(message) # If it is successful print to the user
			except:
				print("Server connection is failed. You will be disconnected...")
				socket.close()
				os._exit(0)



	def sendMessage(self,socket):
		while True:
			message = input()
			# Remove the spaces
			message.strip()
			if message == "exit" :
				print("Thank you for using chat application. You will be disconnected...")
				socket.send(message.encode())
				socket.close()
				os._exit(0)
			elif message == "":
				# If message is empty do not send it because streams do not accept empty strings
				print("You cannot send empty message.") 
			else:	
				socket.send(message.encode())

	def __init__(self,server_ip,server_port):
		# Set the properties
		#self.username = username
		self.server_ip = server_ip
		self.server_port = server_port

		client_socket = socket(AF_INET,SOCK_STREAM)
		try:
			client_socket.connect((self.server_ip,self.server_port))
			#client_socket.send(self.username.encode())
			threading.Thread(target = self.receiveMessage, args = (client_socket,)).start()
			threading.Thread(target = self.sendMessage, args=(client_socket,)).start()
		except:
			print("Connection couldn't be established with the server. Try again later.")
			os._exit(1)




if __name__ == "__main__":
	server_ip = "160.75.196.214"
	if server_ip is "":
		server_ip = input("There is no default server. Enter the server ip that you want to connect: ")
	#username = input("Enter your username: ")
	server_port = 12000
	Client(server_ip,server_port)