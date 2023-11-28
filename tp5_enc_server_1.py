import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('10.1.1.11', 9999))  

s.listen(1)
conn, addr = s.accept()

while True:

    try:
        # On reçoit le calcul du client
        first_nb_len = conn.recv(4).decode()
        second_nb_len = conn.recv(4).decode()
        operand_len = conn.recv(4).decode()

        print(f"{conn.recv(first_nb_len).decode()} | {conn.recv(operand_len).decode()} | {conn.recv(second_nb_len).decode()}")
        
        # Evaluation et envoi du résultat
        # res  = eval(data.decode())
        # conn.send(str(res).encode())
         
    except socket.error:
        print("Error Occured.")
        break

conn.close()
