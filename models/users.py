import json
import re
import random

USER_PATH = 'data/users.json'
VALID_FIELDS = ['Nombre','Apellido','Historial crediticio','Saldo','Password','CVU']

def getUser(username = None):
    """
    Obtiene el usuario que recibe como parámetro, en caso de que este sea None, devuelve todos los usuarios del archivo JSON

    Parámetros:
        username (None | String): Nombre de usuario
    """
    file = open(USER_PATH,'r', encoding='utf-8')
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
    file = open(USER_PATH,'r', encoding='utf-8')
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

    data = getUser()
    userData['CVU'] = generateCVU()

    struct = validStruct(userData)
    if not struct:
        message = "La estructura de usuario no es válida"

    if validUsername(username) and struct:
        data[username] = userData
        message = "Se creó el usuario correctamente"
        file = open(USER_PATH,'w', encoding='utf-8')
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
    
    file = open(USER_PATH,'r', encoding='utf-8')
    data = json.loads(file.read())
    file.close()

    if username in data:
        if 'Password' in data[username] and data[username]['Password'] == password:
            ret = True

    return ret

def increaseBalance(CVU,money,username = None):
    """
        Incrementa el saldo del usuario
    """
    users = getUser()
    keys = list(users.keys())
    values = list(users.values())


    index = 0
    user_found = False
    saldo = 0

    if username and username in users:
        # Método rápido, sin necesidad de recorrer todos los usuarios
        users[username].update({"Saldo" : users[username]['Saldo'] + money})
        saldo = users[username]['Saldo']
        user_found = True
    else:
        #Método largo (cuando no tenemos nombre de usuario).s
        while index < len(users) and not user_found:

            if values[index]["CVU"] == CVU:
                user_found = True

                #Actualización de dinero en cuenta
                users[keys[index]].update({"Saldo" : users[keys[index]]["Saldo"] + money})

                #Variable que retorna informando el nuevo saldo
                saldo = users[keys[index]]["Saldo"]

            index += 1

    if user_found:
        file = open(USER_PATH,'w', encoding='utf-8')
        json.dump(users,file)
        file.close()
    
    return user_found,saldo

def decreaseBalance(money,username):
    """
        Disminuye el saldo del usuario
    """
    users = getUser()
    user_found = False
    saldo = 0

    if username in users:
        user_found = True
        saldo = float(users[username]['Saldo'] - money)
        users[username].update({"Saldo": saldo})

        file = open(USER_PATH,'w', encoding='utf-8')
        json.dump(users,file)
        file.close()
    
    return user_found, saldo


def getBalance(username):
    saldo = 0

    users = getUser()

    if username in users:
        saldo = users[username]["Saldo"]

    return saldo

#! Esta función no se está utilizando (pero debería)
def verificarDNIunico(dni, users):
    for user in users.values():
        if user["DNI"] == dni:
            return True
    return False

def generateCVU():
    """
        Genera un CVU único entre los usuarios
    """
    unique = False
    users = getUser()

    while not unique:
        index = 0
        unique = True
        cvu = "".join([str(random.randint(0,9)) for _ in range(11)])

        while index < len(users.values()):
            if list(users.values())[index]['CVU'] == cvu:
                unique = False
            index += 1

    return cvu

def getCVU(username):
    """
        Retorna el CVU del usuario
    """
    users = getUser()
    return users[username]["CVU"]


def consultCVU(username,users):
    """
        Función con mensaje personalizado para ser llamada desde el menú
    """
    print(f"Su CVU es: {getCVU(username)}")

def consultBalance(username,users):
    """
        Función con mensaje personalizado para ser llamada desde el menú
    """
    print(f"Su saldo es de ${getBalance(username)}")