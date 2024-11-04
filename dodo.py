""" Tâches habituelles.
"""
import os
import subprocess


# Constants
CONFIG_PATH = "./app/settings"
SRC_PATH    = "app"
DOIT_CONFIG = {"backend": "json"}
# // Constants


def task_python_version():
    """ Affiche la version de python.

        Principalement pour test.
    """
    return {'actions': ["python --version"],
            'verbosity': 2}


def task_install():
    """ Installation des composants.
    """
    requirements_path = os.path.join(CONFIG_PATH, "requirements.txt")

    return {'actions': ["pip --require-virtualenv install -r " +
                        requirements_path],
            'verbosity': 2}


def task_uninstall():
    """ Désinstallation des composants.
    """
    return {'actions': ["pip freeze > uninstall",
                        "pip --require-virtualenv uninstall -y -r uninstall",
                        "rm uninstall"],
            'verbosity': 2}


def task_lint():
    """ Lance pylint.
    """
    rc_path  = os.path.join(CONFIG_PATH, ".pylintrc")
    out_path = SRC_PATH

    return {'actions': [f"pylint --rcfile {rc_path}" +
                        " --load-plugins=perflint " +
                        f" --output pylint.out {out_path}"],
            'verbosity': 0}


def task_mongo():
    """ Gère la base mongo de dev.
    """
    compose = os.path.join(CONFIG_PATH, "compose-dev.yaml")

    return {'actions': [f"podman-compose -f {compose} %(params)s"],
            'params':[{"name": "params",
                       "short": "p",
                       "type": str,
                       "choices": (("up --build -d", ""), ("down", "")),
                       "default": "up --build -d",
                       "help": "Choose between up and down"}],
            'verbosity': 0}


def task_uvicorn():
    """ Lance la version uvicorn de l'application.
    """
    def run_uvicorn():
        subprocess.run(['uvicorn', 'app:app', 
                        '--reload', '--reload-exclude', 'data/**'], 
                       check=True)

    return {
        'actions': [run_uvicorn],
        'uptodate': [None],  # Ne pas utiliser la base de données de `doit`
        'verbosity': 2,
    }


def task_docker_build():
    """ Construit les containers de la version docker de l'application.
    """
    return {'actions': ["docker build -t vidimost-db app/"],
            'verbosity': 2}


def task_docker_run():
    """ Lance la version docker de l'application.
    """
    name    = "vidimost-db"
    network = "vidimost_vidimost-network"

    return {'actions': [f"docker run -d --name {name} -p 80:80 --network={network} {name}"],
            'verbosity': 2}


def task_docker_compose():
    """ Lance la version docker de l'application par compose.
    """
    return {'actions': ["docker compose -f docker-compose.yml up --build"],
            'verbosity': 2}


def task_add_element():
    """ Ajoute un élément à la base de données.
    """
    return {'actions': ["python -m app add-element " +
                        " --code %(code)s " +
                        " --value %(value)s " +
                        " --label %(label)s"],
            'params':[{"name": "code",
                       "long": "code",
                       "short": "c",
                       "type": str,
                       "default": "",
                       "help": "Code of the element"},
                      {"name": "value",
                       "long": "value",
                       "short": "v",
                       "type": str,
                       "default": "",
                       "help": "Value of the element"},
                      {"name": "label",
                       "long": "label",
                       "short": "l",
                       "type": str,
                       "default": "",
                       "help": "Label of the element"}],
            'verbosity': 2}


def task_list_elements():
    """ Liste les éléments de la base de données.
    """
    return {'actions': ["python -m app list-elements %(params)s"],
            'params': [{"name": "params",
                        "short": "p",
                        "type": str,
                        "default": "",
                        "help": "Code of the element"}],
            'verbosity': 2}


def task_load_file():
    """ Charge un fichier.
    """
    return {'actions': ["python -m app load-file --path %(path)s"],
            'params': [{"name": "path",
                        "long": "path",
                        "short": "p",
                        "type": str,
                        "default": "",
                        "help": "Path to the file to load"}],
            'verbosity': 2}