import socket
from re import compile

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 9999))

# Récupération d'une string utilisateur
calculation = input("Calcul à envoyer: ")

is_calculation_valid_pattern = compile('^(\+|-)?([0-9]){1,10} (\+|-|\*) (\+|-)?([0-9]){1,10}$')

if not is_calculation_valid_pattern.match(calculation):
    raise TypeError("Veuillez saisir un calcul valide (addition, soustraction ou multiplication) : choisir des nombres entiers compris inférieurs à 4294967295")

array = calculation.split(" ")

if int(array[0]) >= 4294967295 or int(array[2]) >= 4294967295:
    print("Les nombres saisis doivent être inférieur à 4294967295")
    exit(0)
    
first_nb, operand, second_nb = array[0], array[1], array[2]

first_nb_len, operand_len, second_nb_len = len(first_nb), len(operand), len(second_nb)

header = f"{first_nb_len.to_bytes(4, byteorder='big')}{second_nb_len.to_bytes(4, byteorder='big')}{operand_len.to_bytes(4, byteorder='big')}"
# print(header)

sequence = header.encode() + calculation.replace(" ", "").encode()
print(sequence)

# On envoie
s.send(calculation.encode())

# Réception et affichage du résultat
s_data = s.recv(1024)
print(s_data.decode())
s.close()

# first_nb_byte_length = len(array[0].encode())
# second_nb_byte_length = len(array[2].encode())

# print(f"1st nb byte nb : {first_nb_byte_length}\n2nd nb byte nb : {second_nb_byte_length}")

# first_nb_header = first_nb_byte_length.to_bytes(4, byteorder='big')
# second_nb_header = second_nb_byte_length.to_bytes(4, byteorder='big')

# operand_header = 0
# operand_to_bytes = None

# gestion du signe
# if array[1] == "+":
#     operand_to_bytes = int.to_bytes(0, int.bit_length(0))
#     operand_header = int.to_bytes(0, int.bit_length(0))
# elif array[1] == "-":
#     operand_header = int.to_bytes(1, int.bit_length(1))
# else:
#     operand_header = int.to_bytes(2, int.bit_length(2))

# sequence = first_nb_header + int(array[0]).to_bytes(first_nb_byte_length, byteorder='big') + array[1].encode() + second_nb_header + int(array[0]).to_bytes(second_nb_byte_length, byteorder='big')

# print(sequence)
