""" Point d'entrée FastAPI.
"""
from fastapi import FastAPI

from .database.models.elements import find_all_elements


app = FastAPI(title="vidimost-db",
              version="0.0.1")


@app.get("/")
def read_root():
    """ Url example.
    """
    return {"Hello": "World"}


@app.get("/api/elements")
@app.get("/api/elements/{label}")
def get_elements(label=None):
    """ Get the elements list.
    
        Args:
            label (str, optional): Label à filtrer. Defaults to None.
    """
    elements = find_all_elements(label=label)

    return [element.to_dict() for element in elements]
