from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

##Database Schema

# class User(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	username = db.Column(db.String(80), unique=True, nullable=False)
# 	email = db.Column(db.String(120), unique=True, nullable=False)

# 	def __repr__(self):
# 		return '<User %r>' % self.username 

class disabilitycategory(db.Model):
	def __str__(self):
		return self.name 

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)
	disabilities = db.relationship('Disability',
		backref='disabilitycategory', lazy=True)

class Disability(db.Model):
	def __str__(self):
		return '<Disability %r>' % self.name 

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)
	category_id = db.Column(db.Integer, db.ForeignKey('disabilitycategory.id'),
		nullable=False)
	ATR = db.relationship('assistivetechrating', 
		backref='disability')
	community_rating = db.relationship('communityrating', 
		backref='disability')


class devicecategory(db.Model):
	def __str__(self):
		return '<Device Category %r>' % self.name 
	name = db.Column(db.String(80), nullable=False)
	id = db.Column(db.Integer, primary_key=True)

	device = db.relationship('Device',
	 backref='devicecategory', lazy=True)

class assistivetechrating(db.Model):
	def __str__(self):
		return "<ATR %r>" % self.name 

	id = db.Column(db.Integer, primary_key=True)
	disability_id = db.Column(db.Integer, 
		db.ForeignKey('disability.id'), 
		nullable=False)
	effectiveness_rating = db.Column(db.Integer, nullable=False)
	relevance_rating = db.Column(db.Integer, nullable=False)
	narrative = db.Column(db.String(500), nullable=False)
	device = db.relationship('Device', 
		backref='assistivetechrating', lazy=True)

class communityrating(db.Model):
	def __str__(self):
		return "<CR %r>" % self.name 

	id = db.Column(db.Integer, primary_key=True)
	description = db.Column(db.String(500), nullable=False)
	title = db.Column(db.String(50), nullable=False)
	rating = db.Column(db.Integer, nullable=False)
	disability_id = db.Column(db.Integer, 
		db.ForeignKey('disability.id'), 
		nullable=False)
	device = db.relationship('Device',
		backref='communityrating', lazy=True)

class paymentoccurence(db.Model):
	def __str__(self):
		return "<PO %r>" % self.name 

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=False)
	device = db.relationship('Device', 
		backref='paymentoccurence', lazy=True)

class Device(db.Model):
	def __str__(self):
		return '<Device %r>' % self.name 

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)
	description = db.Column(db.String(500), nullable=False)
	price = db.Column(db.Float)
	recurring_price = db.Column(db.Float)
	payment_occurence_id = db.Column(db.Integer, 
		db.ForeignKey('paymentoccurence.id'),
		nullable=False)
	link = db.Column(db.String(), nullable=False)

	category_id = db.Column(db.Integer, 
		db.ForeignKey('devicecategory.id'),
		nullable=False)
	atp_rating_id = db.Column(db.Integer, 
		db.ForeignKey('assistivetechrating.id'),
		nullable=False)
	community_rating_id = db.Column(db.Integer, 
		db.ForeignKey('communityrating.id'),
		nullable=False)

##Routing 
@app.route('/')
def main(name=None):
	disCat = disabilitycategory.query.all()
	return render_template('form.html', disCat=disCat)

# @app.route('/listDevices'):
# def list(name=None):
# 	devices = 
# 	return render_template('list.html', devices=devices)

if __name__ == '__main__':
	app.run()