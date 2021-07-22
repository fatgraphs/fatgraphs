#!/usr/bin/python3
import csv
import os
import sys

sys.path.append(os.path.abspath('..'))
from be.configuration import VERTEX_METADATA_TABLE

def extract_args():
    global SQL_FILE, LABEL_FILE
    if len(sys.argv) < 2:
        raise Exception("You need to pass the path to the labels.csv file")
    SQL_FILE = sys.argv[2] if len(sys.argv) >= 3 else 'metadata_ingestion.sql'
    LABEL_FILE = sys.argv[1]  # '../data/labels.csv'
    return SQL_FILE, LABEL_FILE


SQL_FILE, LABEL_FILE = extract_args()

openFile = open(LABEL_FILE, 'r')
csvFile = csv.reader(openFile)
header = next(csvFile)
headers = list(map((lambda x: x), header))
insert = f'INSERT INTO {VERTEX_METADATA_TABLE} (eth, type, label) VALUES '


def quote(param):
    return '\'' + str(param) + '\''

insert_statements = []
for row in csvFile:
    values = '(' + quote(row[1]) + ', ' + quote(row[0]) + ', ' + quote(row[2]) + ');'
    insert_statements.append(insert + values)
openFile.close()

with open(SQL_FILE, 'w') as output:
    for r in insert_statements:
        output.write(r + '\n')