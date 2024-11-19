from unittest import mock
import os
import models.debitCards as dc

def test_getOneDebitCard_withFakeData():
    fake_data_path = "tests/mockDataTests/mockDebitCards.json"
    
    assert os.path.exists(fake_data_path), f"El archivo {fake_data_path} no existe."

    with mock.patch('models.debitCards.DEBIT_CARD_PATH', fake_data_path):
        username = "user1"
        result = dc.getOneDebitCard(username)
        assert result is not False, "El usuario debería tener una tarjeta."
        assert result["card_number"] == "1234567890123456", "Número de tarjeta incorrecto."
        username = "nonexistentuser"
        result = dc.getOneDebitCard(username)
        assert result is False, "El usuario no debería tener una tarjeta."
