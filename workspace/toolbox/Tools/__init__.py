from Tools import *
from sys import argv
import argparse


tools_dict = {
}

def add_parsers(subparsers):
    for tool in tools_dict.items():
        t_parser = subparsers.add_parser(tool[0])
        tool[1].make_parser(t_parser)

def parse_args():
    parser = argparse.ArgumentParser(prog='Toolbox', description='common tools for everyday usage')
    subs = parser.add_subparsers(title='tools',
                                 description='Registered tools',
                                 help='Run Toolbox {tool} --help for help on specific tool')
    subs.required = True
    add_parsers(subs)
    if len(argv) < 2:
        options = parser.parse_args(['--help'])
    else:
        options = parser.parse_args()
       
    options.func(options)
