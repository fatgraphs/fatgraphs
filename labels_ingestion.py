#!/usr/bin/env python

import sys
import pandas as pd
from be.persistency.persistence_api import persistenceApi

REQUIRED_COLUMNS = ['address', 'label', 'type']

if __name__ == "__main__":
    persistenceApi.ensureLabelsTableExists()
    if len(sys.argv) != 2:
        raise Exception("The ingestion script needs to be called with exactly one argument: the path to the labels.csv")
    raw_path = sys.argv[1]
    raw_labels = pd.read_csv(raw_path)
    print("Label file loaded ...")
    for required_column in REQUIRED_COLUMNS:
        if not required_column in raw_labels:
            raise Exception("The csv file provided to the label ingestion script doesn't contain one of the required columns")

    address_label_type = raw_labels[REQUIRED_COLUMNS].rename(columns={'address': 'eth'})

    persistenceApi.populateLabelsTable(address_label_type)

    print("Labels correctly added to the db")