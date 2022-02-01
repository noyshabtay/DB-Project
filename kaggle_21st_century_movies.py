import csv

# wiki_movie_plots_dupped.csv attributes: 
# Release Year, Title, Origin/Ethnicity, Director, Cast, Genre, Wiki Page, Plot

with open('wiki_movie_plots_dupped.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        # Get release year, title, and wiki page of films released in 21st century
        if int(row[0]) >= 2000:
            movies_data = str(row[0]) + '|' + row[1].strip() + '|' + row[6] + '\n'
            # Write specified attributes to output file
            with open("kaggle_21st_century_movies.csv", "a") as file_object:
                file_object.write(movies_data)
