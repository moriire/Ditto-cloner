import requests as rq
from bs4 import BeautifulSoup as bsoup
from urllib import parse
import asyncio
import os
import re
import time
import random
import pyfiglet
import click


class Crawl:
    def __init__(self, url):
        self.url=url
        self.link=parse.urlparse(self.url)
        """
        try:
            os.mkdir(self.link.netloc)
        except FileExistsError:
            pass
        finally:
            os.chdir(self.link.netloc)
        """
    def path(self, url):
        return parse.urlparse(url).path

    def f_cdn(self, link):
        x=re.match(r'^https://', str(link))
        if x:
            return False
        elif link is None:
            return False
        else:
            return True

    def domain(self, url):
        return parse.urlparse(url).netloc

    def resp(self):
        resp = rq.get(url, allow_redirects=True)
        return resp.text

    def soup(self, tag, attr):
        soup=bsoup(self.resp(), "html.parser")
        f_cdn = tuple(filter(self.f_cdn, soup.find_all(tag)))
        return tuple(
                map(lambda x: f'https://{self.domain(self.url)}/{x.get(attr)}', f_cdn))


    def dhtml(self):
        fn="index.html"
        page = self.path(self.url)
        if page.endswith(".html"):
            fn = page.split("/")[-1]
        elif page == "/" or page == "":
            fn=fn
        p=os.path.join(self.link.netloc, fn)
        try:
            os.makedirs(self.link.netloc, 0o666)
        except:
            pass
        with open(p, "w", encoding="utf8") as html:
            html.write(self.resp())
            print(f"downloaded {fn} in {p}")
            html.close()

    def dload(self, url):
        resp = rq.get(url)
        split = url.split("/")[2:-1]
        splitted= os.path.join(*split)
        fname=self.path(url).split("/")[-1]
        try:
            os.makedirs(splitted, 0o666)
            html = open(os.path.join(splitted, fname), "w")
            html.write(resp.text)
        except (FileExistsError, FileNotFoundError, FileNotFoundError:, OSError):
            pass
        finally:
            print(f"downloaded {fname}")

    async def main(self):
        self.dhtml()
        task=[self.dload(i) for i in self.soup("script", "src")] + [self.dload(i) for i in  self.soup("link", "href")]+ [self.dload(i) for i in  self.soup("img", "src")]
        res = await asyncio.gather(*task)
        print("end")
        return res


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
            x = Crawl(entry['url'])
            return asyncio.run(x.main())
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
    x=Crawl(url)
    click.echo(asyncio.run(x.main()))


@cli.command()
def wall():
    return gui()

if __name__ == '__main__':
    cli()
"""
if __name__== "__main__":
    url="https://testnetlive.online/"
    d=Crawl(url=url)
    #try:
    asyncio.run(d.main())
    #except:
    print("download complete")
"""
