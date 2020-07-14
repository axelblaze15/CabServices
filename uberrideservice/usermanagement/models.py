from __future__ import unicode_literals

from django.db import models
from django.db.models import Model

# Create your models here.

class BaseModel(Model):
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)
	is_deleted = models.BooleanField(default=False)

	class Meta:
		abstract = True

class KYCDocument(BaseModel):
	TYPE_CHOICES = (('DRIVINGLICENSE', 'DRIVINGLICENSE'),
					('AADHAR', 'AADHAR'),
					('PAN', 'PAN'),
					('OTHER', 'OTHER'))
	document_id = models.CharField(max_length=255, primary_key=True)
	user_id = models.CharField(max_length=255, db_index=True)
	avatar = models.URLField(max_length=1000, null=True, blank=True)
	document_type = models.CharField(max_length=10, choices=TYPE_CHOICES)


class Driver(BaseModel):
	GENDER = (
		('Male', 'Male'),
		('Female', 'Female'),
		('Other', 'Other'),
	)
	first_name = models.CharField(max_length=255)
	middle_name = models.CharField(max_length=255,null=True,blank=True)
	last_name = models.CharField(max_length=255)
	mobile_no = models.CharField(max_length=255, db_index=True)
	alt_mobile_no = models.CharField(max_length=255, db_index=True)
	email_id = models.EmailField(max_length=255, db_index=True, null=True,
								blank=True, editable = True)
	gender = models.CharField(max_length=255, choices=GENDER)
	address = models.TextField(null=True, blank=True)

	def serializer(self):
		data = {}
		data['first_name'] = self.first_name
		data['middle_name'] = self.middle_name
		data['last_name'] = self.last_name
		data['mobile_no'] = self.mobile_no
		data['alt_mobile_no'] = self.alt_mobile_no
		data['email_id'] = self.email_id
		data['gender'] = self.gender
		data['address'] = self.address
		return data



class User(BaseModel):
	GENDER = (
		('Male', 'Male'),
		('Female', 'Female'),
		('Other', 'Other'),
	)
	first_name = models.CharField(max_length=255)
	middle_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	mobile_no = models.CharField(max_length=255, db_index=True)
	alt_mobile_no = models.CharField(max_length=255, db_index=True)
	email_id = models.EmailField(max_length=255, db_index=True, null=True,
								blank=True, editable = True)
	gender = models.CharField(max_length=255, choices=GENDER)	
	# wallet = models.ForeignKey('Wallet',null=True,blank=True)

	def serializer(self):
		data = {}
		data['first_name'] = self.first_name
		data['middle_name'] = self.middle_name
		data['last_name'] = self.last_name
		data['mobile_no'] = self.mobile_no
		data['alt_mobile_no'] = self.alt_mobile_no
		data['email_id'] = self.email_id
		data['gender'] = self.gender
		return data




