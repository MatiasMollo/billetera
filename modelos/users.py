import json
import re

USER_PATH = 'data/users.json'

def getUser(username = None):
    """
    Obtiene el usuario que recibe como parámetro, en caso de que este sea None, devuelve todos los usuarios del archivo JSON

    Parámetros:
    
    username (None | String): Nombre de usuario
    """
    with open(USER_PATH,'r') as file:
        data = json.load(file)
        
    if username != None and username in data: 
        user = data[username]
    elif username == None:
        user = data
    else:
        user = False
    file.close()
    return user


def validUserName(userName):
    """
        Verifica que el nombre de usuario siga un patron especifico
        Parámetros:
        userName (String): Nombre de usuario
        
    """
    pattern = r'^[A-Za-z0-9]+$'
    
    if re.match(pattern, userName):
        return True 
    else:
        return False 


def createUser(username,userData):
    """
        Crea un nuevo usuario y lo guarda en el JSON

        Parámetros:

        username (String): Nombre de usuario único
        
        userData (Dict): Estructura del usuario
    """
    ret = False
    #! Verificar que no se repita el nombre de usuario
    #! Filtrar datos de nombre de usuario
    #! Falta validar la estructura del usuario

    with open(USER_PATH,'r') as file:
        data = json.load(file)

    if username not in data:
        data[username] = userData
        with open(USER_PATH,'w') as file:
            json.dump(data,file)
            ret = True

    file.close()
    return ret


print(createUser('Matiass06',{
    "nombre" : "Matias"
}))
