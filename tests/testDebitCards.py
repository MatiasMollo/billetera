import pytest
from unittest import mock
import os
import models.debitCards as dc
import models.users as usuarios
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

fake_data_path = "tests/mockDataTests/mockDebitCards.json"
fake_users = {
    "userPrueba": {
        "nombre": "prueba",
        "apellido": "prueba",
        "password": "prueba",
        "historial_crediticio": 0,
        "dinero": 0,
        "CVU": "12345678912"
    }
}
    
assert os.path.exists(fake_data_path), f"El archivo {fake_data_path} no existe."

# funcion que se ejecutara automaticamente antes de cada prueba
# para setear el path de los datos falsos
@pytest.fixture(autouse=True)
def mock_debit_card_path():
    with mock.patch('models.debitCards.DEBIT_CARD_PATH', fake_data_path):
        yield

# getOneDebitCard
def test_getOneDebitCard_userExists():
    username = "user1"
    result = dc.getOneDebitCard(username)
    assert result is not False, "El usuario debería tener una tarjeta."
    assert result["card_number"] == "1234567890123456", "Número de tarjeta incorrecto."
    logger.info("\n 1-getOneDebitCard: Test de usuario existente pasó exitosamente.")

def test_getOneDebitCard_userDoesNotExist():
    username = "nonexistentuser"
    result = dc.getOneDebitCard(username)
    assert result is False, "El usuario no debería tener una tarjeta."
    logger.info("\n 2-getOneDebitCard: Test de usuario no existente pasó exitosamente.")

def test_getOneDebitCard_intUsername():
    username = 1
    result = dc.getOneDebitCard(username)
    assert result is False, "La función debería devolver False cuando el nombre de usuario no es un string"
    logger.info("\n 3-getOneDebitCard: Test de nombre de usuario int pasó exitosamente.")

def test_getOneDebitCard_noneUsername():
    username = None
    result = dc.getOneDebitCard(username)
    assert result is False, "La función debería devolver False cuando el nombre de usuario es None."
    logger.info("\n 4-getOneDebitCard: Test de nombre de usuario None pasó exitosamente.")
# ---------

# consultCard
def test_consultCard_userExists(capfd):
    username = "user1"
    dc.consultCard(username)
    captured = capfd.readouterr() # Captura la salida del print (en este caso seria "card_number": "1234567890123456")
    assert "card_number: 1234567890123456" in captured.out, "La tarjeta debería existir y tener el número correcto."
    logger.info("\n 1-consultCard: Test de usuario existente pasó exitosamente.")

def test_consultCard_userDoesNotExist(capfd):
    username = "notauser"
    dc.consultCard(username)
    captured = capfd.readouterr()
    assert "No se encontró una tarjeta para este usuario" in captured.out, "Deberia imprimirse el mensaje 'No se encontró una tarjeta para este usuario'"
    logger.info("\n 2-consultCard: Test de usuario no existente pasó exitosamente.")

def test_consultCard_noneUsername(capfd):
    username = None
    dc.consultCard(username)
    captured = capfd.readouterr()
    assert "No se encontró una tarjeta para este usuario" in captured.out, "Deberia imprimirse el mensaje 'No se encontró una tarjeta para este usuario'"
    logger.info("\n 3-consultCard: Test de usuario None pasó exitosamente.")

def test_consultCard_intUsername(capfd):
    username = 1
    dc.consultCard(username)
    captured = capfd.readouterr()
    assert "No se encontró una tarjeta para este usuario" in captured.out, "Deberia imprimirse el mensaje 'No se encontró una tarjeta para este usuario'"
    logger.info("\n 4-consultCard: Test de usuario int pasó exitosamente.")
# ---------

# createDebitCard
def test_createDebitCard_newDebitCard(capfd):
    with mock.patch('models.users.getUser', return_value=fake_users):
        with open(fake_data_path, 'r') as file:
            original_data = json.load(file)

        try:
            with open(fake_data_path, 'w') as file:
                json.dump({}, file)

            username = "userPrueba"
            dc.createDebitCard(username)

            captured = capfd.readouterr()
            assert "Tarjeta de débito creada exitosamente." in captured.out, "La tarjeta debería haberse creado"

            with open(fake_data_path, 'r') as file:
                debit_cards = json.load(file)
                card_details = debit_cards[username]
                assert username in debit_cards, "El usuario debería tener una tarjeta de débito asociada."
                assert card_details["full_name"] == "prueba prueba", "El nombre completo del usuario debería ser el nombre más el apellido."
                assert len(card_details["card_number"]) == 16, "El número de tarjeta debería tener 16 dígitos."
                assert len(card_details["security_code"]) == 4, "El código de seguridad debería tener 4 dígitos."
                assert isinstance(card_details["valid_from"], list) and len(card_details["valid_from"]) == 3, "La fecha de inicio debería ser una lista de 3 elementos."
                assert isinstance(card_details["expires_end"], list) and len(card_details["expires_end"]) == 3, "La fecha de expiración debería ser una lista de 3 elementos."

            logger.info("\n 1-createDebitCard: Test de creación de tarjeta de débito pasó exitosamente.")
        finally:
            with open(fake_data_path, 'w') as file:
                json.dump(original_data, file)

def test_createDebitCard_existingCard(capfd):
        with mock.patch('models.users.getUser', return_value={}):
            username = "user1"
            dc.createDebitCard(username)
            captured = capfd.readouterr()
            assert "Ya tienes una tarjeta de débito asociada a tu cuenta." in captured.out, "deberia imprimirse el mensaje 'Ya tienes una tarjeta de débito asociada a tu cuenta.'"

        logger.info("\n 2-createDebitCard: Test de usuario con tarjeta existente pasó exitosamente.")
# ---------

# getAllDebitCards
def test_getAllDebitCards(capfd):
    result = dc.getAllDebitCards()
    assert isinstance(result, dict), "La función debería devolver un diccionario."
    assert len(result) == 2, "Deberían haber 2 tarjetas de débito."
    logger.info("\n 1-getAllDebitCards: Test de obtención de todas las tarjetas pasó exitosamente.")
# ---------
