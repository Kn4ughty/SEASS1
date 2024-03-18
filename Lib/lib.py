import os
from Lib import timing
from Lib import debug
import subprocess
import platform

__all__ = ["timing", "debug"]


def check_os():
    match os.name:
        case "nt":
            return "nt"
        case "posix":
            return "posix"
        case _:
            raise ValueError("You are in a silly OS probaby change it")


def clear_terminal():
    OS = check_os()
    if OS == "nt":
        os.system("cls")
    elif OS == "posix":
        os.system("printf '\\033c'")
    else:
        raise NotImplementedError("ClearTerminal unknown OS")


def stringToBool(string: str) -> bool:
    return string.lower() in [
        "true",
        "1",
        "t",
        "y",
        "yes",
        "yeah",
        "yup",
        "certainly",
        "uh-huh",
        "yuppers",
        "truth",
    ]

def openPath(path):
    os = platform.system()
    # im terribly sorry any BSD users out there.
    match os:
        case "Windows":
            os.startfile(path)
        case "Darwin":
            subprocess.Popen(["open", path])
        case _:
            subprocess.Popen(["xdg-open", path])