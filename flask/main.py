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

#initialize database -- delete when in production!!!
db.drop_all()
db.create_all()
po = paymentoccurence(name="Once")
db.session.add(po)
db.session.commit()
pom = paymentoccurence(name="Monthly")
db.session.add(pom)
db.session.commit()
dct = devicecategory(name="Touch")
db.session.add(dct)
db.session.commit()
dc = devicecategory(name="Switch")
db.session.add(dc)
db.session.commit()
dc = devicecategory(name="Voice")
db.session.add(dc)
db.session.commit()
hc = homecategory(name="Security")
db.session.add(hc)
db.session.commit()
hcd = homecategory(name="Door")
db.session.add(hcd)
db.session.commit()
hc = homecategory(name="Lights")
db.session.add(hc)
db.session.commit()
device = Device(name="Philips Hue White and Color Wireless Ambiance Starter Kit A19",
	description="Choose between millions of colors and shades of white light to light your home, wirelessly control with your smartphone or tablet, and sync your light immersively to music, games, and movies. ",
	price=199.95, recurring_price=0.00, payment_occurence_id=po.id, 
	link="http://www.amazon.com/gp/product/B014H2P4KW?redirect=true&ref_=s9_acss_bw_cg_ESHPhili_4a1",
	category_id=dc.id, effectiveness_rating=3, narrative="Gives you the ability to activate lights with voice commands.")
device.homecategories.append(hc)
db.session.add(device)
db.session.commit()
device = Device(name="Brilliant One Switch Panel",
	description="Transform your house or apartment into an easy-to-use smart home with the award-winning Brilliant Smart Home Control and all-in-one mobile app. Instantly gain control over all your smart home products via a single app and display that simply installs in place of any light switch. No more hubs, ugly wires, countertop clutter, or switching multiple apps.",
	price=299.99, recurring_price=0.00, payment_occurence_id=po.id, 
	link="https://www.brilliant.tech/products/brilliant-control-two-switch-smart-lighting-smart-home-control?variant=white",
	category_id=dct.id, effectiveness_rating=4.7, narrative="Gives you the ability to activate lights via a phone app.")
device.homecategories.append(hc)
db.session.add(device)
db.session.commit()
device = Device(name="Ring Doorbell Video",
	description="Get instant alerts when visitors press your Doorbell or trigger the built-in motion sensors. Then use the free Ring app to see, hear and speak to guests from your smartphone, tablet or PC.",
	price=99.99, recurring_price=17.00, payment_occurence_id=pom.id, 
	link="https://shop.ring.com/collections/video-doorbells//products/video-doorbell",
	category_id=dct.id, effectiveness_rating=4.7, narrative="Gives you the ability to activate lights via a phone app.")
device.homecategories.append(hcd)
db.session.add(device)
db.session.commit()
#---------------------------------------

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
			devicesFound = devicecategory.query.with_parent(device).all()
			devices.extend(devicesFound)

	return render_template('list.html', devices=devices, 
		categories=categories, homecategories=homecategories)

@app.route('/createDevice', methods=["GET", "POST"])
def createDevice(name=None):
	po = paymentoccurence.query.all()
	dc = devicecategory.query.all()
	hc = homecategory.query.all()
	if request.method == 'POST':
		po = paymentoccurence.query.filter_by(name=request.form.get('payment_occurence')).first()
		dc = devicecategory.query.filter_by(name=request.form.get('device_category')).first()
		device = Device(name=request.form.get('name'), 
		description=request.form.get('desc'), 
		price=request.form.get('price'),
		recurring_price=request.form.get('recurring_price'),
		payment_occurence_id=po.id, 
		link=request.form.get('link'),
		category_id=dc.id, 
		effectiveness_rating=request.form.get('effectiveness_rating'),
		narrative=request.form.get('narrative')
		)
		#add homecategories to device
		for h in request.form.getlist('homeCat[]'): 
			hc = homecategory.query.filter_by(name=h).first()
			#If it doesn't exist, create it 
			if(not hc.id):
				hc = homecategory(name=h)
				db.session.add(hc)
				db.session.commit()
			device.homecategories.append(hc)

		db.session.add(device)
		db.session.commit()
		return redirect(url_for('list'))
	return render_template('create_device.html', po=po, deviceCat=dc, homecategories=hc)

@app.route('/showDevices', methods=["POST"])
def showDeviceOnCategory(name=None):
	#get devices with compatible home categories
	print(request.form.get('homecategory'))
	homeCat = homecategory.query.filter_by(name=request.form.get('homecategory')).first()
	devices = Device.query.filter(Device.homecategories.any(name=homeCat.name)).all()
	deviceCats = request.form.getlist('inputCat[]')	
	if deviceCats: 
		devices = []
	for dc in deviceCats: 
		deviceCat = devicecategory.query.filter_by(name=dc).first()
		homecatquery = homecategory.query.join()
		devices.extend(Device.query.join(devicecategory, Device.category_id==devicecategory.id).filter(devicecategory.id==deviceCat.id).filter(Device.homecategories.any(homecategory.id==homeCat.id)).all())

	return render_template('list_devices_by_category.html', 
		devices=devices, category=homeCat.name)

@app.route('/getDevice/<id>')
def getDevice(id):
	try: 
		device = Device.query.get(id)
	except Exception as e: 
		print(e)

	return render_template('item_details.html', device=device)

@app.route('/editCategories')
def editCategories(name=None):
	deviceCat = devicecategory.query.join(Device).filter(Device.category_id==devicecategory.id).all()
	return render_template('categories.html', deviceCat=deviceCat)

if __name__ == '__main__':
	app.run()