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
        print(first_nb_len)
        if not first_nb_len:
            continue
        second_nb_len = int.from_bytes(conn.recv(4), byteorder='big')
        print(second_nb_len)
        operand_len = int.from_bytes(conn.recv(1), byteorder='big')
        print(operand_len)
        
        first_nb = int.from_bytes(conn.recv(first_nb_len), byteorder='big')
        operand = int.from_bytes(conn.recv(operand_len), byteorder='big')
        second_nb = int.from_bytes(conn.recv(second_nb_len), byteorder='big')
        
        if operand == 0:
            operand = "+"
        elif operand == 1:
            operand = "-"
        else:
            operand = "*"

        calculation = f"{first_nb} {operand} {second_nb}"
        
        # Evaluation et envoi du résultat
        res: int = eval(calculation)
        print(res)
        # conn.send(str(res).encode())
         
    except socket.error:
        print("Error Occured.")
        break

conn.close()
