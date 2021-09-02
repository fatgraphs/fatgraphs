#!/usr/bin/python
import json
raw_configurations = open("../configurations.json")
labelsHome = json.load(raw_configurations)['account_type_home']
print([labelsHome['eoa'], labelsHome['contracts']])