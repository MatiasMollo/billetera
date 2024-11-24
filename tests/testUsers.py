import models.users as users
import json

USER_PATH = 'mockDataTests/mockUsers.json'
users.USER_PATH = USER_PATH #guardado de Path para modelo usuarios

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
    username = "username"
    original_username = username
    counter = 0

    users_db = users.getUser()

    while username in users_db:
        username = original_username + str(counter)
        counter += 1
    
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
    username = "username"
    original_username = username
    counter = 0
    field_counter = 0

    users_db = users.getUser()

    while username in users_db:
        username = original_username + str(counter)
        counter += 1

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




