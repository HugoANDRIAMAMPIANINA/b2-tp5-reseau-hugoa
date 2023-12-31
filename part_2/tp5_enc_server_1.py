import socket

port = 9999
ip_addr = '10.1.1.11'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ip_addr, port))  

print(f"server started at port ")

s.listen(1)

while True:
    
    conn, addr = s.accept()
    
    print(f"client {addr[0]} is connected")

    try:
        # On reçoit le calcul du client
        first_nb_len = int.from_bytes(conn.recv(4), byteorder='big')
        if not first_nb_len:
            continue
        second_nb_len = int.from_bytes(conn.recv(4), byteorder='big')
        operand_len = int.from_bytes(conn.recv(4), byteorder='big')

        calculation = f"{conn.recv(first_nb_len).decode()} {conn.recv(operand_len).decode()} {conn.recv(second_nb_len).decode()}"
        
        # Evaluation et envoi du résultat
        res = eval(calculation)
        conn.send(str(res).encode())
         
    except socket.error:
        print("Error Occured.")
        break

conn.close()
