from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextField, TextAreaField, DecimalField, SelectField, BooleanField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, AnyOf, NumberRange, Email, EqualTo
from .models import (db, Device, devicecategory, paymentoccurence, 
	homecategory, homecategories) 
from .recaptcha3 import Recaptcha3Field

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
	rating = DecimalField('rating', validators=[InputRequired(), NumberRange(min=0, max=5, 
		message="Rating is invalid.")])
	narrative = TextAreaField('narrative', validators=[Length(0, 500, 
		message="Rating description must be less than 500 characters.")])
	warranty_price = DecimalField('warranty_price', places=2)
	warranty_length = StringField('warranty_length', validators=[Length(0, 80, 
		message="Warranty length needs to be between 1 and 80 characters.")])
	subscription_description = TextAreaField('subscription_description', validators=[Length(0, 
		500, message="Subscription description has too many characters, max=500.")])
	image_alt = StringField('image_alt', validators=[Length(0, 80, 
		message="Alt text needs to be between 1 and 80 characters.")])
	recaptcha = Recaptcha3Field(action="deviceCreation", execute_on_load=True)

class AddCategoryForm(FlaskForm):
	name = StringField('name', validators=[InputRequired(), Length(1, 80, 
		message="Category name needs to be between 1 and 80 characters.")])
	recaptcha = Recaptcha3Field(action="addCategory", execute_on_load=True)

class EditCategoryForm(FlaskForm):
	name = StringField('name', validators=[InputRequired(), Length(1, 80, 
		message="Category name needs to be between 1 and 80 characters.")])

class AddHomeCategoryForm(FlaskForm):
	name = StringField('name', validators=[InputRequired(), Length(1, 80, 
		message="Category name needs to be between 1 and 80 characters.")])
	image_alt = StringField('name', validators=[InputRequired(), Length(1, 80, 
		message="Alt text needs to be between 1 and 80 characters.")])
	recaptcha = Recaptcha3Field(action="addHomeCategory", execute_on_load=True)


class EditHomeCategoryForm(FlaskForm):
	name = StringField('name', validators=[InputRequired(), Length(1, 80, 
		message="Alt text needs to be between 1 and 80 characters.")])
	image_alt = StringField('name', validators=[InputRequired(), Length(1, 80, 
		message="Alt text needs to be between 1 and 80 characters.")])
