#!/usr/local/bin/python
import sys
import os
import re
from defroutes import set_old_default_route


def main(argv):
    set_old_default_route()

if __name__ == '__main__':
    main(sys.argv)

