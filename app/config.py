""" Config.
"""
import os

from dynaconf import Dynaconf, \
    Validator

# Constants
SETTINGS_PATH = "settings/settings.yaml"
SECRETS_PATH  = "settings/.secrets.yaml"
# // Constants


base_path     = os.path.dirname(__file__)
settings_path = os.path.join(base_path, SETTINGS_PATH)
secrets_path  = os.path.join(base_path, SECRETS_PATH)

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=[settings_path, secrets_path],
    validators=[Validator("plugins", must_exist=True)]
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
