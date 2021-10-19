import asyncio
import requests
import urllib 
import os
import time
import sys
from pyfiglet import Figlet
import click
from bs4 import BeautifulSoup as BSoup
import random
user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]

user_agent = random.choice(user_agent_list)
#Set the headers 
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
        #self.url = url
        self.tag=tag
        super().__init__(url)
        try:
            self.base_tag = self.head.base['href']
        except TypeError:
            self.base_tag = ''
            
    def __str__(self):
        self.out = self.html#findAll(self.tag)
        return str(self.out)

    def clean(self, url):
        dirs = urllib.parse.urlsplit(url)
        path = dirs.path.rpartition('/')[0]
        return path

                
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
                self.urlfrag.netloc,
                self.urlfrag.path
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
        self.parse = ParseHTML(url, self.tag)
        self.download = Downloader
        self.urlfrag=urllib.parse.urlsplit(url)

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

class Clone(TakeOver, Downloader):
    def __init__(self, url, loc=None, rename=None):
        self.url = url
        self.rename = rename
        self.takeover=TakeOver

        self.download = Downloader
        self.dirs=self.download(url).urlfrag.netloc
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
