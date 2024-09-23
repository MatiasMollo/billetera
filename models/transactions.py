
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
    cuentaOrigen = cuentaDestino = users[nombreUsuario]["CVU"]

    #Se ingresa el dinero en la cuenta destino de Bankando
    ret,saldo = usuarios.increaseBalance(cuentaDestino,monto,nombreUsuario)
    if ret:
        print(f"\nSu dinero ha sido depositado desde su cuenta vinculada. Su nuevo saldo es {saldo}")
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
    ret = False

    while opcion not in ["1","2","3"]:
        print("Por favor, elija una opción válida: ")
        opcion = input()

    if opcion in ["1","2"]:
        tipoTransaccion = "envioInterno" if opcion == "1" else "envioExterno"
        monto = float(input("Ingrese el monto que desea enviar: "))
        dinero_en_cuenta = usuarios.getBalance(nombreUsuario)

        while dinero_en_cuenta < monto and monto != 0:
            print(f"No hay suficiente dinero en la cuenta, su saldo es de ${dinero_en_cuenta}")
            monto = float(input("Ingrese otro monto o presione 0 para salir: "))

        if monto > 0:
            cuentaDestino = input("Ingrese el CBU o CVU de la cuenta destino: ")

            #Validamos formato del CBU/CVU
            while cuentaDestino != "0" and not checkFormat(cuentaDestino):
                print("Formato incorrecto. Revise el número y vuelva a intentar")
                cuentaDestino = input("Ingrese el CBU o CVU de la cuenta destino (0 para volver): ")

            if tipoTransaccion == "envioInterno" and cuentaDestino != "0":
                #Validamos que la cuenta existe en Bankando
                while cuentaDestino != "0" and not checkCVU(cuentaDestino, users):
                    print("No existe esa cuenta en Bankando. Revise el número de CVU")
                    cuentaDestino = input("Ingrese el CBU o CVU de la cuenta destino (0 para volver): ")

                if cuentaDestino != "0":
                    #Se ingresa el dinero en la cuenta destino de Bankando
                    usuarios.increaseBalance(cuentaDestino, monto)

            # Verificamos que el usuario no corte la ejecución
            if cuentaDestino != "0":
                #Se resta el dinero en la cuenta origen del usuario
                ret = usuarios.decreaseBalance(monto,nombreUsuario)
                saldo = float(dinero_en_cuenta - monto)
                print(f"Su dinero ha sido enviado. Su nuevo saldo es ${saldo}")

                #Se guarda el registro individual de la transacción en el archivo de transacciones de Bankando
                registerTransaction(nombreUsuario, tipoTransaccion, monto, cuentaDestino)
                
                ret = (cuentaDestino, monto, saldo, tipoTransaccion)

    return ret

def payUtilities(nombreUsuario, users):
    factura = input("Ingrese el número de la factura que desea pagar: ")
    monto = float(input("Ingrese el monto que desea enviar: "))
    saldo = 0
    tipoTransaccion = "pagoServicio"
    dinero_en_cuenta = usuarios.getBalance(nombreUsuario)

    #Validamos que tenga dinero suficiente en su cuenta
    while monto > dinero_en_cuenta and monto != 0:
        print("No hay dinero suficiente en su cuenta")
        monto = float(input("Ingrese el monto que desea enviar (0 para cancelar): "))

    #Verificamos que el usuario no haya cancelado la operación
    if monto:
        status,saldo = usuarios.decreaseBalance(monto,nombreUsuario)
        print(f"Su factura ha sido pagada. Su nuevo saldo es ${saldo}")

        #Se guarda el registro individual de la transacción en el archivo de transacciones de Bankando
        registerTransaction(nombreUsuario, tipoTransaccion, monto, factura)
    
    return monto, saldo, tipoTransaccion

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
def showReports(nombreUsuario, users):
    print("===================")
    print("1. Mostrar movimientos por fecha")
    print("2. Mostrar movimientos más recientes")
    print("3. Mostrar movimientos por tipo de transacción")
    print("4. Volver")
    print("===================")
    opcion = input()

    transacciones = getTransaction()
    
    while opcion not in ["1","2","3","4"]:
        print("Por favor, ingrese una opción correcta: ")
        opcion = input()
    if opcion == "1":
        showTransactionsByDate(nombreUsuario, transacciones)
    elif opcion == "2":
        showMostRecentTransactions(nombreUsuario, transacciones)
    elif opcion == "3":
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
    
    
    corte = [(clave, valor) for clave, valor in transacciones.items() if valor["nombre_usuario"] == nombreUsuario and tuple(valor["fecha"][:3]) >= fechaInicial and tuple(valor["fecha"][:3]) <= fechaFinal]
    corteOrdenado = sorted(corte)
    if len(corteOrdenado) != 0:
        printReports(corteOrdenado)
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
        printReports(corteOrdenado)
    elif len(corteOrdenado) == 0:
        print("Usted no tiene movimientos registrados")    
    else:
        #Le resta al total de transacciones (ej: 8) la cantidad indicada (ej: 3) para mostrar sólo las últimas posiciones (ej: 5-7)
        rebanado = corteOrdenado[len(corteOrdenado) - cantidad:]
        printReports(rebanado)
  


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
        printReports(corteOrdenado)
    else:
        printReports(corteOrdenado[len(corteOrdenado) - cantidad:])


#Valida el total de transacciones realizadas para saber si podrá mostrar la cantidad solicitada por el usuario o el total existente
def checkTotalUserTransactions(nombreUsuario, transacciones):
    corte = [(clave, valor) for clave, valor in transacciones.items() if valor["nombre_usuario"] == nombreUsuario]
    return len(corte)
    

#Itera sobre los reportes de transacciones seleccionados para mostrarlos en pantalla con un formato legible para el usuario
def printReports(report):
    campos = ["Nombre de usuario", "Tipo de transacción", "Fecha", "Monto", "Cuenta origen", "Cuenta destino", "Número de factura"]
    listaFinal= [transaction for id_number, transaction in report]
    for transaction in listaFinal:
        #El contador sirve para reemplazar la clave por el string adecuado de la lista campos
        contador = 0
        while contador < len(transaction):
            for key, value in transaction.items():
                #Para valores que son iguales en todos los registros
                if contador <= 3:
                    if key == "fecha":
                        print(f"{campos[contador]}:", "/".join([str(elemento) for elemento in value[:3]])) #Convierte el formato fecha a string con / como separador
                        contador += 1
                    else:
                        print(f"{campos[contador]}:", value)
                        contador += 1
                #Para valores que cambian en el registro según la transacción
                else:
                    if key == "cuenta_origen":
                        print(f"{campos[contador]}:", value)
                        contador += 1
                    elif key == "CVU_destino":
                        print(f"{campos[contador+1]}:", value)
                        contador += 1
                    else:
                        print(f"{campos[contador+2]}:", value)
                        contador += 1
        print()