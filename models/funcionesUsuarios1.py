
users = {
    "Matiass07_34": {
        "nombre" : "Matias",
        "apellido" : "Mollo",
        "dni" : "4444444",
        "password" : "12345",
        "historial_crediticio" : 10,
        "dinero" : 100,
    },
    "Car_los_08_44": {
        "nombre" : "Carlos",
        "apellido" : "Avilan",
        "dni" : "5555",
        "password" : "9876",
        "historial_crediticio" : 5,
        "dinero" : 80,
    }
}


#Crear funcion para crear un alias al azar o modificar el alias

def verificarNombreUsuario(nombreUsuario, users):
    return nombreUsuario in users


def verificarDNIunico(dni, users):
    for user in users.values():
        if user["dni"] == dni:
            return True
    return False


def registrarUsuario():
    nombreUsuario = input("Ingrese un nombre de usuario único (caracteres y/o longitud requeridos): ")
    #Acá debemos verificar primero si el nombre cumple con el formato, usando un while también
    while verificarNombreUsuario(nombreUsuario, users):
        print("El nombre de usuario ya está tomado")
        nombreUsuario = input("Por favor, ingrese otro nombre de usuario (caracteres requeridos): ")
    password = input("Ingrese una clave (caracteres y/o longitud requeridos): ")
    #Acá debemos verificar si la clave cumple con el formato, usando un while también
    print("Ahora finalizaremos su registro en Bankando. Por favor complete los siguientes datos que le solicitaremos")
    nuevoUsuario = {}
    nuevoUsuario["nombre"] = input("Ingrese su nombre(s): ")
    nuevoUsuario["apellido"] = input("Ingrese su apellido(s): ")
    dni = input("Ingrese su número de documento (DNI) sin puntos ni espacios: ")
    #Acá verificaremos y manejaremos excepciones si no cumple con el formato
    while verificarDNIunico(dni, users):
        print("El número de DNI ya fue registrado en nuestro sistema")
        dni = input("Por favor, ingrese el número de DNI correcto: ")
    nuevoUsuario["dni"] = dni
    nuevoUsuario["password"] = password
    nuevoUsuario["historial_crediticio"] = 0
    nuevoUsuario["dinero"] = 0
    users[nombreUsuario] = nuevoUsuario
    print("Muchas gracias y bienvenido a Bankando")

    return nombreUsuario, password


#Programa principal
#Al entrar al programa hay dos opciones: login o registrarse como nuevo usuario. Si la persona elige registrarse, hay que hacer lo siguiente:

nombreUsuario, password = registrarUsuario()

#pruebas
print(users[nombreUsuario])
print()
print("Acá está el listado de usuarios")
print(users)