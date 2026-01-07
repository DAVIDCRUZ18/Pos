import subprocess
import requests
from app.config.settings import version

URL_VERSION = "https://github.com/DAVIDCRUZ18/Pos.git/raw/main/version.txt"


def get_remote_version():
    try:
        response = requests.get(URL_VERSION, timeout=5)
        return response.text.strip()
    except:
        return None


def hay_actualizacion():
    remote = get_remote_version()
    if not remote:
        return False

    return remote != version


def actualizar_desde_git():
    try:
        result = subprocess.run(
            ["git", "pull"],
            capture_output=True,
            text=True
        )

        return result.stdout
    except Exception as e:
        return str(e)
