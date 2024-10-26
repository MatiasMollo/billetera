import models.users as user
import models.transactions as transaction
import models.debitCards as card
import logsController.errorHandler as errorsController

MENU = {
    "Ingresar dinero" : transaction.depositMoney,
    "Enviar dinero": transaction.sendMoney,
    "Ver movimientos" : transaction.showReports,
    "Solicitar tarjeta de débito" : card.createDebitCard,
    "Consultar mi tarjeta" : card.consultCard,
    "Pagar servicios" : transaction.payUtilities,
    "Solicitar préstamo" : transaction.requestLoan,
    "Consultar mi CVU": user.consultCVU,
    "Consultar mi saldo": user.consultBalance,
    "Cerrar sesión" : []
}

salir = len(MENU)

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

    return ["1","2","3"]

def printMenu():
    """
        Muestra las opciones del menú
    """
    index = 0
    print("\n===================")
    for option in MENU.keys():
        index += 1
        print(f"{index}. {option}")
    print("===================")

    return range(1,len(MENU)+1)

#Programa principal

option = 0

while option != str(salir):
    print("Bienvenido a su billetera virtual, seleccione una opción del menú")
    validOptions = printLogin()
    salir = len(validOptions) # Sobreescribimos "salir"
    option = input("Opción: ")

    #Verificación de opción válida
    while option not in validOptions:
        print("La opción no es válida, intente nuevamente: ")
        option = input("Opción: ")

    logged = False
    retry = True
    if option == "1": #Inicio de sesión
        while not logged and retry:
            username = input("Ingrese su nombre de usuario: ")
            password = input("Ingrese su contraseña: ")

            if user.login(username,password):
                logged = username # Bandera de estado para saber si el usuario tiene sesión iniciada
                print(f"\nLogin con usuario {username} satisfactorio")
            else:
                print("\nLas credenciales no coinciden con nuestros registros.")
                retry = True if input("¿Desea intentarlo nuevamente? S / N: ") in ["S",'s'] else False

    elif option == "2": #Registro de usuario
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
        error = True
        while error:
            try:
                option = input("Ingrese su opción: ")
                error = False
            except:
                print("La opción no es válida")

        users = user.getUser()
        salir = len(MENU)
        
        while option != str(salir):
            try:
                option = int(option)
                if option in range(1,len(MENU)):
                    #Hace el llamado a la función correspondiente y pasa el usuario autenticado junto con la lista completa de usuarios
                    MENU[list(MENU.keys())[option-1]](logged)
                    printMenu()
                else:
                    print("La opción no es válida")
            except Exception as e:
                errorsController.logError(type(e).__name__, str(e))
                print("\n------------------------------------------")
                print("Ha ocurrido un error, vuelva a intentarlo.")
                print("------------------------------------------")
                printMenu()
            finally:
                option = input("\nIngrese su opción: ")
                print()

        # Sobreescribimos la variable "salir" para que pregunte el inicio de sesión nuevamente
        salir = len(validOptions) 

        #Cerramos la sesión
        logged = False
    else:
        print("¡Hasta luego!")
            