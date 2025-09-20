# Path
from dataclasses import dataclass
from pathlib import Path

# Toml
class TomlException(Exception):
    """For raising a toml exception

    Args:
        Exception (str): Message to send
    """
    def __init__(self, message):
        super().__init__(message)
@dataclass
class TomlHelper:
    table: str
    key: str
class Toml:
    import tomllib
    def loadToml(self, path:Path | str):
        """Loads a toml file
        Args:
            path (Path): Path object or string
        Raises:
            FileNotFoundError: When the file can't be found
        Returns:
            dict: The toml file as a dict
        """
        if type(path) is str: path = Path(path)
        if path.is_file(): return self.tomllib.load(path.open("rb"))
        raise FileNotFoundError(f'"{path}" Is Not a File')
    def loadTomlData(self, path:Path, data:TomlHelper) -> str | int | bool:
        """loads data from a toml file
        Args:
            path (Path | str): Path object or string
            data (TomlHelper): Table, Key
        Raises:
            TomlException: When toml file is missing data
        Returns:
            any: any type of object
        """
        missing = f'Toml Missing "{data.table}.{data.key}"'
        if str(data.table).__contains__('.'):
            l = str(data.table).split('.')
            try: Lt = self.loadToml(path)[l[0]][l[1]]
            except KeyError: raise TomlException(missing)
        else: 
            try: Lt = self.loadToml(path)[data.table]
            except KeyError: raise TomlException(missing)
        try: return Lt[data.key]
        except KeyError: raise TomlException(missing)
    def loadDefaults(self, path:Path, data:TomlHelper, Dict:dict) -> str:
        try: return self.loadTomlData(path, data)
        except (TomlException, FileNotFoundError): return Dict[data.key]

# Env
class EnvException(Exception):
    """For raising a env exception

    Args:
        Exception (str): Message to send
    """
    def __init__(self, message):
        super().__init__(message)
class Env:
    import dotenv
    import os
    def loadEnv(self, path:Path | str, data:str):
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
        if path.is_file():
            try:
                self.dotenv.load_dotenv(path)
                return self.os.environ[data]
            except KeyError: raise EnvException(f'Env Missing "{data}"')
        else: raise FileNotFoundError(f'"{path}" Is Not a File')

class JsonException(Exception):
        """For raising a json exception
        Args:
            Exception (str): Message to send
        """
        def __init__(self, message):
            super().__init__(message)
class Json:
    from json import load as lj
    from json.decoder import JSONDecodeError
    def loadJson(self, path:Path) -> dict:
        """Loads a JSON file
        Args:
            Path (Path): Path of the JSON file
        Raises:
            JsonException: When JSON file empty or any other JSON error
        Returns:
            Dict: a dict with the JSON data in it
        """
        if type(path) is str: path = Path(path)
        with open(path) as file:
            try: return self.lj(file)
            except self.JSONDecodeError as err:
                if file.read().strip() == "": raise JsonException("JSON File Empty")
                else: JsonException(err)