import csv

with open('GoodStocks.csv', 'r', newline='') as f:
    reader = csv.reader(f)
    with open('ValidTickers.csv', 'w', newline='') as g:
        writer = csv.writer(g)
        for row in reader:
            if not '^' in row[0]:
                writer.writerow(row)