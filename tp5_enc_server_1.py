import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('10.1.1.11', 9999))  

s.listen(1)
conn, addr = s.accept()

while True:

    try:
        # On reçoit le calcul du client
        first_nb_len = int.from_bytes(conn.recv(4), byteorder='big')
        if not first_nb_len:
            continue
        second_nb_len = int.from_bytes(conn.recv(4), byteorder='big')
        operand_len = int.from_bytes(conn.recv(4), byteorder='big')
        print(first_nb_len)
        print(second_nb_len, "\n")
        print(operand_len, "\n")

        print(f"{conn.recv(first_nb_len).decode()} | {conn.recv(operand_len).decode()} | {conn.recv(second_nb_len).decode()}")
        
        # Evaluation et envoi du résultat
        # res  = eval(data.decode())
        # conn.send(str(res).encode())
         
    except socket.error:
        print("Error Occured.")
        break

conn.close()
