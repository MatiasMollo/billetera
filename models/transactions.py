
from datetime import datetime

totalTransacciones = 231

users = {
    'Matiass07_34': {
        "nombre" : "Matias",
        "apellido" : "Mollo",
        "DNI": "12345561",
        "password" : "12345",
        "CVU": "46557867773",
        "historial_crediticio" : 10,
        "dinero" : 500,
    },
    'Dani333_': {
        "nombre" : "Daniel",
        "apellido" : "González",
        "DNI": "17464644",
        "password" : "12345",
        "CVU": "44561291222",
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
        "cuenta_origen": "12349855886",
    },
    2: {
        "nombre_usuario": "Dani333_",
        "tipo_transaccion": "envioExterno",
        "fecha": (2024, 8, 24, 10, 19, 24),
        "monto": 4000.00,
        "CVU_destino": "13441919001",
    },
    3: {
        "nombre_usuario": "Dani333_",
        "tipo_transaccion": "ingreso",
        "fecha": (2024, 8, 30, 12, 10, 3),
        "monto": 10853.00,
        "cuenta_origen": "18866710229",
    },
    4: {
        "nombre_usuario": "Carlos12",
        "tipo_transaccion": "pagoServicio",
        "fecha": (2024, 9, 7, 16, 12, 41),
        "monto": 4000.00,
        "numero_factura": "455666",
    },
    5: {
        "nombre_usuario": "Dani333_",
        "tipo_transaccion": "ingreso",
        "fecha": (2024, 9, 10, 20, 32, 55),
        "monto": 10853.00,
        "cuenta_origen": "44231710229",
    },
    6: {
        "nombre_usuario": "Jose_29",
        "tipo_transaccion": "envioInterno",
        "fecha": (2024, 9, 11, 21, 8, 17),
        "monto": 4000.00,
        "CVU_destino": "27298331344",
    },
    7: {
        "nombre_usuario": "Dani333_",
        "tipo_transaccion": "ingreso",
        "fecha": (2024, 9, 14, 23, 11, 5),
        "monto": 10853.00,
        "cuenta_origen": "73829076321",
    },
    8: {
        "nombre_usuario": "Dani333_",
        "tipo_transaccion": "envioInterno",
        "fecha": (2024, 9, 15, 10, 45, 30),
        "monto": 4000.00,
        "CVU_destino": "15364840299",
    }
}

#Registra la fecha y tiempo al momento de la transacción
def registerDate():
    hoy = datetime.datetime.now()
    fechaActual = (hoy.year, hoy.month, hoy.day, hoy.hour, hoy.minute, hoy.second)

    return fechaActual


#Revisa que el CVU cuente con el formato requerido
def checkFormat(cuentaDestino):
    if len(cuentaDestino) == 11:
        return True
    return False


#Deposita dinero a la cuenta del usuario que viene de una cuenta externa
def depositMoney(nombreUsuario, users):
    monto = float(input("Ingrese el monto que desea depositar en su cuenta: "))
    cuentaOrigen = input("Ingrese el CBU o CVU de la cuenta origen de los fondos: ")
    while not checkFormat(cuentaOrigen):
        print("Formato incorrecto. Revise el número y vuelva a intentar")
        cuentaOrigen = input("Ingrese el CBU o CVU de la cuenta origen de los fondos: ")
    dataUsuario = users.get(nombreUsuario)
    cuentaDestino = dataUsuario.get("CVU")
    #Se ingresa el dinero en la cuenta destino de Bankando
    saldo = increaseBalance(cuentaDestino, monto, users)
    print(f"Su dinero ha sido depositado. Su nuevo saldo es {saldo}")
    tipoTransaccion = "ingreso"
    #Se guarda el registro individual de la transacción en el archivo de transacciones de Bankando
    registerTransaction(nombreUsuario, tipoTransaccion, monto, cuentaOrigen, totalTransacciones, transacciones)

    return monto, saldo, tipoTransaccion
    

