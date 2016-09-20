#! /usr/bin/python

from pyquery import PyQuery as pq
from multiprocessing import Process
import json
from lxml import etree
import os


HTML_FORMAT = 'html/{}'
JSON_FORMAT = 'json/{}'

TRANSLATION = {13: None, 160: 32}


def parse(code):
    doc = pq(filename=HTML_FORMAT.format(code))
    pars = doc('body > table:nth-child(6) > tr > td p')

    lines = []
    for par in pars:

        line = []
        for part in pq(par).contents():
            if etree.iselement(part):
                if part.tag == 'i':
                    type = 'i'
                elif part.tag == 'font':
                    type = 'a'
                else:
                    type = 't'

                text = pq(part).text()
            else:
                type = 't'
                text = part

            text = unicode(text).translate(TRANSLATION)

            line.append({'type': type, 'text': text})

        lines.append(line)

    lis = doc('body > table:nth-child(4) > tr > td > font > font > ul li')
    heads = lis.map(lambda i, e: e.text.strip())

    data = {'heads': heads, 'lines': lines}

    with open(JSON_FORMAT.format(code), 'w') as file:
        file.write(json.dumps(data))

    print code


codes = os.listdir(HTML_FORMAT.format(''))

processes = []

for code in codes:
    if __name__ == '__main__':
        p = Process(target=parse, args=(code,))
        processes.append(p)
        p.start()

for p in processes:
    p.join()
