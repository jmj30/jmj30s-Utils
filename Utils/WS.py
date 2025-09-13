from Utils import Path, loadEnv, EnvException

def loadKey(path:Path):
    """Loads Secret Key

    Args:
        path (Path): Path of the env file

    Returns:
        str: Secret Key
    """
    try: return str(loadEnv(path, "SECRET_KEY"))
    except (EnvException, FileNotFoundError):
        try: open(path, 'x').close()
        except FileExistsError: pass
        with open(path, 'rt+') as l:
            if l.read().strip() == "":
                import secrets
                l.write(f'SECRET_KEY="{secrets.token_urlsafe(16)}"')
        print("Shuting down...")
        exit()