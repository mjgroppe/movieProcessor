import glob
import sqlite3
import bs4
import mysql.connector

import imdb
import math
from imdb import IMDb
from doesthedogdie import get_info_for_movie
import random
#curl -H 'Accept: application/json' -H 'X-API-KEY: 80555bc07790b790df1f4558e526fa7f' -v -i 'https://www.doesthedogdie.com/search?q=old%20yeller'


marilynRatings = {
"dog dying":8,
"kids dying":8,
"jumpscares":6,
"choking":5,
"people being burned alive":9,
"spiders":5,
"strobe effects":2,
"parents dying":8,
"finger or toe mutilation":9,
"clowns":2,
"shower scenes":2,
"shaving or cutting":9,
"farting or spitting":2,
"shaky cam":2,
"sexual assault":10,
"horses dying":8,
"car crashes":4,
"cats dying":8,
"people dying by suicide":10,
"blood or gore":8,
"animals (besides dog/cat/horse) dying":8,
"needles or syringes are used":6,
"drownings":8,
"hospital scenes":8,
"drug use":5,
"LGBT people dying":8,
"body dysmorphia":6,
"dragons dying":8,
"sexual content":3,
"planes crashing":4,
"self harming":10,
"eye mutilation":9,
"vomiting":5,
"claustrophobic scenes":6,
"torture":8,
"cancer":6,
"electro-thearpy":7,
"seizures":5,
"ghosts":2,
"people getting hit by cars":6,
"Santa (et al) spoilers":1,
"teeth damage":3,
"falling deaths":8,
"hate speech":7,
"bugs":6,
"snakes":3,
"miscarriages":5,
"bones breaking":5,
"eating disorders":8,
"child abuse":10,
"domestic violence":10,
"mental institutions":9,
"nuclear explosions":2,
"unhappy endings":7,
"heads getting squashed":8,
"demonic possession":7,
"alcohol abuse":4,
"misgendering":6,
"hangings":9,
"childbirth":3,
"animal abuse":10,
"addiction":4,
"dog fighting":7,
"gun violence":7,
"fat jokes":2,
"black guy dies first":8,
"anxiety attacks":7,
"incest":10,
"gaslighting":3,
"abortions":2,
"pregnant woman deaths":8,
"buried alive":8,
"cheating":2,
"stalking":6,
"kidnapping":8,
"ableism":5,
"antisemitism":5
}

class movie:
    def __init__(self, title, year):
        if title == "Dope":
            print("bye")
        self.title = title
        self.year = year
        self.i = imdb.IMDb()
        self.movie = None
        self.credits = None
        self.watched = False
        self.ia = IMDb()
        results = self.ia.search_movie(title)
        for el in results:
            if el.data.get('year') == self.year:
                self.movie = el
                s = self.ia.get_movie(el.getID())
                self.genres = s['genres']
                self.id = self.ia.get_imdbID(el)
                try:
                    for i in s['directors']:
                        self.director = i['name']
                        break
                except:
                    self.director = "John Doe"
                break
        if self.movie is None:
            print(results)
            #print("IMDB doesn't have that movie. Check all credentials.")
            return
        self.credits = self.i.get_movie_full_credits(self.movie.movieID)
        self.cw = []
        self.triggerProbability = 0

    def setContentWarnings(self):
        d = get_info_for_movie(self.title)
        if d is None:
            return
        elif len(d) != len(marilynRatings):
            print("Does the dog die? Has updated their categories. Please take a look and consider updating the ratings.")
        else:
            for el in d:
                topic = el.get('topic_short')
                yes = el.get('yes_votes')
                no = el.get('no_votes')
                if yes == 0:
                    pass
                elif yes >= no:
                    self.cw.append(topic)
            sum = 0
            severe = 0
            total = 0
            neg = 0
            for el in marilynRatings.keys():
                total += marilynRatings.get(el)
            for el in self.cw:
                rating = marilynRatings.get(el)
                if rating is None:
                    pass
                else:
                    sum += rating
                    if rating > 7:
                        sum += rating
                        severe += 1
                    elif rating < 4:
                        sum -= (rating/2)
                        neg += 1
            rawRating = sum/total
            rawRating *= 100
            if severe > 0 and rawRating <= 30:
                rawRating += 25
            if neg > 4:
                rawRating /= 2
            self.triggerProbability = rawRating
    def toStr(self):
        #info = self.movie.get_movie_infoset()
        #print(info)
        #print(self.credits)
        self.cw = []
        self.setContentWarnings()
        string = self.title + " (" + str(self.year) + "), directed by "+self.director+'.\n'
        string += "Content warnings: "
        string += str(self.cw)+'.\n'
        string += "Marilyn's uncomfy rating: "
        string += str(math.ceil(self.triggerProbability))+"/"+str(100)
        return string
def searchByTitle(title):
    collection = "SELECT * FROM Movies WITH "
def searchByActor(name):
    pass
def searchByYear(year):
    pass
def searchByTY(title, year):
    pass
def searchByComfort(comfort, range=0, atLeast=False, atMost=False):
    pass
def searchByGenre(genre):
    pass

if __name__ == '__main__':
    exts = ['mp4', 'mkv','avi']
    drives = ['C:', 'D:']
    badTitle = 0
    badMovie = 0
    lst = []
    connection = sqlite3.connect("myTable.db")
    crsr = connection.cursor()
    try:
        crsr.execute("""CREATE TABLE Movies (
        id INTEGER PRIMARY KEY,
        title VARCHAR(100),
        year INTEGER,
        director VARCHAR(100),
        genre VARCHAR(40),
        comfort INTEGER);""")
    except:
        pass
    #create the sql table for the movies
    for ext in exts:
        for drive in drives:
            vids = glob.glob(drive+'\\**\\*.'+ext, recursive=True)
            for vid in vids:
                #print(vid)
                dir = vid.split("\\")
                filename = dir[len(dir)-1]
                ty = filename.split(" (")
                if len(ty) == 1:
                    badTitle += 1
                   #print("This video title does not fit the acceptable movie format of Title (year). Please alter that and try again.")
                else:
                    year = ty[len(ty)-1][:len(ty[len(ty)-1])-5]
                    title = ty[0:len(ty)-2]
                    if title == "Porco Rosso" or title == "Dope":
                        print("hi")
                    try:
                        mov = movie(str(ty[0]), int(year))
                        if mov.movie is None:
                            badMovie += 1
                            lst.append(ty[0] + " " + str(year))
                        else:
                            mov.filepath = vid
                            print(mov.toStr())
                            crsr.execute("INSERT INTO Movies VALUES ("+str(mov.id)+","+mov.title+","+str(mov.year)+","+mov.director+","+mov.genres[0]+","+str(mov.triggerProbability)+");")
                    except:
                        badMovie += 1
                        lst.append(ty[0]+" " +str(year))
                        #insert the movie into the table
    print("There were " + str(badTitle) + " videos with nonconforming titles.")
    print("There were " + str(badMovie) + " videos that IMDB could not locate.")
    crsr.execute("SELECT * FROM Movies")

    # store all the fetched data in the ans variable
    ans = crsr.fetchall()

    # loop to print all the data
    for i in ans:
        print(i)

    connection.commit()
    connection.close()

