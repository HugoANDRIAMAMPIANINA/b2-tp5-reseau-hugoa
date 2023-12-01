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
        dynamic_header = conn.recv(1)
        if not dynamic_header:
            continue
        
        masked_bits = int.from_bytes(dynamic_header, byteorder='big') & 0b11000000
        
        dynamic_header_byte_len = masked_bits >> 6
        
        print(f"Taille en octets du header : {dynamic_header_byte_len}")
        
        sequence = None
        if dynamic_header_byte_len == 1:
            sequence = conn.recv(int.from_bytes(dynamic_header, byteorder='big') & 0b00111111)
            
        print(sequence)
        break
        
    #     # On reçoit le calcul du client
    #     first_nb_len = int.from_bytes(conn.recv(4), byteorder='big')
        
    #     second_nb_len = int.from_bytes(conn.recv(4), byteorder='big')
        
    #     first_nb = int.from_bytes(conn.recv(first_nb_len), byteorder='big')
    #     operand = int.from_bytes(conn.recv(1), byteorder='big')
    #     second_nb = int.from_bytes(conn.recv(second_nb_len), byteorder='big')
        
    #     if operand == 0:
    #         operand = "+"
    #     elif operand == 1:
    #         operand = "-"
    #     else:
    #         operand = "*"

    #     calculation = f"{first_nb} {operand} {second_nb}"
        
    #     # Evaluation et envoi du résultat
    #     res: int = eval(calculation)
        
    #     res_byte_len = ceil(res.bit_length()/8.0)
        
    #     header = res_byte_len.to_bytes(4, byteorder='big')
        
    #     if res < 0:
    #         header += int.to_bytes(1,1, byteorder='big')
    #         res = abs(res)
    #     else:
    #         header += int.to_bytes(0,1, byteorder='big')
        
    #     sequence = header + res.to_bytes(res_byte_len, byteorder='big')
        
    #     conn.send(sequence)
         
    except socket.error:
        print("Error Occured.")
        break
    
conn.close()