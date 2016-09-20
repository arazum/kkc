#! /usr/bin/python
# -*- coding: utf-8 -*-

from multiprocessing import Process
import json
import os
import codecs
import re


JSON_FORMAT = 'json/{}'
OUTPUT_FILE = 'output.tex'

HEAD_TEXT = r'''\documentclass[11pt]{book}

\usepackage[croatian]{babel}
\usepackage[utf8]{inputenc}
\usepackage{times}
\usepackage{hyperref}

\setlength\parindent{0pt}
\setcounter{secnumdepth}{-2}
\setcounter{tocdepth}{6}

% \RequirePackage[a4paper, left=2.5cm, right=2.5cm, bottom=2.5cm, top=2.5cm]{geometry}

\title{Katekizam Katolicke Crkve}
\date{}
\author{}

\begin{document}

\maketitle
\tableofcontents

'''

FOOT_TEXT = '''
\end{document}
'''

TEX_CONV = { 
        '&': r'\&', 
        '%': r'\%', 
        '$': r'\$', 
        '#': r'\#', 
        '_': r'\_', 
        '{': r'\{', 
        '}': r'\}', 
        '~': r'\textasciitilde{}', 
        '^': r'\^{}', 
        '\\': r'\textbackslash{}', 
        '<': r'\textless', 
        '>': r'\textgreater', 
        }

HEAD_NAMES = ['part', 'chapter', 'section', 'subsection', 'subsubsection', 'paragraph']

BLACKLIST = {'01'}
START_NUMBER = 26


def tex_escape(text):
    regex = re.compile('|'.join(re.escape(unicode(key)) for key in TEX_CONV.keys())) 
    return regex.sub(lambda match: TEX_CONV[match.group()], text)

def get_numbers(text, start):
    regex = re.compile('\d{2,}')
    matches = regex.finditer(text)

    spans = []
    for match in matches:
        if int(match.group()) == start:
            spans.append(match.span())
            start += 1

    return spans


codes = sorted(os.listdir(JSON_FORMAT.format('')))

output = codecs.open(OUTPUT_FILE, 'w', 'utf-8')
output.write(HEAD_TEXT)

pheads = []
number = START_NUMBER

for code in codes:
    if code in BLACKLIST:
        continue

    with open(JSON_FORMAT.format(code)) as file:
        data = json.load(file)

    heads = data['heads']

    matched = 0
    for head, phead in zip(heads, pheads):
        if head != phead:
            break

        matched += 1

    pheads = heads

    for name, head in zip(HEAD_NAMES, heads)[matched:]:
        output.write(u'\\{}{{{}}}\n'.format(name, head))

    lines = data['lines']
    for line in lines:
        for piece in line:
            type = piece['type']

            italic = False
            show = False
            title = False

            if type == 'i':
                italic = True
                show = True
            elif type == 't':
                show = True

            text = piece['text']
            stripped = text.strip()
            if stripped == stripped.upper() and len(re.findall('[A-Z]', stripped)) > 1:
                title = True

            if heads.count(stripped):
                show = False

            if show:
                if title:
                    output.write(u'\\subparagraph*{{{}}}\n'.format(tex_escape(text)))
                else:
                    spans = [(0, 0)] + get_numbers(text, number) + [(len(text), 0)]
                    for index in range(0, len(spans) - 1):
                        left = spans[index][1]
                        right = spans[index + 1][0]

                        if italic:
                            output.write('\\textit{')
                        output.write(tex_escape(text[left:right]))
                        if italic:
                            output.write('}')

                        if index < len(spans) - 2:
                            output.write('\\subparagraph*{{{}}}\n'.format(number))
                            number += 1

        output.write('\n')

    print code

output.write(FOOT_TEXT)
output.close()
