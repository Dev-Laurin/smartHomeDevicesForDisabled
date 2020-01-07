from . import db, file_upload

##Database Schema

# class User(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	username = db.Column(db.String(80), unique=True, nullable=False)
# 	email = db.Column(db.String(120), unique=True, nullable=False)

# 	def __repr__(self):
# 		return '<User %r>' % self.username 

class devicecategory(db.Model):
	def __str__(self):
		return self.name 
		
	name = db.Column(db.String(80), nullable=False)
	id = db.Column(db.Integer, primary_key=True)

class paymentoccurence(db.Model):
	def __str__(self):
		return  self.name 
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=False)
	device = db.relationship('Device', 
		backref='paymentoccurence', lazy=True)

devicecategories = db.Table('devicecategories', 
	db.Column('devicecategory_id', db.Integer, 
		db.ForeignKey('devicecategory.id'), primary_key=True),
	db.Column('device_id', db.Integer, 
		db.ForeignKey('device.id'), primary_key=True))

homecategories = db.Table('homecategories',
	db.Column('homecategory_id', db.Integer, 
		db.ForeignKey('homecategory.id'), primary_key=True),
	db.Column('device_id', db.Integer, 
		db.ForeignKey('device.id'), primary_key=True))

@file_upload.Model
class homecategory(db.Model): 
	def __str__(self):
		return self.name 

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(90), nullable=False)
	image = file_upload.Column(db)

@file_upload.Model
class Device(db.Model):
	def __str__(self):
		return self.name 

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)
	description = db.Column(db.String(500), nullable=False)
	price = db.Column(db.Float, nullable=False)
	has_subscription = db.Column(db.Boolean, default=False, 
		nullable=False)
	recurring_price = db.Column(db.Float)
	subscription_description = db.Column(db.String(500))
	payment_occurence_id = db.Column(db.Integer, 
		db.ForeignKey('paymentoccurence.id'))
	link = db.Column(db.String(500), nullable=False)
	devicecategories = db.relationship('devicecategory',
		secondary=devicecategories, lazy='subquery',
		backref=db.backref('devices', lazy=True))
	homecategories = db.relationship('homecategory', 
		secondary=homecategories, lazy='subquery',
		backref=db.backref('devices', lazy=True))
	rating = db.Column(db.Numeric(10,2), nullable=False)
	narrative = db.Column(db.String(500))
	image = file_upload.Column(db)
	warranty_price = db.Column(db.Float)
	warranty_length = db.Column(db.String(80))
