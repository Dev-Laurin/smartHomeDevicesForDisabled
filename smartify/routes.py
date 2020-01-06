
from flask import (Flask, render_template, request, 
	url_for, redirect, flash)
from flask import current_app as app 
from .models import (db, Device, devicecategory, paymentoccurence, 
	homecategory, homecategories, devicecategories) 
from .forms import CreateDeviceForm, AddCategoryForm, EditCategoryForm
from . import file_upload

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
def editDevice(id):
	form = CreateDeviceForm()
	dc = devicecategory.query.all()
	hc = homecategory.query.all()

	device = Device.query.get_or_404(id)
	device.verb="Edit"
	if device.payment_occurence_id: 
		device.po = paymentoccurence.query.get(device.payment_occurence_id)
	device.dc =[]
	for d in device.devicecategories:
		device.dc.append(d.name) 
	device.hc = []
	for h in device.homecategories: 
		device.hc.append(h.name)

	retFunc = render_template('create_device.html',
		homecategories=hc, devicecategories=dc, form=form, device=device)

	#POST request, we are saving to db 
	if form.validate_on_submit():

		po = paymentoccurence.query.filter_by(name=form.payment_occurence.data).first()

		if device: 

			device.name = form.name.data 
			device.description = form.description.data 
			device.price = form.price.data 
			device.link = form.link.data 
			device.rating = form.rating.data 
			device.narrative = form.narrative.data 
			device.warranty_price = form.warranty_price.data 
			device.warranty_length = form.warranty_length.data 

			if form.is_subscription.data: 

				device.recurring_price = form.recurring_price.data 
				device.payment_occurence_id=po.id 
				device.subscription_description = form.subscription_description.data
				device.has_subscription = form.is_subscription.data 

			#delete previous homecategories 
			device.homecategories = []
			device.devicecategories = []

			image = request.files['image']
			device = file_upload.update_files(device, files={
				"image": image 
			})
	
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

				#add devicecategories to device
				for d in request.form.getlist('deviceCat[]'): 
					dc = devicecategory.query.filter_by(name=d).first()
					#If it doesn't exist, create it 
					if(not dc.id):
						dc = devicecategory(name=d)
						db.session.add(dc)
						db.session.commit()
					device.devicecategories.append(dc)

				db.session.add(device)
				db.session.commit()
				app.logger.info('Device edited.')
				flash('Device edited.', 'success')
				return redirect(url_for('list'))
			except Exception as e: 
				flash('Error. Device was not edited. \n If uploading a file, it must have a filename of 16 characters or less.', 'danger')
				app.logger.info('Error. Device was not edited.')
				app.logger.info(e)
				return retFunc

	elif form.errors:
		#Form validation failed 
		flash('Device not edited, validation failed.', 'danger')
		app.logger.info('Device not edited, validation failed.')
		app.logger.info(form.errors)
		return retFunc
	return retFunc

