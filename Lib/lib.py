from os import system, name

def check_os():
    # TODO make into switch statement
    if name == 'nt':
        return 'nt'
    elif name == 'posix':
        return 'posix'
    else:
        raise ValueError("You are in a silly OS probaby change it")

def clear_terminal():
    OS = check_os()
    if OS == 'nt':
        system('cls')
    elif OS == 'posix':
        system('clear')
    else:
        raise NotImplementedError("ClearTerminal unknown OS")