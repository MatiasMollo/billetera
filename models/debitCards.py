import json
import random
from datetime import datetime

DEBIT_CARD_PATH = '../data/debitCards.json'

def createDebitCard(username, userFullName):
    """
    Obtiene el nombre de usuario y el nombre completo del usuario y crea una tarjeta de débito asociada a él.

    Parámetros:
    
    username (None | String): Nombre de usuario
    userFullName (None | String): Nombre completo del usuario
    """
    # Cuando veamos excepciones vamos a contemplar el caso de que entren parametros vacios
    with open(DEBIT_CARD_PATH, 'r') as file:
        debit_cards = json.load(file)

    if username in debit_cards:
        return "Ya tienes una tarjeta de débito asociada a tu cuenta."

    while True:
        card_number = ''.join([str(random.randint(0, 9)) for _ in range(16)])
        if not any(card_number in card for card in debit_cards.values()):
            break

    security_code = ''.join([str(random.randint(0, 9)) for _ in range(4)])

    valid_from = datetime.now().timetuple()[:3]
    expires_end = (datetime.now().year + 5, datetime.now().month, datetime.now().day)
    debit_card_details = {
        "card_number": card_number,
        "valid_from": valid_from,
        "expires_end": expires_end,
        "security_code": security_code,
        "full_name": userFullName,
    }

    debit_cards[username] = debit_card_details
    with open(DEBIT_CARD_PATH, 'w') as file:
        json.dump(debit_cards, file, indent=4)
    return "Tarjeta de débito creada exitosamente."

def getAllDebitCards():
    """
    Devuelve todas las tarjetas de débito de los usuarios.
    """
    with open(DEBIT_CARD_PATH, 'r') as file:
        debit_cards = json.load(file)
    return debit_cards

def getOneDebitCard(username):
    """
    Devuelve la tarjeta de débito asociada al nombre de usuario.

    Parámetros:
    
    username (String): Nombre de usuario
    """
    with open(DEBIT_CARD_PATH, 'r') as file:
        debit_cards = json.load(file)
    
    if username in debit_cards:
        return debit_cards[username]
    else:
        return "No se encontró una tarjeta de débito asociada a este usuario."
    
print(getOneDebitCard(""))