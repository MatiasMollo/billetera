import json
import random
from datetime import datetime

DEBIT_CARD_PATH = 'data/debitCards.json'

def createDebitCard(username, users):
    """
    Obtiene el nombre de usuario y el nombre completo del usuario y crea una tarjeta de débito asociada a él.

    Parámetros:
    
    username (String): Nombre de usuario
    users (Dict): Usuarios del sistema
    """

    userFullName = users[username]["Apellido"] + " " + users[username]["Nombre"]

    # Cuando veamos excepciones vamos a contemplar el caso de que entren parametros vacios
    with open(DEBIT_CARD_PATH, 'r', encoding='utf-8') as file:
        debit_cards = json.load(file)

    create = True
    if username in debit_cards:
        print("Ya tienes una tarjeta de débito asociada a tu cuenta.")
        create = False

    if create:
        while True:
            card_number = ''.join([str(random.randint(0, 9)) for _ in range(16)])
            if not any(card_number in card for card in debit_cards.values()):
                break

        security_code = ''.join([str(random.randint(0, 9)) for _ in range(4)])

        valid_from = datetime.now().timetuple()[:3]
        expires_end = (datetime.now().year + 5, datetime.now().month, datetime.now().day)
        debit_card_details = {
            "Número de tarjeta": card_number,
            "Válida desde": valid_from,
            "Válida hasta": expires_end,
            "Código de seguridad": security_code,
            "Nombre completo": userFullName,
        }

        debit_cards[username] = debit_card_details
        with open(DEBIT_CARD_PATH, 'w', encoding='utf-8') as file:
            json.dump(debit_cards, file, indent=4)
            
        print("Tarjeta de débito creada exitosamente.")

def getAllDebitCards():
    """
    Devuelve todas las tarjetas de débito de los usuarios.
    """
    with open(DEBIT_CARD_PATH, 'r', encoding='utf-8') as file:
        debit_cards = json.load(file)
    return debit_cards

def getOneDebitCard(username):
    """
    Devuelve la tarjeta de débito asociada al nombre de usuario.

    Parámetros:
    
    username (String): Nombre de usuario
    """
    with open(DEBIT_CARD_PATH, 'r', encoding='utf-8') as file:
        debit_cards = json.load(file)
    
    if username in debit_cards:
        return debit_cards[username]
    else:
        return False
    

def consultCard(username,users):
    """
        Imprime los datos de la tarjeta
    """
    card = getOneDebitCard(username)
    if card:
        print()
        for key,value in card.items():
            if isinstance(value,list):
                value = "/".join([str(elemento) for elemento in value[3::-1]])
            print(f"{key}: {value}")
        print()

    else:
        print("No se encontró una tarjeta para este usuario")