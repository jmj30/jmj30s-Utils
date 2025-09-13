# Path
from pathlib import Path

# Toml Stuff
from tomllib import load as loadTOML

# Env Stuff
from dotenv import load_dotenv as loadENV
from os import environ

# Json Stuff
from json import load as loadJSON
from json.decoder import JSONDecodeError

# Toml
class TomlException(Exception):
    """For raising a toml exception

    Args:
        Exception (str): Message to send
    """
    def __init__(self, message):
        super().__init__(message)

def loadToml(path:Path | str):
    """Loads a toml file

    Args:
        path (Path): Path object or string

    Raises:
        FileNotFoundError: When the file can't be found

    Returns:
        dict: The toml file as a dict
    """
    if type(path) is str: path = Path(path)
    if path.is_file(): return loadTOML(path.open("rb"))
    raise FileNotFoundError(f'"{path}" Is Not a File')

def loadTomlData(path:Path, data:list) -> any:
    """loads data from a toml file

    Args:
        path (Path | str): Path object or string
        data (str): String of the valve to get

    Raises:
        TomlException: When toml file is missing data

    Returns:
        any: any type of object
    """
    if str(data[0]).__contains__('.'):
        l = str(data[0]).split('.')
        try: Lt = loadToml(path)[l[0]][l[1]]
        except KeyError: raise TomlException(f'Toml Missing "{data}"')
    else: 
        try: Lt = loadToml(path)[data[0]]
        except KeyError: raise TomlException(f'Toml Missing "{data}"')
    try: return Lt[data[1]]
    except KeyError: raise TomlException(f'Toml Missing "{data}"')

def loadDefaults(path:Path, data:list, Dict:dict) -> str:
    try: return loadTomlData(path, data)
    except (TomlException, FileNotFoundError): return Dict[data[1]]

# Env
class EnvException(Exception):
    """For raising a env exception

    Args:
        Exception (str): Message to send
    """
    def __init__(self, message):
        super().__init__(message)

def loadEnv(path:Path | str, data:str):
    """Loads the Env file

    Args:
        path (Path | str): Path of the env file
        data (str): String of the value to get

    Raises:
        EnvException: When data could not be found
        FileNotFoundError: When missing the env file

    Returns:
        str: return str
    """
    if type(path) is str: path = Path(path)
    loadENV(path)
    if path.is_file():
        try: return environ[data]
        except KeyError: raise EnvException(f'Env Missing "{data}"')
    else: raise FileNotFoundError(f'"{path}" Is Not a File')

# Json
class JsonException(Exception):
    """For raising a json exception

    Args:
        Exception (str): Message to send
    """
    def __init__(self, message):
        super().__init__(message)

def loadJson(path:Path):
    with open(path) as file:
        try: return loadJSON(file)
        except JSONDecodeError as err:
            if file.read().strip() == "": raise JsonException("JSON File Empty")
            else: JsonException(err)