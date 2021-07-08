#!/usr/bin/env python

import sys
import pandas as pd
from be.persistency.persistence_api import persistence_api

REQUIRED_COLUMNS = ['address', 'label', 'type']

if __name__ == "__main__":
    persistence_api.ensure_labels_table_exists()
    if len(sys.argv) != 2:
        raise Exception("The ingestion script needs to be called with exactly one argument: the path to the labels.csv")
    raw_path = sys.argv[1]
    raw_labels = pd.read_csv(raw_path)
    print("Label file loaded ...")
    for required_column in REQUIRED_COLUMNS:
        if not required_column in raw_labels:
            raise Exception("The csv file provided to the label ingestion script doesn't contain one of the required columns")

    address_label_type = raw_labels[REQUIRED_COLUMNS].rename(columns={'address': 'eth'})

    persistence_api.populate_labels_table(address_label_type)

    print("Labels correctly added to the db")