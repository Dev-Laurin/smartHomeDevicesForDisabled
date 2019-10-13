from django.db import models

class Device(models.Model): 
	def __str__(self):
		return self.name 

	name = models.CharField(max_length=200)
	description = models.TextField()
	price = models.PositiveIntegerField()
	payment_occurence = models.CharField(max_length=30)
	link = models.CharField(max_length=200)
	category = models.ForeignKey(Device_Category, on_delete=models.CASCADE)
	atp_rating = models.ForeignKey(Assistive_Tech_Rating, on_delete=models.CASCADE)
	community_rating = models.ForeignKey(Community_Rating, on_delete=models.CASCADE)

class Disability(models.Model):
	def __str__(self):
		return self.name 

	name = models.CharField(max_length=255)
	category = models.ForeignKey(Disability_Category, on_delete=models.CASCADE)

class Disability_Category(models.Model):
	def __str__(self):
		return self.name 

	name = models.CharField(max_length=200)

class Assistive_Tech_Rating(models.Model): 
	def __str__(self): 
		return self.disability.name 

	device = models.ForeignKey(Device, on_delete=models.CASCADE)
	disability = models.ForeignKey(Disability, on_delete=models.CASCADE)
	device_effectiveness_rating = models.PositiveIntegerField()
	device_relevance_rating = models.PositiveIntegerField()
	narrative = models.TextField()

class Device_Category(models.Model):
	def __str__(self):
		return self.name 

	name = models.CharField(max_length=200)

