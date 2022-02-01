import csv

inp_fname = 'movies_data_combined.csv'
out_fname = 'people_list.csv'
people = set()

with open(inp_fname, 'r', newline='') as in_csvfile:
    reader = csv.reader(in_csvfile, delimiter='|', skipinitialspace=True)

    for row in reader:
        for v in row[7].rstrip(',').split(', '):
            people.add(v)
        for v in row[8].rstrip(',').split(', '):
            people.add(v)
        for v in row[9].rstrip(',').split(', '):
            people.add(v)


print(len(people))
people_list = list(people)

with open(out_fname, 'w', newline='') as out_csvfile:
    writer = csv.writer(out_csvfile)
    
    for index in range(0,len(people_list)):
        writer.writerow([index+1] + [people_list[index]])