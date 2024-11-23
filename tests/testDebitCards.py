import pytest
from unittest import mock
import os
import models.debitCards as dc
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

fake_data_path = "tests/mockDataTests/mockDebitCards.json"
    
assert os.path.exists(fake_data_path), f"El archivo {fake_data_path} no existe."

@pytest.fixture(autouse=True)
def mock_debit_card_path():
    with mock.patch('models.debitCards.DEBIT_CARD_PATH', fake_data_path):
        yield

def test_getOneDebitCard_userExists():
    username = "user1"
    result = dc.getOneDebitCard(username)
    assert result is not False, "El usuario debería tener una tarjeta."
    assert result["card_number"] == "1234567890123456", "Número de tarjeta incorrecto."
    logger.info("\n 1-Test de usuario existente pasó exitosamente.")

def test_getOneDebitCard_userDoesNotExist():
    username = "nonexistentuser"
    result = dc.getOneDebitCard(username)
    assert result is False, "El usuario no debería tener una tarjeta."
    logger.info("\n 2-Test de usuario no existente pasó exitosamente.")

def test_getOneDebitCard_intUsername():
    username = 1
    result = dc.getOneDebitCard(username)
    assert result is False, "La función debería devolver False cuando el nombre de usuario no es un string"
    logger.info("\n 3-Test de nombre de usuario int pasó exitosamente.")

def test_getOneDebitCard_noneUsername():
    username = None
    result = dc.getOneDebitCard(username)
    assert result is False, "La función debería devolver False cuando el nombre de usuario es None."
    logger.info("\n 4-Test de nombre de usuario None pasó exitosamente.")

