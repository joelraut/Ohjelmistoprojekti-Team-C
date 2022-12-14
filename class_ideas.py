import mysql.connector

yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port=3306,
         database='flight_game',
         user='root',
         password='2002',
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


    def check_if_correct(self, id, input, correct, guesses, points):
        guess = int(guesses)
        self.guesses = guess + 1
        self.point = int(points)

        if input == correct:
            check = True
            self.guesses = 5
            msg = f"Correct! You got {points} p!"

        else:
            self.point -= 1
            check = False
            msg = f"Wrong! Guesses left: {self.point}."

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
            "guesses": self.guesses,
            "point": self.point,
            "total_points": Game.total_point_num

        }
        return vastaus