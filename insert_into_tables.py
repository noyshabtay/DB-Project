from os import read
import mysql.connector
import csv

def standard_insert_to_table(cnx, cursor, reader, table_name,  table_attribute, row_index):
    i = 1
    for row in reader:
        if i%100 == 0:
            print(f"row {i} in film_id {row[0]}")
        i += 1
        query_execution(cnx, cursor, table_name,  table_attribute, row[0], row[row_index])

def people_insert_to_table(cnx, cursor, reader, table_name,  table_attribute, row_index):
    d = create_people_dictionary() # the dict holding the mapping: d['people_name'] = id
    i = 1
    for row in reader:
        for attribute in row[row_index].split(', '):
            person_id = d[attribute]
            if i%100 == 0:
                print(f"row {i} in film_id: {row[0]} on person: {attribute} with person_id: {person_id}")
            i += 1
            if person_id == '8874':
                return
            query_execution(cnx, cursor, table_name,  table_attribute, row[0], person_id)

def genre_insert_to_table(cnx, cursor, reader, table_name,  table_attribute, row_index):
    i = 1
    for row in reader:
        for attribute in row[row_index].split(', '):
            if i%100 == 0:
                print(f"row {i} in film_id {row[0]}")
            i += 1
            query_execution(cnx, cursor, table_name,  table_attribute, row[0], attribute)

def query_execution(cnx, cursor, table_name,  table_attribute, id, attribute, table_id="film_id"):
    if attribute == 'NULL':
        return
    query = (f"INSERT INTO {table_name} ({table_id}, {table_attribute}) VALUES (%s, %s)")
    cursor.execute(query, (id, attribute))
    cnx.commit()

def create_people_dictionary():
    d = {}
    with open('people_list.csv', 'r', encoding='utf8',newline='') as input_csv:
        reader = csv.reader(input_csv, delimiter=',', skipinitialspace=True)
        for row in reader:
            id = row[0]
            name = row[1]
            d[name] = id
    return d

def upload_people_table(cnx):
    with open('people_list.csv', 'r', encoding='utf8',newline='') as input_csv:
        reader = csv.reader(input_csv, delimiter=',', skipinitialspace=True)
        cursor = cnx.cursor(buffered=True)
        table_name = "people"
        table_id = "person_id"
        table_attribute = "name"
        print(f"working on table: {table_name}")
        i = 1
        for row in reader:
            id = row[0]
            name = row[1]
            if i%100 == 0:
                print(f"in row {i} uploading person: {name} with id: {id}")
            query_execution(cnx, cursor, table_name,  table_attribute, id, name, table_id)
            i += 1
    cnx.close()
    print(f"finished uploading to table: {table_name}")

def main():
    cnx = mysql.connector.connect(
    host='localhost',
    port=3305,
    user='XXX',
    password='XXX',
    database='XXX'
    )
    
    upload_people_table(cnx)
    
    with open('movies_data_combined.csv', 'r', encoding='utf8',newline='') as input_csv:
        reader = csv.reader(input_csv, delimiter='|', skipinitialspace=True)
        cursor = cnx.cursor(buffered=True)
        tables = [("titles", "title", 1), ("genres", "genre", 6), ("boxOffice", "revenue", 18), ("wiki", "url", 19), ("runtime", "lengthInMinutes", 5), ("imdb", "score", 15), ("plot", "description", 10), ("directors", "director_id", 7), ("writers", "writer_id", 8), ("actors", "actor_id", 9)]
        for table in tables:
            print(f"working on table: {table[0]}")
            if table[2] == 6:
                genre_insert_to_table(cnx, cursor, reader, table[0], table[1], table[2])
            elif table[2] in [7, 8, 9]:
                people_insert_to_table(cnx, cursor, reader, table[0], table[1], table[2])
            else:
                standard_insert_to_table(cnx, cursor, reader, table[0], table[1], table[2])
            print(f"finished uploading to table: {table[0]}")
    cnx.close()

if __name__ == '__main__':
    main()