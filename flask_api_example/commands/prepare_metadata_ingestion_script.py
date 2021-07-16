import csv

openFile = open('/home/carlo/tokengallery/be/data/labels.csv', 'r')
csvFile = csv.reader(openFile)
header = next(csvFile)
headers = list(map((lambda x: x), header))
insert = 'INSERT INTO tg_metadata (eth_source, meta_type, meta_value, entity) VALUES '


def quote(param):
    return '\'' + str(param) + '\''

insert_statements = []
for row in csvFile:
    values = '(' + quote(row[1]) + ', \'type\', ' + quote(row[0]) + ', \'vertex\');'
    insert_statements.append(insert + values)
    values = '(' + quote(row[1]) + ', \'label\', ' + quote(row[2]) + ', \'vertex\');'
    insert_statements.append(insert + values)
openFile.close()
with open('metadata_ingestion.sql', 'w') as output:
    for r in insert_statements:
        output.write(r + '\n')