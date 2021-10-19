import cloner
#import wall
import pyfiglet
import click
import sys
from datetime import datetime
import random
def gui():
    import PySimpleGUI as psg
    layout =[
    [psg.Text('URL:')],
    [psg.Input(key='url')],
    [psg.Text('Save Location:')],
    [psg.FolderBrowse("Click to choose save location", initial_folder="./",
                      tooltip="Click to select folder", key='loc')],
    [psg.Input(key='loc_str', readonly=True)],
    [psg.Exit(), psg.Submit()],
    ]

    win = psg.Window('Gecko Cloner', layout)
    while True:
        clicked, entry = win.read()
        print(entry)
        win['loc_str'].update(value = str(entry['loc']))
        if clicked in ["Exit"]:
            break
        elif clicked == 'Submit':
            x = cloner.Clone(entry['url'])
            return x.run()
            print('Completed')
    #win.close()
    
@click.group()
@click.version_option("1.0.0")
def cli():
    font = random.choice(['dotmatrix','doom', 'coinstak', 'starwars', 'block'][:-2])
    color = random.choice(['red','green', 'yellow','blue'])
    f = pyfiglet.figlet_format('Gecko', font=font)
    click.echo(click.style(f, fg=color, blink=True, bold=True))
    print(f"Mobolaji Abdulsalam - {datetime.now().year}\n\n")
    #print("1. Continue")
    #print("2. GUI")
    
@cli.command(name='gecko')
@click.option('--url', '-u', type=str, required=True, prompt="URL" , help='Enter a valid website address')
@click.option("--dirs", type=str, prompt="Your name", help="Save location", default = "./")
def comm(url, mission, dirs):
    if not url:
        raise Exception('bad')
    x=cloner.Clone(url)
    click.echo(x.run())

@cli.command(name='gui')
def wall():
    return gui()
#"""
if __name__ == '__main__':
    cli()
#"""
