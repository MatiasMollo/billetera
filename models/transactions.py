
from datetime import datetime
import json
import models.users as usuarios
from functools import reduce
import logsController.errorHandler as errorsController
import re

TRANSACTION_PATH = "data/transactions.json"


def getTransaction(id = None):
    """
        Obtiene la transacción correspondiente al parámetro, en caso de que sea None, devuelve todas las transacciones
        
        Parámetros:
            id (None|Integer): Id de la operación
    """
    file = open(TRANSACTION_PATH,'r')
    data = json.loads(file.read())

    if id:
        try:
            transactions = data[id]
        except KeyError:
            raise KeyError(f"La transacción con ID {id} no existe")
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
def depositMoney(nombreUsuario):
    error = True
    while error:
        try:
            monto = float(input("Ingrese el monto que desea depositar en su cuenta: "))
            error = False
        except Exception as e:
            print("El monto debe ser numérico y positivo (presione 0 para cancelar)")

    #Obtenemos el listado de usuarios actualizado
    users = usuarios.getUser()

    cuentaOrigen = cuentaDestino = users[nombreUsuario]["CVU"]
    tipoTransaccion = "ingreso"
    saldo = 0

    if monto > 0:
        #Se ingresa el dinero en la cuenta destino de Bankando
        ret,saldo = usuarios.increaseBalance(cuentaDestino,monto,nombreUsuario)
        if ret:
            print(f"\nSu dinero ha sido depositado desde su cuenta vinculada. Su nuevo saldo es {saldo}")
        else:
            print("No se pudo encontrar la cuenta, intente nuevamente.")

        #Se guarda el registro individual de la transacción en el archivo de transacciones de Bankando
        registerTransaction(nombreUsuario, tipoTransaccion, monto, cuentaOrigen)

    return monto, saldo, tipoTransaccion
    

#Envía dinero a una cuenta destino dentro o fuera de Bankando, y se registra la transacción en transacciones
def sendMoney(nombreUsuario):
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

        error = True
        while error:
            try:
                monto = float(input("Ingrese el monto que desea enviar: "))
                dinero_en_cuenta = usuarios.getBalance(nombreUsuario)

                while dinero_en_cuenta < monto and monto != 0:
                    print(f"No hay suficiente dinero en la cuenta, su saldo es de ${dinero_en_cuenta}")
                    monto = float(input("Ingrese otro monto o presione 0 para salir: "))
                error = False
            except Exception as e:
                print("Ocurrió un error, vuelva a intentarlo.")

        if monto > 0:
            cuentaDestino = input("Ingrese el CBU o CVU de la cuenta destino: ")

            #Validamos formato del CBU/CVU
            while cuentaDestino != "0" and not checkFormat(cuentaDestino):
                print("Formato incorrecto. Revise el número y vuelva a intentar")
                cuentaDestino = input("Ingrese el CBU o CVU de la cuenta destino (0 para volver): ")

            if tipoTransaccion == "envioInterno" and cuentaDestino != "0":
                #Validamos que la cuenta existe en Bankando
                while cuentaDestino != "0" and not checkCVU(cuentaDestino):
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
        else:
            print("Se canceló la operación")

    return ret


def checkBill(servicio, factura):
    patrones = {
        "1": "[0-9]{6}-[0-9]{1}",
        "2": "[A-Z]{2}[0-9]{4}",
        "3": "[A-Z]{2}-[0-9]{4}-[0-9]",
    }
    
    for clave, valor in patrones.items():
        if servicio == clave and re.match(valor, factura):
            return True
    return False


def payUtilities(nombreUsuario):
    print()
    print("===================")
    print("Servicios afiliados")
    print("1. Edenor")
    print("2. Claro")
    print("3. IPlan")
    print("===================")
    servicio = input("Seleccione el servicio que desea pagar: ")
    while servicio not in ["1", "2", "3"]:
        servicio = input("Por favor, seleccione uno de los servicios afiliados: ")
    print()
    print("===================")
    print("Debe introducir a continuación el número de la factura a pagar según el formato del servicio")
    print("=====Ejemplos======")
    print("Edenor: 123456-7")
    print("Claro: AF6789")
    print("IPlan: RE-5678-0")
    print("===================")
    factura = input("Factura: ")
    while not checkBill(servicio, factura):
        factura = input("Por favor, ingrese el número de factura con el formato correcto de su servicio: ")
    monto = float(input("Ingrese el monto a pagar: "))
    saldo = 0
    tipoTransaccion = "pagoServicio"
    dinero_en_cuenta = usuarios.getBalance(nombreUsuario)

    #Validamos que tenga dinero suficiente en su cuenta
    while monto > dinero_en_cuenta and monto != 0:
        print("No hay dinero suficiente en su cuenta")
        monto = float(input("Ingrese el monto a pagar (0 para cancelar): "))

    #Verificamos que el usuario no haya cancelado la operación
    if monto:
        status,saldo = usuarios.decreaseBalance(monto,nombreUsuario)
        print(f"Su factura ha sido pagada. Su nuevo saldo es ${saldo}")

        #Se guarda el registro individual de la transacción en el archivo de transacciones de Bankando
        registerTransaction(nombreUsuario, tipoTransaccion, monto, factura)
    
    return monto, saldo, tipoTransaccion

