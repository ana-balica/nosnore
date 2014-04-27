import csv


def add_row(filename, row):
    with open(filename, "a") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(row)


def add_rows(filename, rows):
    with open(filename, "a") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerows(rows)
