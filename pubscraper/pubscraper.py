#!/usr/bin/env python3
#coding:utf-8

"""
Publication Scraper

This program accepts a url to an IRS publication into several markdown files
broken down by sections contained in the publication. The goal is to produce
digestible, searchable files that can be read and edited as part of a personal
library of tax information.

USAGE

    ./scraper.py [OPTIONS] [URL]

OPTIONS
    -o, --out   The output directory of the files to be converted.
    -c, --css   A CSS selector
"""

import os
import argparse

import requests

from bs4 import BeautifulSoup
from markdownify import markdownify as md

def _getTitle(soup):
    return soup.select_one('.book:first-child .titlepage').h1


# It's not clear why the 'introductory material' section of each publication is
# separated out as an 'article'
def _getSections(soup):
    return soup.select(':is(.article, .chapter)')


def constructDocuments(title, soup, out=None):
    """
    constructDocuments creates markdown documents under a directory [title] for
    each section under [sections].

    Input
        title (string): The title of the document serving as the root directory
        soup (html): The beautiful soup pointer to the document
        out (string): Optionally specify an alternative output directory
    """
    root = title.text

    if not os.path.exists(root):
        os.mkdir(dirname)

    for section in sections:
        filename = (section.h1 or section.h2).text

        with open(f'{dirname}/{filename}.md', 'w+') as f:
            f.write(md(str(section)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Break up an IRS publication into digestable markdown files')
    parser.add_argument('url')
    parser.add_argument('-o', '--out', help='The directory to output the publication files. Default is the current directory')

    args = parser.parse_args()

    # TODO: Allow a publication number as an optional argument
    html = requests.get(args.url)
    soup = BeautifulSoup(html.text, 'html.parser')

    title = _getTitle(soup)

    for article in soup.select('.article'):
        print(article.h1.text)
        for section in article.select('.section .titlepage'):
            print('\t', section.select_one(':is(h2, h4)').text)

    # for h in soup.select(':is(h1, h2, h3, h4, h5, h6).title'):
    #     print(h.parent.name)
    #     print('\t', h.name, h['class'], h.text)

    # sections = _getSections(soup)

    # constructDocuments(title, sections)
