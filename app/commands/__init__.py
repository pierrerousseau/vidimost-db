""" This module contains the commands to manage the database from the CLI.
"""
from datetime import datetime as dt

import click
from app.config import settings
from app.database.models.elements import Element, \
    find_all_elements
from app.database.loader import load_file as cmd_load_file


@click.group()
def cli():
    """ CLI for vidimost-db. 
    """
    pass


@cli.command()
@click.option('--code', help='Code of the element')
@click.option('--value', help='Value of the element')
@click.option('--label', default='', help='Label of the element')
def add_element(code, value, label):
    """ Add an element to the database. 
    """
    date = dt.now()

    element = Element(code, value, date, label)
    element.insert()

    click.echo(f"Element added: {element}")


@cli.command()
@click.option('--code', help='Code of the element to search')
def list_elements(code):
    """ List elements from the database. 
    """
    elements = find_all_elements(code=code)

    for element in elements:
        click.echo(element)


@cli.command()
@click.option('--path', help='Data to load', type=click.Path(exists=True))
def load_file(path):
    """ Load a data file.
    """
    cmd_load_file(path)



if __name__ == '__main__':
    cli()