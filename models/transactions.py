
import datetime

#Uso de tuplas en el TPO

totalTransacciones = 231

transacciones = {
    (1, (2024, 8, 20)): {
        "nombre_usuario": "Dani333_",
        "tipo_transaccion": "ingreso",
        "monto": 10853,
    },
    (2, (2024, 8, 24)): {
        "nombre_usuario": "Dani333_",
        "tipo_transaccion": "envio",
        "monto": 4000,
    },
    (3, (2024, 8, 30)): {
        "nombre_usuario": "Dani333_",
        "tipo_transaccion": "ingreso",
        "monto": 10853,
    },
    (4, (2024, 9, 7)): {
        "nombre_usuario": "Carlos12",
        "tipo_transaccion": "envio",
        "monto": 4000,
    },
    (5, (2024, 9, 10)): {
        "nombre_usuario": "Dani333_",
        "tipo_transaccion": "ingreso",
        "monto": 10853,
    },
    (6, (2024, 9, 11)): {
        "nombre_usuario": "Jose_29",
        "tipo_transaccion": "envio",
        "monto": 4000,
    },
    (7, (2024, 9, 14)): {
        "nombre_usuario": "Dani333_",
        "tipo_transaccion": "ingreso",
        "monto": 10853,
    },
    (8, (2024, 9, 15)): {
        "nombre_usuario": "Dani333_",
        "tipo_transaccion": "envio",
        "monto": 4000,
    }
}


#En esta función debo agregar el destinatario si el alias del receptor está en nuestra base.
#Revisar cómo está pensado en el main

def registrarFecha():
    hoy = datetime.datetime.now()
    fechaActual = (hoy.year, hoy.month, hoy.day)

    return fechaActual


def registrarTransaccion(nombreUsuario, tipoTransaccion, monto, fecha, totalTransacciones):
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


def mostrarMenu():
    
    print("===================")
    print("1. Ingresar dinero")
    print("2. Enviar dinero")
    print("3. Pagar servicio")
    print("4. Ver movimientos")
    print("5. Salir")
    print("===================")

    return [1,2,3]


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
mostrarMenu()