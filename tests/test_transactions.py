import pytest
import models.transactions as transactions
import models.users as users
import json
from datetime import datetime
import random

TRANSACTION_PATH = 'mockDataTests/mockTransactions.json'
transactions.TRANSACTION_PATH = TRANSACTION_PATH

USER_PATH = 'mockDataTests/mockUsers.json'
users.USER_PATH = USER_PATH #guardado de Path para modelo usuarios

transacciones = transactions.getTransaction()

nombreUsuario1 = "Tester4"
nombreUsuario2 = "Prueba5"


def test_getAllTransactions():
    result = transactions.getTransaction()

    file = open(TRANSACTION_PATH,'r')
    data = json.loads(file.read())

    assert result == data


def test_getTransactionsById():
    result = transactions.getTransaction(id="3")

    file = open(TRANSACTION_PATH,'r')
    data = json.loads(file.read())

    assert result == data["3"]


def test_getTransactionsInvalidId():
    with pytest.raises(KeyError):
        transactions.getTransaction(id="1000")


def test_registerDate():
    hoy = datetime.now()
    result = transactions.registerDate()

    assert isinstance(result, tuple), "No es una tupla"
    assert len(result) == 6, "La tupla no tiene todos los campos (6)"
    assert result[0] == hoy.year, "Año incorrecto"
    assert result[1] == hoy.month, "Mes incorrecto"
    assert result[2] == hoy.day, "Día incorrecto"


def test_checkFormat():
    # Caso 1 (longitud correcta, 11 números)
    cuenta = "11122233344"
    assert transactions.checkFormat(cuenta) == True, f"Ocurrió un error con la cuenta {cuenta}"

    # Caso 2 (longitud menor a 11 números)
    cuenta = "11122233"
    assert transactions.checkFormat(cuenta) == False, f"Ocurrió un error con la cuenta {cuenta}"

    # Caso 2 (longitud mayor a 11 números)
    cuenta = "11122233444555"
    assert transactions.checkFormat(cuenta) == False, f"Ocurrió un error con la cuenta {cuenta}"


def test_checkBill():
    #Se prueban los tres servicios y los posibles casos de facturas
    servicio = "1"
    factura = "123456-7"
    assert transactions.checkBill(servicio, factura) == True, "No coincide con el formato"

    servicio = "1"
    factura = "123-7"
    assert transactions.checkBill(servicio, factura) == False, "No coincide con el formato"

    servicio = "2"
    factura = "AF6789"
    assert transactions.checkBill(servicio, factura) == True, "No coincide con el formato"

    servicio = "2"
    factura = "C1F76R"
    assert transactions.checkBill(servicio, factura) == False, "No coincide con el formato"

    servicio = "3"
    factura = "RE-5678-0"
    assert transactions.checkBill(servicio, factura) == True, "No coincide con el formato"

    servicio = "3"
    factura = "CR12345-E"
    assert transactions.checkBill(servicio, factura) == False, "No coincide con el formato"


def test_checkDate():
    #La fecha ya viene en string dada por el usuario y en la función que llama a checkDate se controlan los valores
    fecha = "2024-11-30"
    result = (2024, 11, 30)
    assert transactions.checkDate(fecha) == result, "La fecha no se convirtió a tupla"


def test_checkCVU():
    data = users.getUser()
    current_username = list(data)[0]
    current_cvu = data[current_username]['CVU']
    result = transactions.checkCVU(current_cvu)
    assert result == True, "No se ha encontrado el CVU del usuario"

    new_cvu = users.generateCVU()
    result = transactions.checkCVU(new_cvu)
    assert result == False, "Se ha encontrado un CVU para un usuario inexistente"


def test_checkInteger():
    assert transactions.checkInteger("1234") == True, "Debe devolver True para un número entero válido"
    assert transactions.checkInteger("0") == True, "Debe devolver True para un número entero válido"

    assert transactions.checkInteger("-46") == False, "Debe devolver False para un número negativo"
    assert transactions.checkInteger("12.89") == False, "Debe devolver False para un float"
    assert transactions.checkInteger("4af58j") == False, "Debe devolver False para una cadena"


def test_checkTotalUserTransactions():
    result = transactions.checkTotalUserTransactions(nombreUsuario1, transacciones)
    assert result == 10, f"Debe devolver 10 transacciones para {nombreUsuario1}, pero se obtiene {result}"

    result = transactions.checkTotalUserTransactions(nombreUsuario2, transacciones)
    assert result == 0, f"Debe devolver 0 transacciones para {nombreUsuario2}, pero se obtiene {result}"


def test_loanResult():
    monto = 1000
    cuotas = 12
    calculo = transactions.loanResult(monto, cuotas)
    resultado_esperado = round((1000 + (1000 * 5.67/100 * 12)) / 12, 2)
    assert calculo == resultado_esperado, f"Debería retornar {resultado_esperado} para un monto de {monto} y {cuotas} cuotas"

    monto = 200000
    cuotas = 6
    calculo = transactions.loanResult(monto, cuotas)
    resultado_esperado = round((200000 + (200000 * 5.67/100 * 6)) / 6, 2)
    assert calculo == resultado_esperado, f"Debería retornar {resultado_esperado} para un monto de {monto} y {cuotas} cuotas"

    monto = 999
    cuotas = 3
    calculo = transactions.loanResult(monto, cuotas)
    resultado_esperado = round((999 + (999 * 5.67/100 * 3)) / 3, 2)
    assert calculo == resultado_esperado, f"Debería retornar {resultado_esperado} para un monto de {monto} y {cuotas} cuotas"

    monto = 1
    cuotas = 9
    calculo = transactions.loanResult(monto, cuotas)
    resultado_esperado = round((1 + (1 * 5.67/100 * 9)) / 9, 2)
    assert calculo == resultado_esperado, f"Debería retornar {resultado_esperado} para un monto de {monto} y {cuotas} cuotas"


def test_registerTransaction():
    amount = 100
    origin = users.generateCVU()

    transactions.registerTransaction(
        "username",
        "ingreso",
        amount,
        origin
    )

    date = transactions.registerDate()

    data = transactions.getTransaction()
    current_transaction = data[list(data)[len(data) - 1]]

    assert current_transaction['cuenta_origen'] == origin,"El origen de la última transacción no coincide con el intento de guardado "
    assert date == tuple(current_transaction["fecha"]),"La fecha de registro no coincide con la última transacción"




