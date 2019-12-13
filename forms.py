# from flask_wtf import FlaskForm, RecaptchaField
# from wtforms import StringField, TextField, TextAreaField, DecimalField
# from wtforms.validators import DataRequired, Length, AnyOf 

# class CreateDeviceForm(FlaskForm):
# 	name = StringField('name', validators=[DataRequired(), Length(1, 80, 
# 		message="Device name needs to be between 1 and 80 characters.")])
# 	description = TextAreaField('desc', validators=[DataRequired(), Length(0, 
# 		500, message="Description has too many characters, max=500.")])
# 	price = DecimalField('price', places=2, validators=[DataRequired()])
# 	recurring_price = DecimalField('recurring_price', places=2, validators=[DataRequired()])
# 	payment_occurence = StringField('payment_occurence', 
# 		validators=[DataRequired(), 
# 		AnyOf(payment_occurence.query.all(), message="Not a valid payment occurence.")])
# 	link = StringField('link', validators=[DataRequired(), Length(7, 500, 
# 		message="Hyperlink has too few or too many characters.")])
# 	category = StringField('device_category', validators=[DataRequired(),
# 		AnyOf(devicecategory.query.all(), message="Not a valid device category.")])
# 	rating = StringField('rating', validators=[DataRequired(), 
# 		AnyOf(rating.query.all(), message="Rating is invalid.")])
# 	narrative = TextAreaField('narrative', validators=[Length(0, 500, 
# 		message="Rating description must be less than 500 characters.")])
# 	recaptcha = RecaptchaField()