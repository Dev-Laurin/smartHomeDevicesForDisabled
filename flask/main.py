from flask import (Flask, render_template, request, 
	url_for, redirect, flash)
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

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

	device = db.relationship('Device',
	 backref='devicecategory', lazy=True)

# class assistivetechrating(db.Model):
# 	def __str__(self):
# 		return "<ATR %r>" % self.name 

# 	id = db.Column(db.Integer, primary_key=True)
	
class paymentoccurence(db.Model):
	def __str__(self):
		return  self.name 

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=False)
	device = db.relationship('Device', 
		backref='paymentoccurence', lazy=True)

homecategories = db.Table('homecategories',
	db.Column('homecategory_id', db.Integer, db.ForeignKey('homecategory.id'), primary_key=True),
	db.Column('device_id', db.Integer, db.ForeignKey('device.id'), primary_key=True))

class homecategory(db.Model): 
	def __str__(self):
		return self.name 

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(90), nullable=False)

class Device(db.Model):
	def __str__(self):
		return self.name 

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
	homecategories = db.relationship('homecategory', 
		secondary=homecategories, lazy='subquery',
		backref=db.backref('devices', lazy=True))
	# atp_rating_id = db.Column(db.Integer, 
	# 	db.ForeignKey('assistivetechrating.id'),
	# 	nullable=False)

	effectiveness_rating = db.Column(db.Integer, nullable=False)
	narrative = db.Column(db.String(500), nullable=False)

#Routing 
@app.route('/', methods=["GET", "POST"])
def list(name=None):
	categories = devicecategory.query.all()
	devices = Device.query.all() 
	homecategories = homecategory.query.all()

	#Refiltering devices
	if request.method == 'POST':
		#find all the compatible devices
		
		deviceCats = request.form.getlist('inputCat[]')
		if deviceCats: 
			devices = []
		for dc in deviceCats: 
			deviceCat = devicecategory.query.filter_by(name=dc).first()
			devices.extend(Device.query.filter_by(category_id=deviceCat.id).all())

	return render_template('list.html', devices=devices, 
		categories=categories, homecategories=homecategories)

@app.route('/createDevice', methods=["GET", "POST"])
def createDevice(name=None):
	po = paymentoccurence.query.all()
	dc = devicecategory.query.all()
	if request.method == 'POST':
		po = paymentoccurence.query.filter_by(name=request.form.get('payment_occurence')).first()
		dc = devicecategory.query.filter_by(name=request.form.get('device_category')).first()
		db.session.add(Device(name=request.form.get('name'), 
			description=request.form.get('desc'), 
			price=request.form.get('price'),
			recurring_price=request.form.get('recurring_price'),
			payment_occurence_id=po.id, 
			link=request.form.get('link'),
			category_id=dc.id, 
			effectiveness_rating=request.form.get('effectiveness_rating'),
			narrative=request.form.get('narrative')
			))
		db.session.commit()
		return redirect(url_for('list'))
	return render_template('create_device.html', po=po, deviceCat=dc)

@app.route('/showDevices', methods=["POST"])
def showDeviceOnCategory(name=None):
	#get devices with compatible home categories
	print(request.form)
	print(request.form.get('homecategory')) 
	homeCat = homecategory.query.filter_by(name=request.form.get('homecategory')).first()
	print(homeCat)
	devices = Device.query.all() 
	deviceCats = request.form.getlist('inputCat[]')
	print(deviceCats)
	if deviceCats: 
		devices = []
	for dc in deviceCats: 
		deviceCat = devicecategory.query.filter_by(name=dc).first()
		devices.extend(Device.query.join(devicecategory,
			homecategories).filter(
			category_id=deviceCat.id).filter(
			homecategory_id==homeCat).all())

	return render_template('list_devices_by_category.html', 
		devices=devices, category=homeCat.name)

@app.route('/editCategories')
def editCategories(name=None):
	deviceCat = devicecategory.query.join(Device).filter(Device.category_id==devicecategory.id).all()
	return render_template('categories.html', deviceCat=deviceCat)

if __name__ == '__main__':
	app.run()