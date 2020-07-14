from __future__ import unicode_literals

from django.db import models
from django.db.models import Model, Manager
from django.db import transaction


from usermanagement.models import Driver,User

# Create your models here.

class BaseModel(Model):
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)
	created_by = models.ForeignKey(User)
	updated_by = models.ForeignKey(User)
	is_deleted = models.BooleanField(default=False)

	class Meta:
		abstract = True

class Location(Model):
	longitude = models.CharField(max_length=255)
	latitude = models.CharField(max_length=255)
	city = models.CharField(max_length=255)
	driver = models.ForeignKey(Driver,null=True,blank=True)
	user = models.ForeignKey(User,null=True,blank=True)

	def serializer(self):
		data = {}
		data['longitude'] = self.longitude
		data['latitude'] = self.latitude
		data['city'] = self.city
		data['driver'] = self.driver.serializer() if self.driver else {}
		data['user'] = self.user.serializer() if self.user else {}
		return data

class RideManager(Manager):

	def __init__params(self,start_location,end_location,
							current_location,
							payment_mode,user_id):
		self.start_location = start_location
		self.end_location = end_location
		self.current_location = current_location
		self.payment_mode = payment_mode
		self.user_id = user_id

	def _validate_ride_params(self):
		pass

	def fetch_nearest_driver(self):
		pass

	def calculate_ride_amt(self):
		pass

	def create_ride_instance(self):
		driver = self.fetch_nearest_driver()
		with transaction.atomic():
			new_ride = self.create(driver=driver,
								start_location=self.start_location,
								end_location=self.end_location,
								current_location=self.current_location)
			amount_payable = self.calculate_ride_amt()
			TrackRide.objects.create_track_ride(new_ride,self.user,
										self.start_location,self.end_location)
			Payment.objects.create_payment(new_ride,self.payment_mode,amount_payable)
		return new_ride

	def create_ride(self, start_location,end_location,current_location,
							payment_mode,user_id):
		self.__init__params(start_location,end_location,
							current_location,
							payment_mode,user_id)
		self._validate_ride_params()
		return self.create_ride_instance()

class Ride(BaseModel):
	STATUS = (
		('Active', 'Active'),
		('Inactive', 'Inactive'),
		('InProgress', 'InProgress'),
		('InWait', 'InWait'),
		('Cancelled', 'Cancelled'),
	)
	driver = models.ForeignKey(Driver)
	start_location = models.ForeignKey(Location)
	end_location = models.ForeignKey(Location)
	payment = models.ForeignKey(Payment)
	end_time = models.DateTimeField()
	current_location = models.ForeignKey(Location)
	status = models.CharField(max_length=255, choices=STATUS, default='Active')

	objects = RideManager()


	def serializer(self, user_id=None):
		data = {}
		data['driver'] = self.driver.serializer()
		data['start_location'] = self.start_location.serializer()
		data['end_location'] = self.end_location.serializer()
		data['payment'] = self.payment.serializer()
		data['end_time'] = self.end_time.strftime('%Y-%m-%d %H:%M:%S')
		data['start_time'] = self.created_on.strftime('%Y-%m-%d %H:%M:%S')
		data['current_location'] = self.current_location.serializer()
		data['status'] = self.status 
		data['track_ride'] = {}
		trackride = self.trackride.filter(is_deleted=False,user_id=user_id)
		if trackride.exists():
			data['track_ride'] = trackride.last().serializer()
		return data


class TrackRide(BaseModel):
	UBER_CLASS = (
		('SUV','SUV'),
		('Hatchback', 'Hatchback')
		)
	ride = models.ForeignKey(Ride, related_name='trackride')
	user = models.ForeignKey(User)
	start_location = models.ForeignKey(Location)
	end_location = models.ForeignKey(Location)
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	payment = models.ForeignKey(Payment)
	preferred_class = models.CharField(max_length=255, choices=UBER_CLASS)
	taken_class = models.CharField(max_length=255, choices=UBER_CLASS)


	def serializer(self):
		data = {}
		data['ride'] = self.ride_id
		data['user'] = self.user_id
		data['start_location'] = self.start_location.serializer()
		data['end_location'] = self.end_location.serializer()
		data['payment'] = self.payment.serializer()
		data['end_time'] = self.end_time.strftime('%Y-%m-%d %H:%M:%S')
		data['start_time'] = self.created_on.strftime('%Y-%m-%d %H:%M:%S')
		data['taken_class'] = self.taken_class
		return data


class Payment(Model):
	MODE_OF_PAYMENT = (
		('Cash','Cash'),
		('Card', 'Card')
		)
	PAYMENT_STATUS = (
		('Paid','Paid'),
		('Failed','Failed'),
		('Ready','Ready')
		('Initiated','Initiated')
		)
	payment_id = models.CharField(max_length=255, primary_key=True)
	mode = models.CharField(max_length=255, choices=MODE_OF_PAYMENT)
	status = models.CharField(max_length=255, choices=PAYMENT_STATUS)
	utr = models.CharField(max_length=255, null=True, blank=True)
	currency = models.ForeignKey('Currency',default='INR')
	ride = models.ForeignKey(Ride)

	def serializer(self):
		data = {}
		data['payment_id'] = self.payment_id
		data['mode'] = self.mode
		data['status'] = self.status
		data['utr'] = self.utr
		data['currency'] = self.currency_id

class Feedback(BaseModel):
	driver = models.ForeignKey(Driver)
	user = models.ForeignKey(User)
	comments = models.TextField(null=True, blank=True)



