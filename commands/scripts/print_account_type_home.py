#!/usr/bin/python
import os
from be.configuration import CONFIGURATIONS
print([os.path.abspath(CONFIGURATIONS['account_type_home']['eoa']), os.path.abspath(CONFIGURATIONS['account_type_home']['ca'])])