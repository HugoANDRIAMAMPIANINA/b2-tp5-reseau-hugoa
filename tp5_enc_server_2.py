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
        operand_len = int.from_bytes(conn.recv(1), byteorder='big')
        
        first_nb = int.from_bytes(conn.recv(first_nb_len), byteorder='big')
        operand = conn.recv(operand_len).decode
        second_nb = int.from_bytes(conn.recv(second_nb_len), byteorder='big')

        calculation = f"{first_nb} {operand} {second_nb}"
        
        # Evaluation et envoi du résultat
        res: int = eval(calculation)
        print(res)
        # conn.send(str(res).encode())
         
    except socket.error:
        print("Error Occured.")
        break

conn.close()
