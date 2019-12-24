from smartify.models import * 
import pytest 
from sqlalchemy import exc 

def test_devicecategory(session):
	deviceCat = devicecategory(name="Touch")
	session.add(deviceCat)
	session.commit()

	#Test that item was created
	assert deviceCat.id > 0 
	assert deviceCat.name == "Touch"

	#No Name 
	deviceCat = devicecategory()
	session.add(deviceCat)

	with pytest.raises(exc.IntegrityError): 
		session.commit()

	#Name is too long
	deviceCat = devicecategory(name="laksjdlfkjewklnklnkhlkaslkdfjal;skdjf;askldjflasdkjf")
	session.add(deviceCat)

	with pytest.raises(exc.InvalidRequestError): 
		session.commit()

def test_paymentoccurence(session):
	po = paymentoccurence(name="One Time")
	session.add(po)
	session.commit()

	#Test that item was created
	assert po.id > 0 
	assert po.name == "One Time"

	#No name 
	po = paymentoccurence()
	session.add(po)
	with pytest.raises(exc.IntegrityError): 
		session.commit()

	#Name is too long 
	po = paymentoccurence(name="One Timekjlaksjdlfkjasldkfjasdl;kfjsl;dkfjdklj")
	session.add(po)
	with pytest.raises(exc.InvalidRequestError): 
		session.commit()

def test_homecategory(session):
	hc = homecategory(name="Door")
	session.add(hc)
	session.commit()

	#Test that item was created
	assert hc.id > 0 
	assert hc.name == "Door"

	#No args 
	hc = homecategory()
	session.add(hc)
	with pytest.raises(exc.IntegrityError): 
		session.commit()

	#Too long 
	hc = homecategory(name="Doorjlksdjfladjlfadjsl;fjadsl;kfjasdl;kfjdskl;j")
	session.add(hc)
	with pytest.raises(exc.InvalidRequestError): 
		session.commit()

def test_Device(session):
	deviceCat = devicecategory(name="Touch")
	session.add(deviceCat)
	session.commit()

	po = paymentoccurence(name="One Time")
	session.add(po)
	session.commit()

	device = Device(name="Apple TV", description="A tv made by Apple.", 
		price=100.00, recurring_price=0, payment_occurence_id=po.id, 
		link="www.google.com", category_id=deviceCat.id, rating=3.45, 
		narrative="Works with Apple remote via touch.")
	session.add(device)
	session.commit()

	#validate relationships 
	assert device.category_id == deviceCat.id 
	assert device.payment_occurence_id == po.id 

	#Test that item was created
	assert device.id > 0 
	assert device.name == "Apple TV"
	assert device.description == "A tv made by Apple."
	assert device.price == 100.00 
	assert device.recurring_price == 0 
	assert device.link == "www.google.com"
	#assert device.rating == 3.45 -------SQLite doesn't have decimals
	assert device.narrative == "Works with Apple remote via touch."

	#No args 
	device = Device()
	session.add(device)
	with pytest.raises(exc.IntegrityError): 
		session.commit()
