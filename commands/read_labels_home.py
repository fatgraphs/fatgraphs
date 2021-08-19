#!/usr/bin/python
import json
raw_configurations = open("../configurations.json")
labelsHome = json.load(raw_configurations)['labelsHome']
print(labelsHome)