
from flask import (Flask, render_template, request, 
	url_for, redirect, flash)
from flask import current_app as app 
from .models import *
from .forms import *
from . import file_upload
from werkzeug.security import generate_password_hash, check_password_hash
from flask_user import current_user, login_required, roles_required
import json 

#Routing 
@app.route('/', methods=["GET", "POST"])
def list():
	categories = devicecategory.query.all()
	devices = Device.query.all() 
	homecategories = homecategory.query.all()
	hc = []
	for h in homecategories:
		h.image = file_upload.get_file_url(h, filename="image") 
		if h.image.find("None") != -1: 
			h.image = None 
		hc.append(h)

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
		categories=categories, homecategories=hc)

@app.route('/createDevice/<id>', methods=["GET", "POST"])
@roles_required(['Admin', 'Editor'])
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
			device.image_alt = form.image_alt.data 

			if form.is_subscription.data: 

				device.recurring_price = form.recurring_price.data 
				device.payment_occurence_id=po.id 
				device.subscription_description = form.subscription_description.data
				device.has_subscription = form.is_subscription.data 

			#delete previous 
			device.homecategories = []
			device.devicecategories = []
			device.deviceresources = []

			image = request.files['image']

			#if we are uploading optional image 
			if image:
				#Test that alt text is given first 
				if not form.image_alt.data: 
					flash('Image Alternate Text is required.', 'danger')
					app.logger.info('Image Alternate Text is required.')
					return render_template('create_device.html',
		homecategories=hc, devicecategories=dc, form=form, 
		device=device, message="Image Alternate Text is required.")

				try:  #has this had an image before? 
					if device.image: 
						device = file_upload.update_files(device, files={
							"image": image 
						})
						app.logger.info('Had image before, update it.')
				except Exception as e:  
					device = file_upload.save_files(device, files={
						"image": image 
					})
					app.logger.info('Saving new image.')
	
			try: 
				#add homecategories to device
				for h in request.form.getlist('homeCat[]'): 
					hc = homecategory.query.filter_by(name=h).first()
					#If it doesn't exist, create it 
					if(not hc):
						hc = homecategory(name=h)
						db.session.add(hc)
						db.session.commit()
					device.homecategories.append(hc)

				#add devicecategories to device
				for d in request.form.getlist('deviceCat[]'): 
					dc = devicecategory.query.filter_by(name=d).first()
					#If it doesn't exist, create it 
					if(not dc):
						dc = devicecategory(name=d)
						db.session.add(dc)
						db.session.commit()
					device.devicecategories.append(dc)

				#add resources to device
				for r in request.form.getlist('resources[]'): 
					ru = resourceURL.query.filter_by(url=r).first()
					#If it doesn't exist, create it 
					if(not ru):
						ru = resourceURL(url=r)
						db.session.add(ru)
						db.session.commit()
					device.deviceresources.append(ru)

				db.session.add(device)
				db.session.commit()
				app.logger.info('Device edited.')
				flash('Device edited.', 'success')
				return redirect(url_for('list'))
			except Exception as e: 
				flash('Error. Device was not edited.', 'danger')
				app.logger.error('Error. Device was not edited.')
				app.logger.error(e)
				return render_template('create_device.html',
		homecategories=hc, devicecategories=dc, form=form, 
		device=device, message='Error. Device was not edited.')


	elif form.errors:
		#Form validation failed 
		flash('Device not edited, validation failed.', 'danger')
		app.logger.error('Device not edited, validation failed.')
		app.logger.error(form.errors)
		return render_template('create_device.html',
		homecategories=hc, devicecategories=dc, form=form, 
		device=device, message='Error. Device was not edited.')

	return retFunc

