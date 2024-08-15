""" Tâches habituelles.
"""
import os

# Constants
CONFIG_PATH = "./app/settings"
SRC_PATH    = "app"
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


def task_uvicorn():
    """ Lance la version uvicorn de l'application.
    """
    return {'actions': ["uvicorn app:app --reload"],
            'verbosity': 2}


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
