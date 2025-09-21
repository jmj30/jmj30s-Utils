from Utils import Path, Env, EnvException
import collections

def loadToken(path:Path):
    """Load Bot Token
    Args:
        path (Path): Path of the env file
    Returns:
        str: Bot Token
    """
    try: return Env().loadEnv(path, "TOKEN")
    except (EnvException, FileNotFoundError):
        try: open(path, 'x').close()
        except FileExistsError: pass
        from getpass import getpass
        with open(path, '+at') as file:
            try:
                passwd = getpass("Bot Token: ")
                file.write(f'TOKEN="{passwd}"')
                exit()
            except KeyboardInterrupt:
                print("Bot token not in file please add it")
                exit()

# we want to be absolutely sure this path is correct, so we
# do a bit of complicated path logic to get the src folder
SRC_PATH = Path(__file__).parent.parent.absolute().as_posix()

def file_to_ext(str_path, base_path):
    # changes a file to an import-like string
    str_path = str_path.replace(base_path, "")
    str_path = str_path.replace("/", ".")
    return str_path.replace(".py", "")
def get_all_extensions(str_path, folder="Modules"):
    # gets all extensions in a folder
    ext_files = collections.deque()
    loc_split = str_path.split(folder)
    base_path = loc_split[0]
    if base_path == str_path:
        base_path = base_path.replace("main.py", "")
    base_path = base_path.replace("\\", "/")
    if base_path[-1] != "/":
        base_path += "/"
    pathlist = Path(f"{base_path}/{folder}").glob("**/*.py")
    for path in pathlist:
        str_path = str(path.as_posix())
        str_path = file_to_ext(str_path, base_path)
        if not str_path.startswith("_"):
            ext_files.append(str_path)
    return ext_files