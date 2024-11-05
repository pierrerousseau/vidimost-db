""" Data loading.

    File format example : basecode.csv
    date;label
    DD/MM/YYYY;value
    DD/MM/YYYY;value
    DD/MM/YYYY;value
    DD/MM/YYYY;value
    ...

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

    basecode = os.path.splitext(os.path.basename(path))[0]
    labels   = []

    with open(path, 'r', encoding=encoding) as content:
        for num, line in enumerate(content):
            line = line.strip()
            if num:
                try:
                    date, value = line.split(csv_sep)
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
            
                for label in labels:
                    code = code_sep.join([basecode, label, intdate])
                    
                    element = Element(code, value, dtdate, label)
                    element.update()
                    logging.info(f"Element added: {element}")

            else: # titles line
                try:
                    labels = [label.lower() for label in line.split(csv_sep)[1:]]
                except ValueError as e:
                    logging.warning(f"Ignored, no enough titles: {line}")
                    break