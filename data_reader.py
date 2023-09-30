import csv

with open('data/DevelopmentData.csv') as csvfile:
    data_reader = list(csv.reader(csvfile, delimiter=','))
for row in data_reader:
    print(row[4])
