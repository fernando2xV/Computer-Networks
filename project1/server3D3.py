import socket
import select #used for managing many connections (nodes).
import hashlib
from decimal import Decimal
header_length = 10

TCP_IP = "127.0.0.1" #IP ADDRESS
TCP_PORT = 1234 #PORT NUMBER

#AF_INET is for IPv4
#SOCK.STREAM is for TCP connection
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#This is written so when we re-run code we can use the same address
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #thing you want to set (SOL_SOCKET), what you want to set of that specific thing(re-use address), set the thing (1 is true)

#bind is used to connect to a specific address, connect() is used to connect to remote adress
server_socket.bind((TCP_IP, TCP_PORT))

server_socket.listen()

#----------------------------------------------

sockets_list = [server_socket] #for now we only know the socket belonging to the server (will have the clients here)
clients = {}

print('The Server is ready to receive')

#server will listen to any client socket

#-----------------------------------------------------------------------
def receive_msg(client_socket):
    try:
        message_header = client_socket.recv(header_length)

        #if no message was delivered, return false
        if not (message_header):
            return False
        #else
        message_length = int(message_header.decode("utf-8")) #length of username (eg: Fer = 3)
        return{"header": message_header, "data": client_socket.recv(message_length)}

    except:
        return False

#-----------------------------------------------------------------------

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            #if this is true, a new socket is connected and we need to accept this connection
            client_socket, client_address = server_socket.accept()

            user = receive_msg(client_socket)
            user_skr =user

            #someone just disconnected
            if user is False:
                continue

            sockets_list.append(client_socket)

            clients[client_socket] = user 

            hashed_user = str(user)
            hashed_user = hashed_user.encode('utf-8')
            hashed_user = int(hashlib.sha256(hashed_user).hexdigest(), 16) % (10 **8)

            print("Accepted new connection from {}:{} username:{}\n".format(*client_address, hashed_user))#['data']))#.decode('utf-8')))

        else:
            message = receive_msg(notified_socket)

            if message is False:
                print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))

                #remove this socket from the list of sockets
                sockets_list.remove(notified_socket)

                #remove as well from list of clients
                del clients[notified_socket]

                continue

            user = clients[notified_socket]
            hashed_user_again = user['data']#.encode('utf-8')
            hashed_user_again = int(hashlib.sha256(hashed_user_again).hexdigest(), 16) % (10 **8)
            #print(f'- {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
            print(f'- {hashed_user_again}::: {message["data"].decode("utf-8")}')

            #might be wrong skrt
            #message = str(message)

#MIGHT NEED CHANGES OF ALGORITHMS TO ITERATE THROUGH NODES
            for client_socket in clients:
                if client_socket != notified_socket: #dont want to send the message to the sender
 #after hash256:    
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

                    #hashed_user = Decimal(hashed_user) #import Decimal
                    #hashed_user = str(hashed_user)
                    #hashed_user = bytes(str(hashed_user), encoding = 'utf-8')
                    #user = user.to_bytes(2, 'big') #doesnt work because numbers are too large
                    #client_socket.send(hashed_user)
                    #client_socket.send( message['header'] + message['data'])
                    #client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
