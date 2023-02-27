from socket import *
import sys
import pickle
import threading
import const

class RecvHandler(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.client_socket = sock

    def run(self):
        while True:
            (conn, addr) = self.client_socket.accept()
            marshaled_msg_pack = conn.recv(1024)
            msg_pack = pickle.loads(marshaled_msg_pack)
            print("MESSAGE: " + msg_pack[0] + " - FROM: " + msg_pack[1])
            conn.send(pickle.dumps("ACK"))
            conn.close()
        return

me = str(sys.argv[1])
client_sock = socket(AF_INET, SOCK_STREAM)
my_ip = const.registry[me][0]
my_port = const.registry[me][1]
client_sock.bind((my_ip, my_port))
client_sock.listen(5)

# Put receiving thread to run
recv_handler = RecvHandler(client_sock)
recv_handler.start()

while True:
    server_sock = socket(AF_INET, SOCK_STREAM)
    dest = input("ENTER DESTINATION: ")
    msg = input("ENTER MESSAGE: ")
    # Connect to server
    try:
        server_sock.connect((const.CHAT_SERVER_HOST, const.CHAT_SERVER_PORT))
    except:
        print("Server is down. Exiting...")
        exit(1)
    # Send message and wait for confirmation
    msg_pack = (msg, dest, me)
    marshaled_msg_pack = pickle.dumps(msg_pack)
    server_sock.send(marshaled_msg_pack)
    marshaled_reply = server_sock.recv(1024)
    reply = pickle.loads(marshaled_reply)
    if reply != "ACK":
        print("Error: Server did not accept the message (dest does not exist?)")
    else:
        pass
    server_sock.close()
