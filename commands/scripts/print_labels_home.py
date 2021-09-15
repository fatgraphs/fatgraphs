#!/usr/bin/python
import os
import sys
if os.getcwd().split(os.sep)[-1] == "commands":
    # if it's run from the commands frolder then chdire to be in root
    os.chdir(os.path.abspath(".."))
sys.path.append(os.path.abspath('.'))
from be.configuration import CONFIGURATIONS
print(os.path.abspath(CONFIGURATIONS['labelsHome']))