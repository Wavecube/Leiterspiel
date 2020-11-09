from mysql import connector


class Database:
    def __init__(self, username, password, db_name, host="localhost"):
        self._db_name = db_name
        self.__username = username
        self.__password = password
        self.host = host
        self.connection = None
    
    def connect(self):
        self.connection = connector.connect(
            host=self.host,
            database=self._db_name,
            user=self.__username,
            password=self.__password)
        self.cursor = self.connection.cursor()
        print("Database connection established!")

    def execute(self, sql):
        self.cursor.execute(sql)
        self.connection.commit()

    def select(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def close(self):
        if self.connection.is_connected():
            self.connection.close()
            self.cursor.close()
            print("Database conection closed!")


class Executor:
    def __init__(self, database):
        self.db = database
        self.db.connect()

    def saveScore(self, name:str, score:int):
        name_rs = self.db.select("SELECT spieler_id FROM spieler WHERE name = '" + name + "'")

        if self.db.cursor.rowcount == 0:
            self.db.execute("INSERT INTO spieler(name) VALUES('" + name + "')" )
            name_id = self.db.select("SELECT spieler_id FROM spieler WHERE name = '" + name + "'")[0][0]
        else:
            name_id = name_rs[0][0]

        self.db.execute("INSERT INTO highscore_liste(spieler_id, highscore) VALUES(" + str(name_id) + ", " + str(score) + ")")

    def getScores(self):
        return self.db.select("SELECT id, name, highscore FROM highscore_liste INNER JOIN spieler USING(spieler_id) ORDER BY highscore DESC, name  LIMIT 10")


    def close(self):
        self.db.close()