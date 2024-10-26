from datetime import datetime
import re

def logError(error_type: str, error_message: str):
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    file = open('./logsController/logsErrors.txt', 'a')

    file.write(f"[{current_time}] {error_type}: {error_message}\n")

    file.close()

def getAllErrors():
    file = open('./logsController/logsErrors.txt', 'r')

    content = file.read()

    print(content)

    file.close()

def getAllErrorsByType(error_type: str):
    file = open('./logsController/logsErrors.txt', 'r')
    
    matching_errors = []
    
    pattern = re.compile(fr"{error_type}:", re.IGNORECASE)
    
    for line in file:
        if pattern.search(line):
            matching_errors.append(line)
    
    file.close()

    if(len(matching_errors) > 0):
        print(f"Errores encontrados para '{error_type}':")
        for error in matching_errors:
            print(error)
    else: 
        print(f"Ningun '{error_type}' encontrado")
    