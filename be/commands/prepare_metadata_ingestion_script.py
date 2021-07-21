import csv

from be.configuration import VERTEX_METADATA_TABLE

openFile = open('../data/labels.csv', 'r')
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
with open('metadata_ingestion.sql', 'w') as output:
    for r in insert_statements:
        output.write(r + '\n')