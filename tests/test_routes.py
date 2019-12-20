from smartify.models import * 
import pytest 
from sqlalchemy import exc

def test_home(app, session):
	#test if there are no devices (no exceptions)
	#app.get('/')
	#assert response.status_code == 200

	#test if there are devices 
	#category 
	deviceCat = devicecategory(name="Touch")
	session.add(deviceCat)
	session.commit()

	#homecategory 
	hc = homecategory(name="Door")
	session.add(hc)
	session.commit()

	po = paymentoccurence(name="One Time")
	session.add(po)
	session.commit()

	#device 
	device = Device(name="Apple TV", description="A tv made by Apple.", 
		price=100.00, recurring_price=0, payment_occurence_id=po.id, 
		link="www.google.com", category_id=deviceCat.id, rating=3.45, 
		narrative="Works with Apple remote via touch.")
	device.homecategories.append(hc)
	session.add(device)
	session.commit()

	list()

def test_createDevice(session):
	 assert 1 == 1