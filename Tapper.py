from google.appengine.ext import db

# A Tapper is a player who taps
class Tapper(db.Model):
    # The Facebook UID of the player
    facebook_uid = db.IntegerProperty(required = True)
    
    # The creation date of the profile
    creation_date = db.DateTimeProperty(required = True, auto_now_add=True)
    
    # The latest time the tapper logged in
    login_date = db.DateTimeProperty(required = True, auto_now=True)
    
    # The highest score of the tapper
    score = db.IntegerProperty()
    
    # The date when the highest score of the tapper was saved
    score_time = db.DateTimeProperty()