#Envía dinero a una cuenta destino dentro o fuera de Bankando, y se registra la transacción en transacciones
def sendMoney(nombreUsuario, users):
    print("===================")
    print("1. Enviar a una cuenta de Bankando")
    print("2. Enviar a una cuenta de otro banco")
    print("===================")
    opcion = input()
    while opcion != "1" and opcion != "2":
        print("Por favor, elija una opción válida (1 ó 2): ")
        opcion = input()
    if opcion == "1":
        tipoTransaccion = "envioInterno"
    else:
        tipoTransaccion = "envioExterno"
    monto = float(input("Ingrese el monto que desea enviar: "))
    #Validamos que tenga dinero suficiente en su cuenta
    while not checkBalance(monto, nombreUsuario, users):
        print("No hay dinero suficiente en su cuenta")
        monto = float(input("Ingrese el monto que desea enviar: "))
    cuentaDestino = input("Ingrese el CBU o CVU de la cuenta destino: ")
    #Validamos formato del CBU/CVU
    while not checkFormat(cuentaDestino):
        print("Formato incorrecto. Revise el número y vuelva a intentar")
        cuentaDestino = input("Ingrese el CBU o CVU de la cuenta destino: ")
    if tipoTransaccion == "envioInterno":
        #Validamos que la cuenta existe en Bankando
        while not checkCVU(cuentaDestino, users):
            print("No existe esa cuenta en Bankando. Revise el número de CVU")
            cuentaDestino = input("Ingrese el CBU o CVU de la cuenta destino: ")
            #Validamos de nuevo el formato antes de volver a buscar el nuevo input en Bankando
            while not checkFormat(cuentaDestino):
                print("Formato incorrecto. Revise el número y vuelva a intentar")
                cuentaDestino = input("Ingrese el CBU o CVU de la cuenta destino: ")
        #Se ingresa el dinero en la cuenta destino de Bankando
        increaseBalance(cuentaDestino, monto, users)
    #Se resta el dinero en la cuenta origen del usuario
    saldo = decreaseBalance(monto, nombreUsuario, users)
    print(f"Su dinero ha sido enviado. Su nuevo saldo es {saldo}")
    #Se guarda el registro individual de la transacción en el archivo de transacciones de Bankando
    registerTransaction(nombreUsuario, tipoTransaccion, monto, cuentaDestino, totalTransacciones, transacciones)

    return cuentaDestino, monto, saldo, tipoTransaccion



def payUtilities(nombreUsuario, users):
    factura = input("Ingrese el número de la factura que desea pagar: ")
    monto = float(input("Ingrese el monto que desea enviar: "))
    #Validamos que tenga dinero suficiente en su cuenta
    while not checkBalance(monto, nombreUsuario, users):
        print("No hay dinero suficiente en su cuenta")
        monto = float(input("Ingrese el monto que desea enviar: "))
    saldo = decreaseBalance(monto, nombreUsuario, users)
    print(f"Su factura ha sido pagada. Su nuevo saldo es {saldo}")
    tipoTransaccion = "pagoServicio"
    #Se guarda el registro individual de la transacción en el archivo de transacciones de Bankando
    registerTransaction(nombreUsuario, tipoTransaccion, monto, factura, totalTransacciones, transacciones)
    
    return monto, saldo, tipoTransaccion


#Valida si el monto que se pretende usar está disponible en la cuenta
def checkBalance(monto, nombreUsuario, users):
    if nombreUsuario in users:
        saldo = users[nombreUsuario]["dinero"]
    if saldo >= monto:
        return True
    return False


#Le sirve al usuario para consultar el saldo de su cuenta
def showBalance(nombreUsuario, users):
    dataUsuario = users.get(nombreUsuario)
    saldo = dataUsuario.get("dinero")
    print(f"El saldo de su cuenta es {saldo}")


#Valida si la cuenta existe en Bankando
def checkCVU(cuentaDestino, users):
    for valor in users.values():
        if valor["CVU"] == cuentaDestino:
            return True
    return False


#Le sirve al usuario para consultar el CVU de su cuenta
def showCVU(nombreUsuario, users):
    dataUsuario = users.get(nombreUsuario)
    cuenta = dataUsuario.get("CVU")
    print(f"CVU: {cuenta}")


#Resta el monto de la transacción del saldo del usuario
def decreaseBalance(monto, nombreUsuario, users):
    if nombreUsuario in users:
        saldo = users[nombreUsuario]["dinero"]
        saldo = saldo - monto
        users[nombreUsuario]["dinero"] = saldo
    
    return saldo


