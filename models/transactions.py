
from datetime import datetime
import json
import models.users as usuarios

TRANSACTION_PATH = "data/transactions.json"

totalTransacciones = 231

def getTransaction(id = None):
    """
        Obtiene la transacción correspondiente al parámetro, en caso de que sea None, devuelve todas las transacciones
        
        Parámetros:
            id (None|Integer): Id de la operación
    """
    file = open(TRANSACTION_PATH,'r')
    data = json.loads(file.read())

    if id:
        transactions = data[id]
    else:
        transactions = data
    
    file.close()

    return transactions


#Registra la fecha y tiempo al momento de la transacción
def registerDate():
    hoy = datetime.now()
    fechaActual = (hoy.year, hoy.month, hoy.day, hoy.hour, hoy.minute, hoy.second)

    return fechaActual


#Revisa que el CVU cuente con el formato requerido
def checkFormat(cuentaDestino):
    return len(cuentaDestino) == 11


#Deposita dinero a la cuenta del usuario que viene de una cuenta externa
def depositMoney(nombreUsuario, users):
    monto = float(input("Ingrese el monto que desea depositar en su cuenta: "))
    #! Cuenta origen no debería necesitarse ya que el usuario está logueado
    cuentaOrigen = input("Ingrese el CBU o CVU de la cuenta origen de los fondos: ")

    while not checkFormat(cuentaOrigen):
        print("Formato incorrecto. Revise el número y vuelva a intentar")
        cuentaOrigen = input("Ingrese el CBU o CVU de la cuenta origen de los fondos: ")
        
    dataUsuario = users.get(nombreUsuario)
    cuentaDestino = dataUsuario.get("CVU")

    #Se ingresa el dinero en la cuenta destino de Bankando
    #! saldo = increaseBalance(cuentaDestino, monto, users)
    ret,saldo = usuarios.increaseBalance(cuentaDestino,monto,nombreUsuario)
    if ret:
        print(f"\nSu dinero ha sido depositado. Su nuevo saldo es {saldo}")
    else:
        print("No se pudo encontrar la cuenta, intente nuevamente.")

    tipoTransaccion = "ingreso"

    #Se guarda el registro individual de la transacción en el archivo de transacciones de Bankando
    registerTransaction(nombreUsuario, tipoTransaccion, monto, cuentaOrigen)

    return monto, saldo, tipoTransaccion
    

#Envía dinero a una cuenta destino dentro o fuera de Bankando, y se registra la transacción en transacciones
def sendMoney(nombreUsuario, users):
    print("===================")
    print("1. Enviar a una cuenta de Bankando")
    print("2. Enviar a una cuenta de otro banco")
    print("3. Volver")
    print("===================")

    opcion = input()

    while opcion != "1" and opcion != "2":
        print("Por favor, elija una opción válida (1 ó 2): ")
        opcion = input()

    tipoTransaccion = "envioInterno" if opcion == "1" else "envioExterno"

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
        #! Este while no haría falta ya que se valida que exista el cvu desde el modelo usuario
        while not checkCVU(cuentaDestino, users):
            print("No existe esa cuenta en Bankando. Revise el número de CVU")
            cuentaDestino = input("Ingrese el CBU o CVU de la cuenta destino: ")

            #Validamos de nuevo el formato antes de volver a buscar el nuevo input en Bankando
            while not checkFormat(cuentaDestino):
                print("Formato incorrecto. Revise el número y vuelva a intentar")
                cuentaDestino = input("Ingrese el CBU o CVU de la cuenta destino: ")

        #Se ingresa el dinero en la cuenta destino de Bankando
        usuarios.increaseBalance(cuentaDestino, monto)

    #Se resta el dinero en la cuenta origen del usuario
    saldo = decreaseBalance(monto, nombreUsuario, users)
    print(f"Su dinero ha sido enviado. Su nuevo saldo es ${saldo}")

    #Se guarda el registro individual de la transacción en el archivo de transacciones de Bankando
    registerTransaction(nombreUsuario, tipoTransaccion, monto, cuentaDestino)

    if opcion in [1,2]:
        monto = float(input("Ingrese el monto que desea enviar: "))

        while not checkBalance(monto, nombreUsuario, users):
            print("No hay dinero suficiente en su cuenta")
            monto = float(input("Ingrese el monto que desea enviar: "))

        cuentaDestino = input("Ingrese el CBU o CVU de la cuenta destino: ")

        while not checkFormat(cuentaDestino):
            print("Formato incorrecto. Revise el número y vuelva a intentar")
            cuentaDestino = input("Ingrese el CBU o CVU de la cuenta destino: ")

        if tipoTransaccion == "envioInterno":
            while not checkCVU(cuentaDestino, users):
                print("No existe esa cuenta en Bankando. Revise el número de CVU")
                cuentaDestino = input("Ingrese el CBU o CVU de la cuenta destino: ")
                while not checkFormat(cuentaDestino):
                    print("Formato incorrecto. Revise el número y vuelva a intentar")
                    cuentaDestino = input("Ingrese el CBU o CVU de la cuenta destino: ")

            usuarios.increaseBalance(cuentaDestino, monto)

        saldo = decreaseBalance(monto, nombreUsuario, users)
        print(f"Su dinero ha sido enviado. Su nuevo saldo es {saldo}")

        ret = (cuentaDestino, monto, saldo, tipoTransaccion)
    else:
        ret = False

    return ret



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
    registerTransaction(nombreUsuario, tipoTransaccion, monto, factura)
    
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


#Luego de cada operación, el movimiento se registra acá para el control del banco en el archivo transacciones
def registerTransaction(nombreUsuario, tipoTransaccion, monto, datoTransaccion):
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
    
    #Actualiza el archivo transacciones de Bankando con el nuevo movimiento
    transacciones = getTransaction()
    transacciones[len(transacciones) + 1] = nuevaTransaccion

    file = open(TRANSACTION_PATH,'w')
    json.dump(transacciones,file)
    file.close()


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

"""
#Programa principal
nombreUsuario = "Dani333_"
# tipoTransaccion = "envio"
# monto = 1456
# fecha = registerDate()
# cuentaDestino, monto, saldo, tipoTransaccion = sendMoney(nombreUsuario, users)
# monto, saldo, tipoTransaccion = depositMoney(nombreUsuario, users)
# monto, saldo, tipoTransaccion = payUtilities(nombreUsuario, users)
# print(users)
# # print(cuentaDestino, monto, saldo, tipoTransaccion)
# # numeroTransaccion = registrarTransaccion(nombreUsuario, tipoTransaccion, monto, fecha, totalTransacciones)
# # totalTransacciones += 1
# print(transacciones)
showReports(nombreUsuario, transacciones)
print()
print(transacciones)
print()
print(users)
"""