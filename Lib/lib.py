from os import system, name

def check_os():
    # TODO make into switch statement
    match name:
        case "nt":
            return "nt"
        case "posix":
            return "posix"
        case _:
            raise ValueError("You are in a silly OS probaby change it")

def clear_terminal():
    OS = check_os()
    if OS == 'nt':
        system('cls')
    elif OS == 'posix':
        system('clear')
    else:
        raise NotImplementedError("ClearTerminal unknown OS")