import models.users as users
import json

#Constants
USER_PATH = 'mockDataTests/mockUsers.json'
users.USER_PATH = USER_PATH #guardado de Path para modelo usuarios

#Functions
def generateValidUsername(users_db):
    original_username = username = "username"
    counter = 0

    while username in users_db:
        username = original_username + str(counter)
        counter += 1

    return username

#Tests
def test_getUsers():
    """
        Verifica que los usuarios puedan obtenerse desde el json
    """
    file = open(USER_PATH)
    data = json.loads(file.read())
    file.close()

    assert data == users.getUser(), "Los usuarios no pudieron obtenerse"


def test_createUser():
    """
        Verifica que los usuarios puedan crearse
    """
    name = "name"
    surname = "surname"
    users_db = users.getUser()

    username = generateValidUsername(users_db)
    
    #Estructura válida
    userData = {
        "nombre" : name,
        "apellido": surname,
        "username": username,
        "password": "123456",
        "historial_crediticio": 0,
        "dinero": 0
    }

    users.createUser(username,userData) #Guardado de usuarios
    newUsers = users.getUser() #Obtención se nuevo listado de usuarios

    assert (username in newUsers) == True, "El usuario no pudo ser creado"


def test_failUserCreation():
    """
        Verifica que no se puedan crear usuarios con la estructura incorrecta
    """
    name = "name"
    surname = "surname"
    field_counter = 0

    users_db = users.getUser()
    username = generateValidUsername(users_db)

    #Estructura válida
    userData = {
        "nombre" : name,
        "apellido": surname,
        "username": username,
        "password": "123456",
        "historial_crediticio": 0,
        "dinero": 0
    }

    keys = list(userData.keys())

    for key in keys:
        temp_data = {} #Datos temporales
        
        #Se elimina un campo de la estructura para hacerlo inválido
        if key != keys[field_counter]: 
            temp_data[key] = userData[key]

        ret,message = users.createUser(username,temp_data)
        field_counter += 1
        
        assert ret == False, "Se generó un usuario con una estructura inválida"


def test_getOneUser():
    """
        Verifica la búsqueda de un usuario específico
    """
    file = open(USER_PATH)
    data = json.loads(file.read())
    username = list(data)[0]
    
    assert data[username] == users.getUser(username), "No se puede encontrar un usuario específico"


def test_validUsername():
    """
        Verifica el correcto funcionamiento de la validación para nombre de usuario
    """
    users_db = users.getUser()
    username = generateValidUsername(users_db)

    valid = users.validUsername(username)

    assert valid == True, "La verificación de nombre de usuario falló"


def test_invalidUsername():
    """
        Verifica que no se puedan crear nombres de usuario inválidos
    """
    username = "test username"
    valid = users.validUsername(username)

    assert valid != True, "Se ha generado un nombre de usuario inválido"


def test_successLogin():
    """
        Verifica el correcto funcionamiento del login
    """
    users_db = users.getUser()
    username = list(users_db)[0]
    user = users_db[username]

    #Se obtiene la contraseña del usuario
    login = users.login(username,user['password'])

    assert login == True, "No se pudo autenticar el usuario o no hay usuarios en la DB"


def test_failedLogin():
    """
        Verifica el correcto funcionamiento del login (el mismo debe ser fallido)
    """
    users_db = users.getUser()
    username = list(users_db)[0]
    user = users_db[username]

    #Se altera la contraseña para que no se deba iniciar sesión
    login = users.login(username,(user['password'] + str("0")))

    assert login == False, "Un usuario con contraseña inválida fue autenticado"


def test_increaseBalance():
    """
        Verifica el funcionamiento de incremento de balance por nombre de usuario y cvu
    """
    users_db = users.getUser()
    username = list(users_db)[0]
    cvu = users_db[username]['CVU']
    amount = 100

    #Incremento por nombre de usuario
    current_money = users_db[username]['dinero']
    users.increaseBalance(cvu,amount,username)

    updated_data = users.getUser()
    user = updated_data[username]
    assert user['dinero'] == (current_money + amount), "Fallo la operación de ingreso de dinero por username"

    #Incremento de dinero por CVU (sin nombre de usuario)
    current_money = user['dinero']
    users.increaseBalance(cvu,amount)

    updated_data = users.getUser()
    user = updated_data[username]
    assert user['dinero'] == (current_money + amount), "Falló la operación de ingreso de dinero por CVU"


def test_decreaseBalance():
    users_db = users.getUser()
    username = list(users_db)[0]
    current_money = users_db[username]['dinero']
    amount = 100

    status,saldo = users.decreaseBalance(amount,username)

    assert status == True, "El usuario no fue encontrado en la DB"
    assert saldo == (current_money - amount), "El decremento del balance es incorrecto"


def test_generateCVU():
    """
        Verifica que el CVU generado sea válido y único entre los usuarios
    """

    users_db = users.getUser()
    new_cvu = users.generateCVU()

    assert len(new_cvu) == 11, "El CVU generado no cumple con la longitud correcta"

    for user in users_db.values():
        assert user['CVU'] != new_cvu, "Se ha generado un CVU repetido"




