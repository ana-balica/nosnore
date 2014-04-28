import csv


def add_row(filename, row):
    with open(filename, "a") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(row)


def add_rows(filename, rows):
    with open(filename, "a") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerows(rows)


def read_feature_rows(filename, sid, ica=False):
    with open(filename, "rb") as f:
        reader = csv.reader(f, delimiter=",")
        features = []
        for row in reader:
            if int(row[0]) == int(sid):
                if ica is False:
                    if row[3] == "False":
                        features.extend([float(row[2])])
                else:
                    if row[3] == "True":
                        features.extend([float(row[2])])

        return features