#Suma el monto de la transacción al saldo del usuario
def increaseBalance(CVU, monto, users):
    for clave, valor in users.items():
        if valor["CVU"] == CVU:
            saldo = valor["dinero"]
            saldo = saldo + monto
            valor["dinero"] = saldo

    return saldo


#Luego de cada operación, el movimiento se registra acá para el control del banco en el archivo transacciones
def registerTransaction(nombreUsuario, tipoTransaccion, monto, datoTransaccion, totalTransacciones, transacciones):
    nuevaTransaccion = {}
    nuevaTransaccion["nombre_usuario"] = nombreUsuario
    nuevaTransaccion["tipo_transaccion"] = tipoTransaccion
    fecha = registerDate()
    nuevaTransaccion["fecha"] = fecha
    nuevaTransaccion["monto"] = monto
    if tipoTransaccion == "ingreso":
        nuevaTransaccion["cuenta_origen"] = datoTransaccion
    elif tipoTransaccion == "envioInterno" or tipoTransaccion == "envioExterno":
        nuevaTransaccion["CVU_destino"] = datoTransaccion
    else:
        nuevaTransaccion["numero_factura"] = datoTransaccion
    
    #Calcula qué número de transacción es esta en el historial del banco (actualizando éste) y lo asigna como ID de la transacción registrada
    totalTransacciones += 1
    #Actualiza el archivo transacciones de Bankando con el nuevo movimiento
    transacciones[totalTransacciones] = nuevaTransaccion


#Le muestra al usuario los reportes de sus movimientos por fechas seleccionadas, los más recientes (cantidad a elegir dentro del total) y por tipo de transacción realizada (cantidad a elegir dentro del total)
def showReports(nombreUsuario, transacciones):
    print("===================")
    print("1. Mostrar movimientos por fecha")
    print("2. Mostrar movimientos más recientes")
    print("3. Mostrar movimientos por tipo de transacción")
    print("===================")
    opcion = input()
    while opcion != "1" and opcion != "2" and opcion != "3":
        print("Por favor, ingrese una opción correcta (1, 2 ó 3): ")
        opcion = input()
    if opcion == "1":
        showTransactionsByDate(nombreUsuario, transacciones)
    elif opcion == "2":
        showMostRecentTransactions(nombreUsuario, transacciones)
    else:
        tipoTransaccion = chooseReportByTransaction()
        showTransactionsByType(nombreUsuario, tipoTransaccion, transacciones)


#Submenú de los reportes a mostrar por tipo de transacción
def chooseReportByTransaction():
    print("Seleccione el tipo de transacción que desea consultar")
    print("===================")
    print("1. Carga de dinero en cuenta")
    print("2. Envío de dinero a otra cuenta Bankando")
    print("3. Envío de dinero a una cuenta de otro banco")
    print("4. Pago de servicios")
    print("===================")
    tipoTransaccion = ""
    opcion = input()
    while opcion != "1" and opcion != "2" and opcion != "3" and opcion != "4":
        print("Por favor, ingrese una opción correcta (1, 2, 3 ó 4): ")
        opcion = input()
    if opcion == "1":
        tipoTransaccion = "ingreso"
    elif opcion == "2":
        tipoTransaccion = "envioInterno"
    elif opcion == "3":
        tipoTransaccion = "envioExterno"
    else:
        tipoTransaccion = "pagoServicio"
    
    return tipoTransaccion


#Valida si los valores ingresados en el string del usuario son números enteros
def checkInteger(string):
    return string.isdigit()


#Valida si la fecha ingresada por el usuario cumple con el formato requerido
def checkDate(fechaString):
    formato = "%Y-%m-%d"  #Formato necesario: Año-Mes-Día
    try:
        #Para convertir el string en una fecha válida
        fechaValida = datetime.strptime(fechaString, formato)
        
        #Si es válida, devuelve la tupla (año, mes, día)
        return (fechaValida.year, fechaValida.month, fechaValida.day)
    
    except ValueError:
        #Si no es válida, advertimos que la fecha es incorrecta
        print("Fecha inválida. Verifique el uso del formato correcto: Año-Mes-Día(yyyy-mm-dd)")
        
        return None


