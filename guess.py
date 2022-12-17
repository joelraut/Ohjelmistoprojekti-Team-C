import json

from flask import Flask, request
import requests
from flask_cors import CORS
import mysql.connector
from geopy import distance
import string, random
from game import Game

yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port=3306,
         database='flight_game',
         user='root',
         password='hus-m',
         autocommit=True)

app = Flask(__name__)
cors = CORS(app)


def get_locations():
    cursor = yhteys.cursor()
    cursor.execute("SELECT icao FROM data")
    random_list = cursor.fetchall()
    positions = []
    for i in random_list:
        cursor.execute("SELECT ident, latitude_deg, longitude_deg FROM airport WHERE ident = %s", i)
        position = cursor.fetchall()
        positions.append(position[0])
    return positions


def namae():                                              # uusi
    cursor = yhteys.cursor()
    cursor.execute("SELECT icao FROM data")
    random_list = cursor.fetchall()
    positions = []
    for i in random_list:
        cursor.execute("SELECT country FROM data WHERE icao = %s", i)
        position = cursor.fetchall()
        positions.append(position[0])
    return positions



#   hakee kaikkien maiden icaot
def correct():
    cursor = yhteys.cursor()
    cursor.execute("SELECT icao FROM data")
    right_answer = cursor.fetchall()
    return right_answer

def country_name(answer):
    cursor = yhteys.cursor()
    cursor.execute("SELECT country FROM data WHERE icao = %s", answer)
    country = cursor.fetchone()
    country = country[0]
    print(country)

    return country

#pointTotal = []


@app.route("/loop/<player>")
def loop(player):
    urli = "https://randomuser.me/api/?inc=login"
    response = requests.get(urli).json()
    username = response["results"][0]["login"]["username"]
    player = f"{player}-{username}"
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits   # luodaan pelille id
    id = ''.join(random.choice(letters) for i in range(20))
    game = Game()                                  # luo uuden pelin, lisää tietokantaan
    print(game)
    game.new_game(id, player)
    vastaus = {
        "country_num": 0,
        "locations": get_locations(),
        "id": id,
        "namae": namae(),

    }
    return vastaus


lista = correct()


@app.route("/newCountry/<count>")
def newCountry(count):
    count = int(count)
    answer = random.choice(lista)       # arpoo oikean maan
    lista.remove(answer)                # poistaa ^ listasta

    vastaus = {
        "lista": lista,
        "correct": answer[0],
        "guesses": 0,
        "points": 5,                    # max pisteet alussa 5
        "country_num": count+1,
        "country_name": country_name(answer)

    }
    return vastaus

#   tarkistaa oikein vai väärin
@app.route("/guess/<id>/<input>/<correct>/<guesses>/<points>")
def checking(id, input, correct, guesses, points):
    game = Game()
    vastaus = game.check_if_correct(id, input, correct, guesses, points)
    return vastaus


def get_scoreboard():
    cursor = yhteys.cursor()
    cursor.execute("SELECT id, username, total_points FROM points ORDER BY total_points DESC")
    scoreboard = cursor.fetchall()
    return scoreboard


@app.route("/scoreboard/")
def scoreboard():
    scoreboard = get_scoreboard()
    a = []
    b = []
    c = []
    for i in scoreboard:
        a.append(i[0])
        b.append(i[1])
        c.append(i[2])
    vastaus = {
        "totals": c,
        "usernames": b,
        "ids": a,

    }
    return vastaus

if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=5000)
