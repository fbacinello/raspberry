import csv

f = open("prueba.csv", "w", newline="")
rc = csv.writer(f)

rc.writerow("")
