import csv

with open('data/DevelopmentData.csv') as csvfile:
    data_reader = list(csv.reader(csvfile, delimiter=','))
for row in data_reader:
    print(row)
    print('\n')
print(data_reader[-1][0])
