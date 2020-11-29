import cmap# import Clone
import pyfiglet
import click
import sys


import click


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
        x=cmap.Clone(url)
        #click.echo(
        click.echo(x.run())
    elif mission == 2:
    #x=cmap.Clone(url)
        click.echo(name)


@cli.command(name='wel')
def welcome():
    click.echo('Welcome')


if __name__ == '__main__':
    cli()














"""
@click.group()
@click.version_option("1.0.0")
#@click.help_option("1.0.0")
#@click.option('--help', default=2, help='Lie you need help')
def main():
    f = pyfiglet.figlet_format('Gecko', font='starwars')
    print(f)
    #pass
    
@click.command()
#@click.option('--clone', default=1, help='What would yooou lie to do?')
#@click.option('--count', default=2, help='What would yooou lie to do?')
def start():
    click.echo('a')

#start()
#main()
@main.command()#'start')
@click.argument('url', required=False)
def clone(url):
    print(url)
    #x = Clone(url)
    #click.echo(x.run())

@main.command('start')
@click.option('on', default=1, help='number of greetings')
@click.argument('url', required=False)
def gecko(url):
    print(f)
    x = Clone(url)
    click.echo(x.run())

if __name__ =='__main__':
    args = sys.argv
    if "--help" in args or len(args) == 1:
        click.echo('yes')
    main()
 
"""
