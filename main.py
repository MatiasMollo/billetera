import models.users as user
import models.transactions as transaction

MENU = {
    "1. Ingresar dinero" : "transaction.ingresarDinero",
    "2. Enviar dinero": "transaction.sendMoney",
    "3. Pagar servicio": "transaction.pagarServicio",
    "4. Ver movimientos" : "transaction.verMovimientos",
    "5. Pedir tarjeta" : "transaction.pedirTarjeta",
    "6. Salir" : []
}

def printLogin():
    """
        Muestra las opciones de inicio de sesión

        Return: 
            (Array) Opciones válidas
    """

    print("===================")
    print("1. Iniciar sesión")
    print("2. Registrarme")
    print("3. Salir")
    print("===================")

    return [1,2,3]

def printMenu():
    """
        Muestra las opciones del menú
    """

    print("\n===================")
    for option in MENU.keys():
        print(option)
    print("===================")

    return range(1,len(MENU)+1)

print("Bienvenido a su billetera virtual, seleccione una opción del menú")
validOptions = printLogin()
opcion = int(input("Opción: "))

#Verificación de opción válida
while opcion not in validOptions:
    print("La opción no es válida, intente nuevamente: ")
    opcion = input("Opción: ")


logged = False
retry = True

#Inicio de sesión
if opcion == 1:
    while not logged and retry:
        username = input("Ingrese su nombre de usuario: ")
        password = input("Ingrese su contraseña: ")

        if user.login(username,password):
            logged = username # Bandera de estado para saber si el usuario tiene sesión iniciada
            print(f"\nLogin con usuario {username} satisfactorio")
        else:
            print("\nLas credenciales no coinciden con nuestros registros.")
            retry = True if input("¿Desea intentarlo nuevamente? S / N: ") in ["S",'s'] else False

elif opcion == 2: #Registro de usuario
    
    while retry:
        username = input("Ingrese su nombre de usuario: ")
        name = input("Ingrese su nombre: ")
        lastname = input("Ingrese su apellido: ")
        password = input("Ingrese su contraseña: ")

        (create, message) = user.createUser(username,{
            "nombre" : name,
            "apellido" : lastname,
            "password" : password,
            "historial_crediticio" : 0,
            "dinero" : 0
        })

        #mensaje de estado
        print(f"\n{message}")

        if create:
            logged = username # Iniciamos la sesión del usuario
            retry = False
        else:
            retry = True if input("\n¿Desea intentarlo nuevamente? S/N: ") in ['S','s'] else False

if logged:
    printMenu()
    salir = 6
    option = int(input("Ingrese su opción: "))
    
    while option != salir:
        print(MENU[list(MENU.keys())[option-1]])#()
        option = int(input("Ingrese su opción: "))

else:
    print("Se ha finalizado el programa")
        