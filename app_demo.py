import mysql.connector

cnx = mysql.connector.connect(
host='localhost',
port=3305,
user='XXX',
password='XXX',
database='XXX'
)
cursor = cnx.cursor(buffered=True)

def print_rows():
    for row in cursor:
        print(*row, sep=', ')
    print()

def print_single_value(start, end="", is_decimal=True):
    for row in cursor:
        if is_decimal:
            answer = round(float(str(row).split("'")[1]))
        else:
            answer = row[0]
        print(start, answer, end)
    print()

def print_wiki_query():
    name = ""
    movies = []
    wiki_pages = []
    total_revenue = 0
    for i, row in enumerate(cursor):
        if i == 0:
            name = row[0]
            print(f"The most profitable director is {name}.")
        movies.append(row[1])
        total_revenue += row[2]
        wiki_pages.append(row[3])
    name = name.split()
    print(f"{name[-1]}'s films made a total revenue of {total_revenue} million dollars:")
    for i in range(len(movies)):
        print(f"{movies[i]} - {wiki_pages[i]}")
    print()

def top_actor_in_each_genre():
    query = '''
WITH topActorGenre AS (
SELECT g.genre, a.actor_id, count(g.film_id) AS numFilms
FROM genres AS g, 
		actors AS a
WHERE g.film_id = a.film_id
GROUP BY g.genre, a.actor_id
ORDER BY numFilms DESC ),

maxInGenre AS (
SELECT top.genre, MAX(numFilms) AS maxNumFilms
FROM topActorGenre AS top
GROUP BY top.genre)

SELECT top.genre, p.name, top.numFilms
FROM maxInGenre AS mg
		JOIN topActorGenre AS top
		JOIN people AS p
		ON mg.maxNumFilms = top.numFilms
		AND mg.genre = top.genre
		AND top.actor_id = p.person_id
WHERE top.numFilms > 1'''
    print("The most popular actors in each genre are:")
    print("(Genre, Actor, #movies in this genre)")
    cursor.execute(query)
    print_rows()

def avg_len_of_top_10_percentile(x):
    query = f'''
SELECT AVG(runtime.lengthInMinutes)	AS length
FROM runtime, 
	(
	SELECT titles.film_id as movieID, 
			PERCENT_RANK() OVER (ORDER BY boxOffice.revenue DESC) AS revenueRank
	FROM titles, boxOffice, genres
	WHERE genres.genre = '{x}'
			AND genres.film_id = titles.film_id
			AND titles.film_id = boxOffice.film_id
	) profitableMovies
WHERE runtime.film_id = profitableMovies.movieID
		AND profitableMovies.revenueRank <= 0.1'''
    cursor.execute(query)
    print_single_value("The average length of the top 10 percentile movies is", "minutes.")

def avg_revenue_of_films_about_x(x):
    query = f'''
SELECT AVG(b.revenue) AS averageRevenue
FROM plot AS p 
		JOIN boxOffice AS b 
		ON p.film_id=b.revenue
WHERE MATCH(p.description) 
		AGAINST('{x}' IN NATURAL LANGUAGE MODE)'''
    cursor.execute(query)
    print_single_value(f"The average revenue of films about {x} is", "million dollars.")

def actors_that_were_in_several_top_profitable_films(x):
    query = f'''
WITH topHundredMovies AS 
(
	SELECT t.film_id AS film_id, b.revenue 
	FROM titles AS t, boxOffice AS b
	ORDER BY b.revenue DESC
	LIMIT {x}
)
SELECT p.name AS actor
FROM actors AS a, 
		people AS p, 
		topHundredMovies AS top
WHERE a.film_id = top.film_id
		AND a.actor_id = p.person_id
GROUP BY a.actor_id
HAVING COUNT(a.film_id) > 1'''
    print("Actors that were in several top 100 profitable films are:")
    cursor.execute(query)
    print_rows()

