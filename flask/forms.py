from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextField, TextAreaField, DecimalField
from wtforms.validators import DataRequired 

class CreateDeviceForm(FlaskForm):
	name = StringField('name', validators=[DataRequired()])
	description = TextAreaField('desc', validators=[DataRequired()])
	price = DecimalField('price', places=2, validators=[DataRequired()])
	recurring_price = DecimalField('recurring_price', places=2, validators=[DataRequired()])
	payment_occurence = StringField('payment_occurence', validators=[DataRequired()])
	link = StringField('link', validators=[DataRequired()])
	category = StringField('device_category', validators=[DataRequired()])
	rating = StringField('rating', validators=[DataRequired()])
	narrative = TextAreaField('narrative')
	recaptcha = RecaptchaField()