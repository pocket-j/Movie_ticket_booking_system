from flask import Flask
from flask import request
from flask import render_template
from models import database
from service import service

app = Flask(__name__)

logged_in_user = ""
logged_in = False


@app.route("/", methods=["GET", "POST"])
def entry():
    global logged_in
    global logged_in_user
    if request.method == "POST":
        # print(request.form)
        if "button" in request.form.keys() and request.form["button"] == "Sign Up":
            return render_template("signup.html")
        elif "button" in request.form.keys() and request.form["button"] == "Login":
            return render_template("login.html")
        elif "button" in request.form.keys() and request.form["button"] == "Continue as Guest":
            return render_template("form.html", status=logged_in)
        elif "Register" in request.form.keys() and request.form["Register"] == "Register":
            username = request.form.get("username")
            password = request.form.get("password")
            service().createUser(username, password)
            return render_template("login.html")
        elif "Login" in request.form.keys() and request.form["Login"] == "Login":
            username = request.form.get("username")
            password = request.form.get("password")
            status = service().validateUser(username, password)
            if status:
                logged_in_user = username
                logged_in = True
                return render_template("form.html", status=logged_in)
            else:
                return render_template("login.html", status=logged_in)
        elif "Search" in request.form.keys() and request.form["Search"] == "Search":
            location = request.form.get("location")
            movie = request.form.get("movie")
            theatre = request.form.get("theatre")
            screen = request.form.get("screen")
            seat = request.form.get("seat")
            res = service().getList(location, movie, theatre, screen, seat)
            return render_template("form.html", output_data=res, status=logged_in)
        elif "Book" in request.form.keys() and request.form["Book"] == "Book":
            location = request.form.get("location")
            movie = request.form.get("movie")
            theatre = request.form.get("theatre")
            screen = request.form.get("screen")
            showtime = request.form.get("showtime")
            seat = request.form.get("seat")
            res = service().bookTicket(location, movie, theatre, screen, seat, showtime, logged_in_user)
            if res:
                res = 1
            else:
                res = 2
            return render_template("form.html", booking_status=res, status=logged_in)
    return render_template("open.html")


'''

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        location = request.form.get("location")
        movie = request.form.get("movie")
        theater = request.form.get("theater")
        screen = request.form.get("screen")
        seat = request.form.get("seat")
        li = [location, movie, theater, screen, seat]
        return render_template("form.html", output_data=li)
    return render_template("form.html")

'''

if __name__ == "__main__":
    database()
    app.run(host="127.0.0.1", port=8080, debug=True)