#Le sirve al usuario para consultar el saldo de su cuenta
def showBalance(nombreUsuario):
    dataUsuario = usuarios.get(nombreUsuario)
    saldo = dataUsuario.get("dinero")
    print(f"El saldo de su cuenta es {saldo}")


#Valida si la cuenta existe en Bankando
def checkCVU(cuentaDestino):
    users = usuarios.getUser()
    for valor in users.values():
        if valor["CVU"] == cuentaDestino:
            return True
    return False


#Le sirve al usuario para consultar el CVU de su cuenta
def showCVU(nombreUsuario):
    dataUsuario = usuarios.get(nombreUsuario)
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
def showReports(nombreUsuario):
    print("===================")
    print("1. Mostrar movimientos por fecha")
    print("2. Mostrar movimientos más recientes")
    print("3. Mostrar movimientos por tipo de transacción")
    print("4. Mostrar gastos totales en un mes")
    print("5. Mostrar ingresos totales en un mes")
    print("6. Volver")
    print("===================")
    opcion = input()

    transacciones = getTransaction()
    
    while opcion not in ["1","2","3","4","5","6"]:
        print("Por favor, ingrese una opción correcta: ")
        opcion = input()
    if opcion == "1":
        showTransactionsByDate(nombreUsuario, transacciones)
    elif opcion == "2":
        showMostRecentTransactions(nombreUsuario, transacciones)
    elif opcion == "3":
        tipoTransaccion = chooseReportByTransaction()
        showTransactionsByType(nombreUsuario, tipoTransaccion, transacciones)
    elif opcion == "4":
        showExpensesByMonth(nombreUsuario, transacciones)
    elif opcion == "5":
        showIncomeByMonth(nombreUsuario, transacciones)


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
    
    except ValueError as e:
        #Si no es válida, advertimos que la fecha es incorrecta
        errorsController.logError(type(e).__name__, str(e))
        print("Fecha inválida. Verifique el uso del formato correcto: Año-Mes-Día(yyyy-mm-dd)")
        


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
    while fechaFinal == None or tuple(fechaInicial) > tuple(fechaFinal):
        print()
        print("La fecha final debe ser mayor a la fecha inicial y tener un formato válido")
        fechaUsuarioFinal = input("Por favor, ingrese de nuevo la fecha: ")
        fechaFinal = checkDate(fechaUsuarioFinal)
    
    corte = [(clave, valor) for clave, valor in transacciones.items() if valor["nombre_usuario"] == nombreUsuario and tuple(valor["fecha"][:3]) >= fechaInicial and tuple(valor["fecha"][:3]) <= fechaFinal]
    corteOrdenado = sorted(corte, key= lambda x : x[1]["fecha"])

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
    
    corte = list(filter(lambda valor : valor[1]["nombre_usuario"] == nombreUsuario, transacciones.items()))
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


def showExpensesByMonth(nombreUsuario, transacciones):
    error = True
    while error:
        try:
            mes = int(input("Indique qué mes desea consultar (1-12): "))
            error = False
        except Exception as e:
            print("El dato ingresado no es válido, intente nuevamente")

    corte = list(filter(lambda valor : valor[1]["nombre_usuario"] == nombreUsuario and valor[1]["tipo_transaccion"] != "ingreso" and valor[1]["fecha"][1] == mes, transacciones.items()))
    
    if len(corte) != 0:
        gastos = reduce(lambda x, y : x + y[1]["monto"], corte, 0)
        print()
        print(f"Monto total de pagos y transferencias en el mes: {gastos:.2f} pesos")
        corteOrdenado = sorted(corte)
        printReports(corteOrdenado)
    else:
        print("No se encontraron movimientos en esas fechas")


#Valida el total de transacciones realizadas para saber si podrá mostrar la cantidad solicitada por el usuario o el total existente
def checkTotalUserTransactions(nombreUsuario, transacciones):
    return reduce(lambda x, y : x + 1, filter(lambda valor : valor["nombre_usuario"] == nombreUsuario, transacciones.values()), 0)
    

#Itera sobre los reportes de transacciones seleccionados para mostrarlos en pantalla con un formato legible para el usuario
def printReports(report):
    campos = ["Nombre de usuario", "Tipo de transacción", "Fecha", "Monto", "Cuenta origen", "Cuenta destino", "Número de factura"]
    listaFinal= [transaction for id_number, transaction in report]
    for transaction in listaFinal:
        #El contador sirve para reemplazar la clave por el string adecuado de la lista campos
        contador = 0
        print()
        while contador < len(transaction):
            for key, value in transaction.items():
                #Para valores que son iguales en todos los registros
                if contador <= 3:
                    if key == "fecha":
                        print(f"{campos[contador]}:", "/".join([str(elemento) for elemento in value[2::-1]])) #Convierte el formato fecha a string con / como separador
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


