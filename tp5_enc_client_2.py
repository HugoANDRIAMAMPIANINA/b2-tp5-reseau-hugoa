import socket
from re import compile
from math import ceil

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('10.1.1.11', 9999))

# Récupération d'une string utilisateur
calculation = input("Calcul à envoyer: ")

is_calculation_valid_pattern = compile('^(\+|-)?([0-9]){1,10} (\+|-|\*) (\+|-)?([0-9]){1,10}$')

if not is_calculation_valid_pattern.match(calculation):
    raise TypeError("Veuillez saisir un calcul valide (addition, soustraction ou multiplication) : choisir des nombres entiers compris inférieurs à 4294967295")

array = calculation.split(" ")

if int(array[0]) >= 4294967295  or int(array[2]) >= 4294967295:
    print("Les nombres saisis doivent être inférieur à 4294967295")
    exit(0)
    
first_nb, operand, second_nb = int(array[0]), array[1], int(array[2])

first_nb_len, second_nb_len = ceil(first_nb.bit_length()/8.0), ceil(second_nb.bit_length()/8.0)
print(f"f nb byte {first_nb_len}\ns nb byte {second_nb_len}")

operand = array[1]

if operand == "+":
    operand = 1
elif operand == "-":
    operand = 2
else:
    operand = 3

header = first_nb_len.to_bytes(4, byteorder='big') + second_nb_len.to_bytes(4, byteorder='big') + operand.to_bytes(1, byteorder='big')
print(header)

calculation = first_nb.to_bytes(first_nb_len, byteorder='big') + operand.to_bytes(1, byteorder='big') + second_nb.to_bytes(second_nb_len, byteorder='big')
print(calculation)

sequence = header + calculation
print(sequence)

# On envoie
s.send(sequence)

# Réception et affichage du résultat
res_byte_len = int.from_bytes(s.recv(4), byteorder='big')
res = int.from_bytes(s.recv(res_byte_len), byteorder='big')

print(f"Le résultat du calcul {calculation} est : {res}")

s.close()
exit(0)