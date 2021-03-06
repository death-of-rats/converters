#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path
import re
import urllib.parse
import string

mathSection = re.compile(r"(^|\s)(?P<chevron>\${1,2})\s(?P<eq>.+?)\s(?P=chevron)([\!\"\#\%\&\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\\\]\_\`\{\|\}\~]|\s|$)", flags=re.M)
latexPattern = "_latex"

def search_and_convert(line: str) -> str:
    search = mathSection.finditer(line)
    newLine = []
    lastInd = 0
    for s in search:
        b,e= s.span()
        newLine.append(line[lastInd:b])
        param = urllib.parse.quote(s.group('eq').strip(), safe='')
        url = f"https://render.githubusercontent.com/render/math?math={param}"
        newLine.append(f" <img src=\"{url}\" /> ")
        lastInd = e

    newLine.append(line[lastInd:].rstrip())
    newLine.append("\n")
    return "".join(newLine)

def main(args):
    file = Path(args.file)
    tmpFile = file.parent / Path( file.stem +"_tmp"+ file.suffix)
    if file.stem.endswith(latexPattern):
        tmpFile = file.parent / Path( file.stem.replace("_latex","") + file.suffix)
    with open(tmpFile, 'w') as dst:
        with open(args.file, 'r') as src:
            line = src.readline()
            while line:
                dst.write(search_and_convert(line))
                line = src.readline()

if __name__ == "__main__":
    parser = ArgumentParser(description="Convert latex math to images generated by github.")
    parser.add_argument('file', help="markdown file to be searched for latex math formulas")

    args = parser.parse_args()
    main(args)
