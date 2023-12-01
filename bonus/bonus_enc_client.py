import socket
from re import compile
from math import ceil

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('10.1.1.11', 9999))

# Récupération d'une string utilisateur
calculation = input("Calcul à envoyer: ")

is_calculation_valid_pattern = compile('^(\+)?([0-9]){1,10} (\+|-|\*) (\+)?([0-9]){1,10}$')

if not is_calculation_valid_pattern.match(calculation):
    raise TypeError("Veuillez saisir un calcul valide (addition, soustraction ou multiplication) : choisir des nombres entiers compris entre 0 et 4294967294")

array = calculation.split(" ")

if int(array[0]) >= 4294967295  or int(array[2]) >= 4294967295:
    print("Les nombres saisis doivent être compris entre 0 et 4294967294")
    exit(0)
    
first_nb, operand, second_nb = int(array[0]), array[1], int(array[2])

first_nb_len, second_nb_len = ceil(first_nb.bit_length()/8.0), ceil(second_nb.bit_length()/8.0)

if first_nb == 0:
    first_nb_len = 1
if second_nb == 0:
    second_nb_len = 1

operand = array[1]

if operand == "+":
    operand = 0
elif operand == "-":
    operand = 1
else:
    operand = 2

header = first_nb_len.to_bytes(4, byteorder='big') + second_nb_len.to_bytes(4, byteorder='big')
byte_calculation = first_nb.to_bytes(first_nb_len, byteorder='big') + operand.to_bytes(1, byteorder='big') + second_nb.to_bytes(second_nb_len, byteorder='big')

calc_sequence = header + byte_calculation

calc_sequence_len = len(calc_sequence)
print(f"Taille du message en octet : {calc_sequence_len}")

byte_len = ceil(calc_sequence_len.bit_length()/8.0)
print(f"Nombre d'octet de la longueur du message : {byte_len}")

dynamic_header = None
if byte_len == 1:
    shifted_calc_sequence_len = calc_sequence_len << 6
    shifted_byte_len = byte_len << 2
    combined_value = shifted_calc_sequence_len | shifted_byte_len
    dynamic_header = combined_value.to_bytes(1, byteorder='big')
    

# On envoie
s.send(dynamic_header + calc_sequence)

# Réception et affichage du résultat
res_byte_len = int.from_bytes(s.recv(4), byteorder='big')

is_negative = None
if int.from_bytes(s.recv(1), byteorder='big') == 1:
    is_negative = True
else:
    is_negative = False
    
res = int.from_bytes(s.recv(res_byte_len), byteorder='big')
if is_negative:
    res = -abs(res)
    
print(f"Le résultat du calcul {calculation} est : {res}")

s.close()
exit(0)