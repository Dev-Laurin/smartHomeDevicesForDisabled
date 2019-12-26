
from flask import (Flask, render_template, request, 
	url_for, redirect, flash)
from flask import current_app as app 
from .models import (db, Device, devicecategory, paymentoccurence, 
	homecategory, homecategories) 
from .forms import CreateDeviceForm

#Routing 
@app.route('/', methods=["GET", "POST"])
def list():
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
			devicesFound = devicecategory.query.with_parent(dc).all()
			devices.extend(devicesFound)

	return render_template('list.html', devices=devices, 
		categories=categories, homecategories=homecategories)

@app.route('/createDevice/<id>', methods=["GET", "POST"])
def createDevice(id):
	form = CreateDeviceForm()

	po = paymentoccurence.query.all()
	dc = devicecategory.query.all()
	hc = homecategory.query.all()
	device = Device.query.get_or_404(id)
	device_po = paymentoccurence.query.get(device.payment_occurence_id)
	device_cat = devicecategory.query.get(device.category_id)

	if form.validate_on_submit():

		po = paymentoccurence.query.filter_by(name=form.payment_occurence.data).first()
		dc = devicecategory.query.filter_by(name=form.category.data).first()

		if device: 
			device.name = form.name.data 
			device.description = form.description.data 
			device.price = form.price.data 
			device.recurring_price = form.recurring_price.data 
			device.payment_occurence_id=po.id 
			device.link = form.link.data 
			device.category_id = dc.id 
			device.rating = form.rating.data 
			device.narrative = form.narrative.data 

			#delete previous homecategories 
			device.homecategories = []

		else: 		
			device = Device(name=form.name.data, 
			description=form.description.data, 
			price=form.price.data,
			recurring_price=form.recurring_price.data,
			payment_occurence_id=po.id, 
			link=form.link.data,
			category_id=dc.id, 
			rating=form.rating.data,
			narrative=form.narrative.data
			)
				
		try: 
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
		except Exception as e: 
			flash('Error. Device was not created/edited.', 'danger')
			app.logger.info('Error. Device was not created.')
			app.logger.info(e)
			return render_template('create_device.html', po=po, deviceCat=dc, homecategories=hc, form=form, device=device, device_verb='Create')

		app.logger.info('Device created/edited.')
		flash('Device created.', 'success')
		return redirect(url_for('list'))
	elif form.errors:
		#Form validation failed 
		flash('Device not created/edited, validation failed.', 'danger')
		app.logger.info('Device not created, validation failed.')
		app.logger.info(form.errors)
		return render_template('create_device.html', po=po, deviceCat=dc, homecategories=hc, form=form)

	return render_template('create_device.html', po=po, deviceCat=dc, homecategories=hc, form=form, device=device, device_po=device_po, device_cat=device_cat, device_verb='Edit')

@app.route('/showDevices', methods=["POST"])
def showDeviceOnCategory():
	#get devices with compatible home categories
	homeCat = homecategory.query.filter_by(name=request.form.get('homecategory')).first()
	devices = Device.query.filter(Device.homecategories.any(name=homeCat.name)).all()
	deviceCats = request.form.getlist('inputCat[]')	
	if deviceCats: 
		devices = []
	for dc in deviceCats: 
		deviceCat = devicecategory.query.filter_by(name=dc).first()
		homecatquery = homecategory.query.join()
		devices.extend(Device.query.join(devicecategory, 
			Device.category_id==devicecategory.id)
		.filter(devicecategory.id==deviceCat.id)
		.filter(Device.homecategories
			.any(homecategory.id==homeCat.id)).all())

	return render_template('list_devices_by_category.html', 
		devices=devices, category=homeCat.name)

@app.route('/getDevice/<id>')
def getDevice(id):
	try: 
		device = Device.query.get(id)
	except Exception as e: 
		flash('Device was not found.', 'danger')
		app.logger.info("Device was not found.")
		app.logger.info(e)
		return redirect(url_for('list'))

	return render_template('device_details.html', device=device)

@app.route('/editDevices')
def editDevices():
	devices = Device.query.order_by(Device.category_id).all()

	return render_template('editDevices.html', devices=devices)

@app.route('/editCategories')
def editCategories():
	deviceCat = devicecategory.query.join(Device).filter(Device.category_id==devicecategory.id).all()
	return render_template('categories.html', deviceCat=deviceCat)

@app.route('/deleteDevice/<id>')
def deleteDevice(id):
	try: 
		device = Device.query.get(id)
		db.session.delete(device)
		db.session.commit() 
	except Exception as e: 
		flash('Device could not be deleted.', 'danger')
		app.logger.info('Device could not be deleted.')
		app.logger.info(e)

	return redirect(url_for('editDevices'))

if __name__ == '__main__':
	app.run()