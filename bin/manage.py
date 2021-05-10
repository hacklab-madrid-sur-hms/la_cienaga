#!/usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from la_cienaga.core import management

if __name__ == '__main__':
    management.execute_from_commandline()
