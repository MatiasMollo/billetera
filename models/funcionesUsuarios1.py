import datetime

totalTransacciones = 231

users = {
    'Matiass07_34': {
        "nombre" : "Matias",
        "apellido" : "Mollo",
        "DNI": "12345561",
        "password" : "12345",
        "CVU": "45567867773",
        "historial_crediticio" : 10,
        "dinero" : 50560.45,
    },
    'Dani333_': {
        "nombre" : "Daniel",
        "apellido" : "González",
        "DNI": "17464644",
        "password" : "12345",
        "CVU": "44561291222",
        "historial_crediticio" : 10,
        "dinero" : 10180.00,
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

def checkBalance(monto, nombreUsuario, users):
    if nombreUsuario in users:
        saldo = users[nombreUsuario]["dinero"]
    if saldo >= monto:
        return True
    return False


def checkCVU(cuentaDestino, users):
    for clave, valor in users.items():
        if valor["CVU"] == cuentaDestino:
            return True
    return False


def decreaseBalance(monto, nombreUsuario, users):
    if nombreUsuario in users:
        saldo = users[nombreUsuario]["dinero"]
        saldo = saldo - monto
        users[nombreUsuario]["dinero"] = saldo

    return saldo


def increaseBalance(CVU, monto, users):
    for clave, valor in users.items():
        if valor["CVU"] == CVU:
            saldo = valor["dinero"]
            saldo = saldo + monto
            valor["dinero"] = saldo

    return saldo


def checkFormat(cuentaDestino):
    if len(cuentaDestino) == 11:
        return True
    return False


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
        increaseBalance(cuentaDestino, monto, users)
    saldo = decreaseBalance(monto, nombreUsuario, users)
    print(f"Su dinero ha sido enviado. Su nuevo saldo es {saldo}")

    return cuentaDestino, monto, saldo, tipoTransaccion


nombreUsuario = "Dani333_"
# monto = 2500.16
# cuentaDestino = "445611222"
cuentaDestino, monto, saldo, tipoTransaccion = sendMoney(nombreUsuario, users)
print(users)
print(cuentaDestino)
print(monto)
print(saldo)
print(tipoTransaccion)
print(users)











# users = {
#     "Matiass07_34": {
#         "nombre" : "Matias",
#         "apellido" : "Mollo",
#         "dni" : "4444444",
#         "password" : "12345",
#         "historial_crediticio" : 10,
#         "dinero" : 100,
#     },
#     "Car_los_08_44": {
#         "nombre" : "Carlos",
#         "apellido" : "Avilan",
#         "dni" : "5555",
#         "password" : "9876",
#         "historial_crediticio" : 5,
#         "dinero" : 80,
#     }
# }


# #Crear funcion para crear un alias al azar o modificar el alias

# def verificarNombreUsuario(nombreUsuario, users):
#     return nombreUsuario in users


# def verificarDNIunico(dni, users):
#     for user in users.values():
#         if user["dni"] == dni:
#             return True
#     return False


# def registrarUsuario():
#     nombreUsuario = input("Ingrese un nombre de usuario único (caracteres y/o longitud requeridos): ")
#     #Acá debemos verificar primero si el nombre cumple con el formato, usando un while también
#     while verificarNombreUsuario(nombreUsuario, users):
#         print("El nombre de usuario ya está tomado")
#         nombreUsuario = input("Por favor, ingrese otro nombre de usuario (caracteres requeridos): ")
#     password = input("Ingrese una clave (caracteres y/o longitud requeridos): ")
#     #Acá debemos verificar si la clave cumple con el formato, usando un while también
#     print("Ahora finalizaremos su registro en Bankando. Por favor complete los siguientes datos que le solicitaremos")
#     nuevoUsuario = {}
#     nuevoUsuario["nombre"] = input("Ingrese su nombre(s): ")
#     nuevoUsuario["apellido"] = input("Ingrese su apellido(s): ")
#     dni = input("Ingrese su número de documento (DNI) sin puntos ni espacios: ")
#     #Acá verificaremos y manejaremos excepciones si no cumple con el formato
#     while verificarDNIunico(dni, users):
#         print("El número de DNI ya fue registrado en nuestro sistema")
#         dni = input("Por favor, ingrese el número de DNI correcto: ")
#     nuevoUsuario["dni"] = dni
#     nuevoUsuario["password"] = password
#     nuevoUsuario["historial_crediticio"] = 0
#     nuevoUsuario["dinero"] = 0
#     users[nombreUsuario] = nuevoUsuario
#     print("Muchas gracias y bienvenido a Bankando")

#     return nombreUsuario, password


# #Programa principal
# #Al entrar al programa hay dos opciones: login o registrarse como nuevo usuario. Si la persona elige registrarse, hay que hacer lo siguiente:

# nombreUsuario, password = registrarUsuario()

# #pruebas
# print(users[nombreUsuario])
# print()
# print("Acá está el listado de usuarios")
# print(users)