def how_many_films_of_x_got_score_above_y_on_imdb(x, y):
    query = f'''
SELECT COUNT(i.film_id) AS cnt
FROM imdb AS i
		JOIN directors AS d
		JOIN people AS p
		ON i.film_id=d.film_id
		AND p.person_id=d.director_id
WHERE i.film_id=d.film_id
		AND i.score >= {y}
		AND p.name = "{x}"
GROUP BY d.director_id;'''
    cursor.execute(query)
    print_single_value(f"{x} made", f"films that got score of {y} or above on IMDB.", is_decimal=False)

def wiki_page_of_films_made_by_most_profitable_director():
    query = '''
with topDirector AS (
SELECT d.director_id
FROM directors AS d
		JOIN boxOffice AS b
		JOIN titles AS t
		ON b.film_id=d.film_id
		AND t.film_id=d.film_id
GROUP BY d.director_id
ORDER BY SUM(b.revenue) DESC
LIMIT 1 )
SELECT p.name, t.title, b.revenue, w.url
FROM topDirector AS top
		JOIN directors AS d
		JOIN titles AS t
		JOIN boxOffice AS b
		JOIN wiki AS w
        JOIN people AS p
		ON top.director_id = d.director_id
		AND d.film_id=t.film_id
		AND d.film_id=w.film_id
		AND d.film_id=b.film_id
        AND top.director_id=p.person_id
ORDER BY b.revenue DESC'''
    cursor.execute(query)
    print_wiki_query()

def best_actors_to_work_with_for_each_director():
    query = '''
WITH topConnections AS (
SELECT d.director_id, a.actor_id, COUNT(*) AS cnt
FROM directors AS d
		JOIN actors AS a
		ON d.film_id=a.film_id
GROUP BY d.director_id, a.actor_id
HAVING cnt > 2)
SELECT p1.name AS directorName, p2.name AS actorName, tc.cnt
FROM topConnections AS tc
		JOIN people AS p1
		JOIN people AS p2
		ON tc.director_id = p1.person_id
		AND tc.actor_id = p2.person_id
ORDER BY directorName, cnt DESC'''
    print("For each director, the best actors to work with are:")
    print("(Director, Actor, #movies together)")
    cursor.execute(query)
    print_rows()

def main():
    #query 1
    #assume our client wants to create new movies in each genre for next year.
    #for profitable casting purposes
    #the clients wants to know who are the most popular actors in any genre
    top_actor_in_each_genre()
    #query 2
    #the client want to cast popular actors that will benefit her next movie boxoffice.
    #therefore she wants to cast actors that were in the top X profitable films.
    actors_that_were_in_several_top_profitable_films(100)
    #query 3
    #We believe that a good film is created through good collaborations, 
    #and therefore we recommend that the client choose for the film team 
    #people who have already worked together successfully several times. 
    #Therefore, we present to the client for each director, 
    #which actors work with him the most,
    #so that the client can choose a team of director and main actors in a holistic way.
    best_actors_to_work_with_for_each_director()
    #query 4
    #The client wants her film to get positive reviews. 
    #From a list of directors nominated to direct the film, 
    #she wants to check how many films a director has received a score of Y or higher on IMDB.
    #for example: how many films director Peter Jackson has received a score of at least 8.
    how_many_films_of_x_got_score_above_y_on_imdb("Peter Jackson", 8)
    #query 5
    #The client wants to start a series of films with the same director. 
    #To that end she wants to know who the director whose films are most profitable overall 
    #and read about these films to understand what they have in common.
    wiki_page_of_films_made_by_most_profitable_director()
    #query 6
    #the client needs to decide what is the best length 
    #for her forcasted best selling movies that in an initial making.
    #thus, for example, the clients wants to know what is 
    #the average length of the top 10 percentile profitable movies in the action genre:
    avg_len_of_top_10_percentile("Action")
    #query 7
    #the client wants to decide the general storyline for her next movie
    #she wants to know what the profit is of movies that deal with the subject of x.
    #for example she is considering making a war movie:
    avg_revenue_of_films_about_x("war")
    cnx.close()
    
if __name__ == '__main__':
    main()