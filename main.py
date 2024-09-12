import models.users as user
import models.transactions as transaction

def imprimirLogin():
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

print("Bienvenido a su billetera virtual, seleccione una opción del menú")
validOptions = imprimirLogin()
opcion = int(input("Opción: "))

while opcion not in validOptions:
    print("La opción no es válida, intente nuevamente: ")
    opcion = input("Opción: ")


logged = False
retry = True

if opcion == 1:
    while not logged and retry:
        username = input("Ingrese su nombre de usuario: ")
        password = input("Ingrese su contraseña: ")

        if user.login(username,password):
            logged = True
            print(f"\nLogin con usuario {username} satisfactorio")
        else:
            print("\nLas credenciales no coinciden con nuestros registros.")
            retry = True if input("¿Desea intentarlo nuevamente? Si (1) o 2 (No): ") == "1" else False

        

