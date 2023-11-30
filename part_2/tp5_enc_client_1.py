import socket
from re import compile

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('10.1.1.11', 9999))

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

header = first_nb_len.to_bytes(4, byteorder='big') + second_nb_len.to_bytes(4, byteorder='big') + operand_len.to_bytes(4, byteorder='big')
# print(header)

sequence = header + calculation.replace(" ", "").encode()
print(sequence)

# On envoie
s.send(sequence)

# Réception et affichage du résultat
s_data = s.recv(1024)
print(s_data.decode())
s.close()
exit(0)
