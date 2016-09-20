#! /usr/bin/python

from pyquery import PyQuery as pq
import pycurl
from multiprocessing import Process
import re
import os


TOC_FILE = 'toc.html'
PART_FORMAT = 'orig/{}'
URL_FORMAT = 'http://www.intratext.com/IXT/SCR0001/_{}'


def download(href):
    code = re.match('_P(..?)\.HTM', href).group(1).zfill(2)
    filename = PART_FORMAT.format(code)

    if os.path.isfile(filename) and os.stat(filename).st_size > 0:
        return

    url = URL_FORMAT.format(href)

    f = open(filename, 'w')

    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, f)
    c.perform()
    c.close()

    f.close()

    print code


doc = pq(filename=TOC_FILE)
links = doc('body > table:nth-child(5) > tr > td > font > ul a')
hrefs = links.map(lambda i, e: pq(e).attr('href'))

processes = []

for href in hrefs:
    if __name__ == '__main__':
        p = Process(target=download, args=(href,))
        processes.append(p)
        p.start()

for p in processes:
    p.join()
