import json
import re

USER_PATH = 'data/users.json'
VALID_FIELDS = ['nombre','apellido','historial_crediticio','dinero','password']

def getUser(username = None):
    """
    Obtiene el usuario que recibe como parámetro, en caso de que este sea None, devuelve todos los usuarios del archivo JSON

    Parámetros:
        username (None | String): Nombre de usuario
    """
    file = open(USER_PATH,'r')
    data = json.loads(file.read())
        
    if username != None and username in data: 
        user = data[username]
    elif username == None:
        user = data
    else:
        user = False

    file.close()
    return user


def validUsername(username):
    """
        Verifica que el nombre de usuario siga un patron especifico y sea único en el archivo JSON
        Parámetros:
        userName (String): Nombre de usuario
        
    """
    file = open(USER_PATH,'r')
    users = json.loads(file.read())
    file.close()

    pattern = r'^[A-Za-z0-9_-]+$'
    return re.match(pattern,username) and username not in users

def validStruct(user):
    """
        Valida que la estructura del usuario sea válida y no haya valores vacíos
    """
    struct = set(VALID_FIELDS).issubset(set(user))
    values = [element for element in dict(user).values() if element != ""]
    return struct and len(values) == len(user)

def createUser(username,userData):
    """
        Crea un nuevo usuario y lo guarda en el JSON

        Parámetros:

        username (String): Nombre de usuario único
        
        userData (Dict): Estructura del usuario
    """
    ret = False
    message = "El nombre de usuario ya existe o es inválido."

    file = open(USER_PATH,'r')
    data = json.loads(file.read())

    struct = validStruct(userData)
    if not struct:
        message = "La estructura de usuario no es válida"

    if validUsername(username) and struct:
        data[username] = userData
        message = "Se creó el usuario correctamente"
        file = open(USER_PATH,'w')
        json.dump(data,file)
        file.close()
        ret = True

    return ret,message

def login(username,password):
    """
        Define si la contraseña del usuario es válida

        Parámetros:
            username (String)
            password (String)
    """
    ret = False
    
    file = open(USER_PATH,'r')
    data = json.loads(file.read())
    file.close()

    if username in data:
        if 'password' in data[username] and data[username]['password'] == password:
            ret = True

    return ret


def verificarDNIunico(dni, users):
    for user in users.values():
        if user["dni"] == dni:
            return True
    return False
