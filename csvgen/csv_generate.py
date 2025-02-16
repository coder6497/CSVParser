import random, csv

count = int(input())
names = ["James", "Kate", "John", "Alex", "Mohammad", "Alexey", "Semyon", "Misha"]
data = [[i+1, random.choice(names), random.randint(14, 60), round(random.uniform(1, 100), 3), random.randint(1000, 10000)] for i in range(count)]

with open("peoples.csv", "w") as f:
    headers = ["id", "name", "age", "score", "salary"]
    csvwriter = csv.writer(f, delimiter=';')
    csvwriter.writerow(headers)
    for row in data:
        csvwriter.writerow(row)
f.close()
