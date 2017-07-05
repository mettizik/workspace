"""
This is just a sample to copy template of a tool file
"""

def make_parser(parser):
    from os.path import basename, splitext
    parser.prog = splitext(basename(__file__))[0]
    parser.description = 'TODO'
    parser.set_defaults(func=main)


def main(options):
    raise NotImplementedError("Not implemented yet, I'm sorry")
