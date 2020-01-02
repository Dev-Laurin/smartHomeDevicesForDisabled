from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextField, TextAreaField, DecimalField, SelectField, BooleanField
from wtforms.validators import InputRequired, Length, AnyOf, NumberRange
from .models import (db, Device, devicecategory, paymentoccurence, 
	homecategory, homecategories) 

class CreateDeviceForm(FlaskForm):
	name = StringField('name', validators=[InputRequired(), Length(1, 80, 
		message="Device name needs to be between 1 and 80 characters.")])
	description = TextAreaField('description', validators=[InputRequired(), Length(1, 
		500, message="Description has too many characters, max=500.")])
	price = DecimalField('price', places=2, validators=[InputRequired()])
	recurring_price = DecimalField('recurring_price', places=2)
	po = paymentoccurence.query.all() 
	poChoices = []
	for p in po: 
		poChoices.append((p.name, p.name))
	payment_occurence = SelectField('payment_occurence', choices=poChoices)
	link = StringField('link', validators=[InputRequired(), Length(7, 500, 
		message="Hyperlink has too few or too many characters.")])
	is_subscription = BooleanField()
	categories = devicecategory.query.all() 
	cat = []
	for c in categories: 
		cat.append((c.name, c.name))
	category = SelectField('device_category', choices=cat, validators=[InputRequired()])
	rating = DecimalField('rating', validators=[InputRequired(), NumberRange(min=0, max=5, 
		message="Rating is invalid.")])
	narrative = TextAreaField('narrative', validators=[Length(0, 500, 
		message="Rating description must be less than 500 characters.")])
	subscription_description = TextAreaField('subscription_description', validators=[Length(0, 
		500, message="Subscription description has too many characters, max=500.")])
	#recaptcha = RecaptchaField()

class AddCategoryForm(FlaskForm):
	name = StringField('name', validators=[InputRequired(), Length(1, 80, 
		message="Category name needs to be between 1 and 80 characters.")])

class EditCategoryForm(FlaskForm):
	name = StringField('name', validators=[InputRequired(), Length(1, 80, 
		message="Category name needs to be between 1 and 80 characters.")])