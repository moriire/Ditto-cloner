#!/usr/bin/env python3
import sys
import os 
from datetime import datetime
import random
import asyncio
import requests
import urllib          
import time
import pyfiglet
import click
from bs4 import BeautifulSoup as BSoup
from collections import OrderedDict
import configparser
#config = configparser.ConfigParser()

class MultiOrderedDict(OrderedDict):

    def __setitem__(self, key, value):
        if key in self and isinstance(value, list):
            self[key].extend(value)
        else:
            super().__setitem__(key, value)

    @staticmethod
    def getlist(value):
        return value.split("\n")#os.linesep)
config = configparser.ConfigParser(strict=False, empty_lines_in_values=False, dict_type=MultiOrderedDict, converters={"list": MultiOrderedDict.getlist})
config.read('gecko.ini')
info = config.getlist('info', 'agents')
user_agent = random.choice(info)
headers = {'User-Agent': user_agent}

ICE="""Like you are not connected to the internet."""

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        func(*args, **kwargs)
        end =  time.perf_counter()
        return f"{function} downloaded in {end-start} seconds"
    return wrapper

class Page(BSoup):
    """Page url response such as status code response text"""
    def __init__(self, url):
        self.attributes = dict()
        self.url = url
        self.dirs = urllib.parse.urlsplit(url)
        self.path = self.dirs.netloc
        try: 
            self.resp = requests.get(url, headers=headers)#urllib.request.urlopen(url)#
            super().__init__(self.resp.text,  "html.parser")
        except requests.exceptions.ConnectionError:#ConnectionError:
            print(ICE)
            #raise InternetConnectionError(ICE)
    
    def __int__(self):
        return self.resp.status_code
    
    def __bool__(self):
        return self.resp.status_code==200
    
    def __str__(self):
        return self.resp.text# self.resp.read().decode('utf-8')#
    

class ParseHTML(Page):
    def __init__(self, url, tag=None):
        self.tag=tag
        super().__init__(url)
        try:
            self.base_tag = self.head.base['href']
        except TypeError:
            self.base_tag = ''
            
    def __str__(self):
        self.out = self.__str__()
        return self.out

    def dload(self, url):
        if self.path.endswith(".html"):
            self.path = self.path
        else:
            self.path = "{}.html".format(self.path)
        with open(self.path, "wb") as f:
            f.write(self.resp)
        return self.path

    @staticmethod
    def clean(url):
        return self.path
             
    def gatherLinks(self, tag, param=None):
        links = self.findAll(tag, attrs={param:True})
        dlink = []
        for link in links:
            linker = link[param]
            cdn = linker
            if self.base_tag:
                cdn = self.base_tag.lstrip('/')+linker     
            dlink.append(cdn)
        #folderpath=map(self.clean, dlink)
        return dlink#, list(folderpath)

    def __call__(self, param=None):
       tagsLinks = {'link':'href', 'script':'src', 'img':'href'}
       fpaths = list(map(self.gatherLinks, tagsLinks.keys(), tagsLinks.values()))
       if self.tag:
           fpaths = self.gatherLinks(self.tag, param)
       return fpaths
            
class Downloader:
    def __init__(self, link, loc=None):
        self.link = link
        self.loc = loc
        self.urlfrag = urllib.parse.urlsplit(self.link)
        if self.loc:
            self.location = os.path.join(
                self.loc,
                self.urlfrag.netloc,
                self.urlfrag.path
                )
        self.location = os.path.join(
                self.urlfrag
                )
        
    def folder(self):
        x=0
        dirs=(self.urlfrag.path.lstrip('/')).rpartition('/')[0]#self.location.rpartition('/')[0]
        try: os.makedirs(dirs)#, exist_ok=True)
        except Exception:
            x+=1
        #continue
        return True
    
    def __call__(self, rename=None):
        self.folder()
        filename = self.urlfrag.path.lstrip('/')#[-1]
        r = requests.get(self.link, allow_redirects=True)
        with open(filename, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)    
        return True


class TakeOver(ParseHTML, Downloader):
    def __init__(self, url, tag=None, download=False, stats=False):
        super().__init__(url, tag)#ParseHTML
        self.tag = tag
        self.parse = super().__init__(url)
        self.urlfrag=self.path

    def __segment(self, cpath):
        rsc = ('/').join(('https:/',self.urlfrag.netloc, cpath))
        return rsc

    def flow(self, param=None):
        parser = self.parse(param=param)
        """
        xxc=[]
        for i in parser:
            xxc+=i
        """
        links = tuple(map(self.__segment,  parser))
        return links

class Clone(TakeOver):
    def __init__(self, url, loc=None, rename=None):
        super().__init__(url)
        self.rename = rename
        try:
            os.makedirs(self.dirs)
        except FileExistsError:
            if os.path.isdir(self.dirs):
                pass
        finally:
            os.chdir(self.dirs)
        
    async def getRsc(self, tag, param):
        f = 0
        x=self.takeover(self.url, tag)
        y=x.flow(param)
        for i in y:
            try:
                self.download(i)()
            except OSError:
                continue
            finally:
                f += 1
            print(f"{i}  Completed = {f}, {t}")

    async def main(self):
        # Schedule three calls *concurrently*:
        await Download(self.url)
        await asyncio.gather(
            self.getRsc('img', 'src'),
            self.getRsc('link', 'href'),
            self.getRsc('script', 'src')
            )
        print('completed')
        
    def run(self):
        asyncio.run(self.main())

"""
class Error(Exception):
    pass;
class InternetConnectionError(Error):
    pass
class ValueTooLargeError(Error):
    pass
"""     
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
    
@click.group(invoke_without_command=True)
@click.version_option("1.0.0")
@click.pass_context
def cli(ctx):
    font = 'starwars'#random.choice(['starwars', 'block'])
    color = random.choice(['red','green', 'yellow','blue'])
    f = pyfiglet.figlet_format('Gecko', font=font)
    click.echo(click.style(f, fg=color, blink=True, bold=True))
    click.echo(click.style(f"Mobolaji Abdulsalam - {datetime.now().year}",  fg="blue"))
    help_text ="""
    syntax: python cloner.py gecko --url[url] --loc[loc::optional]\n\t or \n\t python gecko.py \n\t
    URL => URL to be downloaded \n\t
    loc => Directory to save downloaded page.
    if loc is omitted, loc will default to current working directory.       
    """
    click.echo(click.style(help_text, fg="green", blink=True, bold=True))
    if ctx.invoked_subcommand is None:
        v = click.confirm("GUI?")
        if v :
            ctx.forward(wall)
        else:
            url = click.prompt("Enter URL")
            loc = click.prompt("location for project?[Current working Dir]")
            ctx.forward(clone, gui = 0, url = url, loc = loc)
    
@cli.command()
@click.option('--gui', default=0, type=bool)
@click.option('--url', '-u', type=str, required=True, prompt="Enter URL" , help='Enter a valid website address')
@click.option("--loc", type=str, default = "./", prompt="location for project?[Current working Dir]", help="Save location")
@click.pass_context
def clone(ctx, gui, url, loc):
    """
    if not url:
        raise Exception('bad')
    """
    x=Clone(url)
    click.echo(x.run())

@cli.command()
def wall():
    return gui()

if __name__ == '__main__':
    cli()