@app.route('/createDevice', methods=["GET", "POST"])
@app.route('/createDevice/', methods=["GET", "POST"])
def createDevice():
	form = CreateDeviceForm(is_subscription=False)

	device=None 
	hc = homecategory.query.all()
	dc = devicecategory.query.all() 
	retFunc = render_template("create_device.html",
		homecategories=hc, devicecategories=dc, form=form, device=device)
	
	#POST request, we are saving to db 
	if form.validate_on_submit():

		po = paymentoccurence.query.filter_by(name=form.payment_occurence.data).first()
				
		try:
			#There is a subscription 
			if form.is_subscription.data:

				device = Device(name=form.name.data, 
				description=form.description.data, 
				price=form.price.data,
				recurring_price=form.recurring_price.data,
				payment_occurence_id=po.id, 
				link=form.link.data,
				rating=form.rating.data,
				narrative=form.narrative.data, 
				warranty_price=form.warranty_price.data, 
				warranty_length=form.warranty_length.data,  
				subscription_description=form.subscription_description.data, 
				has_subscription=form.is_subscription.data
				)
			else: 

				device = Device(name=form.name.data, 
				description=form.description.data, 
				price=form.price.data,
				link=form.link.data,
				rating=form.rating.data,
				narrative=form.narrative.data, 
				warranty_price=form.warranty_price.data, 
				warranty_length=form.warranty_length.data
				)

			device.po = po.name    
			device.verb="Create"
			image = request.files["image"]
			device = file_upload.save_files(device, files={
				"image": image
			})

			#add homecategories to device
			for h in request.form.getlist('homeCat[]'): 
				hc = homecategory.query.filter_by(name=h).first()
				#If it doesn't exist, create it 
				if(not hc.id):
					hc = homecategory(name=h)
					db.session.add(hc)
					db.session.commit()
				device.homecategories.append(hc)
			#add devicecategories to device
			for d in request.form.getlist('deviceCat[]'): 
				dc = devicecategory.query.filter_by(name=d).first()
				#If it doesn't exist, create it 
				if(not dc.id):
					dc = devicecategory(name=d)
					db.session.add(dc)
					db.session.commit()
				device.devicecategories.append(dc)
			db.session.add(device)
			db.session.commit()
			app.logger.info('Device created.')
			flash('Device created.', 'success')
		except Exception as e: 
			flash('Error. Device was not created. \n If uploading a file, it must have a filename of 16 characters or less.', 'danger')
			app.logger.info('Error. Device was not created.')
			app.logger.info(e)
			return retFunc

		return redirect(url_for('list'))
	elif form.errors:
		#Form validation failed 
		flash('Device not created, validation failed.', 'danger')
		app.logger.info('Device not created, validation failed.')
		app.logger.info(form.errors)
		return retFunc

	return retFunc

@app.route('/showDevices', methods=["POST"])
def showDeviceOnCategory():

	try: 
		#get devices with compatible home categories
		homeCat = homecategory.query.filter_by(name=request.form.get('homecategory')).first()
		devices = Device.query.filter(Device.homecategories
				.any(name=homeCat.name)).all()
		deviceCats = request.form.getlist('inputCat[]')	
		devCatIDs = []
		if deviceCats: 
			devices = []
			for dc in deviceCats: 
				deviceCat = devicecategory.query.filter_by(name=dc).first()
				devCatIDs.append(deviceCat.id)
			devices.extend(db.session.query(Device)
				.join(Device.homecategories)
				.filter_by(id=homeCat.id)
				.join(Device.devicecategories)
				.filter(devicecategory.id.in_(devCatIDs))
				.all())
		#Get image file urls 
		for device in devices: 
			device.image = file_upload.get_file_url(device, filename="image") 
	except Exception as e: 
				flash('Filtering by category failed. Contact site admin.', 'danger')
				app.logger.info('Filtering by category failed.')
				app.logger.info(e)
	return render_template('list_devices_by_category.html', 
			devices=devices, category=homeCat.name)

@app.route('/getDevice/<id>')
def getDevice(id=None):
	try: 
		device = Device.query.get(id)
		device.image = file_upload.get_file_url(device, filename="image") 
	except Exception as e: 
		flash('Device was not found.', 'danger')
		app.logger.info("Device was not found.")
		app.logger.info(e)
		return redirect(url_for('list'))

	return render_template('device_details.html', device=device)

@app.route('/editDevices')
def editDevices():
	devices = Device.query.all()
	return render_template('edit_devices.html', devices=devices)

@app.route('/editHomeCategories')
def editHomeCategories():
	hc = homecategory.query.all()
	return render_template('homecategories.html', categories=hc)

