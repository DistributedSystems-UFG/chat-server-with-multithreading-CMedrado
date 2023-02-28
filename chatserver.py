from socket import *
import threading
import pickle
import const


def handle_client(conn, addr):
    # Recebe a mensagem do cliente

    marshaled_msg_pack = conn.recv(1024)
    msg_pack = pickle.loads(marshaled_msg_pack)
    msg = msg_pack[0]
    dest = msg_pack[1]
    src = msg_pack[2]
    # Imprime informações sobre a mensagem
    print("RELAYING MSG: " + msg + " - FROM: " + src + " - TO: " + dest)

    # Verifica se o destinatário está registrado no servidor
    try:
        dest_addr = const.registry[dest]
    except:
        conn.send(pickle.dumps("NACK"))
        conn.close()
        return

    # Envia uma mensagem de ACK ao cliente que enviou a mensagem  
    conn.send(pickle.dumps("ACK"))
    conn.close()

    # Cria uma conexão com o cliente destinatário
    client_sock = socket(AF_INET, SOCK_STREAM)
    dest_ip = dest_addr[0]
    dest_port = dest_addr[1]

    # Tenta se conectar ao cliente destinatário
    try:
        client_sock.connect((dest_ip, dest_port))
    except:
        print("Error: Destination client is down")
        client_sock.close()
        return

    # Envia a mensagem para o cliente destinatário e aguarda um ACK
    msg_pack = (msg, src)
    marshaled_msg_pack = pickle.dumps(msg_pack)
    client_sock.send(marshaled_msg_pack)
	@@ -41,6 +49,7 @@ def handle_client(conn, addr):
    if reply != "ACK":
        print("Error: Destination client did not receive message properly")

    # Fecha a conexão com o cliente destinatário
    client_sock.close()


server_sock = socket(AF_INET, SOCK_STREAM)
server_sock.bind((const.CHAT_SERVER_HOST, const.CHAT_SERVER_PORT))
server_sock.listen(5)
print("Chat Server is ready...")
while True:
    (conn, addr) = server_sock.accept()
    print("Chat Server: client is connected from address " + str(addr))
    t = threading.Thread(target=handle_client, args=(conn, addr))
    t.start()
