from optparse import OptionParser

from lxml.html.clean import Cleaner

import sys

"""
Shell script that strips MS tags from text
"""

#set up command-line options
desc = """
Takes a text file and strips funky MS tags
"""

parser = OptionParser(description=desc)
parser.add_option("-t", "--txt", help="full path to text file", dest="text")

def main():

    f = open (text,"r")
    data = f.read()
    cleaner = Cleaner(style=True)
    print cleaner.clean_html(data)
    f.close()

######################
# shell command line
######################

if __name__ == "__main__":
    (options, args) = parser.parse_args()
    text = options.text
    if not text:
        print "You must provide a file\n"
        parser.print_help()
        exit(-1)

    sys.exit(main())
