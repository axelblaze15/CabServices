from django.shortcuts import render
from django.views.generic import View

from rideservice.models import Ride
from uberrideservice.utils import send_200
from rideservice.constants import RIDE_DETAILS_FETCHED_SUCCESS
# Create your views here.


class RequestRide(View):

	def __init__(self):
		self.response = {}
		self.response["res_str"] = ""
    	self.response["res_data"] = {}

	def post(self, request, *args, **kwargs):
		data = request.POST
		start_location = data.get('start_location')
		end_location = data.get('end_location')
		current_location = data.get('current_location')
		payment_mode = data.get('payment_mode','Cash')
		user_id = data.get('user_id')
		try:
			ride = Ride.objects.create_ride(start_location,
											end_location,
											current_location,
											payment_mode,
											user_id)
			self.response['res_data'] = ride.serializer()
			self.response['res_str'] = RIDE_DETAILS_FETCHED_SUCCESS
			return send_200(self.response)
		except Exception, e:
			self.response['res_str'] = str(e)
			return send_400(self.response)