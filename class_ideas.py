import mysql.connector
from geopy import distance

yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port=3306,
         database='flight_game',
         user='root',
         password='hus-m',
         autocommit=True)


class Game:
    pointTotal = []
    total_point_num = 0

    def __init__(self):
        #self.id = 0
        #self.player = 'tiia'
        self.guesses = 0
        self.point = 0


    def new_game(self, id, player):
        p = 0
        cursor = yhteys.cursor()
        cursor.execute("INSERT INTO points (id, username, total_points) VALUES ('" + str(id) + "', '" + player + "', '" + str(p) + "')")

    #gets coordinates from database
    def get_location(icao):
        tuple = (icao,)
        sql = '''select latitude_deg, longitude_deg from airport
        where ident = %s'''
        kursori = yhteys.cursor()
        kursori.execute(sql, tuple)
        result = kursori.fetchone()
        return result

    def country_name(answer):
        answer = (answer, )
        cursor = yhteys.cursor()
        cursor.execute("SELECT country FROM data WHERE icao = %s", answer)
        country = cursor.fetchone()
        country = country[0]
        print(country)
        return country

    def check_if_correct(self, id, input, correct, guesses, points):
        guess = int(guesses)
        self.guesses = guess + 1
        self.point = int(points)
        #cursor = yhteys.cursor()
        #cursor.execute("SELECT icao from data WHERE country = %s", input)
        #icao = cursor.fetchone()
        #icao = input
        #print(icao)
        guess_coords = Game.get_location(input)
        correct_coords = Game.get_location(correct)
        print(guess_coords, correct_coords)
        dist = distance.distance(guess_coords, correct_coords).km
        dist = round(dist)
        correct_name = Game.country_name(correct)


        if input == correct:
            check = True
            self.guesses = 5
            msg = f"Correct! You got {points} p!"

        else:
            self.point -= 1
            check = False
            msg = f"Wrong! Guesses left: {self.point}. The distance to the correct country is {dist} km."

        Game.pointTotal.append(self.point)

        if self.guesses == 5:                   # kaikki arvaukset käytetty tai mennyt oikein
            if len(Game.pointTotal) == 1:
                pisteet = Game.pointTotal[0]
            else:
                pisteet = Game.pointTotal[-1]

            Game.total_point_num += pisteet
            Game.pointTotal = []
            # päivittää tietokantaan lopulliset pisteet
            cursor = yhteys.cursor()
            cursor.execute("UPDATE points SET total_points =  " + str(Game.total_point_num) + " WHERE id ='" + id + "'")

        vastaus = {
            "check": check,
            "message": msg,
            "guesses_used_msg": f"Wrong, you got 0 p. The right answer was {correct_name}.",
            "guesses": self.guesses,
            "point": self.point,
            "total_points": Game.total_point_num,
            "distance": dist

        }
        return vastaus
