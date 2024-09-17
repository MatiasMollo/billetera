
import datetime

#Uso de tuplas en el TPO

totalTransacciones = 231

users = {
    'Matiass07_34': {
    "nombre" : "Matias",
    "apellido" : "Mollo",
    "password" : "12345",
    "historial_crediticio" : 10,
    "dinero" : 100,
}
}

transacciones = {
    (1, (2024, 8, 20)): {
        "nombre_usuario": "Dani333_",
        "tipo_transaccion": "ingreso",
        "monto": 10853.00,
        "tarjeta origen": "1234 9855 8866 1022",
    },
    (2, (2024, 8, 24)): {
        "nombre_usuario": "Dani333_",
        "tipo_transaccion": "envioExterno",
        "monto": 4000.00,
        "CVU_destino": "1344",
    },
    (3, (2024, 8, 30)): {
        "nombre_usuario": "Dani333_",
        "tipo_transaccion": "ingreso",
        "monto": 10853.00,
    },
    (4, (2024, 9, 7)): {
        "nombre_usuario": "Carlos12",
        "tipo_transaccion": "pagoServicio",
        "monto": 4000.00,
        "servicio": "Edenor",
        "numero_factura": "455666",
    },
    (5, (2024, 9, 10)): {
        "nombre_usuario": "Dani333_",
        "tipo_transaccion": "ingreso",
        "monto": 10853.00,
    },
    (6, (2024, 9, 11)): {
        "nombre_usuario": "Jose_29",
        "tipo_transaccion": "envioInterno",
        "monto": 4000.00,
        "CVU_destino": "1344",
    },
    (7, (2024, 9, 14)): {
        "nombre_usuario": "Dani333_",
        "tipo_transaccion": "ingreso",
        "monto": 10853.00,
    },
    (8, (2024, 9, 15)): {
        "nombre_usuario": "Dani333_",
        "tipo_transaccion": "envioInterno",
        "monto": 4000.00,
        "CVU_destino": "1344",
    }
}


#En esta función debo agregar el destinatario si el alias del receptor está en nuestra base.
#Revisar cómo está pensado en el main

def registrarFecha():
    hoy = datetime.datetime.now()
    fechaActual = (hoy.year, hoy.month, hoy.day)

    return fechaActual


def sendMoney(nombreUsuario):
    print("===================")
    print("1. Enviar a una cuenta de Bankando")
    print("2. Enviar a una cuenta de otro banco")
    print("===================")
    opcion = int(input())
    while opcion != 1 and opcion != 2:
        print("Por favor, elija una opción válida (1 ó 2)")
        opcion = int(input())
    if opcion == 1:
        tipoTransaccion = "envioInterno"
    else:
        tipoTransaccion = "envioExterno"
    cuentaDestino = input("Ingrese el CBU o CVU de la cuenta destino")
    monto = float(input("Ingrese el monto que desea enviar: "))
    while not checkBalance:
        print("No hay dinero suficiente en su cuenta")
        monto = float(input("Ingrese el monto que desea enviar: "))
    saldo = reduceBalance()
    if tipoTransaccion == 2:
        if #usuario no está (mensaje)
        else:
            increaseBalance(CVU)

    return cuentaDestino, monto, saldo


def checkBalance(monto, nombreUsuario):
    for usuario, valores in users.items(): 
        if usuario == nombreUsuario:
            saldo = valores["monto"]
    if saldo >= monto:
        return True
    return False


def reduceBalance(monto, nombreUsuario):
    for usuario, valores in users.items(): 
        if usuario == nombreUsuario:
            saldo = valores["monto"]
            saldo = saldo - monto
            valores["monto"] = saldo    


def increaseBalance():
    for usuario, valores in users.items(): 
        if usuario == nombreUsuario:
            saldo = valores["monto"]
            saldo = saldo + monto
            valores["monto"] = saldo


