import csv


def csv_data1(title, inf):
    with open("rcd_svr.csv", 'w+', encoding='utf-8', newline='') as data:
        write = csv.writer(data)

        write.writerow(['rows:', title])
        write.writerows(inf)
