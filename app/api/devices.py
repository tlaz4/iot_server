from flask import Blueprint, request
from flask_restful import Resource, Api
from app import db
from app.api.models import Device
from app.api.transmit import TransmitInterface

device_blueprint = Blueprint('device', __name__)
api = Api(device_blueprint)
transmit_interface = TransmitInterface()

class Devices(Resource):

	def get(self, device_id):
		device = Device.query.filter_by(id=device_id).first()

		if not device:
			response_object = {'status': 'fail', 'message': 'Devide does not exist!'}
			return response_object, 404

		else:
			response_object = {'status': 'success', 'data': device.to_json()}
			return response_object, 200

	def patch(self, device_id):
		patch_data = request.get_json()
		device = Device.query.filter_by(id=device_id).first()

		if not device:
			response_object = {'status': 'fail', 'message': 'Device does not exist!'}
			return response_object, 404

		else:
			for k, v in patch_data.items():
				try: 
					getattr(device, k)

				except AttributeError as error:
					response_object = {'status': 'fail', 'message': 'Attribute does not exist'}
					return response_object, 400

				setattr(device, k, v)

		db.session.commit()
		# consider adding a timer attribute to all devices 
		transmit_interface.init_protocol(device.type, device.to_json())

		response_object = {
			'status': 'success',
			'data': device.to_json()
		}

		return response_object, 200
					



class DeviceList(Resource):

	def get(self):
		devices = Device.query.all()

		response_object = {
			'status': 'success',
			'data': {
				'devices': [device.to_json() for device in devices]
			}
		}
		return response_object, 200

api.add_resource(Devices, '/api/devices/<device_id>')
api.add_resource(DeviceList, '/api/devices')
