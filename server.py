"""Server for movie ratings app."""
from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """View homepage."""
    return render_template('homepage.html')

@app.route("/movies")
def all_movies():
    """View all movies."""
    movies = crud.get_movies()
    return render_template("all_movies.html", movies=movies)

@app.route("/movies/<movie_id>")
def show_movie(movie_id):
    """Show details on a particular movie."""
    movie = crud.get_movie_by_id(movie_id)
    return render_template("movie_details.html", movie=movie)

@app.route("/users")
def all_users():
    """View all users."""
    users = crud.get_users()
    return render_template("all_users.html", users=users)

@app.route("/users/<user_id>")
def show_user(user_id):
    """Show details on a particular user."""
    user = crud.get_user_by_id(user_id)
    return render_template("user_details.html", user=user)

@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""
    
    email = request.form.get("email")
    password = request.form.get("password")
    
    user = crud.get_user_by_email(email)
    
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(email, password)
        flash("Account created! Please log in.")
        
    return redirect("/")

@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""
    
    email = request.form.get("email")
    password = request.form.get("password")
    
    user = crud.get_user_by_email(email)
    
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        flash(f"Logged in as {user.email}!")
        
    return redirect("/")

@app.route("/movies/<movie_id>/ratings", methods=["POST"])
def create_movie_rating(movie_id):
    """Create a new rating for the movie."""
    
    # Get the rating score from the form
    score = int(request.form.get("rating"))
    
    # Get the logged-in user's email from the session
    user_email = session.get("user_email")
    
    if user_email is None:
        flash("You must be logged in to rate a movie.")
        return redirect("/")
        
    # Get the user and movie objects
    user = crud.get_user_by_email(user_email)
    movie = crud.get_movie_by_id(movie_id)
    
    # Create the rating
    rating = crud.create_rating(user, movie, score)
    db.session.add(rating)
    db.session.commit()
    
    flash(f"You rated {movie.title} {score} out of 5.")
    
    return redirect(f"/movies/{movie_id}")

@app.route("/logout")
def logout():
    """Log out a user."""
    
    session.pop("user_email", None)
    flash("Logged out.")
    
    return redirect("/")

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True, port=6060)