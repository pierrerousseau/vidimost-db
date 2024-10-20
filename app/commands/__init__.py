""" This module contains the commands to manage the database from the CLI.
"""
import click
from app.database.models.elements import Element
from app.config import settings

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
    element = Element(code=code, value=value, label=label)
    element.insert()

    click.echo(f"Element added: {element}")


@cli.command()
@click.option('--code', help='Code of the element to search')
def list_elements(code):
    """ List elements from the database. 
    """
    element = Element(code='', value=0)
    query = {"code": code} if code else {}
    for doc in element.db.elements.find(query):
        click.echo(Element.from_dict(doc))


if __name__ == '__main__':
    cli()