#Reporte para el usuario de sus movimientos por fecha
def showTransactionsByDate(nombreUsuario, transacciones):
    fechaUsuarioInicial = input("Indique desde qué fecha desea consultar (yyyy-mm-dd): ")
    fechaInicial = checkDate(fechaUsuarioInicial)
    while fechaInicial == None:
        print()
        fechaUsuarioInicial = input("Indique desde qué fecha desea consultar (yyyy-mm-dd): ")
        fechaInicial = checkDate(fechaUsuarioInicial)
        
    fechaUsuarioFinal = input("Indique hasta qué fecha desea consultar: ")
    fechaFinal = checkDate(fechaUsuarioFinal)
    while fechaFinal == None:
        print()
        fechaUsuarioFinal = input("Indique hasta qué fecha desea consultar: ")
        fechaFinal = checkDate(fechaUsuarioFinal)
    
    
    corte = [(clave, valor) for clave, valor in transacciones.items() if valor["nombre_usuario"] == nombreUsuario and valor["fecha"] >= fechaInicial and valor["fecha"] <= fechaFinal]
    corteOrdenado = sorted(corte)
    if len(corte) != 0:
        print(corteOrdenado)
    else:
        print("No se encontraron movimientos en esas fechas")


#Reporte para el usuario de sus movimientos más recientes
def showMostRecentTransactions(nombreUsuario, transacciones):
    cantidad = input("Indique la cantidad de movimientos recientes que desea consultar: ")
    while not checkInteger(cantidad):
        print("Opción inválida. Por favor, asegúrese de ingresar un número entero")
        print()
        cantidad = input("Indique la cantidad de movimientos recientes que desea consultar: ")
    cantidad = int(cantidad)

    totalUsuario = checkTotalUserTransactions(nombreUsuario, transacciones)
    if cantidad > totalUsuario:
        cantidad = totalUsuario
    
    corte = [(clave, valor) for clave, valor in transacciones.items() if valor["nombre_usuario"] == nombreUsuario]
    corteOrdenado = sorted(corte)
    if cantidad >= len(corteOrdenado):
        print(corteOrdenado)
    elif len(corte) == 0:
        print("Usted no tiene movimientos registrados")    
    else:
        #Le resta al total de transacciones (ej: 8) la cantidad indicada (ej: 3) para mostrar sólo las últimas posiciones (ej: 5-7)
        print(corteOrdenado[len(corteOrdenado) - cantidad:])


#Reporte para el usuario de sus movimientos por tipo de transacción
def showTransactionsByType(nombreUsuario, tipoTransaccion, transacciones):
    cantidad = input("Indique la cantidad de movimientos recientes que desea consultar: ")
    while not checkInteger(cantidad):
        print("Opción inválida. Por favor, asegúrese de ingresar un número entero")
        print()
        cantidad = input("Indique la cantidad de movimientos recientes que desea consultar: ")
    cantidad = int(cantidad)
    
    totalUsuario = checkTotalUserTransactions(nombreUsuario, transacciones)
    if cantidad > totalUsuario:
        cantidad = totalUsuario
    
    corte = [(clave, valor) for clave, valor in transacciones.items() if valor["nombre_usuario"] == nombreUsuario and valor["tipo_transaccion"] == tipoTransaccion]
    corteOrdenado = sorted(corte)
    if cantidad >= len(corteOrdenado):
        print(corteOrdenado)
    else:
        print(corteOrdenado[len(corteOrdenado) - cantidad:])


#Valida el total de transacciones realizadas para saber si podrá mostrar la cantidad solicitada por el usuario o el total existente
def checkTotalUserTransactions(nombreUsuario, transacciones):
    corte = [(clave, valor) for clave, valor in transacciones.items() if valor["nombre_usuario"] == nombreUsuario]
    return len(corte)


#Programa principal
nombreUsuario = "Dani333_"
# tipoTransaccion = "envio"
# monto = 1456
# fecha = registerDate()
# cuentaDestino, monto, saldo, tipoTransaccion = sendMoney(nombreUsuario, users)
# # monto, saldo, tipoTransaccion = depositMoney(nombreUsuario, users)
# monto, saldo, tipoTransaccion = payUtilities(nombreUsuario, users)
# print(users)
# # print(cuentaDestino, monto, saldo, tipoTransaccion)
# # numeroTransaccion = registrarTransaccion(nombreUsuario, tipoTransaccion, monto, fecha, totalTransacciones)
# # totalTransacciones += 1
# print(transacciones)
showReports(nombreUsuario, transacciones)