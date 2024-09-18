
import datetime

totalTransacciones = 231

users = {
    'Matiass07_34': {
        "nombre" : "Matias",
        "apellido" : "Mollo",
        "DNI": "12345561",
        "password" : "12345",
        "CVU": "455667773",
        "historial_crediticio" : 10,
        "dinero" : 500,
    },
    'Dani333_': {
        "nombre" : "Daniel",
        "apellido" : "González",
        "DNI": "17464644",
        "password" : "12345",
        "CVU": "445611222",
        "historial_crediticio" : 10,
        "dinero" : 100,
    }
}

transacciones = {
    1: {
        "nombre_usuario": "Dani333_",
        "tipo_transaccion": "ingreso",
        "fecha": (2024, 8, 20, 9, 30, 11),
        "monto": 10853.00,
        "tarjeta origen": "1234 9855 8866 1022",
    },
    2: {
        "nombre_usuario": "Dani333_",
        "tipo_transaccion": "envioExterno",
        "fecha": (2024, 8, 24, 10, 19, 24),
        "monto": 4000.00,
        "CVU_destino": "1344",
    },
    3: {
        "nombre_usuario": "Dani333_",
        "tipo_transaccion": "ingreso",
        "fecha": (2024, 8, 30, 12, 10, 3),
        "monto": 10853.00,
    },
    4: {
        "nombre_usuario": "Carlos12",
        "tipo_transaccion": "pagoServicio",
        "fecha": (2024, 9, 7, 16, 12, 41),
        "monto": 4000.00,
        "servicio": "Edenor",
        "numero_factura": "455666",
    },
    5: {
        "nombre_usuario": "Dani333_",
        "tipo_transaccion": "ingreso",
        "fecha": (2024, 9, 10, 20, 32, 55),
        "monto": 10853.00,
    },
    6: {
        "nombre_usuario": "Jose_29",
        "tipo_transaccion": "envioInterno",
        "fecha": (2024, 9, 11, 21, 8, 17),
        "monto": 4000.00,
        "CVU_destino": "1344",
    },
    7: {
        "nombre_usuario": "Dani333_",
        "tipo_transaccion": "ingreso",
        "fecha": (2024, 9, 14, 23, 11, 5),
        "monto": 10853.00,
    },
    8: {
        "nombre_usuario": "Dani333_",
        "tipo_transaccion": "envioInterno",
        "fecha": (2024, 9, 15, 10, 45, 30),
        "monto": 4000.00,
        "CVU_destino": "1344",
    }
}


#En esta función debo agregar el destinatario si el alias del receptor está en nuestra base.
#Revisar cómo está pensado en el main

def registrarFecha():
    hoy = datetime.datetime.now()
    fechaActual = (hoy.year, hoy.month, hoy.day, hoy.hour, hoy.minute, hoy.second)

    return fechaActual


def sendMoney(nombreUsuario, users):
    print("===================")
    print("1. Enviar a una cuenta de Bankando")
    print("2. Enviar a una cuenta de otro banco")
    print("===================")
    opcion = int(input())
    while opcion != 1 and opcion != 2:
        print("Por favor, elija una opción válida (1 ó 2): ")
        opcion = int(input())
    if opcion == 1:
        tipoTransaccion = "envioInterno"
    else:
        tipoTransaccion = "envioExterno"
    cuentaDestino = input("Ingrese el CBU o CVU de la cuenta destino: ")
    monto = float(input("Ingrese el monto que desea enviar: "))
    while not checkBalance(monto, nombreUsuario, users):
        print("No hay dinero suficiente en su cuenta")
        monto = float(input("Ingrese el monto que desea enviar: "))
    if tipoTransaccion == 2:
        if not checkCVU(cuentaDestino):
            print("No existe esa cuenta en Bankando. Revise el número de CVU")
        else:
            increaseBalance(cuentaDestino, monto, users)
    saldo = decreaseBalance(monto, nombreUsuario, users)
    print(f"Su dinero ha sido enviado. Su nuevo saldo es {saldo}")

    return cuentaDestino, monto, saldo, tipoTransaccion, nombreUsuario


def checkBalance(monto, nombreUsuario, users):
    if nombreUsuario in users:
        saldo = users[nombreUsuario]["dinero"]
    if saldo >= monto:
        return True
    return False


def checkCVU(CVU, users):
    for clave, valor in users.items:
        if valor["CVU"] == CVU:
            return True
    return False


def decreaseBalance(monto, nombreUsuario, users):
    if nombreUsuario in users:
        saldo = users[nombreUsuario]["dinero"]
        saldo = saldo - monto
        users[nombreUsuario]["dinero"] = saldo  


def increaseBalance(CVU, monto, users):
    for clave, valor in users.items:
        if valor["CVU"] == CVU:
            saldo = valor["dinero"]
            saldo = saldo + monto
            valor["dinero"] = saldo


#Revisar si hago todo esto en una sola función o en varias o si registro cada transacción en su propia función

