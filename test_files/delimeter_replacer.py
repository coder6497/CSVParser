import csv

data = []
filename = input("Введите название файла (без .csv):\n")
delimeter = input("Введите разделитель: ")

with open(f'{filename}.csv', "r") as f:
    reader = csv.reader(f, delimiter=delimeter)
    for elem in reader:
        data.append(elem)

with open(f"{filename}_copy.csv", "w") as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerows(data)