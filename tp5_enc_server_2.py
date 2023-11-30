import socket
from math import ceil

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
        
        first_nb = int.from_bytes(conn.recv(first_nb_len), byteorder='big', signed=True)
        operand = int.from_bytes(conn.recv(1), byteorder='big')
        second_nb = int.from_bytes(conn.recv(second_nb_len), byteorder='big', signed=True)
        
        print(second_nb)
        
        if operand == 0:
            operand = "+"
        elif operand == 1:
            operand = "-"
        else:
            operand = "*"

        calculation = f"{first_nb} {operand} {second_nb}"
        print(calculation)
        
        # Evaluation et envoi du résultat
        res: int = eval(calculation)
        
        res_byte_len = ceil(res.bit_length()/8.0)
        
        header = res_byte_len.to_bytes(4, byteorder='big')
        
        sequence = header + res.to_bytes(res_byte_len*2, byteorder='big', signed=True)
        
        conn.send(sequence)
         
    except socket.error:
        print("Error Occured.")
        break
    
conn.close()