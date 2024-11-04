""" Chargement des données.
"""
from datetime import datetime as dt
import os
import logging

from app.database.models.elements import Element

# Constantes
#: séparateur pour fichiers csv
CSV_SEP = ";"
#: séparateur de code
CODE_SEP = "-"
#: encodage des fichiers à charger
ENCODING = "utf-8"
#: format de date
FMT_DATE     = "%d/%m/%Y"
FMT_INT_DATE = "%Y%m%d"
# // Constantes


def load_file(path, fmt_date=FMT_DATE):
    """ Charge un fichier.
    """
    csv_sep      = CSV_SEP
    encoding     = ENCODING
    fmt_int_date = FMT_INT_DATE
    code_sep     = CODE_SEP

    basecode = os.path.basename(path)

    with open(path, 'r', encoding=encoding) as content:
        for line in content:
            line = line.strip()
            try:
                date, value = line.strip().split(csv_sep)
            except ValueError as e:
                logging.warning(f"Ignored, no enough data: {line}")
                continue

            try:
                dtdate  = dt.strptime(date, fmt_date)
                intdate = dtdate.strftime(fmt_int_date)
            except ValueError as e:
                logging.warning(f"Ignored, invalide date: {line}")
                continue

            if not value:
                logging.warning(f"Ignored, no value: {line}")
                continue
        
            code = code_sep.join([basecode, intdate])
            
            element = Element(code=code, value=value, date=dtdate)
            element.update()
            logging.info(f"Element added: {element}")
