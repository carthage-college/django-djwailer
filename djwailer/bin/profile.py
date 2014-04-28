from optparse import OptionParser
from pprint import pprint

import urllib2, json, sys

"""
Shell script that grabs profile data from
LiveWhale API
"""

#set up command-line options
desc = """
Takes a URL and grabs JSON data for processing
"""

parser = OptionParser(description=desc)
parser.add_option("-u", "--url", help="url that returns JSON data", dest="earl")

def main():
    # read the json data from URL
    #data =  urllib2.urlopen(earl)
    #data = response.read()

    #j = json.load(data)
    #k = [i for i, j, k in j[1]]
    #l = json.dumps(k)

    #print j

    response =  urllib2.urlopen(earl)
    data = response.read()
    prof = json.loads(data)

    #print prof
    #print prof[0]
    print prof[0]['url']

######################
# shell command line
######################

if __name__ == "__main__":
    (options, args) = parser.parse_args()
    earl = options.earl
    if not earl:
        print "You must provide a URL\n"
        parser.print_help()
        exit(-1)

    sys.exit(main())
