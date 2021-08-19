from models import request


class service:
    def __init__(self):
        self.request = request()

    def getList(self, location, movie, theater, screen, seat):
        if location != "":
            result = self.request.getMovieByLocation(location)

            return result
        elif movie != "":
            result = self.request.getTheatreByMovies(movie)

            return result

    def createUser(self, username, password):
        self.request.createUser(username, password)

    def validateUser(self, username, password):
        return self.request.validateUser(username, password)

    def bookTicket(self, location, movie, theater, screen, seat, showtime, logged_in_user):
        return self.request.bookTicket(location, movie, theater, screen, seat, showtime, logged_in_user)
