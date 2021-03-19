from app import db

class Button(db.Model):
    # id is the ID for the DB table
    id = db.Column(db.Integer, primary_key=True)
    # button_name is the value displayed on the button as the name of the button
    button_name = db.Column(db.String(64), index=True, unique=True)
    # button_id is the unique id of the button on the webpage. 
    # This property would be needed for JS to update the DOM on loading the data from the DB.
    button_web_id = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<Button {}>'.format(self.button_name)  
