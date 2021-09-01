#!/usr/bin/python
import json, os
raw_configurations = open("../configurations.json")
configurations = json.load(raw_configurations)
print(os.path.join(
    configurations['home'],
    configurations['labelsHome']
    )
)