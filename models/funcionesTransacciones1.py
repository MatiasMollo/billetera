
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
def mostrarTransaccionesPorFecha(nombreUsuario, transacciones):
    #Estas fechas se preguntan acá y se valida el formato. Para esta prueba están asignadas
    fechaInicial = (2024, 8, 15)
    fechaFinal = (2024, 9, 15)
    #Este dato también se pregunta acá. Para esta prueba está asignado
    tipoTransaccion = "envio"
    numero = 3
    
    corte = [(clave[1], valor) for clave, valor in transacciones.items() if clave[1] >= fechaInicial and clave[1] <= fechaFinal and valor["tipo_transaccion"] == tipoTransaccion]
    corteOrdenado = sorted(corte, key= lambda x: x[0])
    print(corteOrdenado[(numero * -1):])


#Programa principal
nombreUsuario = "Dani333_"
tipoTransaccion = "pago"
monto = 1456
fecha = tuple([2024, 9, 15])

numeroTransaccion = registrarTransaccion(nombreUsuario, tipoTransaccion, monto, fecha, totalTransacciones)
totalTransacciones += 1

# print(transacciones)
# print()
# print(transacciones[numeroTransaccion, fecha])
# print(totalTransacciones)