def registerTransaction(nombreUsuario, tipoTransaccion, monto, fecha, totalTransacciones, transacciones):
    #Se podrían hacer todas las preguntas dentro de esta función o afuera y luego se registran acá

    nuevaTransaccion = {}
    nuevaTransaccion["nombre_usuario"] = nombreUsuario
    nuevaTransaccion["tipo_transaccion"] = tipoTransaccion
    nuevaTransaccion["monto"] = monto


   


    totalTransacciones += 1
    tuplaTransaccion = (totalTransacciones, fecha) #asumiendo que fecha ya viene como tupla

    transacciones[tuplaTransaccion] = nuevaTransaccion

    return totalTransacciones




#Crear funciones para balances de cuenta


#En el main habría una opción para elegir esta función
#Falta usar también el nombre de usuario en la lógica


def showReports(nombreUsuario):
    print("===================")
    print("1. Mostrar movimientos por fecha")
    print("2. Mostrar movimientos más recientes")
    print("3. Mostrar movimientos por tipo de transacción")
    print("===================")
    opcion = int(input())
    while opcion != 1 and opcion != 2 and opcion != 3:
        print("Por favor, ingrese una opción correcta (1, 2 ó 3): ")
        opcion = int(input())
    if opcion == 1:
        showTransactionsByDate(nombreUsuario, transacciones)
    elif opcion == 2:
        showMostRecentTransactions()
    else:
        tipoTransaccion = showTransactionsToChoose()
        showTransactionsByType(nombreUsuario, tipoTransaccion, transacciones)


def showTransactionsToChoose():
    print("===================")
    print("1. Carga de dinero en cuenta")
    print("2. Envío de dinero a otra cuenta Bankando")
    print("3. Envío de dinero a una cuenta de otro banco")
    print("4. Pago de servicios")
    print("===================")
    opcion = int(input())
    while opcion != 1 and opcion != 2 and opcion != 3 and opcion != 4:
        print("Por favor, ingrese una opción correcta (1, 2, 3 ó 4): ")
        opcion = int(input())
    if opcion == 1:
        tipoTransaccion == "ingreso"
    elif opcion == 2:
        tipoTransaccion == "envioInterno"
    elif opcion == 3:
        tipoTransaccion == "envioExterno"
    else:
        tipoTransaccion == "pagoServicio"
    
    return tipoTransaccion


def showTransactionsByDate(nombreUsuario, tipoTransaccion, transacciones):
    fechaInicial = input("Indique desde qué fecha desea consultar: ")
    fechaFinal = input("Indique hasta qué fecha desea consultar: ")
    # totalUsuario = calcularTotalTransaccionesUsuario(nombreUsuario, transacciones)
    # if numero > totalUsuario:
    #     numero = totalUsuario
    
    corte = [(clave, valor) for clave, valor in transacciones.items() if valor["fecha"] >= fechaInicial and valor["fecha"] <= fechaFinal and valor["tipo_transaccion"] == tipoTransaccion]
    corteOrdenado = sorted(corte)
    # if numero >= len(corteOrdenado):
    #     print(corteOrdenado)
    # else:
    #     print(corteOrdenado[len(corteOrdenado) - numero:])
    return


def showMostRecentTransactions(nombreUsuario, tipoTransaccion, transacciones):
    cantidad = int(input("Indique la cantidad de movimientos recientes que desea consultar: "))
    totalUsuario = checkTotalUserTransactions(nombreUsuario, transacciones)
    if cantidad > totalUsuario:
        cantidad = totalUsuario
    
    corte = [(clave, valor) for clave, valor in transacciones.items() if valor["nombre_usuario"] == nombreUsuario]
    corteOrdenado = sorted(corte)
    if cantidad >= len(corteOrdenado):
        print(corteOrdenado)
    else:
        print(corteOrdenado[len(corteOrdenado) - cantidad:])


def showTransactionsByType(nombreUsuario, tipoTransaccion, transacciones):
    cantidad = int(input("Indique la cantidad de movimientos que desea consultar: "))
    totalUsuario = checkTotalUserTransactions(nombreUsuario, transacciones)
    if cantidad > totalUsuario:
        cantidad = totalUsuario
    
    corte = [(clave, valor) for clave, valor in transacciones.items() if valor["tipo_transaccion"] == tipoTransaccion]
    corteOrdenado = sorted(corte)
    if cantidad >= len(corteOrdenado):
        print(corteOrdenado)
    else:
        print(corteOrdenado[len(corteOrdenado) - cantidad:])


def checkTotalUserTransactions(nombreUsuario, transacciones):
    corte = [(clave, valor) for clave, valor in transacciones.items() if valor["nombre_usuario"] == nombreUsuario]
    return len(corte)


#Programa principal
nombreUsuario = "Dani333_"
tipoTransaccion = "envio"
monto = 1456
fecha = tuple([2024, 9, 15])

numeroTransaccion = registrarTransaccion(nombreUsuario, tipoTransaccion, monto, fecha, totalTransacciones)
totalTransacciones += 1

# print(transacciones)
# print()
# print(transacciones[numeroTransaccion, fecha])
# print(totalTransacciones)

# mostrarTransaccionesPorOrden(nombreUsuario, transacciones)
mostrarTransaccionesPorTipo(nombreUsuario, transacciones)
print(calcularTotalTransaccionesUsuario(nombreUsuario, transacciones))