@app.route('/editHomeCategory/<id>', methods=["POST"])
def editHomeCategory(id):
	form = EditCategoryForm()
	if form.validate_on_submit():
		try: 
			cat = homecategory.query.get(id)
			cat.name = form.name.data
			db.session.add(cat)
			db.session.commit()
			flash('Category edited.', 'success')
		except Exception as e: 
			flash('Editing category failed.', 'danger')
			app.logger.info('Editing category failed (db).')
			app.logger.info(e)
	else: 
		flash("Category could not be edited. Contact developer.", 'danger')
		app.logger.info(form.errors)
	return redirect(url_for('editHomeCategories'))

@app.route('/addHomeCategory', methods=["GET", "POST"])
def addHomeCategory():
	form = AddCategoryForm()
	if form.validate_on_submit(): 
		hc = homecategory(name=form.name.data)
		try: 
			db.session.add(hc)
			db.session.commit()
			flash("Category created.", 'success')
			app.logger.info("Category created.")
		except Exception as e: 
			flash("Category could not be created.", 'danger')
			app.logger.info('Category could not be created in db.')
			app.logger.info(e)
	elif(form.errors):
		flash('Error adding home category.', 'danger')
		app.logger.info(form.errors)
	return redirect(url_for('editHomeCategories'))

@app.route('/deleteHomeCategory/<id>')
def deleteHomeCategory(id=None):
	try: 
		hc = homecategory.query.get(id)
		db.session.delete(hc)
		db.session.commit() 
		app.logger.info('Category deleted.')
		flash('Category successfully deleted.', 'success')
	except Exception as e: 
		flash('Category could not be deleted. There are still devices that use this category.', 'danger')
		app.logger.info('Device category could not be deleted.')
		app.logger.info(e)
	
	return redirect(url_for('editHomeCategories'))

@app.route('/editCategories')
def editCategories():
	deviceCat = devicecategory.query.all()
	return render_template('categories.html', deviceCat=deviceCat)

@app.route('/editCategory/<id>', methods=["POST"])
def editCategory(id):
	form = EditCategoryForm()
	if form.validate_on_submit():
		try: 
			cat = devicecategory.query.get(id)
			cat.name = form.name.data
			db.session.add(cat)
			db.session.commit()
			flash('Category edited.', 'success')
		except Exception as e: 
			flash('Editing category failed.', 'danger')
			app.logger.info('Editing category failed (db).')
			app.logger.info(e)
	else: 
		flash(form.errors, 'danger')
		app.logger.info(form.errors)
	return redirect(url_for('editCategories'))

@app.route('/addCategory', methods=["GET", "POST"])
def addCategory():
	form = AddCategoryForm()
	if form.validate_on_submit(): 
		dc = devicecategory(name=form.name.data)
		try: 
			db.session.add(dc)
			db.session.commit()
			flash("Category created.", 'success')
			app.logger.info("Category created.")
		except Exception as e: 
			flash("Category could not be created.", 'danger')
			app.logger.info('Category could not be created in db.')
			app.logger.info(e)
	return redirect(url_for('editCategories'))

@app.route('/deleteCategory/<id>')
def deleteCategory(id=None):
	try: 
		dc = devicecategory.query.get(id)
		db.session.delete(dc)
		db.session.commit() 
		app.logger.info('Category deleted.')
		flash('Category successfully deleted.', 'success')
	except Exception as e: 
		flash('Category could not be deleted. There are still devices that use this category.', 'danger')
		app.logger.info('Device category could not be deleted.')
		app.logger.info(e)
	
	return redirect(url_for('editCategories'))

@app.route('/deleteDevice/<id>')
def deleteDevice(id):
	try: 
		device = Device.query.get(id)
		file_upload.delete_files(device, files=["image"])
		db.session.delete(device)
		db.session.commit() 
		flash('Device successfully deleted.', 'success')
		app.logger.info('Device deleted.')
	except Exception as e: 
		flash('Device could not be deleted.', 'danger')
		app.logger.info('Device could not be deleted.')
		app.logger.info(e)
	
	return redirect(url_for('editDevices'))

if __name__ == '__main__':
	app.run()