def registrarTransaccion(nombreUsuario, tipoTransaccion, monto, fecha, totalTransacciones):
    #Se podrían hacer todas las preguntas dentro de esta función o afuera y luego se registran acá

    nuevaTransaccion = {}
    nuevaTransaccion["nombre_usuario"] = nombreUsuario
    nuevaTransaccion["tipo_transaccion"] = tipoTransaccion
    nuevaTransaccion["monto"] = monto


    # if tipoTransaccion == "ingreso":
    #     pass
    # elif tipoTransaccion == "envioInterno":
    #     pass
    # elif tipoTransaccion == "envioExterno":
    #     pass
    # elif tipoTransaccion == "pagoServicio":
    #     pass


    totalTransacciones += 1
    tuplaTransaccion = (totalTransacciones, fecha) #asumiendo que fecha ya viene como tupla

    transacciones[tuplaTransaccion] = nuevaTransaccion

    return totalTransacciones




#Crear funciones para balances de cuenta


#En el main habría una opción para elegir esta función
#Falta usar también el nombre de usuario en la lógica

def mostrarTransaccionesPorFecha(nombreUsuario, transacciones):
    #Estas fechas se preguntan acá y se valida el formato. Para esta prueba están asignadas
    fechaInicial = (2024, 8, 15)
    fechaFinal = (2024, 9, 15)
    #Este dato también se pregunta acá. Para esta prueba está asignado
    tipoTransaccion = "envio"
    numero = 8
    totalUsuario = calcularTotalTransaccionesUsuario(nombreUsuario, transacciones)
    if numero > totalUsuario:
        numero = totalUsuario
    
    corte = [(clave[1], valor) for clave, valor in transacciones.items() if clave[1] >= fechaInicial and clave[1] <= fechaFinal and valor["tipo_transaccion"] == tipoTransaccion]
    corteOrdenado = sorted(corte, key= lambda x: x[0])
    if numero >= len(corteOrdenado):
        print(corteOrdenado)
    else:
        print(corteOrdenado[len(corteOrdenado) - numero:])


def mostrarTransaccionesPorOrden(nombreUsuario, transacciones):
    #Estas fechas se preguntan acá y se valida el formato. Para esta prueba están asignadas
    fechaInicial = (2024, 8, 15)
    fechaFinal = (2024, 9, 15)
    #Este dato también se pregunta acá. Para esta prueba está asignado
    tipoTransaccion = "envio"
    numero = 10
    totalUsuario = calcularTotalTransaccionesUsuario(nombreUsuario, transacciones)
    if numero > totalUsuario:
        numero = totalUsuario
    
    corte = [(clave[0], valor) for clave, valor in transacciones.items() if valor["nombre_usuario"] == nombreUsuario]
    corteOrdenado = sorted(corte, key= lambda x: x[0])
    if numero >= len(corteOrdenado):
        print(corteOrdenado)
    else:
        print(corteOrdenado[len(corteOrdenado) - numero:])


def mostrarTransaccionesPorTipo(nombreUsuario, transacciones):
    #Estas fechas se preguntan acá y se valida el formato. Para esta prueba están asignadas
    fechaInicial = (2024, 8, 15)
    fechaFinal = (2024, 9, 15)
    #Este dato también se pregunta acá. Para esta prueba está asignado
    tipoTransaccion = "envio"
    numero = 3
    totalUsuario = calcularTotalTransaccionesUsuario(nombreUsuario, transacciones)
    if numero > totalUsuario:
        numero = totalUsuario
    
    corte = [(clave[0], valor) for clave, valor in transacciones.items() if valor["tipo_transaccion"] == tipoTransaccion]
    corteOrdenado = sorted(corte, key= lambda x: x[0])
    if numero >= len(corteOrdenado):
        print(corteOrdenado)
    else:
        print(corteOrdenado[len(corteOrdenado) - numero:])


def calcularTotalTransaccionesUsuario(nombreUsuario, transacciones):
    corte = [(clave[0], valor) for clave, valor in transacciones.items() if valor["nombre_usuario"] == nombreUsuario]
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


print("Seleccione la operación a ejecutar:")
validOptions = showMenu()
opcion = int(input("Opción: "))

#Verificación de opción válida
while opcion not in validOptions:
    print("La opción no es válida, intente nuevamente: ")
    opcion = input("Opción: ")