#Calcula el monto proporcional de cada cuota de un préstamo
def loanResult(monto, cuotas):
    tasa = 5.67/100
    resultado = (monto + (monto*tasa*cuotas)) / cuotas

    return round(resultado, 2)

#Muestra las opciones de pago de un préstamo según las cuotas
def showLoan(monto, lista_cuotas):
    print()
    print("Opciones de plazos")
    print("===================")
    lista_resultados = list(map(lambda cuotas : loanResult(monto, cuotas), lista_cuotas))
    contador = 0
    for cantidad in lista_cuotas:
        print(f"{cantidad} cuotas de {lista_resultados[contador]:.2f} pesos")
        contador += 1
    print()

#Función para simular y solicitar un préstamo personal
def requestLoan(nombreUsuario):
    print("===================")
    print("1. Simular préstamo")
    print("2. Solicitar préstamo")
    print("3. Volver")
    print("===================")

    ret = False
    lista_cuotas = [3, 6, 9, 12]
    limite = 1000000
    opcion = input("Opción: ")
    
    while opcion not in ["1","2","3"]:
        print("Por favor, elija una opción válida: ")
        opcion = input("Opción: ")

    if opcion == "1":
        print("El monto límite para un préstamo personal es de 1.000.000 pesos")
        monto = float(input("Ingrese el monto que le gustaría solicitar -sin puntos ni comas-: "))
        while monto <= 0 or monto > limite:
            monto = float(input("Por favor, ingrese un monto válido: "))
        showLoan(monto, lista_cuotas)
        ret = True
    
    elif opcion == "2":
        preguntar = True 
        while preguntar:
            print("El monto límite para un préstamo personal es de 1.000.000 pesos")
            print()
            monto = float(input("Ingrese el monto a solicitar -sin puntos ni comas- (para cancelar y salir marque 0): "))
            while monto < 0 or monto > limite:
                monto = float(input("Por favor, ingrese un monto válido (para cancelar y salir marque 0): "))
            if monto > 0:           
                print(f"Indique el número de cuotas a pagar ({lista_cuotas}): ", end="")
                cuotas = int(input())
                while cuotas not in lista_cuotas:
                    print(f"Indique un número válido de cuotas a pagar ({lista_cuotas}): ", end="")
                    cuotas = int(input())
                print(f"Si confirma en el siguiente paso, su préstamo por {monto:.2f} pesos lo pagará en {cuotas} cuotas de {loanResult(monto, cuotas)} pesos")
                print()

                ejecutar = input(f"¿Quiere solicitar el préstamo indicado? (S/N): ").lower()
                if ejecutar == "s":  
                    users = usuarios.getUser()          
                    cuentaDestino = users[nombreUsuario]["CVU"]
                    tipoTransaccion = "ingreso"
                    saldo = 0
                    ret,saldo = usuarios.increaseBalance(cuentaDestino,monto,nombreUsuario)
                    if ret:
                        print(f"\nEl dinero ha sido depositado en su cuenta vinculada. Su nuevo saldo es {saldo}")
                        preguntar = False
                        ret = registerTransaction(nombreUsuario, tipoTransaccion, monto, cuentaDestino)
                    else:
                        print("No se pudo encontrar la cuenta, intente nuevamente.")
                else:
                    preguntar = False
            else:
                preguntar = False

    return ret


def calculateIncome(corte, total=0.0):
    if not corte:
        return total

    transaccion = corte[0][1]
    monto = transaccion["monto"]

    total += monto

    return calculateIncome(corte[1:], total)


def printIncome(listaIngresos):
    if listaIngresos:
        transaccion = listaIngresos[0][1]
        nombreUsuario = transaccion["nombre_usuario"]
        tipoTransaccion = transaccion["tipo_transaccion"]
        fecha = transaccion["fecha"]
        monto = transaccion["monto"]

        print(f"Nombre de usuario: {nombreUsuario}")
        print(f"Tipo de transacción: {tipoTransaccion}")
        print(f"Fecha: {'/'.join(map(str, fecha[:3]))}")
        print(f"Monto: {monto} ")
        print()

        printIncome(listaIngresos[1:])


def showIncomeByMonth(nombreUsuario, transacciones):
    error = True
    while error:
        try:
            mes = int(input("Indique qué mes desea consultar (1-12): "))
            error = False
        except Exception:
            print("El dato ingresado no es válido, intente nuevamente")

    corte = list(filter(lambda valor : valor[1]["nombre_usuario"] == nombreUsuario and valor[1]["tipo_transaccion"] == "ingreso" and valor[1]["fecha"][1] == mes, transacciones.items()))

    if not corte:
        print("No se encontraron ingresos en este mes")
    else:
        total_ingresos = calculateIncome(corte)
        print(f"El total de ingresos del mes fueron {total_ingresos} pesos")
        print()
        printIncome(corte)