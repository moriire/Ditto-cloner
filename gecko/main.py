import cloner
import pyfiglet
import click
import sys

@click.group()
@click.version_option("1.0.0")
def cli():
    f = pyfiglet.figlet_format('Gecko', font='starwars')
    click.echo(f)
    """GECKO Website Cloner CLI"""
    pass


@cli.command(name='gecko')
@click.option('--url', '-u', type=str, help='Enter a valid website address')
@click.option("--mission", '-m', type=int,  prompt="Your Mission", help="Provide your name")
@click.option("--name", type=str, prompt="Your name", help="Provide your name")
def generic(url, mission, name=None):
    if not url:
        raise Exception('bad')
    if mission == 1:
        x=cloner.Clone(url)
        click.echo(x.run())
    elif mission == 2:
    #x=cmap.Clone(url)
        click.echo(name)


@cli.command(name='wel')
def welcome():
    click.echo('Welcome')

"""
if __name__ == '__main__':
    cli()
"""
