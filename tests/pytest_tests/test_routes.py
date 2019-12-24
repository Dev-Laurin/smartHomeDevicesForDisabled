from smartify.models import * 
import pytest 
from sqlalchemy import exc

def test_home(app, session):
	#test if there are no devices (no exceptions)
	response = app.get('/')
	assert response.status_code == 200

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

	response = app.get('/')
	assert response.status_code == 200

def test_createDevice_good(app, session):
	#Simple Example - everything is right
	po = paymentoccurence(name="One Time")
	session.add(po)
	session.commit()

	deviceCat = devicecategory(name="Touch")
	session.add(deviceCat)
	session.commit()

	hc = homecategory(name="Door")
	session.add(hc)
	session.commit()

	device = Device(name="Apple TV", description="A tv made by Apple.", 
		price=100.00, recurring_price=0, payment_occurence_id=po.id, 
		link="www.google.com", category_id=deviceCat.id, rating=3.45, 
		narrative="Works with Apple remote via touch.")
	device.homecategories.append(hc)

	from smartify.forms import CreateDeviceForm
	form = CreateDeviceForm(formdata=None, obj=device)

	response = app.post('/createDevice', data=form.data, 
		follow_redirects=True)
	assert response.status_code == 200 
	assert Device.query.filter_by(name="Apple TV").first() != None 

def test_createDevice_deviceNameTooLong(app, session):

	po = paymentoccurence(name="One Time")
	session.add(po)
	session.commit()

	deviceCat = devicecategory(name="Touch")
	session.add(deviceCat)
	session.commit()

	hc = homecategory(name="Door")
	session.add(hc)
	session.commit()

	#Name is too long 
	# device = Device(name="Apple Tssvlakjdkfjaskldjfl;askdjflkdj;lkds;lkfsadjfkalsdjfkljsd;fkljasdklfjj;lkasjl;dkfjYEA", description="A tv made by Apple.", 
	# 	price=100.00, recurring_price=0, payment_occurence_id=po.id, 
	# 	link="www.google.com", category_id=deviceCat.id, rating=3.45, 
	# 	narrative="Works with Apple remote via touch.")
	# device.homecategories.append(hc)

	# from smartify.forms import CreateDeviceForm
	# form = CreateDeviceForm(formdata=None, obj=device)

	# response = app.post('/createDevice', data=form.data, 
	# 	follow_redirects=True)
	# assert response.status_code == 200 
	# form.validate()
	# assert form.errors
	# d = Device.query.filter_by(name="Apple Tssvlakjdkfjaskldjfl;askdjflkdj;lkds;lkfsadjfkalsdjfkljsd;fkljasdklfjj;lkasjl;dkfjYEA").first()
	# assert not d 

	#Name is  missing 

	#Name = html script tag 

	#Description is too long 

	#Description is missing 

	#Description holds html script tag 

	#Price is string 

	#Price is missing

	#Price is negative 

	#Recurring price is string 

	#Recurring price is missing

	#Recurring price is negative 

	#Payment occurence is missing 

	#Payment occurence id is invalid 

	#Link is too long 

	#Link is missing

	#Link is a number 

	#Category is missing 

	#Category id is invalid 

	#Rating is string

	#Rating is missing

	#Rating is negative 

	#Narrative is missing

	#Narrative is too long 

	#Narrative = html script tag 