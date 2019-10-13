from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)

	def __repr__(self):
		return '<User %r>' % self.username 

class Device(db.Model):
	def __str__(self):
		return '<Device %r>' % self.name 

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)
	description = db.Column(db.String(500), nullable=False)
	price = db.Column(db.Integer)
	payment_occurence = db.relationship('Payment_Occurence', 
		backref='device', lazy=True)
	link = db.Column(db.String(), nullable=False)
	category = db.relationship('Device_Category',
	 backref='device', lazy=True)
	atp_rating = db.relationship('Assistive_Tech_Rating', 
		backref='device', lazy=True)
	community_rating = db.relationship('Community_Rating',
		backref='device', lazy=True)

class Disability(db.Model):
	def __str__(self):
		return '<Disability %r>' % self.name 

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)
	disability_category = db.relationship('Disability_Category',
		backref='disability', lazy=True)

class Disability_Category(db.Model):
	

@app.route('/')
def main():
    return render_template('form.html')

if __name__ == '__main__':
    app.run()