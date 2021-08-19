import sqlite3


class database:
    def __init__(self):
        self.conn = sqlite3.connect('movies.db')
        self.create_database()
        self.populate_database()

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def create_database(self):
        self.create_table_users()
        self.create_table_movies()
        self.create_table_booking()

    def populate_database(self):
        self.insert_movies()

    def create_table_users(self):
        query = """
                CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT
                );
                """
        self.conn.execute(query)

    def create_table_movies(self):
        query = """DROP TABLE IF EXISTS Movies"""
        self.conn.execute(query)
        query = """
                CREATE TABLE IF NOT EXISTS Movies (
                movie_name TEXT ,
                theatre_name TEXT,
                location TEXT,
                screen TEXT,
                showtime TEXT,
                available_seats text,
                id INTEGER PRIMARY KEY AUTOINCREMENT
                );
                """
        self.conn.execute(query)

    def create_table_booking(self):
        query = """
                CREATE TABLE IF NOT EXISTS booking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT,
                movie_name TEXT,
                theatre_name TEXT,
                location_name TEXT,
                showtime TEXT,
                screen TEXT,
                seat_number TEXT
                );
                """
        self.conn.execute(query)

    def insert_movies(self):
        query = """
                INSERT INTO Movies (movie_name,theatre_name,location,screen, showtime,available_seats)
                VALUES 
                ('Shershaah', 'PVR', 'Bangalore', 'A', '13:30', '1,2,3,4,5'),
                ('Shershaah', 'Inox', 'Bangalore', 'A', '20:00', '1,2,3,4,5'),
                ('Shershaah', 'Gopalan', 'Bangalore', 'A', '21:30', '1,2,3,4,5'),
                ('Shershaah', 'ABC', 'Bangalore', 'A', '11:30', '1,2,3,4,5'),                
                ('Mimi', 'Suresh', 'Bangalore', 'C', '21:00', '1,2,3,4,5'),
                ('Oxygen', 'Inox', 'Bangalore', 'A', '20:30', '11,12,13,14,15'),
                ('Nizhal', 'PVR', 'Hyderabad', 'C', '9:30', '1,2,3,4,5'),
                ('Pagglait', 'Inox', 'Hyderabad', 'B', '11:30', '11,12,13,14,15'),
                ('Master', 'PVR', 'Hyderabad', 'A', '13:30', '1,2,3,4,5'),
                ('Joji', 'Suresh', 'Bangalore', 'C', '21:00', '1,2,3,4,5'),
                ('Sherni', 'Inox', 'Bangalore', 'B', '20:30', '11,12,13,14,15'),
                ('Dia', 'PVR', 'Hyderabad', 'A', '9:30', '1,2,3,4,5'),
                ('Choked', 'Inox', 'Hyderabad', 'B', '11:30', '11,12,13,14,15');
        
                """
        self.conn.execute(query)


class request:

    def __init__(self):
        self.conn = sqlite3.connect("movies.db")
        self.conn.row_factory = sqlite3.Row

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def getMovieByLocation(self, location):
        query = "select movie_name, theatre_name, location,showtime, screen, available_seats from Movies where " \
                f"location = '{location}';"

        result_set = self.conn.execute(query).fetchall()
        result = [{column: row[i]
                   for i, column in enumerate(result_set[0].keys())}
                  for row in result_set]
        return result

    def getTheatreByMovies(self, movie_name):
        query = "select movie_name, theatre_name, location, showtime, screen, available_seats" \
                " from Movies where " \
                f"movie_name = '{movie_name}';"
        result_set = self.conn.execute(query).fetchall()
        result = [{column: row[i]
                   for i, column in enumerate(result_set[0].keys())}
                  for row in result_set]
        return result

    def createUser(self, username, password):
        query = f'insert into user ' \
                f'(username, password) ' \
                f'values ("{username}","{password}")'
        self.conn.execute(query)

    def validateUser(self, username, password):
        query = "select * from user where " \
                f"username = '{username}' and password = '{password}';"
        result_set = self.conn.execute(query).fetchall()
        if len(result_set) == 0:
            return False
        return True

    def createEntry(self, location, movie_name, theatre, screen, seat, showtime, logged_in_user):
        query = "INSERT INTO booking (user_name, movie_name, " \
                "theatre_name, location_name, showtime, screen, seat_number)" \
                " VALUES " \
                f"('{logged_in_user}', '{movie_name}', '{theatre}', " \
                f"'{location}', '{showtime}', '{screen}', '{seat}') ;"
        self.conn.execute(query)

    def updateMovies(self, location, movie_name, theatre, screen, seat, showtime):
        query = "update Movies " \
                f"set  available_seats = '{seat}' where " \
                f"location = '{location}' " \
                f"and movie_name = '{movie_name}' " \
                f"and theatre_name = '{theatre}' " \
                f"and screen = '{screen}' " \
                f"and showtime = '{showtime}' ;"

        self.conn.execute(query)

    def bookTicket(self, location, movie_name, theatre, screen, seat, showtime, logged_in_user):
        query = "select movie_name, theatre_name, location, showtime, screen, available_seats" \
                " from Movies where " \
                f"location = '{location}' " \
                f"and movie_name = '{movie_name}' " \
                f"and theatre_name = '{theatre}' " \
                f"and screen = '{screen}' "\
                f"and showtime = '{showtime}' ;"

        result_set = self.conn.execute(query).fetchall()
        if len(result_set) != 1:
            return False
        s = result_set[0]["available_seats"]
        li = s.split(",")
        if seat not in li:
            return False
        self.createEntry(location, movie_name, theatre, screen, seat, showtime, logged_in_user)
        li.remove(seat)
        s = ','.join(li)
        self.updateMovies(location, movie_name, theatre, screen, s, showtime)

        return True
