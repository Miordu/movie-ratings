"""CRUD operations."""
from model import db, User, Movie, Rating, connect_to_db

def create_user(email, password):
    """Create and return a new user."""
    user = User(email=email, password=password)
    
    db.session.add(user)
    db.session.commit()
    
    return user

def create_movie(title, overview, release_date, poster_path):
    """Create and return a new movie."""
    movie = Movie(
        title=title,
        overview=overview,
        release_date=release_date,
        poster_path=poster_path,
    )
    
    db.session.add(movie)
    db.session.commit()
    
    return movie

def get_movies():
    """Return all movies."""
    return Movie.query.all()

def get_movie_by_id(movie_id):
    """Return a movie by primary key."""
    return Movie.query.get(movie_id)

def get_users():
    """Return all users."""
    return User.query.all()

def get_user_by_id(user_id):
    """Return a user by primary key."""
    return User.query.get(user_id)
if __name__ == '__main__':
    from server import app
    connect_to_db(app)