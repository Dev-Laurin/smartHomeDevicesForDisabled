import os
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask_file_upload import FileUpload 

db = SQLAlchemy()
file_upload = FileUpload(db=db)

def create_app():
	#create and configure the app 
	app = Flask(__name__, instance_relative_config=True, 
		template_folder="templates", static_folder="static")
	app.config.from_envvar('APP_CONFIG_FILE')

	db.init_app(app)
	file_upload.init_app(app)	

	#ensure the instance folder exists 
	try: 
		os.makedirs(app.instance_path)
	except OSError: 
		pass 

	with app.app_context():

		
		#dev_db()
# #---------------------------------------

		from . import routes 

		return app 


def dev_db():
	from .models import (paymentoccurence, 
			devicecategory, devicecategories, homecategory, Device, homecategories)
	#initialize database -- for dev only 
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
	dcs = devicecategory(name="Switch")
	db.session.add(dcs)
	db.session.commit()
	dcv = devicecategory(name="Voice")
	db.session.add(dcv)
	db.session.commit()
	hcs = homecategory(name="Security")
	db.session.add(hcs)
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
		rating=3, narrative="Gives you the ability to activate lights with voice commands.")
	device.devicecategories.append(dct)
	device.homecategories.append(hc)
	db.session.add(device)
	db.session.commit()
	device = Device(name="Brilliant One Switch Panel",
		description="Transform your house or apartment into an easy-to-use smart home with the award-winning Brilliant Smart Home Control and all-in-one mobile app. Instantly gain control over all your smart home products via a single app and display that simply installs in place of any light switch. No more hubs, ugly wires, countertop clutter, or switching multiple apps.",
		price=299.99, recurring_price=0.00, payment_occurence_id=po.id, 
		link="https://www.brilliant.tech/products/brilliant-control-two-switch-smart-lighting-smart-home-control?variant=white",
		rating=4.7, narrative="Gives you the ability to activate lights via a phone app.")
	device.devicecategories.append(dcv)
	device.devicecategories.append(dct)
	device.homecategories.append(hcs)
	db.session.add(device)
	db.session.commit()
	device = Device(name="Ring Doorbell Video",
		description="Get instant alerts when visitors press your Doorbell or trigger the built-in motion sensors. Then use the free Ring app to see, hear and speak to guests from your smartphone, tablet or PC.",
		price=99.99, recurring_price=17.00, payment_occurence_id=pom.id, 
		link="https://shop.ring.com/collections/video-doorbells//products/video-doorbell",
		rating=4.7, narrative="Gives you the ability to activate lights via a phone app.")
	device.devicecategories.append(dcs)
	device.homecategories.append(hcd)
	db.session.add(device)
	db.session.commit()