@app.route('/createDevice', methods=["GET", "POST"])
@app.route('/createDevice/', methods=["GET", "POST"])
@app.route('/createDevice/None', methods=["GET", "POST"])
@roles_required(['Admin', 'Editor'])
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
				image_alt=form.image_alt.data, 
				subscription_description=form.subscription_description.data, 
				has_subscription=form.is_subscription.data, 
				)
			else: 
				device = Device(name=form.name.data, 
				description=form.description.data, 
				price=form.price.data,
				link=form.link.data,
				rating=form.rating.data,
				narrative=form.narrative.data, 
				warranty_price=form.warranty_price.data, 
				warranty_length=form.warranty_length.data, 
				image_alt=form.image_alt.data,
				)

			device.po = po.name    
			device.verb="Create"
			image = request.files["image"]
			if image: 
				#Test that alt text is given first 
				if not form.image_alt.data: 
					flash('Image Alternate Text is required.', 'danger')
					app.logger.info('Image Alternate Text is required.')
					return render_template("create_device.html",
		homecategories=hc, devicecategories=dc, form=form, 
		device=device, message='Image Alternate Text is required.')
	

				device = file_upload.save_files(device, files={
					"image": image
				})

			#add homecategories to device
			for h in request.form.getlist('homeCat[]'): 
				hc = homecategory.query.filter_by(name=h).first()
				#If it doesn't exist, create it 
				if(not hc):
					hc = homecategory(name=h)
					db.session.add(hc)
					db.session.commit()
				device.homecategories.append(hc)
			#add devicecategories to device
			for d in request.form.getlist('deviceCat[]'): 
				dc = devicecategory.query.filter_by(name=d).first()
				#If it doesn't exist, create it 
				if(not dc):
					dc = devicecategory(name=d)
					db.session.add(dc)
					db.session.commit()
				device.devicecategories.append(dc)
			#add resources to device
			for r in request.form.getlist('resources[]'): 
				ru = resourceURL.query.filter_by(url=r).first()
				#If it doesn't exist, create it 
				if(not ru):
					ru = resourceURL(url=r)
					db.session.add(ru)
					db.session.commit()
				device.deviceresources.append(ru)
			db.session.add(device)
			db.session.commit()
			app.logger.info('Device created.')
			flash('Device created.', 'success')
		except Exception as e: 
			flash('Error. Device was not created.', 'danger')
			app.logger.info('Error. Device was not created.')
			app.logger.info(e)
			return render_template("create_device.html",
		homecategories=hc, devicecategories=dc, form=form, 
		device=device, message='Device not created, validation failed.')

		return redirect(url_for('list'))
	elif form.errors:
		#Form validation failed 
		flash('Device not created, validation failed.', 'danger')
		app.logger.info('Device not created, validation failed.')
		app.logger.info(form.errors)
		return render_template("create_device.html",
		homecategories=hc, devicecategories=dc, form=form, 
		 message='Device not created, validation failed.')
	

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
@roles_required(['Admin', 'Editor'])
def editDevices():
	devices = Device.query.all()
	return render_template('edit_devices.html', devices=devices)

@app.route('/editHomeCategories')
@roles_required(['Admin', 'Editor'])
def editHomeCategories():
	form = EditHomeCategoryForm()
	hc = homecategory.query.all()
	cats = []
	for h in hc: 
		h.image = file_upload.get_file_url(h, filename="image")
		cats.append(h)
	return render_template('homecategories.html', 
		categories=cats, form=form)

@app.route('/editHomeCategory/<id>', methods=["POST"])
@roles_required(['Admin', 'Editor'])
def editHomeCategory(id):
	form = EditHomeCategoryForm()
	if form.validate_on_submit():
		try: 
			cat = homecategory.query.get(id)
			cat.name = form.name.data
			cat.image_alt = form.image_alt.data 
			image = request.files['image'] 
			#if we are uploading optional image 
			if image:
				try:  #has this had an image before? 
					if cat.image: 
						cat = file_upload.update_files(cat, files={
							"image": image 
						})
				except Exception as e:  
					cat = file_upload.save_files(cat, files={
						"image": image 
					})
				db.session.add(cat)
				db.session.commit()
				flash('Category edited.', 'success')
			else: 
				db.session.add(cat)
				db.session.commit()
				flash('Category edited.', 'success')
		except Exception as e: 
			flash('Editing category failed.', 'danger')
			app.logger.error('Editing category failed (db).')
			app.logger.info(e)
	else: 
		flash("Category could not be edited. Contact developer.", 'danger')
		app.logger.error(form.errors)
	return redirect(url_for('editHomeCategories'))

