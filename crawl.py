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
        except FileExistsError:
            pass
        except FileNotFoundError:
            pass
        except FileNotFoundError:
            pass
        except OSError:
            pass
        finally:
            print(f"downloaded {fname}")

    async def main(self):
        self.dhtml()
        task=[self.dload(i) for i in self.soup("script", "src")] + [self.dload(i) for i in  self.soup("link", "href")]+ [self.dload(i) for i in  self.soup("img", "src")]
        res = await asyncio.gather(*task)
        print("end")
        return res



if __name__== "__main__":
    url="https://testnetlive.online/"
    d=Crawl(url=url)
    #try:
    asyncio.run(d.main())
    #except:
    print("download complete")
