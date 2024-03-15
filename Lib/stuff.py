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
        system("printf '\\033c\'")
    else:
        raise NotImplementedError("ClearTerminal unknown OS")

def stringToBool(string: bool):
    return string.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh', 'yuppers']