@app.route('/addHomeCategory', methods=["GET", "POST"])
@roles_required(['Admin', 'Editor'])
def addHomeCategory():
	form = AddHomeCategoryForm()
	if form.validate_on_submit(): 
		try: 
			hc = homecategory(name=form.name.data, image_alt=form.image_alt.data)
			image = request.files["image"]
			if image: 
				hc = file_upload.save_files(hc, files={
					"image": image
				})
			db.session.add(hc)
			db.session.commit()
			flash("Category created.", 'success')
			app.logger.info("Category created.")
		except Exception as e: 
			flash("Category could not be created.", 'danger')
			app.logger.error('Category could not be created in db.')
			app.logger.error(e)
	elif(form.errors):
		flash('Error adding home category.', 'danger')
		app.logger.error(form.errors)
	return redirect(url_for('editHomeCategories'))

@app.route('/deleteHomeCategory/<id>')
@roles_required(['Admin', 'Editor'])
def deleteHomeCategory(id=None):
	try: 
		hc = homecategory.query.get(id)
		try: 
			file_upload.delete_files(hc, files=["image"])
		except Exception as e: 
			#image probably doesn't exist -- problem solved.
			app.logger.info("Image doesn't exist?")
			app.logger.info(e)
		db.session.delete(hc)
		db.session.commit() 
		app.logger.info('Category deleted.')
		flash('Category successfully deleted.', 'success')
	except Exception as e: 
		flash('Category could not be deleted. There are still devices that use this category.', 'danger')
		app.logger.error('Device category could not be deleted.')
		app.logger.error(e)
	
	return redirect(url_for('editHomeCategories'))

@app.route('/editCategories')
@roles_required(['Admin', 'Editor'])
def editCategories():
	form = AddCategoryForm()
	deviceCat = devicecategory.query.all()
	return render_template('categories.html', deviceCat=deviceCat, 
		form=form)

@app.route('/editCategory/<id>', methods=["POST"])
@roles_required(['Admin', 'Editor'])
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
			app.logger.error('Editing category failed (db).')
			app.logger.error(e)
	else: 
		flash(form.errors, 'danger')
		app.logger.error(form.errors)
	return redirect(url_for('editCategories'))

@app.route('/addCategory', methods=["GET", "POST"])
@roles_required(['Admin', 'Editor'])
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
			app.logger.error('Category could not be created in db.')
			app.logger.error(e)
	return redirect(url_for('editCategories'))

@app.route('/deleteCategory/<id>')
@roles_required(['Admin', 'Editor'])
def deleteCategory(id=None):
	try: 
		dc = devicecategory.query.get(id)
		db.session.delete(dc)
		db.session.commit() 
		app.logger.info('Category deleted.')
		flash('Category successfully deleted.', 'success')
	except Exception as e: 
		flash('Category could not be deleted. There are still devices that use this category.', 'danger')
		app.logger.error('Device category could not be deleted.')
		app.logger.error(e)
	
	return redirect(url_for('editCategories'))

@app.route('/deleteDevice/<id>')
@roles_required(['Admin', 'Editor'])
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
		app.logger.error('Device could not be deleted.')
		app.logger.error(e)
	
	return redirect(url_for('editDevices'))

@app.route('/editUserAccounts')
@roles_required('Admin')
def editUsers():
	users = User.query.all()

	#JSON obj for javascript
	Users = {}
	for u in users: 
		user_roles = []
		for r in u.roles: 
			user_roles.append(r.name) 
		Users[u.username] = {'id': u.id, 'username': u.username, 
		'roles': user_roles}

	roles = Role.query.all()
	Roles = []
	for r in roles:
		Roles.append(r.name) 

	return render_template('edit_users.html', 
		user_json=Users, users=users, roles=Roles)

@app.route('/editUser/<id>', methods=["POST"])
def editUser(id): 
	try: 
		user = User.query.get(id)
		user.roles = request.form.getlist('roles[]')
		db.session.add(user)
		db.session.commit()
		flash('User updated.', 'success')
		app.logger.info('User updated.')
	except Exception as e: 
		flash('Could not update user.', 'danger')
		app.logger.error("Could not update user roles.")
		app.logger.error(e)
	return redirect(url_for('editUsers'))

if __name__ == '__main__':
	app.run()