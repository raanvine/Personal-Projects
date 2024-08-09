""" INST326 Final Project Deliverable

 Purpose: Having trouble finding a movie to watch? Use this program that 
          will recommmend you different movies based on your search 
          preferance of searching by the movie genre and actor.

 """

import requests
from bs4 import BeautifulSoup
import time
import unittest


class Movie:
    """ A Movie class that stores data for a particular movie
     
     Attributes:
         title (str): The title of the movie
         genre (str): The genre of the movie
         summary (str): The summary/description of the movie
         actors (list): A list of actors starring in the movie

     """

    def __init__(self, title, genre, summary, actors):
         """ Initializes the attributes used for the Movie class
         
         Args:
             title (str): The title of the movie
             genre (str): The genre of the movie
             summary (str): The summary/description of the movie
             actors (list): A list of actors in the movie

         """

         self.title = title
         self.genre = genre
         self.summary = summary
         self.actors = actors

    def __str__(self):
        """ A function which puts the title, genre, summary, and lead actor into a formmated string"

        Side-effects:
            f-string (str): An f-string which formats the result for the movie

        """

        return f"{self.title} ({self.genre}) - {self.summary}\nLead Actor: {self.actors}\n"


    def scrape_movies(genre):
        """ Scrape movie from website and returns movie
     
        Args:
            genre (str): The genre that is being scraped
        
        Returns:
            movie (list): A list which contains a movie extracted from the website

        """

        movies = [] 
        url = 'https://www.imdb.com/search/title/?title_type=feature&genres={}&start={}' 
        databasepage = 1

        while databasepage <= 10: 
            resp = requests.get(url.format(genre, (databasepage-1)*50)) 

            if resp.status_code != 200: 
                break

            resp = requests.get(url.format(genre, databasepage*50)) 
            s = BeautifulSoup(resp.content, 'html.parser') 

            titles = [tit.get_text().strip() for tit in s.select('.lister-item-header a')]
            genres = [gen.get_text().strip() for gen in s.select('.genre')]
            summaries = [summ.get_text().strip() for summ in s.select('.ratings-bar+ .text-muted')]
            actors = [act.get_text().strip() for act in s.select('.lister-item-content .ghost + a')]
        
            movies += [Movie(tit, gen, summ, act) for tit, gen, summ, act in zip(titles, genres, summaries, actors)]

            if s.select('.lister-page-next.disabled'): 
                break

            databasepage+=1 
            time.sleep(5)

        return movies 



    def extractGenres(genre, movies):
         """ Extracts movies with same genres from a url
         
         Args:
             genre (str): The genre to that is being searched for
         
         Returns:
             genre (list): A list of movies that have the same genre searched for 

         """

         genre_movies = []
         for movie in movies:
             if genre in movie.genre:
                genre_movies.append(movie)
         return genre_movies


    def extractMovieActors(actor, movies):
        """Extracts movies of a user-specified actor/actress
         
         Args:
             actors (str): The name of the actor that is being looked for from the url
             movies (str): The movies which the actor is in
         
         Returns:
             actor-movie (list): A list of movies that match the actor which is picked

         """

        actor_movies = []

        for movie in movies:
            if actor in movie.actors:
                actor_movies.append(movie)
        return actor_movies


    def userChoice():
        """ Prompts the user for favorite genre and actor/actress
     
        Returns:
            genre (str): The genre that the user chose
            actor (str): The actor that the user chose

        """

        genre = input("Enter your desired genre: ")
        actor = input("Enter your preferred actor/actress: ")

        return genre, actor


    def movieRecs(genre, actor):
        """ Recommends movies based on the user's preferred genre and actor/actress

        Args:
            genre (str): The movie genre searched for
            actor (str): The actor searched for
        
        Returns:
            movies (list): A list of recommended movies that match the users choice

        """

        url = 'https://www.imdb.com/search/title/?title_type=feature&genres={}&start={}'

        movies = Movie.scrape_movies(genre)

        if genre:
            movies = Movie.extractGenres(genre, movies)

        if actor:
            movies = Movie.extractMovieActors(actor, movies)

        return movies


def main():
    """ The main method pulls all of the methods and functions to runs the code

    Side-effects:
        print (str): The recommended movies are printed

    """
    print("\nTo run the progrm enter a genre such as 'Action' and a actor such as 'Chris Evans' or 'Action' and 'Leonardo DiCaprio")
    print("Once the program has run once, please run it again if you would like to choose a different genre or actor\n")

    genre, actor = Movie.userChoice()
    movies = Movie.movieRecs(genre, actor)

    print('\nRecommended Movies:')
    for movie in movies:
        print(movie)


if __name__ == '__main__':
    main()


"""Unit test for extractMovieActors"""
def test_extractMovieActors():
    #Instances of movies
    movie1 = Movie("The Dark Knight", "Action", "Batman fights crime in Gotham City", ["Christian Bale", "Heath Ledger"])
    movie2 = Movie("Interstellar", "Sci-Fi", "A team of astronauts travel through a wormhole", ["Matthew McConaughey", "Anne Hathaway"])
    movie3 = Movie("The Prestige", "Drama", "Two magicians engage in a competitive rivalry", ["Christian Bale", "Hugh Jackman"])
    movie4 = Movie("Inception", "Action", "A thief steals corporate secrets through dream-sharing technology", ["Leonardo DiCaprio", "Tom Hardy"])

    allMovies = [movie1, movie2, movie3, movie4]

    assert Movie.extractMovieActors("Christian Bale", allMovies) == [movie1, movie3]
    assert Movie.extractMovieActors("Angelina Jolie", allMovies) == []

"""Unit test for testscrapeData"""

class TestScrapeData(unittest.TestCase):
    def testscrapeData(self):
        m=Movie.scrape_movies('Horror',1)
        self.assertIsInstance(m,list)
        self.assertTrue(all(isinstance(movie,Movie) for movie in m))
        self.assertEqual(len(m,50))

class test_other_functions:
    """Unit test for userChoice:"""
    assert Movie.userChoice() == {"genre": "comedy", "actor": "Steven Yeun"}
    assert Movie.userChoice() == {"genre": "action", "actor": "Keanu Reeves"}


    """Unit test for movieRecs"""
    assert Movie.movieRecs(genre = "comedy", actor = "Steven Yeun") == "BEEF"
    assert Movie.movieRecs(genre = "action", actor = "Keanu Reeves") == "John Wick: Chapter 4"

    """Unit Test for extractGenres"""
    assert Movie.extractGenres('genre') == 'Horror'