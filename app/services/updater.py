import subprocess
import requests
from app.config.settings import version


URL_VERSION = "https://raw.githubusercontent.com/DAVIDCRUZ18/Pos/main/version.txt"


def get_remote_version():
    try:
        response = requests.get(URL_VERSION, timeout=5)

        if response.status_code != 200:
            return None

        data = response.text.strip()

        if not data:
            return None

        return data

    except Exception:
        return None


def hay_actualizacion():
    remote = get_remote_version()

    if not remote:
        return False

    return remote.strip() != str(version).strip()


def actualizar_desde_git():
    try:
        result = subprocess.run(
            ["git", "pull"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return f"Error al actualizar:\n{result.stderr}"

        return result.stdout or "Actualización completada."

    except Exception as e:
        return f"Excepción durante actualización: {e}"
